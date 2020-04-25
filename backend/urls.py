from django.contrib import admin
from django.urls import include, path
from . import views
# from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),
    path('<int:course_id>/create-team', views.create_team, name="create-team"),
    path('<int:course_id>/add-student', views.add_student, name="add-student"),

    # Student Views
    path('student-login', views.student_login, name='student-login'),
    path('<int:course_id>/student-home', views.student_home, name='student-home'),
    path('<int:course_id>/peer-assessments', views.peer_assessments, name='peer-assessments'),
    path('<int:course_id>/completed-assessments', views.completed_assessments, name='completed-assessments'),

    # Instructor Views
    path('professor-login', views.professor_login, name='professor-login'),
    path('<int:course_id>/professor-home', views.professor_home, name='professor-home'),
    path('<int:course_id>/all-assessments', views.all_assessments, name='all-assessments'),
    path('<int:course_id>/teams-students', views.teams_students, name='teams-students'),



    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),


]
