from django.contrib import admin
from .models import Feedback,FeedbackPersonel,FeedbackPriorityLevel,FeedbackReason,FeedbackSource,FeedbackType
from .models import City,Company,Country,Department,FeedbackStatusHistory,FeedbackStatus

from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(City)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(Department)

admin.site.register(FeedbackPersonel)
admin.site.register(FeedbackPriorityLevel)
admin.site.register(FeedbackReason)
admin.site.register(FeedbackSource)
admin.site.register(FeedbackType)
admin.site.register(FeedbackStatus)
admin.site.register(FeedbackStatusHistory)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display=["IdDepartment","selected_IdFeedbackReason","IdFeedbackType","IdFeedbackPriorityLevel"]
    def selected_IdFeedbackReason(self,obj):
        html = "<ul>"
        for feedbackreason in obj.IdFeedbackReason.all():
            html += "<li>" +feedbackreason.name +"</li>"
        html += "</ul>"
        return mark_safe(html)
