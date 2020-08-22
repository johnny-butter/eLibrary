from eLibrary.celery import app
from django.core.mail import send_mail
from .models import payOrder


@app.task
def sent_shopping_record_mail(pay_order_id):
    pay_order = payOrder.objects.get(id=pay_order_id)
    pay_order_detail = pay_order.payorderdetail_set.all().values('book__name', 'price', 'quantity')
    shop_history = pay_order.shophistory_set.first()
    user = pay_order.user

    bought_items = []
    for detail in pay_order_detail:
        bought_items.append(f"{detail['book__name']} ({detail['price']}x{detail['quantity']})")

    email_subject = 'eLibrary Shopping Record'
    email_content = [
        f'Dear {user.username},',
        '',
        f'Your transaction id: {shop_history.transaction_id}',
        '',
        'Items you bought:',
        '\n'.join(bought_items),
        '',
        f'Total amount: {shop_history.transaction_total_price} {shop_history.transaction_currency}',
        '',
        'Thank you for visiting',
        '',
        'Best Regards,',
        'eLibrary'
    ]

    mail_sent = send_mail(
        email_subject,
        '\n'.join(email_content),
        'service@elibrary.com',
        [user.email]
    )

    return mail_sent
