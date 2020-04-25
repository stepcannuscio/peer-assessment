from .models import *
from background_task import background

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

#grab the assessments that studnets missed

def get_missed_assignments(request,is_completed):
    current_user = request.user.pk
    missed_assessments = []
    assessments = Assessment_Completion.objects.filter(user_id=current_user)
    assessments.prefetch_related('assessment')
    for assessment in assessments:
        if(datetime.now > assessment.end_date):
            missed_assessments.append(assessment)
    return missed_assessments


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

#Function that gets all teams and students within a course




#function that populates unpublished assessments



#helper function to get the user's aggregate score.
