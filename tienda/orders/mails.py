from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


class Mail:

    @staticmethod
    def send_complete_order(order, user):
        subject = 'Tu pedido ha sido recibido'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'user': user,
        })

        message = EmailMultiAlternatives(subject, 
                                         'Mensaje importante', 
                                         settings.EMAIL_HOST_SENDER,
                                         [settings.EMAIL_HOST_SENDER])
        
        message.attach_alternative(content, 'text/html')
        message.send()