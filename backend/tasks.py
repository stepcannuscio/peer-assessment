from background_task import background
from accounts.models import *
from django.core.mail import send_mail
from accounts.helpers import *
import pytz
from datetime import datetime
from pytz import timezone

@background(schedule=60) #sends an email to students who

def make_automatic_zero():
    incomplete_assessments = Assessment_Completion.objects.filter(is_completed=False)
    past_due_assessments = [] #past due and incomplete
    for assessment in incomplete_assessments:
        if(assessment.assessment.end_date < pytz.utc.localize(datetime.now())):
            past_due_assessments.append(assessment)
    for assessment in past_due_assessments:
        print("HERE!")
        Instructor_Assessment(assessment_completion_id = assessment.id,is_graded=True,grade = 0,comment="incomplete").save()
