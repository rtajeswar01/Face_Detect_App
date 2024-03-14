from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password  
from .models import appAdmin
from lecturer.models import lecturer
from modules.models import Module
from student.models import Student
from schedules.models import Schedule
import json
from django.core.serializers.json import DjangoJSONEncoder


def main(request):
    return render(request, 'main.html')

def login(request):
    if request.method == "POST":
        admin_number = request.POST['adminNumber']
        admin_password = request.POST['adminPassword']

        try:
            admin = appAdmin.objects.get(adminNumber=admin_number)
            if check_password(admin_password, admin.adminPassword):  
                request.session['adminID'] = admin.adminID
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password')
        except appAdmin.DoesNotExist:
            messages.error(request, 'Admin not found')

    return render(request, 'login.html')

def my_login_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('adminID'):
            return HttpResponseRedirect("/login")
        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

@my_login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def lec_register(request):
    if request.method == "POST":
        lecturer_number = request.POST['lecturerNumber']
        lecturer_name = request.POST['lecturerName']
        lecturer_email = request.POST['lecturerEmail']
        lecturer_password = request.POST['lecturerPassword']

        if lecturer.objects.filter(lecturerNumber=lecturer_number).exists():
            messages.error(request, 'Lecturer with this number already exists.')
        elif lecturer.objects.filter(lecturerEmail=lecturer_email).exists():
            messages.error(request, 'Lecturer with this email already exists.')
        else:
            Lecturer = lecturer(
                lecturerNumber=lecturer_number,
                lecturerName=lecturer_name,
                lecturerEmail=lecturer_email,
                lecturerPassword=make_password(lecturer_password),
            )
            Lecturer.save()
            messages.success(request, 'Lecturer registered successfully.')

            return redirect('dashboard')

    return render(request, 'lec_register.html')

@my_login_required
def update_lecturer(request, lecturer_id):
    lecturer_instance = get_object_or_404(lecturer, lecturerID=lecturer_id)

    if request.method == "POST":
        lecturer_instance.lecturerNumber = request.POST.get('lecturerNumber', lecturer_instance.lecturerNumber)
        lecturer_instance.lecturerName = request.POST.get('lecturerName', lecturer_instance.lecturerName)
        lecturer_instance.lecturerEmail = request.POST.get('lecturerEmail', lecturer_instance.lecturerEmail)

        new_password = request.POST.get('lecturerPassword')
        if new_password:
            lecturer_instance.lecturerPassword = make_password(new_password)

        lecturer_instance.save()
        messages.success(request, 'Lecturer updated successfully.')
        return redirect('lecturer_list')

    return render(request, 'update_lecturer.html', {'lecturer_instance': lecturer_instance})

@my_login_required
def delete_lecturer(request, lecturer_id):
    lecturer_instance = get_object_or_404(lecturer, lecturerID=lecturer_id)
    
    if request.method == "POST":
        lecturer_instance.delete()
        messages.success(request, 'Lecturer deleted successfully.')
        return redirect('lecturer_list')

    return render(request, 'delete_lecturer.html', {'lecturer_instance': lecturer_instance})

@my_login_required
def lecturer_list(request):
    lecturers = lecturer.objects.all()
    return render(request, 'lecturer_list.html', {'lecturers': lecturers})

@my_login_required
def module_register(request):
    if request.method == "POST":
        module_name = request.POST['moduleName']
        module_code = request.POST['moduleCode']
        lecturer_id = request.POST['lecturerID']

        if Module.objects.filter(moduleCode=module_code).exists():
            messages.error(request, 'Module with this code already exists.')
        else:
            try:
                lecturer_instance = lecturer.objects.get(lecturerID=lecturer_id)
                module = Module(
                    moduleName=module_name,
                    moduleCode=module_code,
                    lecturer=lecturer_instance,
                )
                module.save()
                messages.success(request, 'Module registered successfully.')
                return redirect('module_list')
            except lecturer.DoesNotExist:
                messages.error(request, 'Lecturer not found.')

    lecturers = lecturer.objects.all()
    
    return render(request, 'module_register.html', {'lecturers': lecturers})

@my_login_required
def update_module(request, module_id):
    module = get_object_or_404(Module, moduleID=module_id)
    
    if request.method == "POST":
        module.moduleName = request.POST.get('moduleName', module.moduleName)
        module.moduleCode = request.POST.get('moduleCode', module.moduleCode)

        lecturer_id = request.POST.get('lecturer')
        module.lecturer = lecturer.objects.get(lecturerID=lecturer_id)

        module.save()  
        return redirect('module_list')

    lecturers = lecturer.objects.all() 
    return render(request, 'update_module.html', {'module': module, 'lecturers': lecturers})

@my_login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, moduleID=module_id)

    if request.method == "POST":
        module.delete()
        return redirect('module_list')

    return render(request, 'delete_module.html', {'module': module})

@my_login_required
def module_list(request):
    modules = Module.objects.all()
    return render(request, 'module_list.html', {'modules': modules})

def student_register(request):
    if request.method == "POST":
        student_name = request.POST["studentName"]
        student_number = request.POST["studentNumber"]
        student_email = request.POST["studentEmail"]
        student_face = request.FILES.get("studentFace")
        selected_modules = request.POST.getlist("modules")

        if Student.objects.filter(studentNumber=student_number).exists():
            messages.error(request, "Student with this number already exists.")
        elif Student.objects.filter(studentEmail=student_email).exists():
            messages.error(request, "Student with this email already exists.")
        else:
            if student_face:
                image_extension = student_face.name.split(".")[-1]
                student_face.name = f"{student_name}.{image_extension}"

            student = Student(
                studentName=student_name,
                studentNumber=student_number,
                studentEmail=student_email,
                studentFace=student_face,
            )
            student.save()

            student.modules.set(selected_modules)

            messages.success(request, "Student registered successfully.")
            return redirect("student_list")

    modules = Module.objects.all()
    return render(request, "student_register.html", {"modules": modules})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


def update_student(request, student_id):
    student = get_object_or_404(
        Student, pk=student_id
    )  
    if request.method == "POST":
        student.studentName = request.POST.get("studentName", student.studentName)
        student.studentNumber = request.POST.get("studentNumber", student.studentNumber)
        student.studentEmail = request.POST.get("studentEmail", student.studentEmail)

        new_face = request.FILES.get("studentFace")
        if new_face:
            image_extension = new_face.name.split(".")[-1]
            new_face.name = f"{student.studentName}.{image_extension}"
            student.studentFace = new_face

        existing_modules_ids = set(student.modules.values_list("moduleID", flat=True))

        new_module_ids = set(int(mid) for mid in request.POST.getlist("modules"))

        modules_to_remove_ids = set(
            int(mid) for mid in request.POST.getlist("modulesToRemove", [])
        )

        updated_module_ids = (
            existing_modules_ids | new_module_ids
        ) - modules_to_remove_ids

        student.modules.set(updated_module_ids)

        student.save()

        messages.success(request, "Student updated successfully.")
        return redirect(
            "student_list"
        ) 

    else:
        modules = Module.objects.all().order_by("moduleName")
        selected_module_ids = student.modules.values_list("moduleID", flat=True)

        context = {
            "student": student,
            "modules": modules,
            "selected_module_ids": list(selected_module_ids),
        }

        return render(request, "update_student.html", context)


def delete_student(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)

    if request.method == "POST":
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('student_list')

    return render(request, 'delete_student.html', {'student': student})

def view_student(request, student_id):
    student = get_object_or_404(Student, studentID=student_id)

    selected_modules = student.modules.all()

    schedules = Schedule.objects.filter(module__in=selected_modules)

    context = {
        'student': student,
        'schedules': schedules,
    }

    return render(request, 'view_student.html', context)


def export_schedules_to_json():
    schedules = Schedule.objects.all()
    schedules_data = [
        {
            "module_name": schedule.module.moduleName,
            "lecturer_name": schedule.lecturer.lecturerName,
            "start_datetime": schedule.startDateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": schedule.endDateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "venue_name": schedule.venueName,
        }
        for schedule in schedules
    ]

    with open("schedule_data.json", "w") as outfile:
        json.dump(schedules_data, outfile, cls=DjangoJSONEncoder)


def schedule_register(request):
    if request.method == "POST":
        module_id = request.POST["module_id"]
        lecturer_id = request.POST["lecturer_id"]
        start_datetime = request.POST["start_datetime"]
        end_datetime = request.POST["end_datetime"]
        venue_name = request.POST["venue_name"]

        try:
            module = Module.objects.get(moduleID=module_id)
            lecturer_instance = lecturer.objects.get(lecturerID=lecturer_id)

            schedule = Schedule(
                module=module,
                lecturer=lecturer_instance,
                startDateTime=start_datetime,
                endDateTime=end_datetime,
                venueName=venue_name,
            )
            schedule.save()

            export_schedules_to_json()
        except Module.DoesNotExist or lecturer.DoesNotExist:
            messages.error(request, "Module or Lecturer not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("schedule_list")

    modules = Module.objects.all()
    lecturers = lecturer.objects.all()
    return render(
        request, "schedule_register.html", {"modules": modules, "lecturers": lecturers}
    )


def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)

    if request.method == "POST":
        module_id = request.POST.get("module_id")
        lecturer_id = request.POST.get("lecturer_id")
        start_datetime = request.POST.get("start_datetime")
        end_datetime = request.POST.get("end_datetime")
        venue_name = request.POST.get("venue_name")

        try:
            module = Module.objects.get(moduleID=module_id)
            lecturer_instance = lecturer.objects.get(lecturerID=lecturer_id)

            schedule.module = module
            schedule.lecturer = lecturer_instance
            schedule.startDateTime = start_datetime
            schedule.endDateTime = end_datetime
            schedule.venueName = venue_name
            schedule.save()

            export_schedules_to_json()
            return redirect("schedule_list")
        except Module.DoesNotExist or lecturer.DoesNotExist:
            messages.error(request, "Module or Lecturer not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    modules = Module.objects.all()
    lecturers = lecturer.objects.all()
    return render(
        request,
        "update_schedule.html",
        {"schedule": schedule, "modules": modules, "lecturers": lecturers},
    )


from django.shortcuts import render, get_object_or_404

def view_schedule(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    selected_modules = student.modules.all()
    schedules = Schedule.objects.filter(module__in=selected_modules).order_by('startDateTime')

    return render(request, 'view_schedule.html', {
        'student': student,
        'schedules': schedules,
    })


def schedule_list(request):
    schedules = Schedule.objects.all()
    modules = Module.objects.all() 
    return render(request, 'schedule_list.html', {'schedules': schedules, 'modules': modules})

def logout_view(request):
    logout(request)
    return render(request, 'logout_view.html')