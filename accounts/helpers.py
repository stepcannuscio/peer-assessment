from .models import *
from background_task import background
import pytz

def get_peer_assessments(request,is_completed):
    current_user = request.user.pk
    completed_assessments =[]
    assessments = Assessment_Completion.objects.filter(user_id=current_user)
    #print(assessments)
    if (is_completed==True):#user selects to see all assessments that are completed
        for assessment in assessments:
            if(assessment.is_completed==True):
                completed_assessments.append(assessment)
    else:#grab everything
        for assessment in assessments:
            if(assessment.is_completed == False):
                completed_assessments.append(assessment)
    return completed_assessments
def get_dashboard(request,is_completed): #can return all assessments, implement
    current_user = request.user.pk
    all_assessments = []
    assessments = Assessment_Completion.objects.filter(user_id=current_user)
    for assessment in assessments:
        all_assessments.append(assessment)
    return all_assessments

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

# def get_teams(request):#from instructor's perspective
#     current_instructor = request.user.pk
#     teams =  []

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
