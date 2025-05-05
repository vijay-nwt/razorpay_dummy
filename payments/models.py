from django.db import models

# Create your models here.
from django.db import models

class Payment(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('advanced', 'Advanced'),
        ('business', 'Business'),
    ]
    
    amount = models.PositiveIntegerField()  # in paise
    currency = models.CharField(max_length=3, default='INR')
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='pending')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status} - {self.plan}"