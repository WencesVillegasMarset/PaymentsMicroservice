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
    "orderId": {
        "required": True,
        "type": str
    }
}


def init():
    """
    Inicializa los servicios Rabbit
    """
    initAuth()
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
    catalogConsumer = threading.Thread(target=listenPayments)
    catalogConsumer.start()


def listenAuth():
    """
    Escucha a eventos de logout enviados por Auth.

    @api {fanout} auth/logout Logout

    @apiGroup RabbitMQ GET

    @apiDescription Escucha de mensajes logout desde auth. Invalida sesiones en cache.

    @apiExample {json} Mensaje
      {
        "type": "article-exist",
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

# TODO : Terminar Rabbit aprendiendo de la documentacion
def listenPayments():
    """
    payment-complete : 

    @api {fanout} payments/payment-complete Successful Payment

    @apiGroup RabbitMQ POST

    @apiDescription Postea eventos sobre pagos a ordenes completos con exito

    @apiExample {json} Mensaje
      {
        "type": "payment-complete",
        "exchange" : "{payments}"
        "queue" : "{payments}"
        "message" : {
            "paymentId": "{paymentId}",
            "orderId": "{orderId}",
        }
    """
   
    EXCHANGE = "payments"
    QUEUE = "payments"

    # try:
    #     connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get_rabbit_server_url()))
    #     channel = connection.channel()

    #     channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

    #     channel.queue_declare(queue=QUEUE)

    #     channel.queue_bind(queue=QUEUE, exchange=EXCHANGE, routing_key=QUEUE)

    #     def callback(ch, method, properties, body):
    #         event = json.body_to_dic(body.decode('utf-8'))
    #         if(len(validator.validateSchema(EVENT_CALLBACK, event)) > 0):
    #             return

    #         if (event["type"] == "article-exist"):
    #             message = event["message"]
    #             if(len(validator.validateSchema(MSG_ARTICLE_EXIST, message)) > 0):
    #                 return

    #             exchange = event["exchange"]
    #             queue = event["queue"]
    #             referenceId = message["referenceId"]
    #             articleId = message["articleId"]

    #             print("RabbitMQ Catalog GET article-exist catalogId:%r , articleId:%r", referenceId, articleId)

    #             try:
    #                 articleValidation.validateArticleExist(articleId)
    #                 sendArticleValid(exchange, queue, referenceId, articleId, True)
    #             except Exception:
    #                 sendArticleValid(exchange, queue, referenceId, articleId, False)

    #         if (event["type"] == "article-data"):
    #             message = event["message"]
    #             if(len(validator.validateSchema(MSG_ARTICLE_EXIST, message)) > 0):
    #                 return

    #             exchange = event["exchange"]
    #             queue = event["queue"]
    #             referenceId = message["referenceId"]
    #             articleId = message["articleId"]

    #             print("RabbitMQ Catalog GET article-data catalogId:%r , articleId:%r", referenceId, articleId)

    #             try:
    #                 article = crud.getArticle(articleId)
    #                 valid = ("enabled" in article and article["enabled"])
    #                 stock = article["stock"]
    #                 price = article["price"]
    #                 articleValidation.validateArticleExist(articleId)
    #                 sendArticleData(exchange, queue, referenceId, articleId, valid, stock, price)
    #             except Exception:
    #                 sendArticleData(exchange, queue, referenceId, articleId, False, 0, 0)

    #     print("RabbitMQ Catalog conectado")

    #     channel.basic_consume(QUEUE, callback, consumer_tag=QUEUE, auto_ack=True)

    #     channel.start_consuming()
    # except Exception:
    #     traceback.print_exc()
    #     print("RabbitMQ Catalog desconectado, intentando reconectar en 10'")
    #     threading.Timer(10.0, initCatalog).start()

