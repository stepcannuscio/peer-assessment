from django.shortcuts import render, redirect
from django.contrib import messages
# from django.utils.translation import ugettext as _
# HOME PAGE #
def index(request):
    return render(request, 'backend/index.html')

# LOGIN PAGES #
def student_login(request):
    return render(request, 'backend/student-login.html')

def professor_login(request):
    return render(request, 'backend/professor-login.html')

# DASHBOARD PAGES
def student_home(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/student-home.html')
    args = {'message': storage}

def professor_home(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/professor-home.html')
    args = {'message': storage}

def peer_assessments(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/peer-assessments.html')
    args = {'message': storage}

def completed_assessments(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/completed-assessments.html')
    args = {'message': storage}
