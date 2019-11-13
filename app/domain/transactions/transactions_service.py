import app.domain.transactions.transactions_crud as transactions_crud
import app.domain.payments.payments_service as payments_service
import app.domain.payments.payments_crud as payments_crud
import app.gateways.rabbit_service as rabbit_service

import app.utils.errors as errors

def process_transaction(params):
    try:
        transaction = transactions_crud.addTransactions(params)
        if params['status'] == 'rejected':
            payment = payments_crud.addStatus(transaction['id_payment'], {
                'status' : 'rejected',
                'status_detail' : 'rejected_by_mercadopago'
            })
            payments_crud.updatePayment(transaction['id_payment'], payment)
            rabbit_service.postPaymentsFailed(transaction['id_payment'])
            return
            
        payments_service.updatePayment(transaction['id_payment'])
    except Exception as err:
        raise err
    

