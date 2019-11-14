import flask

import app.utils.json_serializer as json
import app.utils.errors as errors
import app.gateways.rabbit_service as rabbit_service

def init(app):

    """
    Inicializa las rutas para Gateways de Pagos
    app: Flask
    """
    
    """

    @api {post} /v1/gateways/mercadopago/ipn Get Transactions (IPN)
    @apiName Get Transactions
    @apiGroup MercadoPago


    @apiExample {json} Body
        
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

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK

    @apiUse Errors

    """
    @app.route('/v1/gateways/mercadopago/ipn', methods=['POST'])
    def notificationMercadoPago():
        '''
        Metodo para recibir notificaciones acerca de creaciones de pagos
        '''
        try:
            # validar que la request sea de mercadopago
            # TODO : Validar lo que entra por este endpoint
            params = json.body_to_dic(flask.request.data)
            #creo el evento de rabbit y lo mando
            rabbit_service.postTransactions(params)
            return flask.Response(status=200)
        except Exception as err:
            return errors.handleError(err)


    
