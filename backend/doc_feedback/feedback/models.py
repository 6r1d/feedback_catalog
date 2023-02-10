"""
Set up the models used for the Feedback app
"""

from django.db import models


class Feedback(models.Model):
    """
    Set up the feedback model
    """
    message = models.TextField(help_text="A text of user's message.")
    email = models.CharField(max_length=400, help_text="User's email")
    url = models.CharField(
        help_text="Page URL for the feedback",
        max_length=600, default='', blank=True
    )
    feedback_type = models.CharField(
        max_length=400,
        help_text="Feedback type, be it a suggestion or an error."
    )
    created_at = models.DateTimeField(
        help_text="The date at which this message was recorded",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        help_text=(
            "The date at which this message was "
            "changed by someone with write access"
        ),
        auto_now=True
    )

    def __repr__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ['id']
