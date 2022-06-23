from datetime import date
import datetime

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from app.forms import LoginForm, PasswordChangeForm
from app.models import Project, Engineer, WorkType, WorkReport


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
            a.append(report.date)
            a.append(report.project.name)
            a.append(report.engineer.full_name)
            a.append(report.work_type.name)
            a.append(report.period)
            a.append(report.text)
            arr.append(a)

        return render(request, 'main.html', {"user": user.username, 'projects': projects, 'engineers': engineers, 'work_types': work_types,  'arr': arr})

    def post(self, request):
        user = request.user
        print(request.POST.get("date"))
        project = Project.objects.filter(name=request.POST.get("project"))[0]
        engineer = Engineer.objects.filter(full_name=request.POST.get("engineer"))[0]
        work_type = WorkType.objects.filter(name=request.POST.get("work_type"))[0]
        work_report = WorkReport(manager=user, date=request.POST.get("date"), project=project, engineer=engineer, work_type=work_type, period=request.POST.get("period"), text=request.POST.get("text"))
        work_report.save()
        return redirect('/main')
        # projects = list(map(lambda x: x.name, Project.objects.all()))
        # engineers = list(map(lambda x: x.full_name, Engineer.objects.all()))
        # work_types = list(map(lambda x: x.name, WorkType.objects.all()))
        # arr = []
        # work_reports = WorkReport.objects.filter(manager=user)
        # for report in work_reports:
        #     a = []
        #     a.append(report.date)
        #     a.append(report.project.name)
        #     a.append(report.engineer.full_name)
        #     a.append(report.work_type.name)
        #     a.append(report.period)
        #     a.append(report.text)
        #     arr.append(a)
        # return render(request, 'main.html', {"user": user, 'projects': projects, 'engineers': engineers, 'work_types': work_types, 'arr': arr})


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
        return render(request, 'admin.html', {'user': user.username})


class TimeControl(View):

    def get(self, request):
        user = request.user
        arr = []
        sum = 0
        dateC = date.today()
        date2 = dateC + datetime.timedelta(days=1)
        projects = []
        for i in WorkReport.objects.filter(manager=user, date__range=(dateC, date2)):
            projects.append(i.project)

        for project in list(set(projects)):
            a = []
            a.append(project.name)
            company_sum = WorkReport.objects.filter(manager=user, date__range=(dateC, date2), project=project).aggregate(Sum('period')).get('period__sum')
            sum += company_sum
            a.append(company_sum)
            arr.append(a)
        a = ['', sum]
        arr.append(a)
        return render(request, 'timecontrol.html', {'user': user.username, 'arr': arr})