from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from accounts.models import *
from accounts.helpers import *
from accounts.forms import *

# HOME PAGE
def index(request):
    return render(request, 'backend/index.html')

# COURSES PAGE
def courses(request):
    course_enrollment_objects = get_list_or_404(Course_Enrollment, user=request.user.pk)
    courses = []
    for obj in course_enrollment_objects:
        course = get_object_or_404(Course, id=obj.course_id)
        courses.append(course)

    return render(request, 'backend/courses.html', {'courses': courses})

""" STUDENT PAGES """

def student_login(request):
    return render(request, 'backend/student-login.html')

def student_home(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)
    total_assessments, completed_assessments, todo_assessments, \
        missed_assessments = get_student_dashboard(request, course)

    return render(request, 'backend/student-home.html', {'course': course,
        'total_assessments': total_assessments, 'completed_assessments': completed_assessments,
        'todo_assessments': todo_assessments, 'missed_assessments': missed_assessments})
    args = {'message': storage}

def peer_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)

    todo_assessments, missed_assessments = get_peer_assessments(request, course)

    return render(request, 'backend/peer-assessments.html', {'course': course,
        'todo_assessments':todo_assessments,
        'missed_assessments': missed_assessments})
    args = {'message': storage}

def assess_peer_home(request, course_id, assessment_id):
    course = get_object_or_404(Course, id=course_id)
    assessment = get_object_or_404(Peer_Assessment, id=assessment_id)

    if request.META['HTTP_REFERER'].endswith("completed-assessments"):
        print('completedddd')
        current_team = get_current_team(request.user, course)
        teammates = get_teammates(current_team.team.id, request.user)
    else:
        teammates, current_team = get_students_not_assessed(request, course, assessment_id)

    return render(request, 'backend/assess-peer-home.html', {
        'students': teammates,'assessment': assessment, 'course': course,
})

def assess_peer(request, course_id, assessment_id):
    student_id = request.POST.get('student')
    student = get_object_or_404(User, id=student_id)

    course = get_object_or_404(Course, id=course_id)
    assessment = get_object_or_404(Peer_Assessment, id=assessment_id)

    not_open_ended, open_ended = get_questions(assessment)

    return render(request, 'backend/assess-peer.html', {
        'course': course, 'assessment': assessment, 'student': student,
        'open_ended': open_ended, 'not_open_ended': not_open_ended})

def save_answer(request, course_id, assessment_id, student_id):
    if request.method == 'POST':

        questions = request.POST.getlist('question')
        scores = request.POST.getlist('score')
        answers = request.POST.getlist('answer')

        for i in range(len(scores)):
            question = Question.objects.get(id=questions[i])

            update = Assessment_Completion.objects.get(user=request.user, assessment_id=assessment_id, student_id=student_id)
            if update:
                # answer = Answers.objects.get(question=question, user=request.user, student_id=student_id) 
            if question.is_open_ended != True:

                answer = Answer(question = question,
                    user=request.user, student_id=student_id, score=scores[i])
                update = Assessment_Completion.objects.get(user=request.user, assessment_id=assessment_id, student_id=student_id)
                update.is_completed = True
                update.save()
                answer.save()

        for i in range(len(answers)):
            question = Question.objects.get(id=questions[i+len(scores)])
            answer = Answer(answer=answers[i], question = question,
                user=request.user, student_id=student_id)
            answer.save()

        messages.success(request, f'Successfully completed assessment')

    assessment = Peer_Assessment.objects.get(id=assessment_id)
    course = Course.objects.get(id=course_id)
    teammates, current_team = get_students_not_assessed(request, course, assessment)

    if teammates:
        return redirect('assess-peer-home', course_id, assessment_id)
    else:
        return redirect('peer-assessments', course_id)

def completed_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)

    completed_assessments, editable_assessments = get_peer_assessments(request, course, completed=True)

    return render(request, 'backend/completed-assessments.html', {'course': course,
        'completed_assessments': completed_assessments, 'editable_assessments': editable_assessments})
    args = {'message': storage}


""" INSTRUCTOR PAGES """

def professor_login(request):
    return render(request, 'backend/professor-login.html')

def professor_home(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)

    return render(request, 'backend/professor-home.html', {'course': course})
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

    return render(request, 'backend/teams-students.html', {'course': course,
        'teams': teams, 'students_on_teams': students_on_teams, 'all_students': all_students})
    args = {'message': storage}

def create_team(request, course_id):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['name']
            course = get_object_or_404(Course, id=course_id)
            team = Team(course=course, name=team_name)
            try:
                team.validate_unique()
                team.save()
                messages.success(request, f'Successfuly created new team: {team_name}')
            except:
                messages.error(request, 'Team names must be unique within courses')
        else:
            messages.error(request, 'Form incorrect, trying again')

    return redirect('teams-students', course_id)

def add_student(request, course_id):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            team = form.cleaned_data['team']
            try:
                user_teams = Team_Enrollment.objects.filter(user_id = user.id)
                for user_team in user_teams:
                    team_obj = Team.objects.get(pk = user_team.team_id)
                    if team_obj.course_id == course_id:
                        user_team.is_active = False
                        user_team.save()
                team.add(user)
                messages.success(request, f'Successfuly added {user.name} to team: {team.name}')
            except:
                messages.error(request, 'Failed to add user to course')
        else:
            messages.error(request, 'Form incorrect, trying again')

    return redirect('teams-students', course_id)
