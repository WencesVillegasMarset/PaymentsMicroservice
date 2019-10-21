define({ "api": [
  {
    "type": "fanout",
    "url": "auth/logout",
    "title": "Logout",
    "group": "RabbitMQ_GET",
    "description": "<p>Escucha de mensajes logout desde auth. Invalida sesiones en cache.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"article-exist\",\n  \"message\" : \"tokenId\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_GET",
    "name": "FanoutAuthLogout"
  },
  {
    "type": "fanout",
    "url": "payments/payment-complete",
    "title": "Successful Payment",
    "group": "RabbitMQ_POST",
    "description": "<p>Postea eventos sobre pagos a ordenes completos con exito</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"payment-complete\",\n  \"exchange\" : \"{payments}\"\n  \"queue\" : \"{payments}\"\n  \"message\" : {\n      \"paymentId\": \"{paymentId}\",\n      \"orderId\": \"{orderId}\",\n  }",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_POST",
    "name": "FanoutPaymentsPaymentComplete"
  }
] });
