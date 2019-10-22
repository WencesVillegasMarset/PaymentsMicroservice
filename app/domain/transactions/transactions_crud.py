import datetime
# TODO : Investigar Repository Pattern para no acoplar a mongo este servicio
import bson.objectid as bson
import app.domain.payments.transaction_schema as schema

import app.utils.mongo as db
import app.utils.errors as errors


def getTransactions(paymentId):
    '''
    Obtiene todas las transacciones de un payment con id = paymentId
    paymentId : string ObjectId
    return [dict(propiedad, valor)] Transaction
    '''
    '''
    
    @api {get} /v1/payments/:paymentId/transactions Get Transactions
    @apiName Get Transactions
    @apiGroup Payments

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
        {
            "paymentId": "{id del pago}"
        }
        @apiUse Errors
    '''
    try:
        results = []
        cursor = db.transactions.find({'id_payment': paymentId})
        for doc in cursor:
            results.append(doc)
        return results
    except Exception:
        raise errors.InvalidArgument('id_payment', 'Invalid object id')

def addTransactions(params):
    '''
    Crea una transaccion para un payment con id = paymentId
    paymentId : string ObjectId
    return dict(propiedad, valor) Transaction
    '''
    
    transaction = schema.new_transaction()
    transaction.update(params)

    '''
    Debe consultar a orders los detalles de la orden
    debe validar las preferencias de pago 
    '''
    schema.validate_schema(transaction)

    transaction["_id"] = db.transactions.insert_one(transaction).inserted_id

    return transaction