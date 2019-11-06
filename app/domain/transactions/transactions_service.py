import app.domain.transactions.transactions_crud as transactions_crud
import app.domain.payments.payments_service as payments_service
import app.utils.errors as errors

def process_transaction(params):
    try:
        transaction = transactions_crud.addTransactions(params)
        payments_service.updatePayment(transaction['id_payment'])
    except Exception as err:
        raise err
    

