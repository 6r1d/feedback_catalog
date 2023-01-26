from django.contrib import admin
from .models import Feedback

FEEDBACK_ICONS = {
    'error': '❌',
    'suggestion': '💡'
}

class FeedbackAdmin(admin.ModelAdmin):
    """
    I wanna get printed in the Admin!
    """

    list_display = ('pk', 'custom_feedback_type', 'created_at', 'content', 'email', 'url')

    @admin.display(empty_value='N/A', description="Content")
    def content(self, obj):
        return obj.message[:75] + '…' \
               if len(obj.message) > 75 \
               else obj.message

    @admin.display(empty_value='N/A', description="Type")
    def custom_feedback_type(self, obj):
        result = obj.feedback_type
        return FEEDBACK_ICONS.get(result) or '?'

admin.site.register(Feedback, FeedbackAdmin)