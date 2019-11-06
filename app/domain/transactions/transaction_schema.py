import datetime
 
import numbers
import app.utils.schema_validator as validator
import app.utils.errors as errors

'''
    Validaciones del esquema de base de datos
    Definimos diccionarios que validan los datos que puede modificar el usuario
'''


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
        "minLen": 1,
        "maxLen": 60
    },
    "external_reference":{
        "type": str,
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


def validate_schema(document):

    err = validator.validateSchema(TRANSACTION_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
    
