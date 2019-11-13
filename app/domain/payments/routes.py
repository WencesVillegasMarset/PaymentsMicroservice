
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
    
    """

    @api {post} /v1/payments/ Create Payment
    @apiName Create Payment
    @apiGroup Payments

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "order_id": "{id de la orden}",
            "payment_preference": {
                "installments": "{número de cuotas}",
                "id_payment_method": "{id del método de pago}",
                "currency": "{moneda elegida}",
                "payment_service": "{servicio de procesamiento pagos a utilizar}",
        }

    @apiSuccessExample {json} Response
        HTTP/1.1 201 CREATED
        {
            "_id": "{id del payment}",
            "payment_preference": {
                "id_payment_method": "{id del método de pago}",
                "installments": "{número de cuotas}",
                "currency": "{moneda elegida}",
                "payment_service": "{servicio de procesamiento pagos a utilizar}",
            },
            "id_order": "{id de la orden}",
            "id_user": "{id del usuario}",
            "external_reference": "{referencia externa}",
            "status": [{
                    "status": "{estado del payment}",
                    "status_detail": "{observaciones}",
            }],
            "total_amount": "{monto total del payment}",
            "total_paid_amount": "{monto total pagado (sum(transactions)}",
            "updated": "{fecha última actualización}",
            "created": "{fecha creación}"
        }

        @apiUse Errors

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

    """
    
    @api {post} /v1/payments/:paymentId/cancel Cancel Payment
    @apiName Cancel Payment
    @apiGroup Payments

    @apiUse AuthHeader

    @apiExample {json} Body

        {
            "detail": "{detalle o descripcion (opcional)}"
        }

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
         {
            "_id": "{id del payment}",
            "payment_preference": {
                "payment_method": "{método de pago}",
                "installments": "{numero de cuotas}",
                "currency": "{moneda elegida}",
                "payment_service": "{servicio de procesamiento pagos a utilizar}",
            },
            "id_order": "{id de la orden}",
            "id_user": "{id del usuario}",
            "external_reference": "{referencia externa}",
            "status": [{
                    "status": "{estado del payment}",
                    "status_detail": "{observaciones}",
                    "created": "{fecha creación}"
            }],
            "total_amount": "{monto total del payment}",
            "total_paid_amount": "{monto total pagado (sum(transactions)}",
            "updated": "{fecha última actualización}",
            "created": "{fecha creación}"
        }

    @apiUse Errors

    """

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


    """
    
    @api {get} /v1/payments/:paymentId Get Payment
    @apiName Get Payment
    @apiGroup Payments

    @apiUse AuthHeader

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
        {
            "_id": "{payment id}",
            "payment_preference": {
                "payment_method": "{método de pago}",
                "installments": "{numero de cuotas}",
                "currency": "{currency selected}",
                "payment_service": "{payment processing service selected}",
            },
            "id_order": "{id de la orden}",
            "id_user": "{id del usuario}",
            "external_reference": "{referencia externa}",
            "status": [{
                    "status": "{estado del payment}",
                    "status_detail": "{observaciones}",
                    "created": "{fecha creación}"
            }],
            "total_amount": "{monto total del payment}",
            "total_paid_amount": "{monto total pagado (sum(transactions)}",
            "updated": "{fecha última actualización}",
            "created": "{fecha creación}"
        }
    
    @apiUse Errors

    """

    @app.route('/v1/payments/<paymentId>', methods=['GET'])
    def getPayment(paymentId):
        try:
            token = flask.request.headers.get("Authorization")
            user = security.isValidToken(token)
            return json.dic_to_json(payments_crud.getPayment(paymentId))
        except Exception as err:
            return errors.handleError(err)

    """
    
    @api {get} /v1/payments/:paymentId/transactions Get Payment Transactions
    @apiName Get Payment Transactions
    @apiGroup Payments

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
        [   
            {
            "payment_id": "{id del payment}",
            "amount": "{cantidad abonada}",
            "status": "{estado de la transaction}",
            "external_reference": "{referencia externa}",
            "created": "{fecha creación}"
            }
        ]
    
    @apiUse Errors

    """
    @app.route('/v1/payments/<paymentId>/transactions', methods=['GET'])
    def getTransactions(paymentId):
        try:
            return json.dic_to_json(transactions_crud.getTransactions(paymentId))
        except Exception as err:
            return errors.handleError(err)

    
