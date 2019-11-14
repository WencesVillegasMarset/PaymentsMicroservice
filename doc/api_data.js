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
    "group": "C__Users_Jorge_Documents_repos_PaymentsMicroservice_doc_main_js",
    "groupTitle": "C__Users_Jorge_Documents_repos_PaymentsMicroservice_doc_main_js",
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
    "group": "C__Users_Jorge_Documents_repos_PaymentsMicroservice_public_main_js",
    "groupTitle": "C__Users_Jorge_Documents_repos_PaymentsMicroservice_public_main_js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/v1/payments/:paymentId/cancel",
    "title": "Cancel Payment",
    "name": "Cancel_Payment",
    "group": "Payments",
    "examples": [
      {
        "title": "Body",
        "content": "\n{\n    \"detail\": \"{detalle o descripcion (opcional)}\"\n}",
        "type": "json"
      },
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Response",
          "content": "HTTP/1.1 200 OK\n {\n    \"_id\": \"{id del payment}\",\n    \"payment_preference\": {\n        \"payment_method\": \"{método de pago}\",\n        \"installments\": \"{numero de cuotas}\",\n        \"currency\": \"{moneda elegida}\",\n        \"payment_service\": \"{servicio de procesamiento pagos a utilizar}\",\n    },\n    \"id_order\": \"{id de la orden}\",\n    \"id_user\": \"{id del usuario}\",\n    \"external_reference\": \"{referencia externa}\",\n    \"status\": [{\n            \"status\": \"{estado del payment}\",\n            \"status_detail\": \"{observaciones}\",\n            \"created\": \"{fecha creación}\"\n    }],\n    \"total_amount\": \"{monto total del payment}\",\n    \"total_paid_amount\": \"{monto total pagado (sum(transactions)}\",\n    \"updated\": \"{fecha última actualización}\",\n    \"created\": \"{fecha creación}\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app/domain/payments/routes.py",
    "groupTitle": "Payments",
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/v1/payments/",
    "title": "Create Payment",
    "name": "Create_Payment",
    "group": "Payments",
    "examples": [
      {
        "title": "Body",
        "content": "{\n    \"order_id\": \"{id de la orden}\",\n    \"payment_preference\": {\n        \"installments\": \"{número de cuotas}\",\n        \"id_payment_method\": \"{id del método de pago}\",\n        \"currency\": \"{moneda elegida}\",\n        \"payment_service\": \"{servicio de procesamiento pagos a utilizar}\",\n}",
        "type": "json"
      },
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "success": {
      "examples": [
        {
          "title": "Response",
          "content": "HTTP/1.1 201 CREATED\n{\n    \"_id\": \"{id del payment}\",\n    \"payment_preference\": {\n        \"id_payment_method\": \"{id del método de pago}\",\n        \"installments\": \"{número de cuotas}\",\n        \"currency\": \"{moneda elegida}\",\n        \"payment_service\": \"{servicio de procesamiento pagos a utilizar}\",\n    },\n    \"id_order\": \"{id de la orden}\",\n    \"id_user\": \"{id del usuario}\",\n    \"external_reference\": \"{referencia externa}\",\n    \"status\": [{\n            \"status\": \"{estado del payment}\",\n            \"status_detail\": \"{observaciones}\",\n    }],\n    \"total_amount\": \"{monto total del payment}\",\n    \"total_paid_amount\": \"{monto total pagado (sum(transactions)}\",\n    \"updated\": \"{fecha última actualización}\",\n    \"created\": \"{fecha creación}\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app/domain/payments/routes.py",
    "groupTitle": "Payments",
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/v1/payments/:paymentId",
    "title": "Get Payment",
    "name": "Get_Payment",
    "group": "Payments",
    "success": {
      "examples": [
        {
          "title": "Response",
          "content": "HTTP/1.1 200 OK\n{\n    \"_id\": \"{payment id}\",\n    \"payment_preference\": {\n        \"payment_method\": \"{método de pago}\",\n        \"installments\": \"{numero de cuotas}\",\n        \"currency\": \"{currency selected}\",\n        \"payment_service\": \"{payment processing service selected}\",\n    },\n    \"id_order\": \"{id de la orden}\",\n    \"id_user\": \"{id del usuario}\",\n    \"external_reference\": \"{referencia externa}\",\n    \"status\": [{\n            \"status\": \"{estado del payment}\",\n            \"status_detail\": \"{observaciones}\",\n            \"created\": \"{fecha creación}\"\n    }],\n    \"total_amount\": \"{monto total del payment}\",\n    \"total_paid_amount\": \"{monto total pagado (sum(transactions)}\",\n    \"updated\": \"{fecha última actualización}\",\n    \"created\": \"{fecha creación}\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app/domain/payments/routes.py",
    "groupTitle": "Payments",
    "examples": [
      {
        "title": "Header Autorización",
        "content": "Authorization=bearer {token}",
        "type": "String"
      }
    ],
    "error": {
      "examples": [
        {
          "title": "401 Unauthorized",
          "content": "HTTP/1.1 401 Unauthorized",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/v1/payments/:paymentId/transactions",
    "title": "Get Payment Transactions",
    "name": "Get_Payment_Transactions",
    "group": "Payments",
    "success": {
      "examples": [
        {
          "title": "Response",
          "content": "HTTP/1.1 200 OK\n[   \n    {\n    \"payment_id\": \"{id del payment}\",\n    \"amount\": \"{cantidad abonada}\",\n    \"status\": \"{estado de la transaction}\",\n    \"external_reference\": \"{referencia externa}\",\n    \"created\": \"{fecha creación}\"\n    }\n]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./app/domain/payments/routes.py",
    "groupTitle": "Payments",
    "error": {
      "examples": [
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"path\" : \"{Nombre de la propiedad}\",\n    \"message\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "400 Bad Request",
          "content": "HTTP/1.1 400 Bad Request\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        },
        {
          "title": "500 Server Error",
          "content": "HTTP/1.1 500 Server Error\n{\n    \"error\" : \"{Motivo del error}\"\n}",
          "type": "json"
        }
      ]
    }
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
        "content": "{\n  \"type\": \"transaction_task_queue\",\n  \"message\" : {\n      \"amount\":{Float},\n      \"status\":{String},\n      \"id_payment\":{String},\n      \"external_reference\":{String}\n  }\n}",
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
    "title": "Payment Complete",
    "group": "RabbitMQ_GET_MOCK",
    "description": "<p>Escucha a eventos de payments-complete enviados por Payments.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"payment-complete\",\n  \"exchange\" : \"{payments}\"\n  \"message\" : {\n      \"paymentId\": \"{paymentId}\",\n  }\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_GET_MOCK",
    "name": "FanoutPaymentsPaymentComplete"
  },
  {
    "type": "fanout",
    "url": "payments/payments-failed",
    "title": "Payment Complete",
    "group": "RabbitMQ_GET_MOCK",
    "description": "<p>Escucha a eventos de payments-failed enviados por Payments.</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"payment-failed\",\n  \"exchange\" : \"{payments-failed}\"\n  \"message\" : {\n      \"paymentId\": \"{paymentId}\",\n  }\n}",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_GET_MOCK",
    "name": "FanoutPaymentsPaymentsFailed"
  },
  {
    "type": "fanout",
    "url": "payments/payment-complete",
    "title": "Payment Complete",
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
    "url": "payments/payments-failed",
    "title": "Payment Failed",
    "group": "RabbitMQ_POST",
    "description": "<p>Postea eventos sobre pagos fallidos</p>",
    "examples": [
      {
        "title": "Mensaje",
        "content": "{\n  \"type\": \"payment-failed\",\n  \"exchange\" : \"{payments-failed}\"\n  \"queue\" : \"\"\n  \"message\" : {\n      \"paymentId\": \"{paymentId}\",\n  }",
        "type": "json"
      }
    ],
    "version": "0.0.0",
    "filename": "./app/gateways/rabbit_service.py",
    "groupTitle": "RabbitMQ_POST",
    "name": "FanoutPaymentsPaymentsFailed"
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
