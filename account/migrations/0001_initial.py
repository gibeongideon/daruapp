# Generated by Django 3.1.7 on 2021-03-11 16:40

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
            name='AccountSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('curr_unit', models.FloatField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'd_accounts_setup',
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
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('now_bal', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='now_bal')),
                ('trans_type', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_transactions_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_trans_logs',
                'ordering': ('-created_at',),
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
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_accountcredit_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_refcredits',
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
                ('common_var', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curr_vars', to='account.curr_variable')),
            ],
            options={
                'db_table': 'd_currency',
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
                ('withrawned', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_withrawals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_withrawals',
            },
        ),
        migrations.CreateModel(
            name='CashDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('deposited', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('currency_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_deposits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_deposits',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('token_count', models.IntegerField(default=0)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('actual_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('withrawable_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('refer_balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('trial_balance', models.DecimalField(decimal_places=2, default=50000, max_digits=12)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_accounts',
                'ordering': ('-user_id',),
            },
        ),
    ]
