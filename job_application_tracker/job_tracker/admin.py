from django.contrib import admin
from .models import JobPost, Application
from django.core.mail import send_mail
from .views import send_status_update_email  # or from .utils import send_status_update_email

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'salary_min', 'salary_max', 'level', 'job_type')
    search_fields = ('title', 'company')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at', 'interview_date')
    list_filter = ('status',)
    readonly_fields = ('applied_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'job', 'name', 'email', 'resume', 'status', 'applied_at', 'interview_date')
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = obj.__class__.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                send_status_update_email(obj.user, obj.job, obj.status)

        super().save_model(request, obj, form, change)
