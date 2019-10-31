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
    # paymentsProducer = threading.Thread(target=listenTransactions)
    # paymentsProducer.start()
def initTransactions():
    """
    Inicializa RabbitMQ para publicar y recibir mensajes acerca de transacciones.
    """
    paymentsProducer = threading.Thread(target=listenTransactions)
    paymentsProducer.start()

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
    """
    Escucha a transacciones a procesar emitidas por adaptadores de pago.

    @api {direct} payments/transactions New Transaction

    @apiGroup RabbitMQ GET

    @apiDescription Escucha a transacciones a procesar emitidas por adaptadores de pago.

    @apiExample {json} Mensaje
      {
        "type": "logout",
        "message" : "tokenId"
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
            event = json.body_to_dic(body.decode('utf-8'))
            
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)

        print("RabbitMQ PaymentTransactions conectado")

        channel.basic_consume(queue=QUEUE, on_message_callback=callback)

        channel.start_consuming()

    except Exception:
        print("RabbitMQ PaymentTransactions desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initTransactions).start()

def postTransactions(message):
    # TODO : Documentar esto
    """
    transaction-recieved : 

    @api {fanout} transactions/transaction_task_queue Post New Transaction

    @apiGroup RabbitMQ POST

    @apiDescription Postea transacciones recibidas a procesar 

    @apiExample {json} Mensaje
      {
        "type": "payment-complete",
        "exchange" : "{''}"
        "queue" : ""
        "message" : {
            "transaction": "{paymentId}",
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
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

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