from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Add three fields to existing Django User model.
      : daru_code  and my_code for reference
      : phone number field
    """
    my_code = models.CharField(max_length=150, blank=True, null=True)
    daru_code = models.CharField(max_length=150, default='ADMIN')
    phone_number = models.CharField(max_length=150, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    @staticmethod
    def format_mobile_no(mobile): # hard coded for kenya # need refactor
        mobile = str(mobile)
        if (
            mobile.startswith("07") or mobile.startswith("01"))\
                and len(mobile) == 10:
            return "254"+mobile[1:]
        elif mobile.startswith("254") and len(mobile) == 12:
            return mobile
        elif (
            mobile.startswith("7") or mobile.startswith("1"))\
                and len(mobile) == 9:
            return "254"+mobile
        else:
            return mobile+"-invalid"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.my_code = 'DA' + str(self.username).upper()
            self.phone_number = self.format_mobile_no(self.phone_number)

        super(User, self).save(*args, **kwargs)
    