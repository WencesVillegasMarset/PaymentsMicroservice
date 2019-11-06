define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "C__Users_Jorge_Documents_repos_payments_service_doc_main_js",
    "groupTitle": "C__Users_Jorge_Documents_repos_payments_service_doc_main_js",
    "name": ""
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./public/main.js",
    "group": "C__Users_Jorge_Documents_repos_payments_service_public_main_js",
    "groupTitle": "C__Users_Jorge_Documents_repos_payments_service_public_main_js",
    "name": ""
  },
  {
    "type": "direct",
    "url": "payments/transaction_task_queue",
    "title": "Process Transaction",
    "group": "RabbitMQ_GET",
    "description": "<p>Escucha a transacciones a procesar emitidas por adaptadores de pago.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"logout\",\n  \"message\" : \"tokenId\"\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_GET",
    "name": "DirectPaymentsTransaction_task_queue"
  },
  {
    "type": "fanout",
    "url": "auth/logout",
    "title": "Logout",
    "group": "RabbitMQ_GET",
    "description": "<p>Escucha de mensajes logout desde auth. Invalida sesiones en cache.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"logout\",\n  \"message\" : \"tokenId\"\n}",
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
        "content": "{\n  \"type\": \"payment-complete\",\n  \"exchange\" : \"{payments}\"\n  \"queue\" : \"\"\n  \"message\" : {\n      \"paymentId\": \"{paymentId}\",\n  }",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_POST",
    "name": "FanoutPaymentsPaymentComplete"
  },
  {
    "type": "fanout",
    "url": "transactions/transaction_task_queue",
    "title": "Post New Transaction",
    "group": "RabbitMQ_POST",
    "description": "<p>Postea transacciones recibidas a procesar</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"transaction\",\n  \"exchange\" : \"{''}\"\n  \"queue\" : \"\"\n  \"message\" : {\n      \"amount\":{Float},\n      \"id_payment\":{String},\n      \"status\":{String},\n      \"external_reference\":{String}\n  }",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_POST",
    "name": "FanoutTransactionsTransaction_task_queue"
  }
] });
