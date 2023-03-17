"""
View code for the Feedback app.
Contains the main route to accept data, TODO.
"""

from json import loads
from json.decoder import JSONDecodeError
from time import mktime
from datetime import datetime
from dateutil import parser as dt_parser
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from feedback.models import Feedback
from feedback.util import to_dict

DEFAULT_ROUTE = 'status'

def login_view(request):
    """
    Either returns the login page or processes
    the login request to log users in.
    """
    # Set a default route to redirect if logged in
    result = redirect(DEFAULT_ROUTE)
    # Render a login form, handle the login request,
    # or show an error
    if not request.user.is_authenticated:
        if request.method =='GET':
            result = render(request, 'login.html')
        elif request.method =='POST':
            user = authenticate(
                username=request.POST.get('login', ''),
                password=request.POST.get('password', '')
            )
            if user is not None:
                login(request, user)
        else:
            result = HttpResponseBadRequest()
    return result

def logout_view(request):
    """
    Log users out and redirects them to the default route.
    """
    logout(request)
    return redirect(DEFAULT_ROUTE)

def index_view(request, current_page=1, search_term='*', feedback_type='*'):
    """
    Provides a feedback list page with pagination.
    """
    if search_term != '*':
        feedback_items = Feedback.search_by_term(search_term)
    elif feedback_type != '*':
        feedback_items = Feedback.search_by_feedback_type(feedback_type)
    else:
        feedback_items = Feedback.get_search_index()
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
    """
    Handles the feedback-recording logic.
    """
    result = (
        "This page only handles "
        "the input form from the documentation."
    )
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)
        feedback_inst = Feedback(
            feedback_type=body.get('kind'),
            message=body.get('feedback'),
            email=body.get('contact'),
            url=body.get('location')['href']
        )
        feedback_inst.save()
        result = 'Ok'
    return HttpResponse(result)

def import_view(request):
    """
    Either returns the import page or processes
    the imported file.
    """
    # Set a default route to redirect if logged in
    result = redirect(DEFAULT_ROUTE)
    # If user is able to import or export data, perform the action
    if request.user.is_authenticated and request.user.is_staff:
        if request.method =='POST':
            print('Data import')
        elif request.method =='GET':
            result = render(request, 'data_import.html')
        else:
            result = HttpResponseBadRequest()
    return result

def import_data_view(request):
    """
    Handles the data import logic.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied('Error! You are not authenticated!')
    import_data = get_import_file(request)
    if import_data:
        if 'importUsers' in request.POST:
            if 'users' in import_data:
                for user_data in import_data['users']:
                    apply_user_model(user_data)
        if 'importRecords' in request.POST:
            if 'feedback' in import_data:
                for feedback_record in import_data['feedback']:
                    apply_feedback_model(feedback_record)
    return redirect('import')

def export_view(request):
    """
    Either returns the export page or processes
    the imported file.
    """
    # ?
    result = redirect('status')
    if request.user.is_authenticated:
        if request.method =='GET':
            cur_ts = mktime(datetime.now().timetuple())
            utc_ts = datetime.utcfromtimestamp(cur_ts)
            str_ts = utc_ts.strftime("%Y_%m_%d_%H_%M_%S")
            result = render(request, 'data_export.html', {"datetime": str_ts})
        else:
            result = HttpResponseBadRequest()
    return result

def serialize_model_contents(in_mod):
    """
    A generator that serializes all the items of a provided model.
    """
    for inst in in_mod:
        yield to_dict(inst)

def export_data_view(request, mode: str):
    """
    Returns the exported data.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied('You need to authenticate')
    output = {}
    if mode in ['r', 'ur']:
        output['feedback'] = list(serialize_model_contents(Feedback.objects.all()))
    if mode in ['u', 'ur']:
        output['users'] = list(serialize_model_contents(get_user_model().objects.all()))
    response = JsonResponse(
        output,
        json_dumps_params={
            'indent': 4,
            'ensure_ascii': False
        }
    )
    response['Content-Disposition'] = 'inline;'
    return response

def get_import_file(request):
    """
    Returns the parsed data to import or None.
    """
    result = None
    if 'import_data' in request.FILES:
        try:
            result = loads(request.FILES['import_data'].read())
        except JSONDecodeError:
            pass
    return result

def update_model(updated_model, data_src: dict, applicable_keys: list):
    """
    Updates one model with data_src dict
    """
    for mkey, mval in data_src.items():
        if mkey in applicable_keys:
            # Use setattr on normal values and .set on lists
            if getattr(updated_model, mkey).__class__.__name__ == 'ManyRelatedManager':
                getattr(updated_model, mkey).set(mval)
            else:
                setattr(updated_model, mkey, mval)
    updated_model.save()

def apply_feedback_model(feedback: dict):
    """
    Changes the database depending on the content of the feedback record.
    """
    fid = feedback.get('id')
    applicable = [
        'message', 'email', 'url', 'feedback_type'
        'created_at', 'updated_at'
    ]
    in_upd_datetime = dt_parser.parse(feedback.get('updated_at'))
    in_crt_datetime = dt_parser.parse(feedback.get('created_at'))
    current_model_lookup = Feedback.objects.filter(id=fid)
    if current_model_lookup:
        current_model = current_model_lookup.first()
        # If the input model was created after the current one, a new record is made.
        # If both are created at the same time, but the input was updated after,
        # update the local contents.
        if current_model.created_at < in_crt_datetime:
            new_feedback = Feedback(**{key: feedback[key] for key in applicable})
            new_feedback.save()
        elif current_model.created_at == in_crt_datetime and \
             current_model.updated_at < in_upd_datetime:
            update_model(current_model, feedback, applicable)
    else:
        # Create the feedback record if unavailable
        new_feedback = Feedback(**{key: feedback[key] for key in applicable})
        new_feedback.save()

def apply_user_model(user: dict):
    """
    Changes the database depending on the content of the user record.
    """
    uid = user.get('id')
    user_model_lookup = get_user_model().objects.filter(id=uid)
    join_datetime = dt_parser.parse(user.get('date_joined'))
    applicable = [
        "password", "last_login", "is_superuser", "username", "first_name", "last_name",
        "email", "is_staff", "is_active", "date_joined", "groups", "user_permissions"
    ]
    if user_model_lookup:
        user_model = user_model_lookup.first()
        # Update the user if found
        if user_model.id == uid and user_model.date_joined == join_datetime:
            # Update model data with "user" dictionary
            update_model(user_model, user, applicable)
    else:
        # Create user if doesn't exist
        new_user = get_user_model()(**{key: user[key] for key in applicable})
        new_user.save()
