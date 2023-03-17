"""
Configures URLs for the Feedback app
"""

from django.urls import path

from feedback.views import index_view, form_view, \
                           login_view, logout_view, \
                           import_view, export_view, \
                           import_data_view, export_data_view

urlpatterns = [
    path('', index_view, name="feedback_default"),
    path('form', form_view, name='form'),
    path('import', import_view, name='import'),
    path('export', export_view, name='export'),
    path('export_data/<str:mode>', export_data_view, name='export_data'),
    path('import_data', import_data_view, name='import_data'),
    path('list/<int:current_page>', index_view, name="feedback-index"),
    path('list/', index_view, name="feedback-index"),
    path(
        'list_search/<str:search_term>/<int:current_page>',
        index_view,
        name="feedback-search-index"
    ),
    path(
        'list_query/<str:ftype>/<int:current_page>',
        index_view,
        name="feedback-query-index"
    ),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
]
