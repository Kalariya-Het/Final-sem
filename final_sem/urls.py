"""final_sem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from attendance_system import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('home',views.home,name="home"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('admin_page',views.admin_page,name="admin_page"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('forget_pass_admin',views.forget_pass_admin,name="forget_pass_admin"),
    path('forget_pass_admin_view',views.forget_pass_admin_view,name="forget_pass_admin_view"),
    path('change_admin_pass',views.change_admin_pass,name="change_admin_pass"),
    path('faculty_edit/<int:id>',views.faculty_edit,name="faculty_edit"),
    path('faculty_add/<int:id>',views.faculty_add,name="faculty_add"),
    path('attendance',views.attendance,name="attendance"),
    path('holiday_page',views.holiday_page,name="holiday_page"),
    path('holidays',views.holidays,name="holidays"),
    path('face_train',views.face_train,name="face_train"),
    path('faculty_login',views.faculty_login,name="faculty_login"),
    path('pass_change/<int:id>',views.pass_change,name="pass_change"),
    path('forget_pass',views.forget_pass,name="forget_pass"),
    path('forget_change_pass',views.forget_change_pass,name="forget_change_pass"),
    path('<int:id>/',views.faculty_update,name='faculty_update'),
    path('faculty_delete/<int:id>',views.faculty_delete,name='faculty_delete'),
    path('take_pic',views.take_pic,name='take_pic'),
    path('recognize',views.recognize,name='recognize'),
    path('search',views.search,name='search'),
    #path('search_faculty',views.search_faculty,name='search_faculty'),
    path('report',views.report,name='report'),
    path('pdf_report',views.pdf_report,name='pdf_report'),
    path('leave_page',views.leave_page,name="leave_page"),
    path('leave_grant',views.leave_grant,name="leave_grant"),
    path('logout',views.logout,name="logout"),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
