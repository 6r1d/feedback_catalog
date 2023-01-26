from django.conf import settings
from django.urls import resolve

def app_title(request):
    """
    Returns:
        (str): a title for the current application
    """
    return {'APP_TITLE': settings.APP_TITLE}

def url_name(request):
    """
    Returns
        (str): the Django name for current URL
    """
    return {'URL_NAME': resolve(request.path_info).url_name}