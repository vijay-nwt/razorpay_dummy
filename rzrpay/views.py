from django.shortcuts import render

# Create your views here.
import razorpay
import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Plan, Customer, Subscription,Payment
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))

def subscribe(request, plan_id):
    print("request:",request.__dict__)
    plan = get_object_or_404(Plan, id=plan_id)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        contact = request.POST['contact']
        # Create Razorpay Customer
        cust_data = {
            "name": name,
            "email": email,
            "contact": contact,
            "fail_existing": 0  # set to 0 to reuse existing or 1 to fail if exists
        }
        cust = razorpay_client.customer.create(data=cust_data)  # Creates customer via API&#8203;:contentReference[oaicite:5]{index=5}
        customer = Customer.objects.create(
            razorpay_customer_id=cust['id'],
            name=name, email=email, contact=contact
        )
        # Create Razorpay Subscription
        sub_data = {
            "plan_id": plan.razorpay_plan_id,
            "customer_id": cust['id'],
            "total_count": int(request.POST.get('total_count', 12)),  # e.g. 12 cycles
            "quantity": 1,
            "customer_notify": 1,
            # Optionally schedule start time (UNIX timestamp):
            # "start_at": int(datetime.now().timestamp())
        }
        subscription_response = razorpay_client.subscription.create(data=sub_data)  # API call&#8203;:contentReference[oaicite:6]{index=6}
        subscription = Subscription.objects.create(
            plan=plan,
            customer=customer,
            razorpay_subscription_id=subscription_response['id'],
            status=subscription_response['status'],
            total_count=subscription_response['total_count'],
            paid_count=subscription_response['paid_count']
        )
        return redirect('subscription_detail', pk=subscription.pk)
    return render(request, 'subscribe.html', {'plan': plan})



@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        # Read and verify webhook payload
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        payload = request.body.decode()
        print("payload:",payload)
        signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
        try:
            razorpay_client.utility.verify_webhook_signature(payload, signature, webhook_secret)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Invalid signature")

        data = json.loads(payload)
        event = data.get('event')
        sub_data = data['payload']['subscription']['entity']
        sub_id = sub_data['id']
        subscription = Subscription.objects.filter(razorpay_subscription_id=sub_id).first()
        if not subscription:
            return HttpResponse(status=200)  # ignore unknown subscriptions

        # Handle subscription events
        if event == 'subscription.activated':
            subscription.status = sub_data.get('status', subscription.status)
            subscription.current_start = datetime.fromtimestamp(sub_data.get('current_start')) if sub_data.get('current_start') else None
            subscription.current_end   = datetime.fromtimestamp(sub_data.get('current_end')) if sub_data.get('current_end') else None
            subscription.save()
        elif event == 'subscription.charged':
            # A payment was made; record it
            pay_data = data['payload']['payment']['entity']
            Payment.objects.create(
                subscription=subscription,
                razorpay_payment_id=pay_data['id'],
                invoice_id=pay_data.get('invoice_id'),
                amount=pay_data['amount'],
                currency=pay_data['currency'],
                status=pay_data['status'],
                created_at=datetime.fromtimestamp(pay_data['created_at'])
            )
        elif event == 'subscription.cancelled':
            subscription.status = 'cancelled'
            subscription.save()
    # (Handle other events as needed)
    return HttpResponse(status=200)


from django.views import View

def plan_list(request):
    plans = Plan.objects.all()
    return render(request, 'plan_list.html', {'plans': plans})

def subscription_detail(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    return render(request, 'subscription_detail.html', {'subscription': subscription,'KEY_ID': settings.KEY_ID})

