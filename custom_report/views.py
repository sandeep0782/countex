from django.shortcuts import render,redirect
from .models import Report, SAMPLING
from track.views import get_group
from track.models import Buyer
from django.contrib.auth.decorators import login_required
from .services import report_dict
from track.decorators import *
from django.contrib.auth.models import User


@login_required
@allowed_users(allowed_roles=['admin', 'RM'])
def custom_report(request):
    error = get_group(request.user.id)
    report_choice = request.GET.get("report", "0")
    report = Report.objects.filter(report_type=report_choice)
    if report_choice == "0":
        report = Report.objects.all()
    return render(request, 'custom_report.html', {'report_choice':SAMPLING, 'report':report, 'selected_choice':report_choice, 'error':error})

@login_required
@allowed_users(allowed_roles=['admin', 'RM'])
def single_report(request,pid):
    error = get_group(request.user.id)
    # owner= request.GET.get("owner", request.user.username)
    alluser = Buyer.objects.all()
    report = Report.objects.get(id=pid)
    sub_dict = report_dict.get(report.report_name)
    template_name = sub_dict.get("template_name")
    obj = sub_dict.get("method")(request)
    # subuser = get_single_report_user(request.user)
    return render(request, template_name, {"obj":obj, 'report_status':SAMPLING, 'alluser':alluser,'error':error})

