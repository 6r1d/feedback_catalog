from json import loads
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth import logout

from .models import Feedback

def login_view(request):
    """
    Either returns the login page or processes
    the login request to log users in.
    """
    result = redirect('status')
    if not request.user.is_authenticated:
        if request.method =='POST':
            user = authenticate(
                username=request.POST.get('login', ''),
                password=request.POST.get('password', '')
            )
            if user is not None:
                login(request, user)
        elif request.method =='GET':
            result = render(request, 'login.html')
        else:
            result = HttpResponseBadRequest()
    return result

def logout_view(request):
    """
    Log users out and redirects one to the status window.
    """
    logout(request)
    return redirect('status')

def index_view(request, current_page=1, search_term='*', ftype='*'):
    if search_term != '*':
        feedback_items = Feedback.objects.filter(message__contains=search_term).order_by('id')
    elif ftype != '*':
        feedback_items = Feedback.objects.filter(feedback_type=ftype).order_by('id')
    else:
        feedback_items = Feedback.objects.get_queryset().order_by('id')
    feedback_paginator = Paginator(feedback_items, 5)
    page = feedback_paginator.page(current_page)
    return render(
        request,
        'feedback_idx.html',
        {
            'search_term': search_term,
            'feedbacks': page.object_list,
            'current_page': current_page,
            'paginator_obj': feedback_paginator,
            'page_obj': page
        }
    )

@csrf_exempt
def form_view(request):
    result = (
        "Please send a POST request "
        "with your documentation suggestion."
    )
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        feedback_inst = Feedback(
            feedback_type=body.get('feedbackType'),
            message=body.get('message'),
            email=body.get('email'),
            url=body.get('url')
        )
        feedback_inst.save()
        result = 'Ok'
    return HttpResponse(result)
