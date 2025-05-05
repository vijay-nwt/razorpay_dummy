import os
import razorpay

# Get Razorpay credentials from environment variables
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise ValueError("Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Get all plans
plans = client.plan.all()
print(plans)