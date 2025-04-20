# exams/admin.py

from django.contrib import admin
from .models import Exam, Question, Option
from django import forms


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = "__all__"
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)

        # Set the correct input format for the datetime fields
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']

        # Prepopulate with existing datetime values (ensure correct format)
        if self.instance.start_time:
            self.fields['start_time'].initial = self.instance.start_time.strftime('%Y-%m-%dT%H:%M')
        if self.instance.end_time:
            self.fields['end_time'].initial = self.instance.end_time.strftime('%Y-%m-%dT%H:%M')



class QuestionInline(admin.TabularInline):
    model = Question

class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "get_department", "samester", "start_time", "end_time")
    list_filter = ("teacher__department", "samester")
    search_fields = ("title", "teacher__full_name", "teacher__department__name")
    form = ExamForm

    inlines = [QuestionInline]

    def get_department(self, obj):
        return obj.teacher.department if obj.teacher else None
    get_department.admin_order_field = 'teacher__department'
    get_department.short_description = 'Department'

class OptionInline(admin.TabularInline):    # or StackedInline for a diffrent style
    model = Option
    extrea = 4 # display four option
    max_num = 4
    min_num = 4
    can_delete = False

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "text", "marks")
    list_filter = ("exam",)
    search_fields = ("text",)
    form = QuestionForm

    inlines = [OptionInline]

    # exams/admin.py

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = "__all__"
        widgets = {
            'text': forms.TextInput(attrs={'size': '50'}),
        }

class OptionAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")
    list_filter = ("question",)
    search_fields = ("text",)
    form = OptionForm





admin.site.register(Exam, ExamAdmin)

