from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin

from app.forms import UserCreationForm
from app.models import Manager, Project, WorkType, Engineer, WorkReport


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ('first_name', 'last_name', 'work_time', 'work_position')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'work_time', 'work_position')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'work_time', 'work_position')}
         ),
    )
    filter_horizontal = ()

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

@admin.register(WorkReport)
class WorkReportAdmin(admin.ModelAdmin):
    list_display = ('manager', 'date', 'get_project_name', 'get_engineer_name', 'get_work_type_name', 'period', 'text')
    list_filter = ('date', 'manager', 'project', 'engineer', 'work_type', 'period')

    @display(ordering='project__name', description='Name')
    def get_project_name(self, obj):
        return obj.project.name

    @display(ordering='engineer__full_name', description='Name')
    def get_engineer_name(self, obj):
        return obj.engineer.full_name

    @display(ordering='work_type__name', description='Name')
    def get_work_type_name(self, obj):
        return obj.work_type.name
