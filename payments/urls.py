from django.urls import path
from . import views

urlpatterns = [
    # path('', views.create_payment, name='create_payment'),
    path('create-payment/', views.create_payment, name='create_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('', views.payment_list, name='payment_list'),
    path('webhook/', views.razorpay_webhook, name='razorpay_webhook'),
]