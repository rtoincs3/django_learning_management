from django.contrib import admin
from .models import TeacherProfile
from django import forms


# Register your models here.

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = "__all__"
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("id","full_name", "user", "teacher_role", "department", "joining_date")
    search_fields = ("full_name", "user__teacher_id")
    form = TeacherProfileForm

admin.site.register(TeacherProfile, TeacherProfileAdmin)