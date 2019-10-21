
import flask

import app.domain.payments.payments_crud as crud
import app.domain.payments.rest_validations as restValidator
import app.utils.errors as errors
import app.utils.json_serializer as json
import app.utils.security as security


def init(app):
    """
    Inicializa las rutas para Payments\n
    app: Flask
    """

    @app.route('/v1/payments', methods=['POST'])
    def addPayment():
        try:
            security.isValidToken(flask.request.headers.get("Authorization"))

            params = json.body_to_dic(flask.request.data)

            #params = restValidator.validateAddArticleParams(params)

            result = crud.addPayment(params)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/payments/<paymentId>/cancel', methods=['POST'])
    def cancelPayment(paymentId):
        try:
            security.isValidToken(flask.request.headers.get("Authorization"))

            params = json.body_to_dic(flask.request.data)

            #params = restValidator.validateCancelPaymentParams(paymentId, params)
            # insertar logica para cancelar
            #result = crud.updateArticle(paymentId, params)
            result = None
            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/payments/<paymentId>', methods=['GET'])
    def getPayment(paymentId):
        try:
            return json.dic_to_json(crud.getPayment(paymentId))
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/articles/<paymentId>/transactions', methods=['GET'])
    def getTransactions(paymentId):
        try:
            return json.dic_to_json(crud.getTransactions(paymentId))
        except Exception as err:
            return errors.handleError(err)

    
