from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',views.home,name='home'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('admin',views.admin, name='admin'),
    path('apply/<int:job_id>/',views.apply_job, name='apply_job'),
    path('dashboard/jobs/', views.dashboard_jobs, name='dashboard_jobs'),

    path('dashboard/applied/', views.dashboard_applied, name='dashboard_applied'),
    path('dashboard/interview/', views.dashboard_interview, name='dashboard_interview'),
    path('dashboard/offered/', views.dashboard_offered, name='dashboard_offered'),
    path('dashboard/rejected/', views.dashboard_rejected, name='dashboard_rejected'),
]
