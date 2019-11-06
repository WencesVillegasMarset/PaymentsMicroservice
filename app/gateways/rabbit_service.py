# coding=utf_8

import threading
import traceback

import pika

import app.domain.payments.payments_crud as crud
import app.domain.payments.rest_validations as articleValidation
import app.utils.config as config
import app.utils.json_serializer as json
import app.utils.schema_validator as validator
import app.utils.security as security

EVENT = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    }
}

EVENT_CALLBACK = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    },
    "exchange": {
        "required": True
    },
    "queue": {
        "required": True
    }
}


MSG_PAYMENT_COMPLETE = {
    "paymentId": {
        "required": True,
        "type": str
    },
}


def init():
    """
    Inicializa los servicios Rabbit
    """
    initAuth()
    initTransactions()
    initPayments()


def initAuth():
    """
    Inicializa RabbitMQ para escuchar eventos logout.
    """
    authConsumer = threading.Thread(target=listenAuth)
    authConsumer.start()


def initPayments():
    """
    Inicializa RabbitMQ para enviar eventos acerca de payments.
    """
    paymentsConsumer = threading.Thread(target=listenPayments)
    paymentsConsumer.start()

def initTransactions():
    """
    Inicializa RabbitMQ para publicar y recibir mensajes acerca de transacciones.
    """
    transactionConsumer = threading.Thread(target=listenTransactions)
    transactionConsumer.start()

def listenAuth():
    """
    Escucha a eventos de logout enviados por Auth.

    @api {fanout} auth/logout Logout

    @apiGroup RabbitMQ GET

    @apiDescription Escucha de mensajes logout desde auth. Invalida sesiones en cache.

    @apiExample {json} Mensaje
      {
        "type": "logout",
        "message" : "tokenId"
      }
    """
    EXCHANGE = "auth"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.body_to_dic(body.decode('utf-8'))
            if(len(validator.validateSchema(EVENT, event)) > 0):
                return

            if (event["type"] == "logout"):
                security.invalidateSession(event["message"])

        print("RabbitMQ Auth conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception:
        print("RabbitMQ Auth desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initAuth).start()


def listenTransactions():
    
    import app.domain.transactions.transactions_crud as transactions_crud 
    import app.domain.transactions.transactions_service as transactions_service 

    """
    Escucha a transacciones a procesar emitidas por adaptadores de pago.

    @api {direct} payments/transaction_task_queue Process Transaction

    @apiGroup RabbitMQ GET

    @apiDescription Escucha a transacciones a procesar emitidas por adaptadores de pago.

    @apiExample {json} Mensaje
      {
        "type": "transaction_task_queue",
        "message" : {
            "amount":{Float},
            "status":{String},
            "id_payment":{String},
            "external_reference":{String}
        }
      }
    """

    QUEUE = "transaction_task_queue"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )

        channel = connection.channel()

        channel.queue_declare(queue=QUEUE, durable=True)

        def callback(ch, method, properties, body):

            params = json.body_to_dic(body.decode('utf-8'))
            transactions_service.process_transaction(params)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)

        print("RabbitMQ PaymentTransactions conectado")

        channel.basic_consume(queue=QUEUE, on_message_callback=callback)

        channel.start_consuming()

    except Exception as err:
        print(err)
        print("RabbitMQ PaymentTransactions desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initTransactions).start()

def postTransactions(message):
    # TODO : Documentar esto
    """
    Postea eventos de notificacion acerca de transacciones de pagos

    @api {fanout} transactions/transaction_task_queue Post New Transaction

    @apiGroup RabbitMQ POST

    @apiDescription Postea transacciones recibidas a procesar 

    @apiExample {json} Mensaje
      {
        "type": "transaction",
        "exchange" : "{''}"
        "queue" : ""
        "message" : {
            "amount":{Float},
            "id_payment":{String},
            "status":{String},
            "external_reference":{String}
        }
    """

    QUEUE = "transaction_task_queue"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE, durable=True)

        message = message
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE,
            body=json.dic_to_json(message),
            properties=pika.BasicProperties(delivery_mode=2))

        connection.close()

    except Exception:
        print("Error enviando mensaje a " + QUEUE)


def postPayments(paymentId):
    """
    payment-complete : 

    @api {fanout} payments/payment-complete Successful Payment

    @apiGroup RabbitMQ POST

    @apiDescription Postea eventos sobre pagos a ordenes completos con exito

    @apiExample {json} Mensaje
      {
        "type": "payment-complete",
        "exchange" : "{payments}"
        "queue" : ""
        "message" : {
            "paymentId": "{paymentId}",
        }
    """
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.exchange_declare(exchange='payments', exchange_type='fanout')
        message = {
            "paymentId": paymentId
        }
        channel.basic_publish(exchange='payments', routing_key='', body=json.dic_to_json(message))

        connection.close()

    except Exception:
        print("Error conectando a RabbitMQ")
    
# TODO : Escuchar orders-placed

def listenPayments():
    """
    Escucha a eventos de payments-complete enviados por Payments.

    @api {fanout} payments/payment-complete Payment Complete

    @apiGroup RabbitMQ GET

    @apiDescription Escucha a eventos de payments-complete enviados por Payments.

    @apiExample {json} Mensaje
      {
        "type": "payment-complete",
        "exchange" : "{payments}"
        "message" : {
            "paymentId": "{paymentId}",
        }
      }
    """
    EXCHANGE = "payments"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.body_to_dic(body.decode('utf-8'))
            print(event)

        print("RabbitMQ Payments GET conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception:
        print("RabbitMQ Payments desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initAuth).start()