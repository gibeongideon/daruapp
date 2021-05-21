# Generated by Django 3.1.7 on 2021-05-21 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebPa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('navbar_eder', models.CharField(blank=True, default='Daru Wheel', max_length=100, null=True)),
                ('footer1', models.CharField(blank=True, default='Darius & Co.', max_length=100, null=True)),
                ('footer2_url', models.CharField(blank=True, default='https://www.github.com/gibeongideon', max_length=100, null=True)),
                ('footer3', models.CharField(blank=True, max_length=100, null=True)),
                ('header1', models.CharField(blank=True, default='Welcome to Daruwheel', max_length=100, null=True)),
                ('header2', models.CharField(blank=True, default='Play and Win Real Cash', max_length=100, null=True)),
                ('header3', models.CharField(blank=True, max_length=100, null=True)),
                ('header4', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright_text', models.CharField(blank=True, max_length=30, null=True)),
                ('mpesa_header_depo_msg', models.TextField(blank=True, default='Enter amount and click send.Check M-pesa SMS send to your mobile NO you register with to confirm transaction.', max_length=300, null=True)),
                ('share_info', models.TextField(blank=True, default='Share the code to other people to get credit whenever they bet.Once someone register you will always get some credit whenever they place stake.Make sure they entered the code correctly when they signup.', max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
