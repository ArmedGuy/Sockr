"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
import urllib.request
from lxml import etree
from app.models import *

class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        ticket = request.GET.get("ticket")
        service = "http://%s/login" % request.get_host()
        if not ticket:
            return HttpResponseRedirect("https://weblogon.ltu.se/cas/login?service=%s" % service)
        else:
            res = urllib.request.urlopen("https://weblogon.ltu.se/cas/serviceValidate?ticket=%s&service=%s" % (ticket, service))
            tree = etree.parse(res)
            if tree.getroot()[0].tag.endswith("authenticationSuccess"):
                ideal = tree.getroot()[0][0].text
                user = authenticate(remote_user=ideal)
                if not user:
                    return HttpResponseRedirect("/?nope")
                login(request, user)
                return HttpResponseRedirect("/?")
            else:
                return HttpResponseRedirect("/?failed")


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("https://weblogon.ltu.se/cas/logout?service=http://%s" % request.get_host())

class CoursesView(TemplateView):
    template_name = "app/courses.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'groups': ProblemGroup.objects.all()
        })

class CourseView(TemplateView):
    template_name = "app/course.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'group': ProblemGroup.objects.get(id=kwargs['group'])
        })

class ProblemView(TemplateView):
    template_name = "app/problem.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'problem': Problem.objects.get(id=kwargs['problem'])
        })
        
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
