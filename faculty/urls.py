from django.urls import path
from . import views

urlpatterns = [
    path("", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacherlogin/", views.teacher_login, name="teacher_login"),
    path("teacherlogout/", views.teacher_logout, name="teacher_logout"),
    path("createexam/", views.create_exam, name="create_exam"),
    path("manageexam/", views.manage_exam, name="manage_exam"),
    path("add-question/<int:exam_id>", views.add_question, name="add_question"),
    path("manageexam/<int:exam_id>", views.update_exam, name="update_exam"),
    path("manage-question/<int:question_id>", views.update_question, name="update_question"),
    path("exam/<int:exam_id>/add-question", views.add_question, name="add_question"),
    path("exam/<int:exam_id>/delete-question/<int:question_id>", views.delete_question, name="delete_question")
]