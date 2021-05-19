# Generated by Django 3.1.7 on 2021-05-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=3)),
                ('expires_in', models.BigIntegerField()),
            ],
            options={
                'db_table': 'tbl_access_token',
            },
        ),
        migrations.CreateModel(
            name='B2CRequest',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('conversation_id', models.CharField(blank=True, max_length=40, null=True)),
                ('originator_conversation_id', models.CharField(blank=True, max_length=40, null=True)),
                ('response_code', models.CharField(blank=True, max_length=5, null=True)),
                ('response_description', models.TextField(blank=True, null=True)),
                ('request_id', models.CharField(blank=True, max_length=20, null=True)),
                ('error_code', models.CharField(blank=True, max_length=20, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'B2C Requests',
                'db_table': 'tbl_b2c_requests',
            },
        ),
        migrations.CreateModel(
            name='B2CResponse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('conversation_id', models.CharField(blank=True, max_length=40, null=True)),
                ('originator_conversation_id', models.CharField(blank=True, max_length=40, null=True)),
                ('result_type', models.CharField(blank=True, max_length=5, null=True)),
                ('result_code', models.CharField(blank=True, max_length=5, null=True)),
                ('result_description', models.TextField(blank=True, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=20, null=True)),
                ('transaction_receipt', models.CharField(blank=True, max_length=20, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('working_funds', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('utility_funds', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('paid_account_funds', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
                ('mpesa_user_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_registered_customer', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'verbose_name_plural': 'B2C Responses',
                'db_table': 'tbl_b2c_response',
            },
        ),
        migrations.CreateModel(
            name='C2BRequest',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(blank=True, max_length=20, null=True)),
                ('transaction_id', models.CharField(max_length=20, unique=True)),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('business_short_code', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_ref_number', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=50, null=True)),
                ('org_account_balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20, null=True)),
                ('third_party_trans_id', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_validated', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'C2B Requests',
                'db_table': 'tbl_c2b_requests',
            },
        ),
        migrations.CreateModel(
            name='OnlineCheckout',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('phone', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('is_paybill', models.BooleanField(default=True)),
                ('checkout_request_id', models.CharField(default='', max_length=50)),
                ('account_reference', models.CharField(default='', max_length=50)),
                ('transaction_description', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_message', models.CharField(blank=True, max_length=100, null=True)),
                ('merchant_request_id', models.CharField(blank=True, max_length=50, null=True)),
                ('response_code', models.CharField(blank=True, max_length=5, null=True)),
                ('response_description', models.CharField(blank=True, max_length=100, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Online Checkout Requests',
                'db_table': 'tbl_online_checkout_requests',
            },
        ),
        migrations.CreateModel(
            name='OnlineCheckoutResponse',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('merchant_request_id', models.CharField(blank=True, max_length=50, null=True)),
                ('checkout_request_id', models.CharField(default='', max_length=50)),
                ('result_code', models.CharField(blank=True, max_length=5, null=True)),
                ('result_description', models.CharField(blank=True, max_length=100, null=True)),
                ('mpesa_receipt_number', models.CharField(blank=True, max_length=50, null=True)),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
                ('phone', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Online Checkout Responses',
                'db_table': 'tbl_online_checkout_responses',
            },
        ),
    ]
