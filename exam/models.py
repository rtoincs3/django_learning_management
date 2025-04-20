from django.db import models
from faculty.models import TeacherProfile
from users.models import Department   #department Only
from student.models import StudentProfile


# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)

    '''Data integrity - -Department
        Suppose a teacher is moved to another department, or their profile changes —
        If you save department directly inside Exam, the exam stays safe and doesn't break.
    '''
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    samester = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_miniutes = models.PositiveIntegerField(help_text="Exam Duration in Miniutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="question")
    text = models.TextField()
    marks = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"Q: {self.text}"
    

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="Options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
