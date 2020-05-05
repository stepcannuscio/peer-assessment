"""
Shell Commands

from accounts.models import *

***
Create Assessment:

from datetime import datetime
from pytz import timezone
import pytz


start_dt = pytz.utc.localize(datetime(2020,4,25,10,0,0))
end_dt =  pytz.utc.localize(datetime(2020,5,26,23,59,59))

p12 = Peer_Assessment(name="Delivery 12", start_date=start_dt, end_date=end_dt)
p12.save()

***
Add Questions to Assessment:

q1 = Question.objects.get(pk=1)
q2 = Question.objects.get(pk=2)
q3 = Question.objects.get(pk=4)
q4 = Question.objects.get(pk=5)
q5 = Question.objects.get(pk=6)
q6 = Question.objects.get(pk=7)
q7 = Question.objects.get(pk=8)
q8 = Question.objects.get(pk=9)
q9 = Question.objects.get(pk=3)
q10 = Question.objects.get(pk=10)

questions = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10]

for question in questions:
    p12.add(question)

***
Add Assessment to Course:

course = Course.objects.get(pk=4)
p6 = Peer_Assessment.objects.get(pk=6)
course.add_assessment(p6)

"""

from .models import *
from background_task import background
import pytz
from collections import OrderedDict
from django.db.models import Avg,Count

def get_teammates(team, user, exclude=None):
    if exclude:
        exclude.append(user)
        teammates = Team_Enrollment.objects.filter(team=team).exclude(user__in=exclude).select_related('user')
    else:
        teammates = Team_Enrollment.objects.filter(team=team).exclude(user=user).select_related('user')

    return teammates

def get_current_team(user, course):
    active_teams = Team_Enrollment.objects.filter(user=user.pk, is_active=True).select_related('team')

    course_team = None
    for team in active_teams:
        if team.team.course_id == course.id:
            course_team = team

    return team

def get_student_assessments(request, course):
    current_user = request.user.pk
    course_assessments = Course_Assessment.objects.filter(course = course).select_related('assessment')

    assessments = []
    for assessment in course_assessments:
        if assessment.assessment.is_published:
            student_assessment = Assessment_Completion.objects.filter(user_id=current_user, assessment_id=assessment.assessment_id)
            assessments += student_assessment
    return assessments

def get_student_dashboard(request, course):
    current_team = get_current_team(request.user, course)
    teammates = get_teammates(current_team.team.id, request.user)
    student_assessments = get_student_assessments(request, course)

    completed_assessments, assessments_length = get_complete_assessments(student_assessments, teammates)
    todo_assessments, missed_assessments = get_incomplete_assessments(student_assessments)

    total_assessments = completed_assessments + todo_assessments + missed_assessments

    return total_assessments, completed_assessments, todo_assessments, missed_assessments

def get_professor_dashboard(course):
    # Total assessments completed:
    # 1) get all assessments for this course
    # 2) get all assessment completions for this course and filter by is_completed=True
    # 3) total_assessments_completed = length of that array
    assessment_completions = get_course_assessments(course)
    total_assessments = len(assessment_completions)

    completed_assessments = get_course_assessments(course, is_completed=True)
    total_assessments_completed = len(completed_assessments)

    assessments_to_grade = 0
    for assessment in completed_assessments:
        try:
            instructor_assessment = Instructor_Assessment.objects.get(assessment_completion = assessment)
            if instructor_assessment.is_graded != True: # not graded
                # assessments_to_grade.append(assessment)
                assessments_to_grade += 1
        except:
            # assessments_to_grade.append(assessment)
            assessments_to_grade += 1

    assessments_missing = 0
    # dup_assessments = []

    incomplete_assessments = get_course_assessments(course, is_completed=False)

    for assessment in incomplete_assessments:
        if pytz.utc.localize(datetime.now()) > assessment.assessment.end_date: # Past due
            print(assessment)
            # if assessment.assessment not in dup_assessments:
            assessments_missing += 1
                # dup_assessments.append(assessment.assessment)

    print(f'Total Assessments Completed: {total_assessments_completed}')
    print(f'Total Assessments: {total_assessments}')
    print(f'Assessments to Grade: {assessments_to_grade}')
    print(f'Assessments Missing: {assessments_missing}')


    # Total assessments:
    # 1) length of all assessments for this course

    # Assessments to grade:
    # 1) get all assessments for this course
    # 2) get all assessment completions for this course and filter by is_completed=True
    # 3) loop through those assessment completions to see if an instructor assessment exists for it
    #    if it does not exist then add +1 to assessments_to_grade
    #    if it does exist, check if it is graded, if it's not add +1 to assessments_to_grade

    # Assessments missing:
    # 1) get all assessments for this course
    # 2) check which assessments are past due
    # 3) loop through the past due assessments to get their corresponding assessment_completions
    #    to see if they are completed --> if not completed, then assessments missing is +1

    # students = Course_Enrollment.objects.filter(course=course).select_related('user')
    #
    #
    # completed_assessments, assessments_length = get_complete_assessments(assessment_completions, students)
    # todo_assessments, missed_assessments = get_incomplete_assessments(assessment_completions)


    return total_assessments_completed, total_assessments, assessments_to_grade, assessments_missing





def get_peer_assessments(request, course, completed=False, team_info=False):
    current_team = get_current_team(request.user, course)
    teammates = get_teammates(current_team.team.id, request.user)
    student_assessments = get_student_assessments(request, course)

    if completed == False:
        todo_assessments, missed_assessments = get_incomplete_assessments(student_assessments)
        if team_info:
            return todo_assessments, missed_assessments, current_team, teammates
        else:
            return todo_assessments, missed_assessments
    else:
        completed_assessments, assessments_length = get_complete_assessments(student_assessments, teammates)
        editable_assessments = []
        for assessment in completed_assessments:
            if pytz.utc.localize(datetime.now()) < assessment.end_date:  # Not past due
                editable_assessments.append(assessment)
        return completed_assessments, editable_assessments

def get_incomplete_assessments(assessments):
    missed_assessments = []
    todo_assessments = []
    dup_assessments = []

    for assessment in assessments:
        if assessment.is_completed == False:


            if pytz.utc.localize(datetime.now()) > assessment.assessment.end_date:
                # Past due - missed
                if assessment.assessment not in dup_assessments:
                    missed_assessments.append(assessment)
                    dup_assessments.append(assessment.assessment)
            else:
                # To do
                if assessment.assessment not in dup_assessments:
                    todo_assessments.append(assessment)
                    dup_assessments.append(assessment.assessment)
    return todo_assessments, missed_assessments

def get_complete_assessments(assessments, teammates):
    completed_assessments = []
    assessment_log = {}

    for assessment in assessments:
        id = assessment.assessment.id
        if assessment.is_completed:

            if id not in assessment_log.keys():
                assessment_log[id] = 1
            else:
                assessment_log[id] += 1
        else:
            if id not in assessment_log.keys():
                assessment_log[id] = 0

    for key, value in assessment_log.items():
        if value == len(teammates):
            assessment = Peer_Assessment.objects.get(pk=key)
            completed_assessments.append(assessment)

    return completed_assessments, len(assessment_log.keys())

def get_students_not_assessed(request, course, assessment_id):
    current_team = get_current_team(request.user, course)
    teammates = get_teammates(current_team.team.id, request.user)

    complete_teammates = []

    for teammate in teammates:
        assessment = Assessment_Completion.objects.get(user=request.user, assessment_id=assessment_id, student=teammate.user, course=course)
        if assessment.is_completed:
            complete_teammates.append(teammate.user)
    teammates = get_teammates(current_team.team.id, request.user, exclude=complete_teammates)

    return teammates, current_team

def get_students_not_graded(user, course):
    current_students = Course_Enrollment.objects.filter(course = course).exclude(user=user).select_related('user')

    assessment_completions = get_course_assessments(course, is_completed=True)

    assessments_completed = []

    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='team_users')
    team = models.ForeignKey('Team',on_delete=models.CASCADE,related_name='teams')
    is_active = models.BooleanField(default = True)

    teams = []
    for student in current_students:
        team_enrollments = Team_Enrollment.objects.filter(user=student.user, is_active=True).select_related('user', 'team')
        for team in team_enrollments:
            if team.team.course == course:
                teams.append(team)


    for assessment in assessment_completions:
        try:
            instructor_assessment = Instructor_Assessment.objects.get(assessment_completion = assessment)
            if instructor_assessment.is_graded != True: # not graded
                assessments_completed.append(assessment)
        except:
            instructor_assessment = Instructor_Assessment(assessment_completion = assessment)
            instructor_assessment.save()
            assessments_completed.append(assessment)


    return assessments_completed, teams

def get_course_assessments(course, is_completed=None):
    course_assessments = Course_Assessment.objects.filter(course = course).select_related('assessment')

    assessment_completions = []
    for assessment in course_assessments:
        if is_completed != None:
            completed_assessments = Assessment_Completion.objects.filter(assessment_id=assessment.assessment_id, course=course, is_completed=is_completed).select_related('assessment', 'user')
        else:
            completed_assessments = Assessment_Completion.objects.filter(assessment_id=assessment.assessment_id, course=course).select_related('assessment')
        assessment_completions += completed_assessments

    return assessment_completions


def get_questions(assessment_id):
    questions = Question_Assessment.objects.filter(assessment=assessment_id).select_related('question')
    open_ended = []
    not_open_ended = []

    for question in questions:
        if question.question.is_open_ended:
            open_ended.append(question)
        else:
            not_open_ended.append(question)

    return not_open_ended, open_ended





# @background(schedule = 60)
# def generate_results(request):
#     current_user = request.user.pk
#     user_assessments = Assessment_Completion.objects.filter(user_id=current_user)



#Function that gets all teams and students within a course(instructor perspective)
def get_all_courses(request): #maybe modify this so you can get current vs previous classes
    current_user = request.user.pk
    current_courses = []
    courses = Course_Enrollment.objects.filter(user=current_user).select_related('course')
    for course in courses:
        current_courses.append(course)
    #print(current_courses[0].course.name)
    return current_courses #also returns course attributes, so you can grab info related to courses

def get_students(request): #This would only be called once you know which course you're in
    current_instructor = request.user.pk
    students = []  # not is_Staff, #matches user_id and is
    instructor_course = Course_Enrollment.objects.filter(user = current_instructor).select_related('user') #this returns all courses with the current user's id (teacher) and all users related
    current_students = Course_Enrollment.objects.filter(course_id = instructor_course[0].course_id).select_related('user')
    for student in current_students:
        if(student.user.is_staff==False):
            students.append(student)
    return students
def get_teams(request,course_id):#from instructor's perspective, at this point the course you are in is already known. Just need to populate the teams
    current_instructor = request.user.pk
    current_teams = Team.objects.filter(course_id = course_id)
    team_students = []
    for team in current_teams:
        students = Team_Enrollment.objects.filter(team = team.id)
        team_students.append(students)
    return team_students

def get_students_aggregate(request,course_id): #from instructor's perspective
    teams = get_teams(request,course_id) #returns a list of team_enrollment objects
    student_score = {}
    team_score = {}
    student_open_ended = {}
    for team in teams:
        count = team.aggregate(Count('team_id'))#QuerySet of students count
        student_count = count['team_id__count'] #num of students
        current_total = 0 #holds sum of scores
        for student in team:#student score
            # s = Answer.objects.filter(student__id = student.id)
            scores = Answer.objects.filter(student__id = student.user.id,question__is_open_ended=False, assessment_completion__is_completed = True).aggregate(Avg('score'))# all scores where student_id is
            #open_ended_answers = Answer.objects.filter(student__id = student.user.id,assessment_completion__assessment_id = assessment_id,question__is_open_ended=True,assessment_completion__is_completed = True)
            student_score[student.user.id]=scores['score__avg']
            if(scores['score__avg']!=None):
                current_total += scores['score__avg']
            curr_team_id = student.team.id
        if(student_count!=0):
            team_score[curr_team_id] = current_total/student_count
    return student_score, team_score
#Students can see the aggregate value of their own get_own_results (What other people said about them)
def get_own_results(request,course_id,assessment_id):
    current_user = request.user.pk
    temp = Answer.objects.filter(student__id=current_user,assessment_completion__assessment_id=assessment_id,assessment_completion__is_completed=True,question__is_open_ended=False)
    avg_question_score = temp.values('question__question').annotate(average_rating=Avg('score'))
    questions = []
    scores = []
    for question in avg_question_score:
        for key,val in question.items():
            if(key == 'question__question'):
                questions.append(val)
            if(key == 'average_rating'):
                scores.append(val)
    return questions,scores
def get_student_overall_grade(request,course_id):#grab the grade the teacher gives student
    current_user = request.user.pk
    grades = Instructor_Assessment.objects.filter(assessment_completion__student_id = current_user,is_graded=True,assessment_completion__course_id=course_id)
    avg_grades = grades.aggregate(Avg('grade'))
    return avg_grades['grade__avg']
    #find all teams with the instructor's course_id



#     instructor_c = team.objects.filter(user = current_instructor).select_related('course')

#from studnet perspective, student should be able to change answer after assessment complete (function that allows them to update their answers )

#click on an assessment, and it gives you all questions for that assessment

#function that gives overall score to student.

#helper function to get the assessments that instructor has graded

#function that gets the assessments that need to be graded from the instructor side

#function that gets the students who did not finish the assessment (from the instructor side)

#function that populates team they're in, assessment it's for .
#Once they click on it, it shows that Question, and relative scores and answers.

#In All Assessments


# Once someone clicks on an assessment, show all the teams for that assessment, click on a team and show all students in the team and whether or not
# it has been completed


#download function that gives the average score for each person in a team, and also shows the open ended answers

#function that changes from unpublished to published





#function that populates unpublished assessments



#helper function to get the user's aggregate score.
