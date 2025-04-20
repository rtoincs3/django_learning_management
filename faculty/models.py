from django.db import models
from django.contrib.auth import get_user_model
from users.models import Department

# Create your models here.

CustomUser = get_user_model()

def teacher_profile_upload_path(instance, filename):
    return f"teacher_profile/{instance.teacher_id}/{filename}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    profile_picture = models.ImageField(upload_to=teacher_profile_upload_path, blank=True, null=True)

    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject_specialization = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    experience_year = models.IntegerField(default=0)

    teacher_role = models.CharField(max_length=20, null=True, blank=True)
    # all fields to create teacher profile
    teacher_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, default=3398)

    def save(self, *args, **kwargs):
        # if not user create user
        if not self.user:
            user = CustomUser.objects.create_user(
                username=self.teacher_id,
                teacher_id = self.teacher_id,
                password=self.password,
                user_type='teacher'
            )

            self.user = user
        super(TeacherProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}"

