# rzrpay/management/commands/sync_plans.py
from django.core.management.base import BaseCommand
from django.conf import settings
import razorpay
from rzrpay.models import Plan



class Command(BaseCommand):
    help = "Sync Razorpay subscription plans into local DB"

    def handle(self, *args, **options):
        client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
        plans_data = client.plan.all()
        print("plan data:",plans_data)
        items = plans_data.get('items', [])

        for p in items:
            item = p['item']  # extract nested plan details
            Plan.objects.update_or_create(
                razorpay_plan_id=p['id'],
                defaults={
                    'name': item['name'],
                    'description': item.get('description', ''),
                    'amount': item['amount'],  # in paise, matches your model
                    'currency': item['currency'],
                    'interval': p['period'],
                    'interval_count': p['interval']
                }
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Synced {len(items)} plan(s) successfully."))
