# coding=utf_8
# Son las validaciones de los servicios rest, se validan los parametros obtenidos desde las llamadas externas rest

import numbers

import app.domain.payments.payments_crud as crud
import app.utils.errors as error
import app.utils.schema_validator as schemaValidator
VALID_CURRENCIES = ['ARS']
# Son validaciones sobre las propiedades que pueden actualizarse desde REST

PAYMENT_CANCEL_SCHEMA = {
    "status_detail": {
        "required": False,
        "type": str,
        "minLen": 1,
        "maxLen": 2300,
    }
}

PAYMENT_ADD_SCHEMA = {
    "id_order": {
        "required": True,
        "type": str,
    },
    "payment_preference": {
        "id_payment_method":{
            "required": True,
            "type": str,
        },
        "installments":{
            "required": True,
            "type": numbers.Integral,
        },
        "currency":{
            "required": True,
            "type": str,
            "minLen": 3,
            "maxLen": 3
        },
        "payments_service":{
            "required": True,
            "type": str,
            "minLen": 1,
            "maxLen": 60
        }
    }
}
def validateCancelPaymentParams(params):
    res = schemaValidator.validateAndClean(PAYMENT_CANCEL_SCHEMA, params)
    return res

def validateAddPaymentParams(params):
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")
    res = schemaValidator.validateAndClean(PAYMENT_ADD_SCHEMA, params)
    validateCurrency(res['payment_preference']['currency'])
    return res

def validateEditPaymentParams(paymentId, params):
    """
    Valida los parametros para cancelar un payment.\n
    params: dict<propiedad, valor> Article
    """
    if (not paymentId):
        raise error.InvalidArgument("_id", "Invalido")

    return schemaValidator.validateAndClean(PAYMENT_CANCEL_SCHEMA, params)

def validateCurrency(currency):
    '''
    Valida que la denominacion solicitada pertenezca a las que maneja el servicio
    '''
    if (currency not in VALID_CURRENCIES):
        raise error.InvalidArgument("currency", "Invalida")
