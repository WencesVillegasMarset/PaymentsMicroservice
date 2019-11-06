import datetime
import bson.objectid as bson
import app.domain.payments.payment_schema as payment_schema
import app.gateways.rabbit_service as rabbit_service
import app.domain.payments.payments_crud as payments_crud
import app.domain.transactions.transactions_crud as transactions_crud
import app.utils.errors as errors

def updatePayment(paymentId):
    payment = payments_crud.getPayment(paymentId)
    transactions = transactions_crud.getTransactions(paymentId)

    transaction_total = 0
    for transaction in transactions:
        transaction_total += transaction['amount']

    payment['total_paid_amount'] = transaction_total

    if payment['total_amount'] == payment['total_paid_amount']:
        status = payment_schema.new_payment_status()
        status['status'] = 'Completed'
        payment['payment_status'].append(status)

    payments_crud.updatePayment(paymentId, payment)

    if payment['total_amount'] == payment['total_paid_amount']:
        rabbit_service.postPayments(paymentId)
        
    return payment
