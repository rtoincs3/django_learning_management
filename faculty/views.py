from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile
from  exam.models import Exam, Question, Option
from django.http import Http404
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime


# Create your views here.



def teacher_dashboard(request):
    teacher_info = None
    if request.user.is_authenticated:
        try:
            teacher_info = TeacherProfile.objects.get(user=request.user)
        except TeacherProfile.DoesNotExist:
            teacher_info = None
    return render(request, "faculty/teacher_dashboard.html", {'teacher_info': teacher_info})


def teacher_login(request):
    if request.method == "POST":
        teacher_id = request.POST.get('teacher_id')
        password = request.POST.get('password')


        try:
            #  Find by teacher id
            user = CustomUser.objects.get(teacher_id=teacher_id, user_type='teacher')
        
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            # authenticate user
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("teacher_dashboard")
            else:
                return render(request,"faculty/teacher_login.html")
        else:
            return render(request,"faculty/teacher_login.html")
    return  render(request,"faculty/teacher_login.html")

def teacher_logout(request):

    logout(request)
    return redirect("teacher_login")


@login_required
def create_exam(request):
    # get teacher profile
    teacher = TeacherProfile.objects.get(user=request.user)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get("description")
        samester = request.POST.get("semester")
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        duration_minutes = request.POST.get('duration_minutes')


        # Now create Exam
        exam = Exam.objects.create(
            title=title,
            description=description,
            teacher=teacher,
            department=teacher.department,
            samester=samester,
            start_time=start_time,
            end_time=end_time,
            duration_miniutes=duration_minutes,

        )

        return redirect('add_question', exam_id=exam.id)



    return render(request, "faculty/teacher_exam_create.html")
    

@login_required
def add_question(request, exam_id):
    # get the exam with exam_id


    exam = get_object_or_404(Exam, id=exam_id)

    # check if current teacher created exam or not
    if request.user !=exam.teacher.user:
        raise Http404("You are not authorized to add questions")
    
    if request.method == "POST":
        question_text = request.POST.get("question_text")
        marks = request.POST.get('marks')

        question = Question.objects.create(
            exam=exam,
            text=question_text,
            marks=marks
        )

        # now for options

        option_texts = request.POST.getlist('option_texts')
        correct_option = request.POST.get('correct_option')


        for idx, option_text in enumerate(option_texts):
            is_correct = (str(idx) == correct_option)

            Option.objects.create(
                question=question,
                text=option_text,
                is_correct=is_correct
            )

            return redirect('add_question', exam_id=exam.id)
        
        

    
    return render(request, "faculty/teacher_add_question.html")


@login_required
def manage_exam(request):
    exams = Exam.objects.all()

    return render(request, 'faculty/teacher_manage_exam.html', {'exams': exams})


@login_required
def update_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam).prefetch_related("Options")

    if request.method == "POST":
        try:
            #  ------------------- UPDATE EXAM INFO --------------------------------
            exam.title = request.POST.get('exam_title')
            exam.description = request.POST.get('description')
            exam.samester = request.POST.get('exam_samester')
            exam.duration_miniutes = request.POST.get('exam_duration')
            exam.start_time = request.POST.get('start_time')
            exam.end_time = request.POST.get('end_time')
            exam.save()
            messages.success(request, "Exam Info Update Succesfully")

        except Exception as e:
            messages.error(request, f"Error Occured {e}")

    context = {
        'exam': exam,
        'questions': questions
    }
    return render(request, "faculty/teacher_update_exam.html", context)


@login_required
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        try:
            question.text = request.POST.get(f"q_text_{question.id}")
            question.marks = request.POST.get(f"q_marks_{question.id}")
            question.save()

            correct_option_id = request.POST.get(f"q_correct_{question.id}")
            for option in question.Options.all():
                option_text = request.POST.get(f"q_option_{question.id}_{option.id}")
                option.text = option_text
                option.is_correct = (str(option.id) == correct_option_id)
                option.save()
            
            messages.success(request, "Question and options updated successfully!")

        except Exception as e:
            messages.error(request, "Error Occured {e}")
    
    return redirect("update_exam", exam_id=question.exam_id)



@login_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == "POST":
        q_text = request.POST.get("question_text")
        marks = request.POST.get("marks")
        options = request.POST.getlist("options")
        correct_index = request.POST.get("correct_option")

        if not options or len(options) < 2:
            messages.error(request, "Please provide at least two options.")
            return redirect("update_exam", exam_id=exam.id)

        if correct_index is None:
            messages.error(request, "Please select the correct option.")
            return redirect("update_exam", exam_id=exam.id)

        correct_index = int(correct_index)

        question = Question.objects.create(
            exam=exam,
            text=q_text,
            marks=marks
        )

        for idx, opt_text in enumerate(options):
            Option.objects.create(
                question=question,
                text=opt_text.strip(),
                is_correct=(idx == correct_index)
            )

        messages.success(request, "Question Added Successfully")
        return redirect("update_exam", exam_id=exam.id)

    return redirect("update_exam", exam_id=exam.id)

@login_required
def delete_question(request, exam_id, question_id):
    # Retrieve the exam and question
    exam = get_object_or_404(Exam, id=exam_id)
    question = get_object_or_404(Question, id=question_id, exam=exam)

    # # Debugging to print user and teacher info
    # print(f"Exam Teacher: {exam.teacher}")
    # print(f"Logged-in User: {request.user}")
    # print(f"Exam Teacher ID: {exam.teacher.id}")
    # print(f"Logged-in User ID: {request.user.id}")
    print(f"exam teacher user -- {exam.teacher.user}")
    print(f"request user -- {request.user}")

    # Check if the current user is the teacher of the exam
    if exam.teacher.user != request.user:  # Compare user IDs
        messages.error(request, "You don't have permission to delete this question")
        return redirect("update_exam", exam_id=exam.id)

    # Delete the question and all related options (because of on_delete=models.CASCADE)
    question.delete()

    messages.success(request, "Question deleted successfully")
    return redirect("update_exam", exam_id=exam.id)
