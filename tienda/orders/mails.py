from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

class Mail:
    
    @staticmethod
    def get_aboslute_url(url):
        reverse_url = reverse(url)
        if settings.DEBUG:
            return f'http://127.0.0.1:8000{reverse_url}'

    @staticmethod
    def send_complete_order(order, user):
        subject = 'Tu pedido ha sido recibido'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'user': user,
            'next_url': Mail.get_aboslute_url('orders:completed')
        })

        message = EmailMultiAlternatives(subject, 
                                         'Mensaje importante', 
                                         settings.EMAIL_HOST_SENDER,
                                         [settings.EMAIL_HOST_SENDER])
        
        message.attach_alternative(content, 'text/html')
        message.send()