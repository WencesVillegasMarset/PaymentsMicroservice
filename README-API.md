<a name="top"></a>
# Payments Service v0.1.0

Microservicio de Payments en Python, para ejemplo ecommerce

- [MercadoPago](#mercadopago)
	- [Get Transactions (IPN)](#get-transactions-(ipn))
	
- [Payments](#payments)
	- [Cancel Payment](#cancel-payment)
	- [Create Payment](#create-payment)
	- [Get Payment](#get-payment)
	- [Get Payment Transactions](#get-payment-transactions)
	
- [RabbitMQ_GET](#rabbitmq_get)
	- [Process Transaction](#process-transaction)
	- [Logout](#logout)
	
- [RabbitMQ_GET_MOCK](#rabbitmq_get_mock)
	- [Payment Complete](#payment-complete)
	- [Payment Complete](#payment-complete)
	
- [RabbitMQ_POST](#rabbitmq_post)
	- [Payment Complete](#payment-complete)
	- [Payment Failed](#payment-failed)
	- [Post New Transaction](#post-new-transaction)
	


# <a name='mercadopago'></a> MercadoPago

## <a name='get-transactions-(ipn)'></a> Get Transactions (IPN)
[Back to top](#top)



	POST /v1/gateways/mercadopago/ipn



### Examples

Body

```

{ // Ejemplo de webhook, en la practica mando el JSON de transaccion directo
    "id": 12345,
    "live_mode": true,
    "type": "payment",
    "date_created": "2015-03-25T10:04:58.396-04:00",
    "application_id": 123123123,
    "user_id": 44444,
    "version": 1,
    "api_version": "v1",
    "action": "payment.created",
    "data": {
        "id": "999999999"
    }
}
```


### Success Response

Response

```
HTTP/1.1 200 OK
```


### Error Response

400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
# <a name='payments'></a> Payments

## <a name='cancel-payment'></a> Cancel Payment
[Back to top](#top)



	POST /v1/payments/:paymentId/cancel



### Examples

Body

```

{
    "detail": "{detalle o descripcion (opcional)}"
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Response

```
HTTP/1.1 200 OK
 {
    "_id": "{id del payment}",
    "payment_preference": {
        "payment_method": "{método de pago}",
        "installments": "{numero de cuotas}",
        "currency": "{moneda elegida}",
        "payment_service": "{servicio de procesamiento pagos a utilizar}",
    },
    "id_order": "{id de la orden}",
    "id_user": "{id del usuario}",
    "external_reference": "{referencia externa}",
    "status": [{
            "status": "{estado del payment}",
            "status_detail": "{observaciones}",
            "created": "{fecha creación}"
    }],
    "total_amount": "{monto total del payment}",
    "total_paid_amount": "{monto total pagado (sum(transactions)}",
    "updated": "{fecha última actualización}",
    "created": "{fecha creación}"
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='create-payment'></a> Create Payment
[Back to top](#top)



	POST /v1/payments/



### Examples

Body

```
{
    "order_id": "{id de la orden}",
    "payment_preference": {
        "installments": "{número de cuotas}",
        "id_payment_method": "{id del método de pago}",
        "currency": "{moneda elegida}",
        "payment_service": "{servicio de procesamiento pagos a utilizar}",
}
```
Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Response

```
HTTP/1.1 201 CREATED
{
    "_id": "{id del payment}",
    "payment_preference": {
        "id_payment_method": "{id del método de pago}",
        "installments": "{número de cuotas}",
        "currency": "{moneda elegida}",
        "payment_service": "{servicio de procesamiento pagos a utilizar}",
    },
    "id_order": "{id de la orden}",
    "id_user": "{id del usuario}",
    "external_reference": "{referencia externa}",
    "status": [{
            "status": "{estado del payment}",
            "status_detail": "{observaciones}",
    }],
    "total_amount": "{monto total del payment}",
    "total_paid_amount": "{monto total pagado (sum(transactions)}",
    "updated": "{fecha última actualización}",
    "created": "{fecha creación}"
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='get-payment'></a> Get Payment
[Back to top](#top)



	GET /v1/payments/:paymentId



### Examples

Header Autorización

```
Authorization=bearer {token}
```


### Success Response

Response

```
HTTP/1.1 200 OK
{
    "_id": "{payment id}",
    "payment_preference": {
        "payment_method": "{método de pago}",
        "installments": "{numero de cuotas}",
        "currency": "{currency selected}",
        "payment_service": "{payment processing service selected}",
    },
    "id_order": "{id de la orden}",
    "id_user": "{id del usuario}",
    "external_reference": "{referencia externa}",
    "status": [{
            "status": "{estado del payment}",
            "status_detail": "{observaciones}",
            "created": "{fecha creación}"
    }],
    "total_amount": "{monto total del payment}",
    "total_paid_amount": "{monto total pagado (sum(transactions)}",
    "updated": "{fecha última actualización}",
    "created": "{fecha creación}"
}
```


### Error Response

401 Unauthorized

```
HTTP/1.1 401 Unauthorized
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## <a name='get-payment-transactions'></a> Get Payment Transactions
[Back to top](#top)



	GET /v1/payments/:paymentId/transactions





### Success Response

Response

```
HTTP/1.1 200 OK
[   
    {
    "payment_id": "{id del payment}",
    "amount": "{cantidad abonada}",
    "status": "{estado de la transaction}",
    "external_reference": "{referencia externa}",
    "created": "{fecha creación}"
    }
]
```


### Error Response

400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "path" : "{Nombre de la propiedad}",
    "message" : "{Motivo del error}"
}
```
400 Bad Request

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```
500 Server Error

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
# <a name='rabbitmq_get'></a> RabbitMQ_GET

## <a name='process-transaction'></a> Process Transaction
[Back to top](#top)

<p>Escucha a transacciones a procesar emitidas por adaptadores de pago.</p>

	DIRECT payments/transaction_task_queue



### Examples

Mensaje

```
{
  "type": "transaction_task_queue",
  "message" : {
      "amount":{Float},
      "status":{String},
      "id_payment":{String},
      "external_reference":{String}
  }
}
```




## <a name='logout'></a> Logout
[Back to top](#top)

<p>Escucha de mensajes logout desde auth. Invalida sesiones en cache.</p>

	FANOUT auth/logout



### Examples

Mensaje

```
{
  "type": "logout",
  "message" : "tokenId"
}
```




# <a name='rabbitmq_get_mock'></a> RabbitMQ_GET_MOCK

## <a name='payment-complete'></a> Payment Complete
[Back to top](#top)

<p>Escucha a eventos de payments-complete enviados por Payments.</p>

	FANOUT payments/payment-complete



### Examples

Mensaje

```
{
  "type": "payment-complete",
  "exchange" : "{payments}"
  "message" : {
      "paymentId": "{paymentId}",
  }
}
```




## <a name='payment-complete'></a> Payment Complete
[Back to top](#top)

<p>Escucha a eventos de payments-failed enviados por Payments.</p>

	FANOUT payments/payments-failed



### Examples

Mensaje

```
{
  "type": "payment-failed",
  "exchange" : "{payments-failed}"
  "message" : {
      "paymentId": "{paymentId}",
  }
}
```




# <a name='rabbitmq_post'></a> RabbitMQ_POST

## <a name='payment-complete'></a> Payment Complete
[Back to top](#top)

<p>Postea eventos sobre pagos a ordenes completos con exito</p>

	FANOUT payments/payment-complete



### Examples

Mensaje

```
{
  "type": "payment-complete",
  "exchange" : "{payments}"
  "queue" : ""
  "message" : {
      "paymentId": "{paymentId}",
  }
```




## <a name='payment-failed'></a> Payment Failed
[Back to top](#top)

<p>Postea eventos sobre pagos fallidos</p>

	FANOUT payments/payments-failed



### Examples

Mensaje

```
{
  "type": "payment-failed",
  "exchange" : "{payments-failed}"
  "queue" : ""
  "message" : {
      "paymentId": "{paymentId}",
  }
```




## <a name='post-new-transaction'></a> Post New Transaction
[Back to top](#top)

<p>Postea transacciones recibidas a procesar</p>

	FANOUT transactions/transaction_task_queue



### Examples

Mensaje

```
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
```




