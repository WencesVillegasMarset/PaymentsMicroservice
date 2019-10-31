import datetime
# TODO : Investigar Repository Pattern para no acoplar a mongo este servicio
import bson.objectid as bson
import app.domain.payments.payment_schema as schema

import app.utils.mongo as db
import app.utils.errors as errors


def getPayment(paymentId):
    '''
    Obtiene un payment con id = paymentId
    paymentId : string ObjectId
    return dict(propiedad, valor) Payment
    '''
    '''
    
    @api {get} /v1/payments/:paymentId Get Payment
    @apiName Get Payment
    @apiGroup Payments

    @apiSuccessExample {json} Response
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
        @apiUse Errors
    '''
    try:
        result = db.payments.find_one({'_id': bson.ObjectId(paymentId)})
        if (not result):
            raise errors.InvalidArgument('_id', 'Payment does not exist')
        return result
    except Exception:
        raise errors.InvalidArgument('_id', 'Invalid object id')

def addPayment(params, order, user):
    '''
    Create a new Payment
    params: dict(property, value) Payment
    return: dict(property, value) Payment
    '''
    '''

    @api {post} /v1/payments/ Create Payment
    @apiName Create Payment
    @apiGroup Payments

    @apiUse AuthHeader

    @apiExample {json} Body
        {
        "order_id": "{id de la orden}",
        "payment_preference": {
            "installments": "{número de cuotas}",
            "id_payment_method": "{id del método de pago}",
            "currency": "{moneda elegida}",
            "payment_service": "{servicio de procesamiento pagos a utilizar}",
        }

    @apiSuccessExample {json} Response
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

        @apiUse Errors

    '''
    payment = schema.new_payment()
    payment.update(params)
    payment['total_amount'] = order['totalPayment']
    payment['id_user'] = user['id']

    '''
    Debe consultar a orders los detalles de la orden
    debe validar las preferencias de pago 
    '''
    schema.validate_schema(payment)

    payment["_id"] = db.payments.insert_one(payment).inserted_id

    return payment

def updatePayment(paymentId, params):
    """
    Updates a Payment. 
    payment: string ObjectId
    params: dict<propiedad, valor> Payment
    return: dict<propiedad, valor> Payment
    """

    payment = getPayment(paymentId)

    payment.update(params)

    payment["updated"] = datetime.datetime.utcnow()
    
    schema.validate_schema(payment)
    
    del payment['_id']
    res = db.payments.replace_one({'_id': bson.ObjectId(paymentId)}, payment)
    payment['_id'] = paymentId

    return payment
    

def addStatus(paymentId, params):
    '''
    Crea un nuevo objeto payment_status
    '''
    payment = getPayment(paymentId)

    status = schema.new_payment_status()
    status.update(params)

    payment['payment_status'].append(status)

    return payment