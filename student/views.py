from django.shortcuts import render, redirect, get_object_or_404
from users.models import CustomUser
from .models import StudentProfile
from exam.models import Exam
from exam.models import Question
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

# Create your views here.
@login_required(login_url='login')
def student_dashboard(request):
    student_info = None
    if request.user.is_authenticated:
        try:
            student_info = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            student_info = None

    
    return render(request, "student/student_dashboard.html", {'student_info': student_info})

# ###########################################
@login_required(login_url='login')
def student_profile(request):
    student_info = None

    if request.user.is_authenticated:
        try:
            student_info = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            student_info = None

    return render(request, "student/student_profile.html", {'student_info': student_info})


def student_login(request):
    if request.method == "POST":
        roll_number = request.POST.get('roll_number')
        password = request.POST.get("password")

        try:
            # try to find user by roll number
            user = CustomUser.objects.get(roll_number=roll_number, user_type='student')

        except CustomUser.DoesNotExist:
            user = None
        

        if user is not None:
            # authentication user
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')
            else:
                return render(request, 'student/student_login.html')
        else:
            return render(request, 'student/student_login.html')
        

    return render(request, 'student/student_login.html')


def user_logout(request):

    logout(request)
    return redirect('login')  # after logout, redirect to login page


@login_required
def available_exams(request):
    #  get student profil einformation
    student = StudentProfile.objects.get(user=request.user)
    

    #  get currnt time zone to filter out exam
    current_time = timezone.now()
    
    # get exam based of department samester and start and end time
    exams =  Exam.objects.filter(
        department=student.department,
        samester=student.samester,
        start_time__lte=current_time,
        end_time__gte=current_time
    ).annotate(total_marks = Sum('question__marks'))
    return render(request, "student/student_available_exam.html", {'exams': exams})


@login_required
def start_exam(request, exam_id):
    #  fetch exam related to button click
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam).prefetch_related('Options')

    # validate if exam is within allowed time
    current_time = timezone.now()
    if current_time < exam.start_time or current_time > exam.end_time:
        # handle error
        return redirect("availale_exam")
    
    # processed with exam
    return render(request, "student/student_start_exam.html", {'exam': exam, 'questions': questions})