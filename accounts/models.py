from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser,BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.crypto import get_random_string
import pytz

class MyUserManager(BaseUserManager):
    def create_user(self,name,surname,email,eagle_id,password = None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name = name,
            surname = surname,
            email = self.normalize_email(email),
            eagle_id = eagle_id
        )
        user.is_staff = False ## access to admin site
        user.is_superuser = False
        user.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_instructor_user(self,name,surname,email,eagle_id,password = None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            name = name,
            surname = surname,
            email = self.normalize_email(email),
            eagle_id = eagle_id
        )
        user.is_staff = True
        user.is_superuser = False
        user.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,name,surname,email,eagle_id, password = None):
        user = self.create_user(
            name = name,
            surname = surname,
            email=email,
            eagle_id = eagle_id,
            password = password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    def get_by_natural_key(self,email_):
        return self.get(email=email_)

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100,unique = True)
    eagle_id = models.IntegerField(unique = True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)

    objects = MyUserManager() #enables access to the methods written for managin permissions and accessing data
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname','eagle_id']
    def __str__(self):
        return self.email
    def get_short_name (self):
        return self.email
    def get_natural_key(self):
        return self.email
    def clean(self):
        if len(str(self.eagle_id)) != 8:
            raise ValidationError("Eagle ID must be 8 integers")
    def make_random_password(self,length = 15,allowed_chars = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'):
        return get_random_string(length,allowed_chars)

class Course_Enrollment(models.Model):
    course = models.ForeignKey('Course',on_delete=models.CASCADE,related_name='enrolled_courses')
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='enrolled_users')

class Team_Enrollment(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='team_users')
    team = models.ForeignKey('Team',on_delete=models.CASCADE,related_name='teams')
    is_active = models.BooleanField(default = True)

class Team(models.Model): #each team can be of 2 or more students
    course = models.ForeignKey('Course',on_delete=models.CASCADE,related_name='team_course',default = "")
    name = models.CharField(max_length = 50)

    class Meta:
        constraints = [ # Make sure the combo of team name and course are unique
            models.UniqueConstraint(fields=['course', 'name'], name='unique_team')
        ]
    def add(self,user):
        Team_Enrollment(user=user,team = self).save()

        teammates = Team_Enrollment.objects.filter(team=self).exclude(user=user).select_related('user')
        assessments = Course_Assessment.objects.filter(course=self.course).select_related('assessment')
        for mate in teammates:
            for assessment in assessments:
                try:
                    Assessment_Completion(user=mate.user,assessment=assessment.assessment,student=user,course = self.course).save()
                except:
                    print('failed1')
                try:
                    Assessment_Completion(user=user,assessment=assessment.assessment,student=mate.user,course = self.course).save()
                except:
                    pass

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length = 30)
    code = models.CharField(max_length = 30)
    section_number = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField()
    sem_of_realization = models.CharField(max_length = 30)

    class Meta:
        constraints = [ # makes sure the combination of code, section_number, year, and sem_of_realization are unique
            models.UniqueConstraint(fields=['code','section_number','year','sem_of_realization'],name = 'unique_course'),
        ]

    def add_assessment(self, assessment):
        Course_Assessment(course = self, assessment=assessment).save()
        students = Course_Enrollment.objects.filter(course= self).select_related('user')

        for student in students:
            if student.user.is_staff == False:
                course_team = None
                active_teams = Team_Enrollment.objects.filter(user_id=student.user.id, is_active=True).select_related('team')
                for team in active_teams:
                    if team.team.course == self:
                        course_team = team
                teammates = Team_Enrollment.objects.filter(team=team.team.id).exclude(user=student.user.id).select_related('user')

                for mate in teammates:
                    try:
                        Assessment_Completion(user = student.user, assessment=assessment, student=mate.user, course=self).save()
                    except:
                        pass


    def add_user(self, user):
        Course_Enrollment(course=self, user=user).save()

    def add_team(self, team):
        Team(course=self, name=team).save()

    def __str__(self):
        return self.name

class Course_Assessment(models.Model):
    course = models.ForeignKey('Course',on_delete=models.CASCADE,related_name='peer_courses')
    assessment = models.ForeignKey('Peer_Assessment',on_delete=models.CASCADE,related_name="course_assessment")

class Peer_Assessment(models.Model):
    name = models.CharField(max_length = 200,default="")
    start_date = models.DateTimeField(default = "")
    end_date = models.DateTimeField(default = "")
    is_published = models.BooleanField(default=False)
    def add(self,question):
        Question_Assessment(assessment=self,question=question).save()
    def __str__(self):
        return self.name

class Assessment_Completion(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='user_assessment')
    assessment = models.ForeignKey('Peer_Assessment',on_delete=models.CASCADE,related_name="assessment_name")
    is_completed = models.BooleanField(default = False)
    student = models.ForeignKey('User',on_delete=models.CASCADE,related_name='student_assessment', default="")
    course = models.ForeignKey('Course',on_delete=models.CASCADE,related_name='completion_courses', default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','assessment','student','course'],name = 'unique_assessment_completion'),
        ]

class Instructor_Assessment(models.Model):
    assessment_completion = models.ForeignKey('Assessment_Completion',on_delete=models.CASCADE,related_name='instructor_completion')
    is_graded = models.BooleanField(default=False)
    grade = models.PositiveIntegerField(default=0)
    comment = models.TextField(default="")

class Question_Assessment(models.Model):
    question = models.ForeignKey('Question',on_delete=models.CASCADE,related_name='questions')
    assessment = models.ForeignKey('Peer_Assessment',on_delete=models.CASCADE,related_name="question_assessment")

class Question(models.Model):
    question = models.CharField(max_length = 1000)
    is_open_ended = models.BooleanField(default=False)

class Answer(models.Model):
    answer = models.TextField(default="", blank=True)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,related_name='question_answer')
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='user_answer')
    student = models.ForeignKey('User',on_delete=models.CASCADE,related_name='student_answer', default="")
    score = models.PositiveIntegerField(default=0, blank=True)
    assessment_completion = models.ForeignKey('Assessment_Completion',on_delete=models.CASCADE,related_name='answer_completion', default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question','user','student','assessment_completion'],name = 'unique_answer'),
        ]
