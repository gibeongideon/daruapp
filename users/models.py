from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .validators import validate_refercode


class User(AbstractUser):
    """Add three fields to existing Django User model.
      : referer_code  , code n 4ne-nuber for reference
    """

    code = models.CharField(
        max_length=150, unique=True, null=True
    )  # auto generated on save
    referer_code = models.CharField(
        validators=[validate_refercode], max_length=150, blank=True, null=True
    )
    phone_number = models.CharField(max_length=150, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.username

    @staticmethod
    def format_mobile_no(mobile):  # hard coded for kenya # need refactor
        mobile = str(mobile)
        if (mobile.startswith("07") or mobile.startswith("01")) and len(mobile) == 10:
            return "254" + mobile[1:]
        if mobile.startswith("254") and len(mobile) == 12:
            return mobile
        if (mobile.startswith("7") or mobile.startswith("1")) and len(mobile) == 9:
            return "254" + mobile

        return mobile + "-invalid_phone_number"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = (
                str(uuid.uuid4()).upper()[:3] + "D" + str(self.username[-3:]).upper()
            )  # Auto generate code
            # if self.phone_number is None:
            self.phone_number = self.format_mobile_no(self.username)

        super(User, self).save(*args, **kwargs)
