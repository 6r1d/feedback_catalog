"""
Feedback application configuration.
"""

from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """
    Set up the app name and the default primary key type.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
