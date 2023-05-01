# Generated by Django 4.1.3 on 2023-05-01 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('authorization_code', models.CharField(max_length=50)),
                ('subscription_plan', models.BooleanField(default=False)),
                ('payment_interval', models.CharField(choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], max_length=10, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('card_first_six_digit', models.CharField(max_length=6)),
                ('card_last_four_digit', models.CharField(max_length=4)),
                ('ccv', models.CharField(max_length=3)),
                ('country_code', models.CharField(max_length=4)),
                ('expiry_month', models.CharField(max_length=2)),
                ('expiry_year', models.CharField(max_length=4)),
                ('card_type', models.CharField(choices=[('visa', 'Visa'), ('verve', 'Verve'), ('master card', 'Master Card')], max_length=11, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('S', 'Success'), ('F', 'Failed')], default='P', max_length=1)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_time'],
                'permissions': [('view_history', 'Can view history')],
            },
        ),
    ]