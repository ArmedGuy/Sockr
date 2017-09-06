from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from app.models import *

class LanguageAdmin(ModelAdmin):
    pass

admin.site.register(ProgrammingLanguage, LanguageAdmin)
admin.site.register(ProblemGroup)


class ProblemAdmin(ModelAdmin):
    list_display = ('list_name',)
    def list_name(self, obj):
        return "%s (%s)" % (obj.name, obj.group.name)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Error)
admin.site.register(Submission)
class RunnerAdmin(ModelAdmin):
    filter_horizontal = ('problems',)

admin.site.register(Runner, RunnerAdmin)
