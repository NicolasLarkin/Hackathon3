from django.urls import path
from .views import create_payment, execute_payment

urlpatterns = [
    path('create/', create_payment, name='create_payment'),
    path('execute/', execute_payment, name='execute_payment'),
]