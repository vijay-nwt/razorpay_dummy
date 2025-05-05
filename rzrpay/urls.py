# rzrpay/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plan_list, name='plan_list'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('subscription/<int:pk>/', views.subscription_detail, name='subscription_detail'),
    path('webhook_rzr/', views.razorpay_webhook, name='razorpay_webhook'),
]
