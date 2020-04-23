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
    courses = Course_Enrollment.objects.filter(user_id = request.user.pk)
    # assessment_ids = []
    completed_count = 0
    for course in courses:
        assessments = Course_Assessment.objects.filter(course_id=course.course_id)

        for assessment in assessments:
            completed_assessments = Assessment_Completion.objects.filter(
                assessment_id=assessment.assessment_id,user_id = request.user.pk, is_completed=True)
            for completed in completed_assessments:
                completed_count += 1
    print(completed_count)
    # for assessment in assessment_ids:
    #     print(assessment.course_id)
    # print(completed_assessments)



    #     print(id.team_id)
    # print(team_ids)
    # team = get_object_or_404(Team, pk=team_enrollment.team_id)
    # course  = get_object_or_404(Course, pk=team.course_id)
    # asssessment = get_object_or_404(Course_Assessment, course_id=course.id)

    # print(asssessment.assessment_id)

    # return render(request, 'polls/detail.html', {'question': question})
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
