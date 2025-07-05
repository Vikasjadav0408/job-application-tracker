from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class JobPost(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=50, null=True, blank=True)
    job_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview Scheduled'),
        ('offer', 'Offered'),
        ('rejected', 'Rejected'),
    ]
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    interview_date = models.DateTimeField(null=True, blank=True, help_text='Date and time for scheduled interview (admin set)')
    # applied_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        user = self.user.username if self.user else "Unknown User"
        job = self.job.title if self.job else "Unknown Job"
        return f"{user} applied for {job}"
