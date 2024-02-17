from config.celery import app
from django.core.mail import send_mail
from .models import Order


@app.task
def order_created(order_id):
    """ Задача для отправки уведомления по электронной почте при успешном создании заказа. """
    order = Order.objects.get(id=order_id)
    subject = f'Номер заказа. {order_id}'
    message = f'Дорогой {order.first_name}, \nВы успешно разместили заказ.\
                Идентификатор вашего заказа {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@gmail.com',
                          [order.email])
    return mail_sent
