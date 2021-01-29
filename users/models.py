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

    def save(self, *args, **kwargs):
        if not self.pk:
            self.my_code = 'DA' + str(self.username).upper()

        super(User, self).save(*args, **kwargs)