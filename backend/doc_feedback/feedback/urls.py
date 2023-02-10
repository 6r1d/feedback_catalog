"""
Configures URLs for the Feedback app
"""

from django.urls import path

from feedback.views import index_view, form_view, login_view, logout_view

urlpatterns = [
    path('', index_view, name="feedback_default"),
    path('form', form_view, name='form'),
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
