# Generated by Django 5.1.6 on 2025-04-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='plan',
            field=models.CharField(choices=[('basic', 'Basic'), ('advanced', 'Advanced'), ('business', 'Business')], default='basic', max_length=20),
        ),
    ]
