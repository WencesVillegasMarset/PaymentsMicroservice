import datetime
 
import numbers
import app.utils.schema_validator as validator
import app.utils.errors as errors

'''
    Validaciones del esquema de base de datos
    Definimos diccionarios que validan los datos que puede modificar el usuario
'''


PAYMENT_DB_SCHEMA = {
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
            "lenght": 3,
        },
        "payments_service":{
            "required": True,
            "type": str,
            "minLen": 1,
            "maxLen": 60
        }
    },
    "id_user": {
        "required": True,
        "type": str,
    },
    "external_reference": {
        "required": True,
        "type": str,
    },
    "payment_status":{
        "status":{
            "required": True,
            "type": str,
            "minLen": 1,
            "maxLen": 60
        },
        "status_detail":{
            "required": False,
            "type": str,
            "minLen": 1,
            "maxLen": 2300,
        }
    },
    "total_amount":{
        "required": False,
        "type": numbers.Real,
        "min": 0
    },
    "total_paid_amount":{
        "required": False,
        "type": numbers.Real,
        "min": 0
    },
}


TRANSACTION_DB_SCHEMA = {
    "amount":{
        "required": True,
        "type": numbers.Real,
        "min": 0
    },
    "id_payment":{
        "required": True,
        "type": str,
    },
    "status":{
        "required": True,
        "type": str,
        "min": 0
    },
    "external_reference":{
        "type": str,
        "minLen": 1,
        "maxLen": 60
    }
}

def new_transaction():
    '''
        Crea una nueva transaccion inicializada
    '''

    return {
        "amount":0,
        "status":'',
        "id_payment":'',
        "external_reference":'',
        "created": datetime.datetime.utcnow(),
        "updated":datetime.datetime.utcnow()
    }

def new_payment():

    return {
        "id_order":'',
        "id_user":'',
        "external_reference":'',
        "payment_preference":{
            "id_payment_method":'',
            "installments":0,
            "currency":'',
            "payments_service":''
        },
        "payment_status":{
            "status":'',
            "status_detail":'',
        },
        "total_amount":0.0,
        "total_paid_amount":0.0,
        "created": datetime.datetime.utcnow(),
        "updated":datetime.datetime.utcnow()
    }

def validate_schema(document):

    err = validator.validateSchema(PAYMENT_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
    
