"""
Definition of views.
"""

import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect, Http404, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.db.models import Q
from django.db.models.aggregates import Count
import urllib.request
from lxml import etree
from app.models import *
import traceback

class LoginView(TemplateView):
    template_name = "app/login.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class LtuLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        casEndpoint = "https://weblogon.ltu.se/cas"
        ticket = request.GET.get("ticket")
        service = "http://%s/login/ltu" % request.get_host()
        if not ticket:
            return HttpResponseRedirect("%s/login?service=%s" % (casEndpoint, service))
        else:
            res = urllib.request.urlopen("%s/serviceValidate?ticket=%s&service=%s" % (casEndpoint, ticket, service))
            tree = etree.parse(res)
            if tree.getroot()[0].tag.endswith("authenticationSuccess"):
                username = tree.getroot()[0][0].text
                if "-" not in username:
                    username = "%s@ltu.se" % username
                else:
                    username = "%s@student.ltu.se" % username
                user = authenticate(remote_user=username)
                if not user:
                    return HttpResponseRedirect("/?nope")
                login(request, user)
                return HttpResponseRedirect("/?")
            else:
                return HttpResponseRedirect("/?failed")

class LuddLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        casEndpoint = "https://vortex.ludd.ltu.se/cas"
        ticket = request.GET.get("ticket")
        service = "http://%s/login/ludd" % request.get_host()
        if not ticket:
            return HttpResponseRedirect("%s/login?service=%s" % (casEndpoint, service))
        else:
            res = urllib.request.urlopen("%s/serviceValidate?ticket=%s&service=%s" % (casEndpoint, ticket, service))
            tree = etree.parse(res)
            if tree.getroot()[0].tag.endswith("authenticationSuccess"):
                username = tree.getroot()[0][0].text
                username = "%s@ludd.ltu.se" % username
                user = authenticate(remote_user=username)
                if not user:
                    return HttpResponseRedirect("/?nope")
                login(request, user)
                return HttpResponseRedirect("/?")
            else:
                return HttpResponseRedirect("/?failed")


class LogoutView(TemplateView):
    def post(self, request, *args, **kwargs):
        casEndpoint = "https://weblogon.ltu.se/cas"
        service = "ltu"
        if "ludd" in request.user.username:
            casEndpoint = "https://vortex.ludd.ltu.se/cas"
            service = "ludd"
        logout(request)
        return HttpResponseRedirect("%s/logout?service=http://%s/login/%s" % (casEndpoint, request.get_host(), service))

class QueueView(TemplateView):
    template_name = "app/queue.html"
    def get(self, request, *args, **kwargs):
        queue = Submission.objects.exclude(state__in=['failed', 'passed']).order_by('submitted_time')
        return render(request, self.template_name, {
            'queue': queue
        })

class CoursesView(TemplateView):
    template_name = "app/courses.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'groups': ProblemGroup.objects.all()
        })

class CourseView(TemplateView):
    template_name = "app/course.html"
    def get(self, request, *args, **kwargs):
        pg = ProblemGroup.objects.get(id=kwargs['group'])
        problems = Problem.objects.filter(group=pg).annotate(
                users=Count('submission__submitter', distinct=True),
                submissions=Count('submission'))
        tot_subs = 0
        tot_users = 0
        for p in problems:
            tot_subs += p.submissions
            tot_users += p.users
        return render(request, self.template_name, {
            'group': pg,
            'problems': problems,
            'stats': {
                'submissions': tot_subs,
                'users': tot_users
            }
        })

class ProblemView(TemplateView):
    template_name = "app/problem.html"
    def get(self, request, *args, **kwargs):
        problem = Problem.objects.get(id=kwargs['problem'])
        submissions = []
        num_subs = Submission.objects.filter(problem=problem).count()
        num_win_subs = Submission.objects.filter(problem=problem).filter(state='passed').count()
        if request.user.is_authenticated:
            submissions = Submission.objects.filter(submitter__id = request.user.id).filter(problem=problem).order_by('-submitted_time')
        return render(request, self.template_name, {
            'problem': Problem.objects.get(id=kwargs['problem']),
            'submissions': submissions,
            'stats': {
                'submissions': num_subs,
                'successful': num_win_subs,
            }
        })

class SubmitView(TemplateView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            problem = Problem.objects.get(id=kwargs['problem'])
            code = request.POST.get("content", "")
            
            s = Submission(problem = problem, submitter = request.user, state = 'submitted')
            s.test_code = code
            s.save()
            return redirect('submission', s.id)
        else:
            return redirect('/login')


class SubmissionView(TemplateView):
    template_name = "app/submission.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'submission': Submission.objects.get(id=kwargs['submission']),
        })

class ApiSubmissionView(TemplateView):
    def get(self, request, *args, **kwargs):
        key = request.GET.get("key", False)
        count = request.GET.get("count", 1)
        if not key:
            raise Http404()
        try:
            runner = Runner.objects.get(secret_key=key)
            r_subs = runner.submissions.filter(state='testing')
            submissions = []
            if len(r_subs):
                for s in r_subs:
                    if count == 0:
                        break
                    count -= 1
                    s.started_time = datetime.now()
                    s.save()
                    submissions.append(s.to_json())
            else:
                for s in Submission.objects.filter(problem__in=runner.problems.all(), state='submitted'):
                    if count == 0:
                        break
                    count -= 1
                    s.state = 'testing'
                    s.runner = runner
                    s.started_time = datetime.now()
                    s.save()
                    submissions.append(s.to_json())
            return JsonResponse(submissions, safe = False)
        except:
            traceback.print_exc()
            raise Http404()
        

class ApiSubmissionReportView(TemplateView):
    def post(self, request, *args, **kwargs):
        key = request.GET.get("key", False)
        if not key:
            raise Http404()
        try:
            runner = Runner.objects.get(secret_key=key)
            submission = Submission.objects.get(pk=kwargs['submission'], runner=runner)
            json_data = json.loads(request.body.decode('utf-8'))
            json_data['finished_time'] = datetime.now()
            if "thrown_error" in json_data:
                try:
                    err = Error.objects.get(Q(key=json_data['thrown_error']), Q(language=submission.problem.group.language) | Q(submission.problem))
                    json_data['thrown_error'] = err.id
                except:
                    err = None
                    if(json_data['thrown_error_type'] == "runtime" or json_data['thrown_error_type'] == "compile"):
                        err = Error(language=submission.problem.group.language, key=json_data['thrown_error'], type=json_data['thrown_error_type'])
                        err.description = json_data.get("thrown_error_desc", "The program failed to execute")
                        err.read_more_link = "https://google.com/search?q={}+{}".format(submission.problem.group.language, json_data['thrown_error'])                        
                    if(json_data['thrown_error_type'] == "program"):
                        err = Error(problem=submission.problem, key=json_data['thrown_error'], type=json_data['thrown_error_type'])
                        err.description = json_data.get("thrown_error_desc", "The program produced an incorrect value")
                        err.read_more_link = "/problem/{}".format(submission.problem.id)
                    err.save()
                    json_data['thrown_error'] = err.id
            if "thrown_error_type" in json_data:
                del json_data['thrown_error_type']
            if "thrown_error_desc" in json_data:
                del json_data['thrown_error_desc']
            Submission.objects.filter(pk=submission.id, runner=runner).update(**json_data)
            return "", 200
        except:
            traceback.print_exc()
            raise Http404()

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
