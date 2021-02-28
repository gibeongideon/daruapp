
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm2(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class"       : "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class"       : "form-control"
            }
        ))

class SignUpForm2(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Phone_number",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Phone_number",                
    #             "class": "form-control"
    #         }
    #     ))
    daru_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "daru_code",                
                "class": "form-control"
            }
        ))
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Refer Code",                
    #             "class": "form-control"
    #         }
    #     ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'password1', 'password2')
        
        
        
        
        
        
        
        


class SignUpForm(UserCreationForm):
    """Prepares help texts, class and placeholder attributes.

    Define methods to increase and decrese token_count amount,
    betting and check if bet is possible.
    """
    error_messages = {
        'invalid_code': _(
            "invalid code.The code doent exist"
        ),
    }
    
    username = forms.CharField(max_length=50, required=True,
        label='',
        help_text='E.g   07200200200 or 01200200200',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number.  ie 071001000'
        }))

    # first_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'First name...'
    #     }))

    # last_name = forms.CharField(max_length=30, required=False,
    #     label='', help_text='Optional',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Last name...'
    #     }))

    # phone_number = forms.CharField(max_length=150, required=True,
    #     label='',
    #     help_text='E.g   07200200200 or 01200200200',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Phone Number...'
    #     }))

    email = forms.EmailField(max_length=254, required=True,
        label='', help_text='Required. Inform a valid email unique address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email...'
        }))

    daru_code = forms.CharField(max_length=150, required=True,
        label='',
        help_text='Enter your referer CODE here.Dont have ? Enter ADMIN',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Refer code Dont have ?Enter ADMIN'
        }))

    password1 = forms.CharField(required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password...'
        }))

    password2 = forms.CharField(required=True,
        label='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password...'
        }))

    class Meta:
        model = User
        fields = ('username','email','daru_code', 'password1', 'password2')

    # def cleaned_daru_code(self):
    #     user =User.objects.get(username=self.username)
    #     if self.daru_code not in User.codes():
    #         raise ValidationError(
    #             self.error_messages['invalid_code'],
    #             code='invalid_code',
    #         )

