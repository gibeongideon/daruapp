from django.db import models

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True



class WebPa(models.Model):
    navbar_eder= models.CharField(max_length=30,default='Daru Wheel', blank =True,null=True)
    footer1= models.CharField(max_length=30,default='Darius & Co.', blank =True,null=True)
    footer2_url= models.CharField(max_length=30,default='https://www.github.com/gibeongideon', blank =True,null=True)
    footer3= models.CharField(max_length=30, blank =True,null=True)
    header1= models.CharField(max_length=30,default='Welcome to Daruwheel', blank =True,null=True)
    header2= models.CharField(max_length=30,default='Play and Win Real Cash', blank =True,null=True)
    header3= models.CharField(max_length=30, blank =True,null=True)
    header4= models.CharField(max_length=30, blank =True,null=True)
    copyright_text= models.CharField(max_length=30, blank =True,null=True)

    mpesa_header_depo_msg = models.CharField(
        max_length=30,
        default='Enter amount and click send.Check M-pesa SMS send to your mobile NO you register with to confirm transaction.',
        blank =True,
        null=True)

