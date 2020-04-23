from models import *
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
import random
from django.utils import timezone


def dummy_create_users():
    random_names=['Peter','Step','Carter','Jonathon']
    random_surnames = ['Song','Cannuscio','Beaulieu','Lin']
    emails = ['petersong98@gmail.com','cannuscs@bc.edu','carterb33@gmail.com','jlin@gmail.com']
    is_stuff = [True,False]
    eagle_id = [12345678,87654321,13572468,24681357]

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