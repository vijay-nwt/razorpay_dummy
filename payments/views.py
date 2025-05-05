from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from .models import Payment
import razorpay
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount')) * 100  # Convert to paise
        plan = request.POST.get('plan')
        print("amount:", amount, "plan:", plan)
        
        # Create Razorpay Order
        try:
            print("Creating Razorpay order with:", {
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })
            order = client.order.create({
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            })
        except razorpay.errors.ServerError as e:
            print("Razorpay Server Error:", e)
            return HttpResponse("Razorpay server error. Please try again later.", status=500)
        
        # Save to database
        payment = Payment.objects.create(
            amount=amount,
            razorpay_order_id=order['id'],
            plan=plan
        )
        
        return render(request, 'payments.html', {
            'key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount,
        })
    
    # For GET requests, show the plans
    return render(request, 'payments.html', {
        'key_id': settings.RAZORPAY_KEY_ID,
    })

@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        print(f"payload:{payload}")
        received_signature = request.headers.get('X-Razorpay-Signature')
        print("signature:",received_signature)

        try:
            # Verify signature
            client.utility.verify_webhook_signature(
                payload,
                received_signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )
            
            data = json.loads(payload)
            event_type = data.get('event')

            if event_type == 'payment.captured':
                payment_data = data['payload']['payment']['entity']
                payment = Payment.objects.get(
                    razorpay_order_id=payment_data['order_id']
                )
                payment.razorpay_payment_id = payment_data['id']
                payment.razorpay_signature = received_signature
                payment.status = 'completed'
                payment.save()

            elif event_type == 'payment.failed':
                # Handle failed payment
                pass

            return HttpResponse(status=200)
        
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse('Invalid signature', status=403)
        except Exception as e:
            return HttpResponse(str(e), status=500)

    return HttpResponse(status=405)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')
    return render(request, 'payment_list.html', {'payments': payments})