"""
Contains the form configuration and bindings
for the feedback catalog application.
"""

from django.contrib import admin
from django import forms
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Configure the Feedback model form
    """

    def __init__(self, *args, **kwargs):
        """
        Define the feedback form fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['message'].help_text = 'User\'s suggestions'
        self.fields['url'].help_text = 'Feedback page URL'
        self.fields['email'].help_text = 'User\'s e-mail'
        self.fields['feedback_type'].help_text = 'Type'

    class Meta:
        model = Feedback
        fields = ('message', 'feedback_type', 'url', 'email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Sets the FeedbackForm as default for the Feedback model admin.
    """
    form = FeedbackForm
