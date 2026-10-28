from django.contrib import admin
from .models import Account

# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active')
    # search_fields = ('email', 'username')
    # readonly_fields = ('date_joined', 'last_login')

    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

