from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from .models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()


def validate_refercode(refercode):
    from .models import User  # fix circular import
    usecode = User.objects.get(id=1).code
    try:
        User.objects.get(code=refercode)
    except User.DoesNotExist:
        raise ValidationError(
            _('No one has such refer-code.Enter correctly or Use %(usecode)s if you  dont have one'),
            params={'refercode': refercode, 'usecode': usecode}
        )
