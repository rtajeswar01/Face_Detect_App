from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password  
from .models import lecturer

def lec_login(request):
    if request.method == "POST":
        lec_number = request.POST['lecturerNumber']
        lec_password = request.POST['lecturerPassword']

        try:
            Lecturer = lecturer.objects.get(lecturerNumber=lec_number)
            if check_password(lec_password, Lecturer.lecturerPassword):  
                request.session['lecturerID'] = Lecturer.lecturerID 
                return redirect('lec_dashboard') 
            else:
                messages.error(request, 'Invalid password')
        except lecturer.DoesNotExist:
            messages.error(request, 'Lecturer not found')

    return render(request, 'lec_login.html')

def lec_login_required(function):
    def wraper(request, *args, **kwargs):
        if 'lecturerID' not in request.session.keys():
            return HttpResponseRedirect("/lec_login")
        else:
            return function(request, *args, **kwargs)

    wraper.__doc__=function.__doc__
    wraper.__name__=function.__name__
    return wraper

from datetime import datetime
from schedules.models import Schedule
from django.utils.timezone import make_aware


@lec_login_required
def lec_dashboard(request):
    current_time = make_aware(datetime.now())
    lecturer_id = request.session.get("lecturerID")
    current_lecturer = lecturer.objects.get(lecturerID=lecturer_id)

    active_classes = Schedule.objects.filter(
        lecturer_id=lecturer_id,
        startDateTime__lte=current_time,
        endDateTime__gte=current_time,
    ).first()

    context = {
        "schedule": active_classes,
        "lecturer_name": current_lecturer.lecturerName, 
    }
    return render(request, "lec_dashboard.html", context)


def lec_logout_view(request):
    logout(request)
    return render(request, 'lec_logout_view.html')
