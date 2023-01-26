from django import template
from feedback.models import Feedback

register = template.Library()

@register.simple_tag()
def feedback_record_count(ftype:str='*'):
    result = 0
    if ftype == '*':
        result = Feedback.objects.all().count()
    else:
        result = Feedback.objects.filter(feedback_type=ftype).count()
    return result
