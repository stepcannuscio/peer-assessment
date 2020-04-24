from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import *
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
    # # team_enrollment = get_object_or_404(Team_Enrollment, user=request.user.pk)
    # team_ids = Team_Enrollment.objects.filter(user=request.user.pk)

    # courses = Course_Enrollment.objects.filter(user_id = request.user.pk)
    # completed_count = 0
    # for course in courses:
    #     assessments = Course_Assessment.objects.filter(course_id=course.course_id)
    #
    #     for assessment in assessments:
    #         completed_assessments = Assessment_Completion.objects.filter(
    #             assessment_id=assessment.assessment_id,user_id = request.user.pk, is_completed=True)
    #         for completed in completed_assessments:
    #             completed_count += 1
    # print(completed_count)

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

def all_assessments(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/all-assessments.html')
    args = {'message': storage}

def teams_students(request):
    storage = messages.get_messages(request)
    return render(request, 'backend/teams-students.html')
    args = {'message': storage}
