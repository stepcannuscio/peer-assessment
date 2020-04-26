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

    course = get_object_or_404(Course, id=course_id)

    total_assessments, completed_assessments, todo_assessments, missed_assessments = get_student_dashboard(request, course_id)

    return render(request, 'backend/student-home.html', {'course': course,
        'total_assessments': total_assessments, 'completed_assessments': completed_assessments,
        'todo_assessments': todo_assessments, 'missed_assessments': missed_assessments})

    args = {'message': storage}

def professor_home(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'backend/professor-home.html', {'course': course})
    args = {'message': storage}

def peer_assessments(request, course_id):
    storage = messages.get_messages(request)

    course = get_object_or_404(Course, id=course_id)
    teams = Team_Enrollment.objects.filter(user_id=request.user.pk, is_active=True).select_related('team')

    team = None
    for user_team in teams:
        if user_team.team.course_id == course_id:
            team = user_team
    print(team)

    students = []
    if team:
        students = Team_Enrollment.objects.filter(team=team.team.id).exclude(user=request.user).select_related('user')

    print(students[0].user.id)

    total_assessments, completed_assessments, todo_assessments, missed_assessments = get_student_dashboard(request, course_id)

    return render(request, 'backend/peer-assessments.html', {'course': course,
        'student': students[0], 'todo_assessments':todo_assessments,
        'missed_assessments': missed_assessments})

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

def save_answer(request, course_id, assessment_id, student_id):
    if request.method == 'POST':
        print('post')
        assessment = Peer_Assessment.objects.get(id=assessment_id)
        # questions = Question_Assessment.objects.filter(assessment=assessment_id).select_related('question')


        questions = request.POST.getlist('question')
        scores = request.POST.getlist('score')
        answers = request.POST.getlist('answer')

        student = User.objects.get(id=student_id)


        print(questions)
        print(scores)
        print(answers)

        for i in range(len(scores)):
            question = Question.objects.get(id=questions[i])

            if question.is_open_ended != True:
                answer = Answer(question = question,
                    user=request.user, student=student, score=scores[i])

            answer.save()

        for i in range(len(answers)):
            question = Question.objects.get(id=questions[i+len(scores)])

            answer = Answer(answer=answers[i], question = question,
                user=request.user, student=student)
            answer.save()

        messages.success(request, f'Successfully completed assessment')

    return redirect('peer-assessments', course_id)


def assess_peer(request, course_id, assessment_id, student_id):
    print('*** ASSESS PEER ***')
    print(course_id)
    print(assessment_id)
    print(student_id)
    student = User.objects.get(id=student_id)

    course = get_object_or_404(Course, id=course_id)
    assessment = get_object_or_404(Peer_Assessment, id=assessment_id)
    teams = Team_Enrollment.objects.filter(user_id=request.user.pk, is_active=True).select_related('team')

    team = None
    for user_team in teams:
        if user_team.team.course_id == course_id:
            team = user_team
    print(team)

    students = []
    if team:
        students = Team_Enrollment.objects.filter(team=team.team.id).exclude(user=request.user).select_related('user')

    print(students[0].user.name)

    questions = Question_Assessment.objects.filter(assessment=assessment_id).select_related('question')

    open_ended = []
    not_open_ended = []
    # answers = []
    for question in questions:
        if question.question.is_open_ended:
            open_ended.append(question)
        else:
            not_open_ended.append(question)

    return render(request, 'backend/assess-peer.html', {
        'course': course, 'assessment': assessment, 'team': team, 'student': student,
        'students': students,
        'open_ended': open_ended, 'not_open_ended': not_open_ended})
