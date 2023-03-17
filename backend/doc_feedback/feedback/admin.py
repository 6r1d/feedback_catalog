"""
Configures admin panel for the Feedback app
"""

from django.contrib import admin
from feedback.models import Feedback

FEEDBACK_ICONS = {
    'error': '❌',
    'suggestion': '💡'
}

class FeedbackAdmin(admin.ModelAdmin):
    """
    Set up admin configuration for the feedback model.
    Configures fields that are available
    and functions for ones that have to be reformatted.
    """

    list_display = ('pk', 'custom_feedback_type', 'created_at', 'content', 'email', 'url')

    # pylint: disable=R0201
    @admin.display(empty_value='N/A', description="Content")
    def content(self, obj):
        """
        Shortens the long message for admin display.
        """
        return obj.message[:75] + '…' \
               if len(obj.message) > 75 \
               else obj.message

    # pylint: disable=R0201
    @admin.display(empty_value='N/A', description="Type")
    def custom_feedback_type(self, obj):
        """
        Displays the message type as an icon.
        """
        result = obj.feedback_type
        return FEEDBACK_ICONS.get(result) or '?'

admin.site.register(Feedback, FeedbackAdmin)
