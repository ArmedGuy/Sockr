from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from app.models import *

class LanguageErrorInline(TabularInline):
    model = Error
    fields = ('language', 'type', 'key', 'description', 'read_more_link')

class LanguageAdmin(ModelAdmin):
    inlines = (LanguageErrorInline,)

admin.site.register(ProgrammingLanguage, LanguageAdmin)
admin.site.register(ProblemGroup)

class ProblemErrorInline(TabularInline):
    model = Error
    fields = ('problem', 'type', 'key', 'description', 'read_more_link')

class ProblemAdmin(ModelAdmin):
    inlines = (ProblemErrorInline,)
    list_display = ('list_name',)
    def list_name(self, obj):
        return "%s (%s)" % (obj.name, obj.group.name)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Error)
admin.site.register(Submission)