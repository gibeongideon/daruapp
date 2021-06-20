# Generated by Django 3.1.7 on 2021-06-20 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('token_count', models.IntegerField(default=0)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('actual_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('withraw_power', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('refer_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('trial_balance', models.DecimalField(decimal_places=2, default=50000, max_digits=12)),
                ('cum_deposit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cum_withraw', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'd_accounts',
                'ordering': ('-user_id',),
            },
        ),
        migrations.CreateModel(
            name='AccountSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('curr_unit', models.FloatField(blank=True, default=0, null=True)),
                ('min_redeem_refer_credit', models.FloatField(blank=True, default=1000, null=True)),
                ('auto_approve', models.BooleanField(blank=True, default=False, null=True)),
                ('withraw_factor', models.FloatField(blank=True, default=1, null=True)),
            ],
            options={
                'db_table': 'd_accounts_setup',
            },
        ),
        migrations.CreateModel(
            name='C2BTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('phone_number', models.BigIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('success', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('confirmed', models.BooleanField(blank=True, default=False, null=True)),
                ('deposited', models.BooleanField(blank=True, null=True)),
                ('deposit_type', models.CharField(blank=True, default='Shop Deposit', max_length=100, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'd_deposits',
            },
        ),
        migrations.CreateModel(
            name='CashTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('success', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashWithrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('cancelled', models.BooleanField(blank=True, default=False, null=True)),
                ('withrawned', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'db_table': 'd_withrawals',
            },
        ),
        migrations.CreateModel(
            name='Curr_Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('curr_unit', models.DecimalField(decimal_places=5, default=1, max_digits=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=30)),
                ('rate', models.DecimalField(blank=True, decimal_places=5, max_digits=6, null=True)),
                ('amount_equip_to_one_ksh', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'd_currency',
            },
        ),
        migrations.CreateModel(
            name='RefCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('current_bal', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('credit_from', models.CharField(blank=True, max_length=200, null=True)),
                ('closed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'd_refcredits',
            },
        ),
        migrations.CreateModel(
            name='RefCreditTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('succided', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'd_refcredit_trans',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('now_bal', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='now_bal')),
                ('trans_type', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'd_trans_logs',
                'ordering': ('-created_at',),
            },
        ),
    ]
