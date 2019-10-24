import mercadopago
# TODO : Duda, donde crearia ese DTO?, hago una funcion dentro de este wrapper (adaptador) para MP?

TRANSACTION_STATUS_MAP = {
    "pending":{
        "internal_status": "pending",
        "description": "El usuario no completo el proceso de pago todavía."
    },
    "approved":{
        "internal_status": "approved",
        "description": "El pago fue aprobado y acreditado."
    },
    "authorized":{
        "internal_status": "pending",
        "description": "El pago fue autorizado pero no capturado todavía."
    },
    "in_process":{
        "internal_status": "pending",
        "description": "El pago está en revisión."
    },
    "in_mediation":{
        "internal_status": "pending",
        "description": "El usuario inició una disputa."
    },
    "rejected":{
        "internal_status": "cancelled",
        "description": "El pago fue rechazado. El usuario podría reintentar el pago."
    },
    "cancelled":{
        "internal_status": "cancelled",
        "description": "El pago fue cancelado por una de las partes o el pago expiró."
    },
    "refunded":{
        "internal_status": "refunded",
        "description": "El pago fue devuelto al usuario."
    },
    "charged_back":{
        "internal_status": "refunded",
        "description": "Se ha realizado un contracargo en la tarjeta de crédito del comprador."
    }
}

def parseTransaction(data):
    pass
def parsePayment(data):
    pass
def cancelPayment():
    pass
def createPayment():

def updatePayment():

