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

def assess_results(request, course_id, assessment_id):
    course = get_object_or_404(Course, id=course_id)
    assessment = get_object_or_404(Peer_Assessment, id=assessment_id)
#    aggResults = get_own_results(request, course_id=course_id, assessment_id=assessment_id)

    if request.META['HTTP_REFERER'].endswith("completed-assessments"):
        print('completedddd')
        current_team = get_current_team(request.user, course)
        teammates = get_teammates(current_team.team.id, request.user)
    else:
        teammates, current_team = get_students_not_assessed(request, course, assessment_id)

    return render(request, 'backend/assess-results.html', { 
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

        assessment_completion = Assessment_Completion.objects.get(user=request.user, assessment_id=assessment_id, student_id=student_id, course_id=course_id)

        for i in range(len(scores)):
            question = Question.objects.get(id=questions[i])

            if question.is_open_ended != True:

                if assessment_completion.is_completed: # Update
                    update = Answer.objects.get(question=question, user=request.user, student_id=student_id, assessment_completion=assessment_completion)
                    update.score = scores[i]
                    update.save()
                else:
                    answer = Answer(question = question,
                        user=request.user, student_id=student_id, score=scores[i], assessment_completion=assessment_completion)

                    answer.save()

        for i in range(len(answers)):
            question = Question.objects.get(id=questions[i+len(scores)])

            if assessment_completion.is_completed: # Update
                update = Answer.objects.get(question=question, user=request.user, student_id=student_id, assessment_completion=assessment_completion)
                update.answer = answers[i]
                update.save()
            else:
                answer = Answer(answer=answers[i], question = question,
                    user=request.user, student_id=student_id, assessment_completion=assessment_completion)
                answer.save()

        assessment_completion.is_completed = True
        assessment_completion.save()

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

    total_assessments_completed, total_assessments, assessments_to_grade, \
        assessments_missing = get_professor_dashboard(course)

    print(f'Total Assessments Completed: {total_assessments_completed}')
    print(f'Total Assessments: {total_assessments}')
    print(f'Assessments to Grade: {assessments_to_grade}')
    print(f'Assessments Missing: {assessments_missing}')

    return render(request, 'backend/professor-home.html', {'course': course,
        'total_assessments_completed': total_assessments_completed, 'total_assessments': total_assessments,
        'assessments_to_grade': assessments_to_grade, 'assessments_missing': assessments_missing})
    args = {'message': storage}

def all_assessments(request, course_id):
    storage = messages.get_messages(request)
    course = get_object_or_404(Course, id=course_id)

    assessments_to_grade, teams = get_students_not_graded(request.user, course)
    course_assessments = Course_Assessment.objects.filter(course = course).select_related('assessment')

    return render(request, 'backend/all-assessments.html', {'course': course,
        'assessments_to_grade': assessments_to_grade, 'teams': teams,
        'assessments': course_assessments})
    args = {'message': storage}

def grade_assessment_home(request, course_id, assessment_completion_id):
    course = get_object_or_404(Course, id=course_id)
    assessments = Assessment_Completion.objects.filter(id=assessment_completion_id).select_related('user', 'assessment')
    assessment = assessments[0]
    instructor_assessment = Instructor_Assessment.objects.get(assessment_completion = assessment)

    answers = Answer.objects.filter(user=assessment.user, student=assessment.student, assessment_completion = assessment).select_related('question')

    return render(request, 'backend/grade-assessments.html', {'course': course,
        'answers': answers, 'instructor_assessment': instructor_assessment,
        'assessment': assessment})
    args = {'message': storage}

def grade_assessment(request, course_id, assessment_completion_id):
    if request.method == 'POST':
        print(request.POST)

        instructor_assessment_id = request.POST.getlist('instructor-assessment-id')[0]
        grade = request.POST.getlist('grade')[0]
        comment = request.POST.getlist('comment')[0]

        instructor_assessment = Instructor_Assessment.objects.get(id=instructor_assessment_id)
        instructor_assessment.grade = grade
        instructor_assessment.comment = comment
        instructor_assessment.is_graded = True
        instructor_assessment.save()

    return redirect('all-assessments', course_id)

def create_assessment(request, course_id):
    if request.method == 'POST':
        assessment_name = request.POST.getlist('assessment-name')[0]
        start_date = request.POST.getlist('start-date')[0]
        end_date = request.POST.getlist('end-date')[0]

        assessment = Peer_Assessment(name=assessment_name, start_date=start_date, end_date=end_date)
        assessment.save()
        course = Course.objects.get(id=course_id)
        course.add_assessment(assessment)

    return redirect('all-assessments', course_id)

def view_questions(request, course_id, assessment_id):
    assessment = Peer_Assessment.objects.get(id=assessment_id)

    course_assessments = Course_Assessment.objects.filter(course_id = course_id).select_related('assessment')

    all_questions = []
    for course_assessment in course_assessments:
        questions = Question_Assessment.objects.filter(assessment=course_assessment.assessment).select_related('question')
        for question in questions:
            if question.question not in all_questions:
                all_questions.append(question.question)

    current_questions = Question_Assessment.objects.filter(assessment=assessment).select_related('question')

    return render(request, 'backend/view-questions.html', {'assessment': assessment,
        'course_id': course_id, 'all_questions': all_questions, 'current_questions': current_questions})
    args = {'message': storage}

def add_question(request, course_id, assessment_id):
    if request.method == 'POST':

        assessment = Peer_Assessment.objects.get(id=assessment_id)
        question_ids = request.POST.getlist('question')

        for question_id in question_ids:
            question = Question.objects.get(id=question_id)
            assessment.add(question)

        new_questions = request.POST.getlist('new-question')
        bools = request.POST.getlist('bool')

        if len(new_questions) >= 1 and new_questions[0] != "":

            for i in range(len(new_questions)):
                question = Question(question=new_questions[i], is_open_ended=bools[i])
                question.save()
                assessment.add(question)
        assessment.is_published = True
        assessment.save()

    return redirect('all-assessments', course_id)

def create_question(request, course_id):
    if request.method == 'POST':
        print(request.POST)

        question = request.POST.getlist('question')[0]
        is_open_ended = request.POST.getlist('bool')[0]


    return redirect('all-assessments', course_id)

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
    student_scores,team_scores = get_students_aggregate(request,course_id = course_id)
    # Load all students on teams
    students_on_teams = []
    for team in teams:
        students = Team_Enrollment.objects.filter(team=team.id)
        students_on_teams += students

    return render(request, 'backend/teams-students.html', {'course': course,'student_scores':student_scores, 'team_scores':team_scores,
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
