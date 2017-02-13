"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=64, help_text='The common name for the programming language (can be including version')
    docs = models.CharField(max_length=256, help_text='A link to the documentation for the language')
    ace_name = models.CharField(max_length=256, help_text='The name used in the ACE editor to provide syntax highlighting', default = 'python')
    download_link = models.CharField(max_length=256, help_text='A link to download tools for the language.')

    def __str__(self):
        return self.name

class ProblemGroup(models.Model):
    name = models.CharField(max_length=64, help_text='Name of course or generic problem group')
    language = models.ForeignKey(ProgrammingLanguage, help_text='The Programming Language being used for this test group')
    
    def __str__(self):
        return self.name

class Problem(models.Model):
    name = models.CharField(max_length=256, help_text='Name for the Problem/Lab')
    description = models.TextField(help_text='Supports Markdown/HTML')
    show_output = models.BooleanField(default = True, help_text='Decides if test output should be show in a submission.')
    group = models.ForeignKey(ProblemGroup, related_name="problems", verbose_name="Course/Problem Group")
    test_key = models.CharField("Test suite name", max_length=64, help_text='The name of the test on the test server that this problem will use')

    def __str__(self):
        return self.name

ERROR_TYPES = (
    ('compile', 'Compile-time error'),
    ('runtime', 'Runtime exception'),
    ('program', 'Wrong result')
)
class Error(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, null=True, blank = True)
    problem = models.ForeignKey(Problem, null=True, blank = True)
    type = models.CharField(max_length=32, choices=ERROR_TYPES, help_text='Which step in the process the error can occur')
    key = models.CharField(max_length=64, help_text='An unique-ish key that the test server reports this problem as.')
    description = models.TextField(help_text='Describe what the problem is and how you can solve it')
    read_more_link = models.CharField(max_length=256, help_text='A link to read more about the error')
    
    def __str__(self):
        return "%s %s" % (self.get_type_display(), self.key)
    
    def __unicode__(self):
        return self.__str__()
    

SUBMISSION_STATES = (
    ('submitted', 'Submitted'),
    ('testing', 'Testing'),
    ('passed', 'Accepted'),
    ('failed', 'Failed')
)
class Submission(models.Model):
    problem = models.ForeignKey(Problem)
    submitter = models.ForeignKey(User)
    submitted_time = models.DateTimeField(auto_now_add=True)
    started_time = models.DateTimeField(blank = True, null = True)
    finished_time = models.DateTimeField(blank = True, null = True)
    state = models.CharField(max_length=32, choices=SUBMISSION_STATES)
    test_code = models.TextField()
    output_log = models.TextField(blank = True)
    thrown_error = models.ForeignKey(Error, null = True, default = None)
    thrown_error_raw = models.TextField(blank = True)
    thrown_error_line = models.IntegerField(blank = True, default = 0)

    def __str__(self):
        return "#%d: %s - %s (%s)" % (self.id, self.problem.name, self.problem.group.name, self.submitter.username)

    def get_html_state(self):
        html = ""
        if  self.state == 'submitted':
            html = "<span class='text-info'><b>Submitted</b></span>"
        elif self.state == 'testing':
            html = "<span class='text-primary'><b>Testing</b></span>"
        elif self.state == 'passed':
            html = "<span class='text-success'><b>Accepted</b></span>"
        elif self.state == 'failed':
            html = "<span class='text-danger'><b>Failed</b></span>"
        return mark_safe(html)