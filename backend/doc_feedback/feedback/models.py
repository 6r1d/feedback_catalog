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

    def serialize(self):
        """
        Serialize the model data.
        """
        return {
            'pk': self.pk,
            'feedback_type': self.feedback_type,
            'message': self.message,
            'email': self.email,
            'url': self.url,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
    @classmethod
    def search_by_term(cls, search_term: str, ordering:str='id'):
        """
        Shows a text search by an index.
        """
        return cls.objects.filter(message__contains=search_term).order_by(ordering)

    @classmethod
    def search_by_feedback_type(cls, feedback_type: str, ordering:str='id'):
        """
        Shows a text search by feedback type.
        """
        return cls.objects.filter(feedback_type=feedback_type).order_by(ordering)

    @classmethod
    def get_search_index(cls, ordering:str='id'):
        """
        Returns a list of items ordered.
        """
        return cls.objects.get_queryset().order_by(ordering)

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ['id']
