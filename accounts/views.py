from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils.translation import ugettext as _
from .helpers import *


# AUTH #
def log_in(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:

        # Student tries to login from professor page
        if request.META['HTTP_REFERER'].endswith('professor-login') and user.is_staff != True:
            print('professor page but not professor ')
            messages.error(request, 'You must login from the student page')
            return redirect('/professor-login')

        # Professor tries to login from student page
        elif request.META['HTTP_REFERER'].endswith('student-login') and user.is_staff:
            print('student page but professor ')
            messages.error(request, 'You must login from the professor page')
            return redirect('/student-login')

        # Professor logs in from correct page
        elif request.META['HTTP_REFERER'].endswith('professor-login') and user.is_staff == True:
            login(request, user)
            print('logged in')
            return redirect('/courses')

        # Student logs in from correct page
        elif request.META['HTTP_REFERER'].endswith('student-login') and user.is_staff != True:
            login(request, user)
            print('logged in')
            #get_peer_assessments(request,is_completed=False)
            return redirect('/courses')

        else:
            messages.error(request, 'Wrong Credentials')
            if request.META['HTTP_REFERER'].endswith('professor-login'):
                return redirect('/professor-login')
            elif request.META['HTTP_REFERER'].endswith('student-login'):
                return redirect('/student-login')

    # Invalid Credentials
    else:
        print('invalid login')
        messages.error(request, 'Wrong Credentials')
        if request.META['HTTP_REFERER'].endswith('professor-login'):
            return redirect('/professor-login')
        elif request.META['HTTP_REFERER'].endswith('student-login'):
            return redirect('/student-login')

def log_out(request):
    try:
        if request.user.is_staff:
            logout(request)
            return redirect('/professor-login')
        else:
            logout(request)
            return redirect('/student-login')
    except:
        if request.user.is_staff:
            return redirect('/professor-home')
        else:
            return redirect('/student-home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        print(f'{request.user}')
        print(f'{request.POST}')
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            if request.user.is_staff:
                return redirect('/professor-home')
            else:
                return redirect('/student-home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change-password.html', {
        'form': form
    })
