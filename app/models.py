"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=64, help_text='The common name for the programming language (can be including version')
    docs = models.CharField(max_length=256, help_text='A link to the documentation for the language')
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
    language = models.ForeignKey(ProgrammingLanguage, null=True)
    problem = models.ForeignKey(Problem, null=True)
    type = models.CharField(max_length=32, choices=ERROR_TYPES, help_text='Which step in the process the error can occur')
    key = models.CharField(max_length=64, help_text='An unique-ish key that the test server reports this problem as.')
    description = models.TextField(help_text='Describe what the problem is and how you can solve it')
    read_more_link = models.CharField(max_length=256, help_text='A link to read more about the error')
    

SUBMISSION_STATES = (
    ('submitted', 'Submitted'),
    ('testing', 'Currently being tested'),
    ('success', 'Test attempt passed'),
    ('fail', 'Test attempt not passed')
)
class Submission(models.Model):
    problem = models.ForeignKey(Problem)
    submitter = models.ForeignKey(User)
    state = models.CharField(max_length=32, choices=SUBMISSION_STATES)
    state_data = models.TextField()
    test_code = models.TextField()

    def __str__(self):
        return "%s - %s (%s)" % (self.problem.name, self.problem.group.name, self.submitter.username)