"""
URL configuration for finalattd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from accounts import views as accounts_views
from lecturer import views as lecturer_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accounts_views.main, name="home"),
    path("login/", accounts_views.login, name="login"),
    path("dashboard/", accounts_views.dashboard, name="dashboard"),
    path("logout_view/", accounts_views.logout_view, name="logout_view"),
    path("lec_reg/", accounts_views.lec_register, name="lec_register"),
    path("lec_login/", lecturer_views.lec_login, name="lec_login"),
    path("lec_dashboard/", lecturer_views.lec_dashboard, name="lec_dashboard"),
    path("lec_logout_view/", lecturer_views.lec_logout_view, name="lec_logout_view"),
    path("module_register/", accounts_views.module_register, name="module_register"),
    path("module_list/", accounts_views.module_list, name="module_list"),
    path(
        "module/update/<int:module_id>/",
        accounts_views.update_module,
        name="update_module",
    ),
    path(
        "module/delete/<int:module_id>/",
        accounts_views.delete_module,
        name="delete_module",
    ),
    path("lecturer_list/", accounts_views.lecturer_list, name="lecturer_list"),
    path(
        "update_lecturer/<int:lecturer_id>/",
        accounts_views.update_lecturer,
        name="update_lecturer",
    ),
    path(
        "delete_lecturer/<int:lecturer_id>/",
        accounts_views.delete_lecturer,
        name="delete_lecturer",
    ),
    path("student/register/", accounts_views.student_register, name="student_register"),
    path("student/list/", accounts_views.student_list, name="student_list"),
    path(
        "student/update/<int:student_id>/",
        accounts_views.update_student,
        name="update_student",
    ),
    path(
        "student/delete/<int:student_id>/",
        accounts_views.delete_student,
        name="delete_student",
    ),
    path(
        "schedule/register/", accounts_views.schedule_register, name="schedule_register"
    ),
    path("schedule/list/", accounts_views.schedule_list, name="schedule_list"),
    path(
        "view_student/<int:student_id>/",
        accounts_views.view_student,
        name="view_student",
    ),
    path(
        "view_schedule/<int:student_id>/",
        accounts_views.view_schedule,
        name="view_schedule",
    ),
    path(
        "schedule/update/<int:schedule_id>/",
        accounts_views.update_schedule,
        name="update_schedule",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
