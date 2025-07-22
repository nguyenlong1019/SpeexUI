from django.contrib import admin
from core.models.log import AccessLog, EmailLog 
from core.models.user import User 
from django.contrib.contenttypes.models import ContentType 
from django.contrib.sessions.models import Session 
from django.contrib.admin.models import LogEntry 
from django.contrib.auth.admin import UserAdmin 
from django.utils.translation import gettext_lazy as _
from libs.utils import to_localdate


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    search_fields = ['id', 'model']
    list_display = ['id', 'app_label', 'model']
    list_filter = ['app_label']
    
    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Loại nội dung'
        self.model._meta.verbose_name_plural = 'Loại nội dung'
        return super().get_model_perms(request)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date_formatted']

    def get_readonly_fields(self, request, obj = ...):
        return [field.name for field in self.model._meta.get_fields()]

    
    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Phiên làm việc'
        self.model._meta.verbose_name_plural = 'Phiên làm việc'
        return super().get_model_perms(request)

    @admin.display(description='Expire date')
    def expire_date_formatted(self, obj):
        return to_localdate(obj.expire_date)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user']
    list_display = ['id', 'user', 'action_flag', 'change_message']
    list_filter = ['user']
    ordering = ['-action_time']

    def get_readonly_fields(self, request, obj = ...):
        return [field.name for field in self.model._meta.get_fields()]


    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Action Log'
        self.model._meta.verbose_name_plural = 'Action Log'
        return super().get_model_perms(request)
    

@admin.register(User)
class UserAccountAdmin(UserAdmin):
    list_display = ['email', 'fullname', 'updated_at_display']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_superuser', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at',]
    fieldsets = (
        (None, {'fields': ('id', 'created_at', 'updated_at')}),
        (None, {'fields': ('email', 'fullname')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'fullname', 'is_staff', 'is_superuser'), # form add 
        }),
    )
    search_fields = ('id', 'email',)
    ordering = ['-updated_at']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user_email',]
    list_display = ['id', 'user_email', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    search_fields = ['id', 'ip_address', 'user_agent']
    list_display = ['id', 'page_name', 'ip_address', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at', 'page_name', 'country']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']

