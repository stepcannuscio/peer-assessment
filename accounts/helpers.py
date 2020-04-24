from .models import *


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







