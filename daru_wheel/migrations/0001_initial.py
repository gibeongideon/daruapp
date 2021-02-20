# Generated by Django 3.1.4 on 2021-02-18 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CumulativeGain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('gain', models.FloatField(blank=True, default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DaruWheelSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('return_val', models.FloatField(blank=True, default=0, null=True)),
                ('min_redeem_refer_credit', models.FloatField(blank=True, default=1000, null=True)),
                ('refer_per', models.FloatField(blank=True, default=0, null=True)),
                ('closed_at', models.FloatField(blank=True, default=4.7, help_text='sensitive settings value.Dont edit', null=True)),
                ('results_at', models.FloatField(blank=True, default=4.8, help_text='sensitive settings value.Dont edit', null=True)),
                ('wheelspin_id', models.IntegerField(blank=True, default=1, help_text='super critical setting value.DONT EDIT!', null=True)),
                ('curr_unit', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
            ],
            options={
                'db_table': 'd_daruwheel_setup',
            },
        ),
        migrations.CreateModel(
            name='MarketType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, default='M', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('odds', models.FloatField(blank=True, max_length=10, null=True)),
                ('mrtype', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mrtypes', to='daru_wheel.markettype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WheelSpin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('results_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('receive_results', models.BooleanField(blank=True, default=False, null=True)),
                ('per_retun', models.FloatField(blank=True, default=0, null=True)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wp_markets', to='daru_wheel.markettype')),
            ],
            options={
                'db_table': 'd_wheel_markets',
            },
        ),
        migrations.CreateModel(
            name='Stake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('current_bal', models.FloatField(default=0, max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('stake_placed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wheelspins', to='daru_wheel.wheelspin')),
                ('marketselection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marketselections', to='daru_wheel.selection')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wp_stakes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('resu', models.IntegerField(blank=True, null=True)),
                ('return_per', models.FloatField(blank=True, null=True)),
                ('gain', models.DecimalField(blank=True, decimal_places=5, max_digits=100, null=True, verbose_name='gain')),
                ('closed', models.BooleanField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, null=True)),
                ('cumgain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gains', to='daru_wheel.cumulativegain')),
                ('market', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rmarkets', to='daru_wheel.wheelspin')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutCome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('result', models.IntegerField(blank=True, null=True)),
                ('pointer', models.IntegerField(blank=True, null=True)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('market', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='marketoutcomes', to='daru_wheel.wheelspin')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Istake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('stake_placed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('real', models.BooleanField(default=False)),
                ('marketselection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imarketselections', to='daru_wheel.selection')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wp_istakes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IoutCome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('inbank', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='inbank')),
                ('outbank', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='outbank')),
                ('result', models.IntegerField(blank=True, null=True)),
                ('pointer', models.IntegerField(blank=True, null=True)),
                ('closed', models.BooleanField(blank=True, default=False, null=True)),
                ('stake', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='istakes', to='daru_wheel.istake')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
