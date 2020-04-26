from .models import *
from background_task import background
import pytz

def get_student_assessments(request, course):
    current_user = request.user.pk
    course_assessments = Course_Assessment.objects.filter(course = course).select_related('assessment')

    assessments = []

    for assessment in course_assessments:
        student_assessment = Assessment_Completion.objects.filter(user_id=current_user).filter(assessment=assessment.assessment_id)
        assessments += student_assessment

    return assessments


def get_student_dashboard(request, course):

    student_assessments = get_student_assessments(request, course)

    total_assessments = []
    completed_assessments = []
    todo_assessments = []
    missed_assessments = []

    for assessment in student_assessments:
        if assessment.is_completed == True:
            completed_assessments.append(assessment)
        elif assessment.is_completed == False:
            # print(f'End date: {assessment.assessment.end_date}')
            # print(f'Localized time: {pytz.utc.localize(datetime.now())}')
            if(pytz.utc.localize(datetime.now()) > assessment.assessment.end_date):
                missed_assessments.append(assessment)
            else:
                todo_assessments.append(assessment)
        total_assessments.append(assessment)

    return total_assessments, completed_assessments, todo_assessments, missed_assessments
# @background(schedule = 60)
# def generate_results(request):
#     current_user = request.user.pk
#     user_assessments = Assessment_Completion.objects.filter(user_id=current_user)


#grab the assessments that students missed
def get_missed_assignments(request):
    current_user = request.user.pk
    missed_assessments = []
    assessments = Assessment_Completion.objects.filter(user_id=current_user).select_related('assessment')
    for assessment in assessments:
        if(pytz.utc.localize(datetime.now()) > assessment.assessment.end_date):
            missed_assessments.append(assessment)
    return missed_assessments

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
    current_teams = Team.objects.filter(course = course_id)
    team_students = []
    for team in current_teams:
        students = Team_Enrollment.objects.filter(team = team.id)
        team_students.append(students)

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
