from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text = 'User\'s suggestions'
        self.fields['url'].help_text = 'Feedback page URL'
        self.fields['email'].help_text = 'User\'s e-mail'
        self.fields['feedback_type'].help_text = 'Type'

    class Meta:
        model = FeedbackForm
        exclude = ()

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackForm
