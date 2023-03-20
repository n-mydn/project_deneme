from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from .models import Feedback,Department,FeedbackStatusHistory,FeedbackType,FeedbackSource,FeedbackReason,FeedbackPersonel,f_status_choice,priority_choice

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["IdCompany","Name","Surname","Email","PhoneNumber","IdDepartment","IdFeedbackType","IdFeedbackSource","IdFeedbackReason","IdFeedbackPersonel","Content","Photo"]

class AdminFeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields=["IdFeedbackStatus","IdFeedbackPriorityLevel","LastSolveDate"]
        widgets = {
            "LastSolveDate": DateTimePickerInput(),
        }

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ["name","status"]


class StatusHistoryForm(ModelForm):
    class Meta:
        model = FeedbackStatusHistory
        fields = ["history_note","history_file"]


class StatusForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["IdFeedbackStatus",]


class FeedbackTypeForm(ModelForm):
    class Meta:
        model = FeedbackType
        fields= ["name","status"]

class FeedbackReasonForm(ModelForm):
    class Meta:
        model = FeedbackReason
        fields= ["name","status"]

class FeedbackSourceForm(ModelForm):
    class Meta:
        model = FeedbackSource
        fields= ["name","status"]

class FeedbackPersonelForm(ModelForm):
    class Meta:
        model = FeedbackPersonel
        fields= ["name",]


"""
YEARS= [x for x in range(1940,2021)]
class AdminFeedbackForm(forms.ModelForm):
    feedback_status = forms.CharField(label="Durum",widget=forms.Select(choices=f_status_choice))
    feedback_level = forms.CharField(label="Seviye",widget=forms.Select(choices=priority_choice))
    feedback_lastdate = forms.DateTimeField(label="Son zaman")
    class Meta:
        model = Feedback
        fields=[
            "feedback_status",
            "feedback_level",
            "feedback_lastdate",
        ]
"""