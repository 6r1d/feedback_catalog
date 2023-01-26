from django.db import models


class Feedback(models.Model):
    message = models.TextField()
    email = models.CharField(max_length=400)
    url = models.CharField(max_length=600, default='', blank=True)
    # Feedback type: general, idea, issue
    # Named in camelcase to use with feedback-js
    feedback_type = models.CharField(max_length=400)
    # Dates of the creation and updating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ['id']