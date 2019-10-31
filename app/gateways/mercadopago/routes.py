import flask

import app.utils.json_serializer as json
import app.utils.errors as errors
import app.gateways.rabbit_service as rabbit_service

def init(app):

    """
    Inicializa las rutas para Gateways de Pagos
    app: Flask
    """

    @app.route('/v1/gateways/mercadopago/ipn', methods=['POST'])
    def notificationMercadoPago():
        '''
        Metodo para recibir notificaciones acerca de creaciones de pagos
        '''
        try:
            # validar que la request sea de mercadopago
            params = json.body_to_dic(flask.request.data)
            #creo el evento de rabbit y lo mando
            rabbit_service.postTransactions(params)
            return flask.Response(status=200)
        except Exception as err:
            return errors.handleError(err)


    
