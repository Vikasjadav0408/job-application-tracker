from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,'index.html');

def login(request):
    return render(request,'login.html');

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        # (Add password validation here if needed)
        user = User.objects.create_user(username=username, email=email, password=password1)
        send_welcome_email(user)
        # Optionally, log the user in or redirect
        return render(request, 'register.html', {'success': True})
    return render(request, 'register.html')

def admin(request):
    return render(request,'admin.html');

from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    if Application.objects.filter(user=request.user, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect('dashboard_jobs')

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        Application.objects.create(user=request.user, job=job, resume=resume)
        messages.success(request, "Application submitted!")
        return redirect('dashboard_jobs')

    return render(request, 'apply_job.html', {'job': job})

from .models import JobPost, Application

def dashboard_jobs(request):
    tab = request.GET.get('tab', 'jobs')
    jobs = JobPost.objects.all()
    user_applied_job_ids = []
    applied = Application.objects.filter(user=request.user, status='applied')
    interviewed = Application.objects.filter(user=request.user, status='interview')
    offered = Application.objects.filter(user=request.user, status='offer')
    rejected = Application.objects.filter(user=request.user, status='rejected')
    if request.user.is_authenticated:
        user_applied_job_ids = list(Application.objects.filter(user=request.user).values_list('job_id', flat=True))
    return render(request, 'dashboard.html', {
        'jobs': jobs,
        'tab': tab,
        'applied': applied,
        'interviewed': interviewed,
        'offered': offered,
        'rejected': rejected,
        'user_applied_job_ids': user_applied_job_ids,
    })


def dashboard_applied(request):
    tab = request.GET.get('tab', 'applied')
    applied = Application.objects.filter(user=request.user, status='applied')
    interviewed = Application.objects.filter(user=request.user, status='interview')
    offered = Application.objects.filter(user=request.user, status='offer')
    rejected = Application.objects.filter(user=request.user, status='rejected')
    return render(request, 'dashboard.html', {
        'applied': applied,
        'tab': tab,
        'interviewed': interviewed,
        'offered': offered,
        'rejected': rejected,
    })

def dashboard_interview(request):
    tab = request.GET.get('tab', 'interview')
    interviewed = Application.objects.filter(user=request.user, status='interview')
    applied = Application.objects.filter(user=request.user, status='applied')
    offered = Application.objects.filter(user=request.user, status='offer')
    rejected = Application.objects.filter(user=request.user, status='rejected')
    return render(request, 'dashboard.html', {
        'interviewed': interviewed,
        'tab': tab,
        'applied': applied,
        'offered': offered,
        'rejected': rejected,
    })

def dashboard_offered(request):
    offered = Application.objects.filter(user=request.user, status='offer')
    return render(request, 'dashboard.html', {
        'applied': [],
        'interviewed': [],
        'offered': offered,
        'tab': 'offered',
        'rejected': [],
    })

def dashboard_rejected(request):
    rejected = Application.objects.filter(user=request.user, status='rejected')
    return render(request, 'dashboard.html', {
        'applied': [],
        'interviewed': [],
        'offered': [],
        'rejected': rejected,
        'tab': 'rejected',
    })

def send_status_update_email(user, job, status):
    subject = "Your job application status has been updated"
    message = f"Hi {user.username},\n\nThe status of your application for '{job.title}' has been updated to: {status}.\n\nRegards,\nAdmin Team"
    send_mail(subject, message, 'vikasjadav888@gmail.com', [user.email])

def send_welcome_email(user):
    
    subject = "Welcome to Job Application Tracker!"
    message = f"Hi {user.username},\n\nThank you for registering at Job Application Tracker. We're excited to have you on board!\n\nBest regards,\nThe Team"
    send_mail(subject, message, 'vikasjadav888@gmail.com', [user.email])
