# Razorpay Integration Workflow Documentation

## Overview
This document outlines the workflow and implementation details of the Razorpay subscription-based payment system integration. The system is built using Django and integrates with Razorpay's subscription API to handle recurring payments.

## System Architecture

### Core Models

#### 1. Plan Model
- Represents subscription plans in the system
- Key fields:
  - `razorpay_plan_id`: Unique identifier from Razorpay
  - `name`: Plan name
  - `amount`: Amount in paise (1 INR = 100 paise)
  - `interval`: Billing interval (monthly/yearly)
  - `interval_count`: Frequency multiplier
  - `currency`: Default is INR

#### 2. Customer Model
- Stores customer information
- Key fields:
  - `razorpay_customer_id`: Unique identifier from Razorpay
  - `name`: Customer's name
  - `email`: Customer's email
  - `contact`: Customer's contact number

#### 3. Subscription Model
- Manages subscription details
- Key fields:
  - `razorpay_subscription_id`: Unique identifier from Razorpay
  - `plan`: Foreign key to Plan model
  - `customer`: Foreign key to Customer model
  - `status`: Current subscription status
  - `current_start`: Start date of current billing cycle
  - `current_end`: End date of current billing cycle
  - `total_count`: Total number of billing cycles
  - `paid_count`: Number of successful payments

#### 4. Payment Model
- Tracks individual payments
- Key fields:
  - `subscription`: Foreign key to Subscription model
  - `razorpay_payment_id`: Unique identifier from Razorpay
  - `invoice_id`: Optional invoice reference
  - `amount`: Payment amount
  - `status`: Payment status
  - `created_at`: Payment timestamp

## Workflow

### 1. Plan Creation
1. Create a plan in Razorpay dashboard or via API
2. Store plan details in the Plan model
3. Plan becomes available for subscription

### 2. Customer Onboarding
1. Create customer record in Razorpay
2. Store customer details in Customer model
3. Customer is now ready for subscription

### 3. Subscription Process
1. Customer selects a plan
2. Create subscription in Razorpay
3. Store subscription details in Subscription model
4. Subscription status is tracked and updated

### 4. Payment Processing
1. Razorpay automatically processes payments based on subscription schedule
2. Each payment is recorded in Payment model
3. Payment status is updated in real-time
4. Failed payments are handled according to Razorpay's retry policy

### 5. Subscription Management
- Track subscription status
- Monitor payment history
- Handle subscription cancellations
- Process subscription updates

## Integration Points

### Razorpay API Integration
- Plan creation and management
- Customer creation and management
- Subscription creation and tracking
- Payment processing and verification
- Webhook handling for real-time updates

### Webhook Events
The system handles various Razorpay webhook events:
- Payment success/failure
- Subscription status changes
- Invoice generation
- Payment retry attempts

## Security Considerations
- All sensitive data is stored securely
- API keys are managed through environment variables
- Webhook signatures are verified
- Payment data is encrypted

## Error Handling
- Failed payment retry mechanism
- Subscription status monitoring
- Payment verification
- Error logging and notification

## Best Practices
1. Always verify webhook signatures
2. Implement proper error handling
3. Maintain audit logs
4. Regular status monitoring
5. Backup of critical data

## Testing
- Test plans in test mode
- Verify webhook handling
- Test payment flows
- Validate subscription lifecycle

## Maintenance
- Regular status checks
- Monitor payment success rates
- Update API integrations as needed
- Maintain documentation 