from django.contrib import admin

# Register your models here.
from .models import Plan, Customer, Subscription, Payment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'interval', 'interval_count', 'currency')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'created_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('razorpay_subscription_id', 'plan', 'customer', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_payment_id', 'subscription', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status',)
