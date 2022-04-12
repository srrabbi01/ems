from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models.query_utils import Q

from api.models import *

from app_dashboard.forms import *
from app_dashboard.models import *
from app_dashboard.utils import *
from app_dashboard.decorators import *
# Create your views here.



#------------------------- auth -------------------------#
@user_is_admin
def login_view(request):
    username = ''
    if request.user.is_authenticated:        
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username =  request.POST.get('username',None)
            password =  request.POST.get('password',None)
            userObject = User.objects.filter(email = username).last()
            if userObject:
                username = userObject.username
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next',None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('dashboard')
            else:
                messages.error(request,"Email / Phone or Password didn't match. Please try again!")
    return render(request, 'app_auth/login.html',{'username':username})



@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')





def registration_view(request):
    form = UserRegistrationForm()
    userform = UserCreationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES)
        updated_request = request.POST.copy()
        updated_request['username']= request.POST.get('phone')
        userform = UserCreationForm(updated_request)

        if form.is_valid() and userform.is_valid():
            new_userform=userform.save(commit=False)
            new_userform.email = request.POST.get('email')
            new_userform.save()

            new_form = form.save(commit=False)
            new_form.user = new_userform
            new_form.reg_no = getRegnum()
            new_form.save()
            obj = UserRegistration.objects.get(phone = new_form.phone)
            messages.success(request, 'Account Created successfully !')
            accountCreatedNotifyMailFunc(obj)
            return redirect('login')
    divisions = Division.objects.all()
    context = {
        'divisions':divisions,
        'form' : form,
        'userform':userform,
    }
    return render(request, 'app_auth/registration.html',context)



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    c = {
                        "email":user.email,
                        # 'domain':'127.0.0.1:8000',
                        'domain':'ems.excellentworld.xyz',
                        'site_name': 'Ems',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                        # 'protocol': 'http',
                        }
                    html_version = 'app_auth/password_reset/password_reset_email.html'
                    html_message = render_to_string(html_version,c)
                    try:
                        message = EmailMessage(subject, html_message, settings.DEFAULT_FROM_EMAIL,[user.email])
                        message.content_subtype = 'html'
                        message.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("password_reset_done")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="app_auth/password_reset/password_reset.html", context={"password_reset_form":password_reset_form})