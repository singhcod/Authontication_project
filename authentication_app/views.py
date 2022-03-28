from django.shortcuts import render,redirect
from .forms import SignupForm,EditProfileForm,EditAdminForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User

# Registration Form for signup


def sign_up(request):
    if request.method == 'POST':
        fm = SignupForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account_created Successfully')
            fm.save()
    else:
        fm = SignupForm()
    return render(request,'authentication/signup.html',{'form':fm})

# login view function
def user_login(request):
    if not request.user.is_authenticated:  #for authentication not display agaain after login
        if request.method == 'POST':
            fm = AuthenticationForm(request = request, data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)

                if user is not None:
                    login(request,user)
                    messages.success(request, 'Successfully Login')
                    return redirect('/profile/')
        else:
            fm = AuthenticationForm()
        return render(request,'authentication/login.html',{'form':fm})
    else:
        return redirect('/profile/')

#log out for every user

def log_out(request):
    logout(request)
    return redirect('/login/')



# creating profile

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser == True:
                users = User.objects.all()
                fm = EditAdminForm(request.POST,instance=request.user)
            else:
                users = None
                fm = EditProfileForm(request.POST,instance=request.user)
            if fm.is_valid():
                messages.success(request, 'Profile Updated Successfully !!')
                fm.save()

        else:
            if request.user.is_superuser == True:
                users = User.objects.all()
                fm = EditAdminForm(instance = request.user)
            else:
                users = None
                fm = EditProfileForm(instance = request.user)
        return render(request,'authentication/profile.html',{'name':request.user,'form':fm,'users':users})
    else:
        return redirect('/login/')

# change password with old password

def changepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user = request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                return redirect('/profile/')
        else:
            fm = PasswordChangeForm(user = request.user)
        return render(request,'authentication/changepassword.html',{'form':fm})
    else:
        return redirect('/login/')


# change password without old password
def changepassword1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user = request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                return redirect('/profile/')
        else:
            fm = SetPasswordForm(user = request.user)
        return render(request,'authentication/changepassword1.html',{'form':fm})
    else:
        return redirect('/login/')


def user_detail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk = id)
        fm = EditAdminForm(instance=pi)
        return render(request,'authentication/userdetail.html',{'form':fm})
    else:
        return redirect('/login/')