from django.db import models

# Create your models here.
from django.db import models

class Plan(models.Model):
    razorpay_plan_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(help_text="Amount in paise (1 INR = 100 paise)")
    currency = models.CharField(max_length=10, default='INR')
    interval = models.CharField(max_length=20)        # e.g. 'monthly', 'yearly'
    interval_count = models.PositiveIntegerField(default=1)  # frequency multiplier
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.amount/100:.2f} {self.currency})"


class Customer(models.Model):
    razorpay_customer_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    razorpay_subscription_id = models.CharField(max_length=100, unique=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    current_start = models.DateTimeField(null=True, blank=True)
    current_end = models.DateTimeField(null=True, blank=True)
    total_count = models.IntegerField(default=0)
    paid_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sub {self.razorpay_subscription_id} ({self.status})"


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    razorpay_payment_id = models.CharField(max_length=100, unique=True)
    invoice_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"Payment {self.razorpay_payment_id} ({self.amount/100:.2f} {self.currency})"
