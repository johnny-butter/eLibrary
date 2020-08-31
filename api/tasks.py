from datetime import datetime
from eLibrary.celery import app
from django.core.mail import send_mail
from django.db.models import Sum
from .models import PayOrder, PayOrderDetail, BookTop3


@app.task
def sent_shopping_record_mail(pay_order_id):
    pay_order = PayOrder.objects.get(id=pay_order_id)
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


@app.task
def get_top3_books():
    top3_query = PayOrderDetail.objects. \
        filter(pay_order__state=1). \
        values('book'). \
        annotate(Sum('quantity')). \
        order_by('-quantity__sum')[:3]

    count_time = datetime.now().strftime('%Y%m%d%H')

    BookTop3.objects.bulk_create([
        BookTop3(
            book_id=item['book'],
            book_count=item['quantity__sum'],
            count_time=count_time
        )
        for item in top3_query
    ])
