from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from accounts.models import *
from accounts.helpers import *
from accounts.forms import *





# from django.utils.translation import ugettext as _
# HOME PAGE #
def index(request):
    return render(request, 'backend/index.html')

# LOGIN PAGES #
def student_login(request):
    return render(request, 'backend/student-login.html')

def professor_login(request):
    return render(request, 'backend/professor-login.html')

def courses(request):
    course_enrollment_objects = get_list_or_404(Course_Enrollment, user=request.user.pk)
    courses = []
    for obj in course_enrollment_objects:
        course = get_object_or_404(Course, id=obj.course_id)
        courses.append(course)
    return render(request, 'backend/courses.html', {'courses': courses})

# DASHBOARD PAGES
def student_home(request, course_id):
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
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'backend/student-home.html', {'course': course})
    args = {'message': storage}

def professor_home(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'backend/professor-home.html', {'course': course})
    args = {'message': storage}

def peer_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'backend/peer-assessments.html', {'course': course})
    args = {'message': storage}

def completed_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'backend/completed-assessments.html', {'course': course})
    args = {'message': storage}

def all_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'backend/all-assessments.html', {'course': course})
    args = {'message': storage}

def teams_students(request, course_id):
    storage = messages.get_messages(request)

    # Get course
    course = get_object_or_404(Course, id=course_id)

    # Load all teams in this course
    teams = Team.objects.filter(course=course.id)

    # Load all students in this course
    student_enrollments = Course_Enrollment.objects.filter(course=course.id)
    all_students = []
    for stud in student_enrollments:
        student = User.objects.get(pk=stud.user_id)
        if not student.is_staff:
            all_students.append(student)

    # Load all students on teams
    students_on_teams = []
    for team in teams:
        students = Team_Enrollment.objects.filter(team=team.id)
        students_on_teams += students





    # enrollments = []
    # for team in teams:
    #     try:
    #         enrollment = get_list_or_404(Team_Enrollment, team=team.id)
    #         enrollments += enrollment
    #     except:
    #         print(f'No students on {team.name}')

    # students = []
    # for enrollment in enrollments:
    #     if enrollment.user_id != request.user.pk:
    #         student = get_list_or_404(User, id=enrollment.user_id)
    #         students += student

    # course_enrollments = get_list_or_404(Course_Enrollment, course=course.id)
    # for stud in course_enrollments:
    #     if stud.user_id != request.user.pk:
    #         student = get_list_or_404(User, id=stud.user_id)
    #         students += student
    # course_enrollments = get_list_or_404(Course_Enrollment, course=course.id)


    return render(request, 'backend/teams-students.html', {'course': course,
        'teams': teams, 'students_on_teams': students_on_teams, 'all_students': all_students})
    args = {'message': storage}

def create_team(request, course_id):

    if request.method == 'POST':
        print('post')
        form = CreateTeamForm(request.POST)
        print('form created')
        if form.is_valid():
            team_name = form.cleaned_data['name']
            course = get_object_or_404(Course, id=course_id)
            team = Team(course=course, name=team_name)
            print(team.name)
            try:
                team.validate_unique()
                print('valid unique')
                team.save()
                print('team addedd successfuly')
                messages.success(request, f'Successfuly created new team: {team_name}')
                print('team created successfully')
            except:
                print('not valid unique')
                messages.error(request, 'Team names must be unique within courses')
        else:
            messages.error(request, 'Form incorrect, trying again')
            print(form.errors.as_data())
    print(str(course_id))
    return redirect('teams-students', course_id)

def add_student(request, course_id):

    if request.method == 'POST':
        print('post')
        form = AddStudentForm(request.POST)
        print('form created')
        if form.is_valid():
            print(form.cleaned_data)
            user = form.cleaned_data['user']
            print(user)
            team = form.cleaned_data['team']
            print(team)

            try:
                user_teams = Team_Enrollment.objects.filter(user_id = user.id)

                for user_team in user_teams:
                    team_obj = Team.objects.get(pk = user_team.team_id)
                    if team_obj.course_id == course_id:
                        print("user already on a team in this course!")
                        user_team.is_active = False
                        user_team.save()
                team.add(user)
                messages.success(request, f'Successfuly added {user.name} to team: {team.name}')
                print('user addedd successfuly')
            except:
                print('not valid addition')
                messages.error(request, 'Failed to add user to course')
        else:
            messages.error(request, 'Form incorrect, trying again')
            print(form.errors.as_data())
    print(str(course_id))
    return redirect('teams-students', course_id)
