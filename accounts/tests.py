#from .models import User as _User
from .models import *
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
import random
from django.test import TestCase
from django.utils import timezone



class ModelTests(TestCase):
    def test_create_users(self):
        random_names=['Peter','Step','Carter','Jonathon']
        random_surnames = ['Song','Cannuscio','Beaulieu','Lin']
        emails = ['petersong98@gmail.com','cannuscs@bc.edu','carterb33@gmail.com','jlin@gmail.com']
        teacher_names = ["Maira","John","Ziyuan","Rosemarie"]
        teacher_surnames =["Samary","Spanger","Meng","Tagliamonte"]
        teacher_emails = ["samaman@gmail.com","spanger@god.com","ziyuan@LSD.org","tagliamonte@firsttimecoder.com"]

        is_stuff = [True,False]
        eagle_id = [12345678,87654321,13572468,24681357]
        teacher_eagle_id =[17362590,19847264,18876655,19999234]
        
        for i in range(len(random_names)):
            users = User(name = random_names[i],surname = random_surnames[i],email = emails[i],eagle_id= eagle_id[i],is_staff =  random.choice(is_stuff))
            users.save()
    #def test_create_teams(self):
        emails = ['petersong98@gmail.com','cannuscs@bc.edu']
        emails2 = ['carterb33@gmail.com','jlin@gmail.com']
        for i in range(2):
            team1 = Team(name = 'Team1',user = get_user_model().objects.get_by_natural_key(emails[i]))
            team1.save()
            team2 = Team(name = 'Team2',user =get_user_model().objects.get_by_natural_key(emails2[i]))
            team2.save()
    #def test_create_courses(self):
        course_names = ['SWE','DB&APPLICATIONS']
        course_codes= ['CSCI3356','CSCI2256']
        section_number = [1,4]
        year = [2019,2020]
        sem_of_realization = ['Fall','Spring']
        for i in range(2):
            course1 = Course(name = course_names[i],code = course_codes[i],section_number=section_number[i],year = year[i],sem_of_realization=sem_of_realization[i])
            course1.save()