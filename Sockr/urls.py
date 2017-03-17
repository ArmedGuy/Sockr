"""
Definition of urls for Sockr.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        app.views.LoginView.as_view(),
        name='login'),
    url(r'^logout$',
        app.views.LogoutView.as_view(),
        name='logout'),
    url(r'^courses/$',
        app.views.CoursesView.as_view(),
        name='courses'),
    url(r'^course/(?P<group>[0-9]+)/$',
        app.views.CourseView.as_view(),
        name='course'),
    url(r'^problem/(?P<problem>[0-9]+)/$',
        app.views.ProblemView.as_view(),
        name='problem'),
    url(r'^problem/(?P<problem>[0-9]+)/submit/$',
        app.views.SubmitView.as_view(),
        name='submit'),
    url(r'^submission/(?P<submission>[0-9]+)/$',
        app.views.SubmissionView.as_view(),
        name='submission'),

    url(r'^api/submissions/$',
        app.views.ApiSubmissionView.as_view(),
        name='api_submissions'),
    url(r'^api/submission/(?P<submission>[0-9]+)/report/$',
        app.views.ApiSubmissionReportView.as_view(),
        name='api_submission_report'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
