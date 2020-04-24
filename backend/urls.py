from django.contrib import admin
from django.urls import include, path
from . import views
# from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),

    # Student Views
    path('student-login', views.student_login, name='student-login'),
    path('student-home', views.student_home, name='student-home'),
    path('peer-assessments', views.peer_assessments, name='peer-assessments'),
    path('completed-assessments', views.completed_assessments, name='completed-assessments'),

    # Instructor Views
    path('professor-login', views.professor_login, name='professor-login'),
    path('professor-home', views.professor_home, name='professor-home'),
    path('all-assessments', views.all_assessments, name='all-assessments'),
    path('teams-students', views.teams_students, name='teams-students'),



    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),


]
