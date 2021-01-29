
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect ,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login 
from django.http import HttpResponseNotFound
from django.contrib.auth import views as auth_views
# from django.contrib.auth.models import User
from .models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import  SignUpForm,SignUpForm2 ,LoginForm2


def login_view(request):
    form = LoginForm2(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "users/accounts/login.html", {"form": form, "msg" : msg})


@login_required(login_url='/users/login')
def user_page(request):
 
    # return redirect(reverse('users:user_page'))
    return render(request, 'users/page-user.html',{'user': request.user})

@login_required(login_url='/users/login')
def mine_users(request):
    mine_users = User.objects.filter(daru_code =request.user.my_code)
    
    return render(request, 'users/mine_users.html',{'mine_users': mine_users})

@login_required(login_url='/users/login')
def notification(request):
    context={}
    return render(request, 'users/notification.html',context)
    



##

class CustomLoginView(auth_views.LoginView):
    """Collect methods which extends django authentication functionality."""

    def form_valid(self, form):
        """Extend basic validation with user remember functionality.

        Check if remember checkbox was set by user and store session data
        in such case.
        """
        if self.request.POST.get('remember_me', None):
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def register(request):
    """Responsible for validation and creation of new users.

    Check if all required inputs are filled, if password and
    password confirmation are equal, if user with posted username
    already not exists and then create new user with possible friend username
    or blank string. After succesed registration proceed authentication
    and redirect to index path, otherwise return error messages to source
    registration form.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # phone_number = form.cleaned_data.get('phone_number')
            # daru_code = form.cleaned_data.get('daru_code')
    
            user = authenticate(username=username, password=raw_password)
            # user.phone_number = phone_number
            # user.daru_code = daru_code

            user.save()
            
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})