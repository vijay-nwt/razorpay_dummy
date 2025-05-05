from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'status', 'created_at')  # Replace with your actual field names

admin.site.register(Payment, PaymentAdmin)

