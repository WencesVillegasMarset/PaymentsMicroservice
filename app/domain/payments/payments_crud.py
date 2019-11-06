import datetime
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