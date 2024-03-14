from django.contrib import admin
from .models import appAdmin
from lecturer.models import lecturer
from modules.models import Module
from student.models import Student
from schedules.models import Schedule


@admin.register(appAdmin)
class appAdminAdmin(admin.ModelAdmin):
    list_display = ("adminID", "adminNumber", "adminName")
    list_filter = ("adminNumber", "adminName")
    search_fields = ("adminNumber", "adminName")


@admin.register(lecturer)
class lecturerAdmin(admin.ModelAdmin):
    list_display = ("lecturerID", "lecturerNumber", "lecturerName", "lecturerPassword")
    list_filter = ("lecturerNumber", "lecturerName")
    search_fields = ("lecturerNumber", "lecturerName")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("moduleID", "moduleName", "moduleCode", "lecturer_name")
    list_filter = ("moduleName", "moduleCode")
    search_fields = ("moduleName", "moduleCode")

    def lecturer_name(self, obj):
        return obj.lecturer.lecturerName

    lecturer_name.short_description = "Lecturer Name"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "studentID",
        "studentName",
        "studentNumber",
        "studentEmail",
        "studentFace",
        "modules_list",
    )
    list_filter = ("studentName", "studentNumber", "studentEmail")

    def modules_list(self, obj):
        return ", ".join([module.moduleName for module in obj.modules.all()])

    modules_list.short_description = "Modules"
    filter_horizontal = ("modules",)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("module", "lecturer", "startDateTime", "endDateTime", "venueName")
    list_filter = ("module", "lecturer", "startDateTime", "endDateTime")
    search_fields = ("module__moduleName", "lecturer__lecturerName", "venueName")


admin.site.register(Schedule, ScheduleAdmin)
