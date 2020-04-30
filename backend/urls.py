from django.contrib import admin
from django.urls import include, path
from . import views
# from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),

    # Student Views
    path('student-login', views.student_login, name='student-login'),
    path('<int:course_id>/student-home', views.student_home, name='student-home'),
    path('<int:course_id>/peer-assessments', views.peer_assessments, name='peer-assessments'),
    path('<int:course_id>/peer-assessments/<int:assessment_id>/assess-peer-home', views.assess_peer_home, name="assess-peer-home"),
    path('<int:course_id>/peer-assessments/<int:assessment_id>/assess-peer', views.assess_peer, name="assess-peer"),
    path('<int:course_id>/peer-assessments/<int:assessment_id>/save-answer/<int:student_id>', views.save_answer, name="save-answer"),
    path('<int:course_id>/completed-assessments', views.completed_assessments, name='completed-assessments'),

    # Instructor Views
    path('professor-login', views.professor_login, name='professor-login'),
    path('<int:course_id>/professor-home', views.professor_home, name='professor-home'),
    path('<int:course_id>/all-assessments', views.all_assessments, name='all-assessments'),
    path('<int:course_id>/all-assessments/<int:assessment_completion_id>', views.grade_assessment_home, name='grade-assessment-home'),
    path('<int:course_id>/all-assessments/<int:assessment_completion_id>/grade-assessment', views.grade_assessment, name='grade-assessment'),
    path('<int:course_id>/create-assessment', views.create_assessment, name="create-assessment"),
    path('<int:course_id>/view-questions/<int:assessment_id>', views.view_questions, name="view-questions"),
    path('<int:course_id>/view-questions/<int:assessment_id>/add-question', views.add_question, name="add-question"),
    path('<int:course_id>/create-question', views.create_question, name="create-question"),
    path('<int:course_id>/teams-students', views.teams_students, name='teams-students'),
    path('<int:course_id>/create-team', views.create_team, name="create-team"),
    path('<int:course_id>/add-student', views.add_student, name="add-student"),

    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),


]
