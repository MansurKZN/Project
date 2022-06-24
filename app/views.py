import os
from datetime import date
import datetime
import pandas as pd
import requests

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from app.forms import LoginForm, PasswordChangeForm
from app.models import Project, Engineer, WorkType, WorkReport, Manager
from project import settings


class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('admin')
        else:
            return reverse_lazy('main')

def logout_user(request):
    logout(request)
    return redirect('login')


class MainPage(View):

    def get(self, request):
        user = request.user
        projects = list(map(lambda x: x.name, Project.objects.all()))
        engineers = list(map(lambda x: x.full_name, Engineer.objects.all()))
        work_types = list(map(lambda x: x.name, WorkType.objects.all()))
        arr = []
        work_reports = WorkReport.objects.filter(manager=user)
        for report in work_reports:
            a = []
            a.append(report.id)
            a.append(report.date.__format__("%Y-%m-%d %H:%M"))
            a.append(report.project.name)
            a.append(report.engineer.full_name)
            a.append(report.work_type.name)
            a.append(report.period)
            a.append(report.text)
            arr.append(a)
        date = datetime.datetime.now().__format__("%Y-%m-%dT%H:%M")

        paginator = Paginator(arr, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'main.html', {"user": user.username, 'projects': projects, 'engineers': engineers, 'work_types': work_types, 'date': date, 'arr': arr, 'page_obj': page_obj})

    def post(self, request):
        if request.POST.get("update_id"):

            work_report = WorkReport.objects.get(id=request.POST.get("update_id"))
            work_report.date = request.POST.get("update_date")
            work_report.project = Project.objects.filter(name=request.POST.get("update_project"))[0]
            work_report.engineer = Engineer.objects.filter(full_name=request.POST.get("update_engineer"))[0]
            work_report.work_type = WorkType.objects.filter(name=request.POST.get("update_work_type"))[0]
            work_report.period = request.POST.get("update_period")
            work_report.text = request.POST.get("update_text")
            work_report.save()
        else:
            user = request.user
            project = Project.objects.filter(name=request.POST.get("project"))[0]
            engineer = Engineer.objects.filter(full_name=request.POST.get("engineer"))[0]
            work_type = WorkType.objects.filter(name=request.POST.get("work_type"))[0]
            work_report = WorkReport(manager=user, date=request.POST.get("date"), project=project, engineer=engineer, work_type=work_type, period=request.POST.get("period"), text=request.POST.get("text"))
            work_report.save()
        return redirect('/main')


class Profie(View):

    def get(self, request):
        user = request.user
        form = PasswordChangeForm()
        return render(request, 'profile.html', {"user": user, 'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        user = request.user
        message = ''
        error = ''
        if user.check_password(form.data.get('password_old')):
            if form.data.get('password_new') == form.data.get('password_retype'):
                user.set_password(form.data.get('password_new'))
                user.save()
                message = 'Password changed successfully'
            else:
                error = 'New password and retype password not equal'
                form.add_error(None, 'Password change error')
        else:
            error = 'Old password is incorrect'
            form.add_error(None, 'Password change error')
        return render(request, 'profile.html', {"user": user, 'form': form, 'message': message, 'error': error})


class AdminInfo(View):

    def get(self, request):
        user = request.user
        arr = []
        date_start = date(date.today().year, date.today().month, 1)
        date_end = date(date.today().year, date.today().month + 1, 1)
        projects = Project.objects.all()
        columns = []
        columns.append("Manager")
        columns.append("Work Time")
        for project in projects:
            columns.append(project.name)

        for manager in Manager.objects.filter(is_superuser=False):
            a = []
            work_time = manager.work_time
            a.append(f'{manager.first_name} {manager.last_name}')
            a.append(work_time)
            person_sum = 0
            for project in projects:
                time_for_project = WorkReport.objects.filter(manager=manager, date__range=(date_start, date_end), project=project).aggregate(Sum('period')).get('period__sum')
                if time_for_project:
                    percent_project_work = round(((int(time_for_project) / 60) * 100 / work_time) / 100, 3)
                else:
                    percent_project_work = 0
                person_sum += percent_project_work
                a.append(percent_project_work)
            a.append(person_sum)
            arr.append(a)
        return render(request, 'admin.html', {'user': user.username, 'columns': columns, 'arr': arr})

    def post(self, request):
        arr = []
        date_start = date(date.today().year, date.today().month, 1)
        date_end = date(date.today().year, date.today().month + 1, 1)
        projects = Project.objects.all()
        columns = []
        columns.append("Manager")
        columns.append("Work Time")
        for project in projects:
            columns.append(project.name)
        arr.append(columns)
        for manager in Manager.objects.filter(is_superuser=False):
            a = []
            work_time = manager.work_time
            a.append(f'{manager.first_name} {manager.last_name}')
            a.append(work_time)
            person_sum = 0
            for project in projects:
                time_for_project = WorkReport.objects.filter(manager=manager, date__range=(date_start, date_end),
                                                             project=project).aggregate(Sum('period')).get(
                    'period__sum')
                if time_for_project:
                    percent_project_work = round(((int(time_for_project) / 60) * 100 / work_time) / 100, 3)
                else:
                    percent_project_work = 0
                person_sum += percent_project_work
                a.append(percent_project_work)
            a.append(person_sum)
            arr.append(a)


        df = pd.DataFrame(arr)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace=True)
        file_name = f'Work_time_{date_start}_{date_end}.xlsx'
        df.to_excel(excel_writer=f'{settings.BASE_DIR}/static/{file_name}', index=False)

        # host_port = request.META['HTTP_HOST']
        # requests.get(f'http://{host_port}/static/{file_name}')

        # redirect(f'/static/{file_name}')
        #
        # for item in os.listdir(f"{settings.BASE_DIR}/static/"):
        #     if item.endswith(".xlsx"):
        #         os.remove(item)

        return redirect(f'/static/{file_name}')

class TimeControl(View):

    def get(self, request):
        user = request.user
        arr = []
        sum = 0
        date_start = date.today()
        date_end = date_start + datetime.timedelta(days=1)
        projects = []
        for i in WorkReport.objects.filter(manager=user, date__range=(date_start, date_end)):
            projects.append(i.project)

        for project in list(set(projects)):
            a = []
            a.append(project.name)
            company_sum = WorkReport.objects.filter(manager=user, date__range=(date_start, date_end), project=project).aggregate(Sum('period')).get('period__sum')
            sum += company_sum
            a.append(company_sum)
            arr.append(a)
        a = ['', sum]
        arr.append(a)
        return render(request, 'timecontrol.html', {'user': user, 'arr': arr})

    def post(self, request):
        user = request.user
        arr = []
        sum = 0
        date_start = datetime.date.fromisoformat(request.POST.get("date"))
        date_end = date_start + datetime.timedelta(days=1)
        projects = []
        for i in WorkReport.objects.filter(manager=user, date__range=(date_start, date_end)):
            projects.append(i.project)
        for project in list(set(projects)):
            a = []
            a.append(project.name)
            company_sum = WorkReport.objects.filter(manager=user, date__range=(date_start, date_end),
                                                    project=project).aggregate(Sum('period')).get('period__sum')
            sum += company_sum
            a.append(company_sum)
            arr.append(a)
        a = ['', sum]
        arr.append(a)
        return render(request, 'timecontrol.html', {'user': user, 'arr': arr})