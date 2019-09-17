from celery import task
from django.core.mail import send_mail
from .models import shopHistory


@task
def sent_transaction_mail(transaction_id, userName, userMail):
    """
    :param transaction_id: braintree id of the transaction
    :return: mail_sent
    """

    transaction = shopHistory.objects.filter(transaction_id=transaction_id)

    items = []
    for item in transaction:
        items.append(item.book.name)

    subject = 'Trading Successful! (id:{})'.format(transaction_id)
    message = 'Dear {},\n\nYou have successfully got the book(s):\n{}.'.format(
        userName, '\n'.join(items))

    mail_sent = send_mail(
        subject, message, 'service@elibrary.com', [userMail])

    print(mail_sent, type(mail_sent))
    return mail_sent
