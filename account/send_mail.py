from django.core.mail import send_mail

HOST = '34.159.244.62'


def send_confirmation_email(user, code):
    link = f'http://{HOST}/accounts/activate/{code}/'
    # server_link = '/api/v1/accounts/activate/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужноперейти по ссылке ниже:'
        f'\n{link}'
        f'\nСсылка работает один раз!',
        'forminerabbit@gmail.com',
        [user],
        fail_silently=False
    )
