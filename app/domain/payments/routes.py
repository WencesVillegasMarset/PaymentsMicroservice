
import flask

import app.domain.payments.payments_crud as payments_crud
import app.domain.transactions.transactions_crud as transactions_crud

import app.domain.payments.rest_validations as restValidator
import app.utils.errors as errors
import app.utils.json_serializer as json
import app.utils.security as security
import app.utils.orders as orders



def init(app):

    """
    Inicializa las rutas para Payments\n
    app: Flask
    """

    @app.route('/v1/payments', methods=['POST'])
    def addPayment():
        try:
            # TODO Duda : Como sacar las busquedas order y user en otro lado? se puede hacer?
            token = flask.request.headers.get("Authorization")
            user = security.isValidToken(token)
            params = json.body_to_dic(flask.request.data)
            params = restValidator.validateAddPaymentParams(params)

            order = orders.getOrder(params['id_order'], token)

            # se comunica con un servicio externo
            result = payments_crud.addPayment(params, order, user)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/payments/<paymentId>/cancel', methods=['POST'])
    def cancelPayment(paymentId):
        try:
            security.isValidToken(flask.request.headers.get("Authorization"))
            params = json.body_to_dic(flask.request.data)
            params = restValidator.validateCancelPaymentParams(params)
            params['status'] = 'cancelled'
            # aca hago el crud yo pero tendria que hacerse cuando llegue la notificacion de mp
            # llamo a mp y cancelo
            updated_payment = payments_crud.addStatus(paymentId, params)
            res = payments_crud.updatePayment(paymentId, updated_payment)
            return json.dic_to_json(res)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/payments/<paymentId>', methods=['GET'])
    def getPayment(paymentId):
        try:
            return json.dic_to_json(payments_crud.getPayment(paymentId))
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/payments/<paymentId>/transactions', methods=['GET'])
    def getTransactions(paymentId):
        try:
            return json.dic_to_json(transactions_crud.getTransactions(paymentId))
        except Exception as err:
            return errors.handleError(err)

    
