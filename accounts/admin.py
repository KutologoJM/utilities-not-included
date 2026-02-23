from django.contrib.sessions.models import Session
from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )
    raw_id_fields = ('groups', 'user_permissions')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'expire_date', 'data')
    readonly_fields = ('session_key', 'session_data', 'expire_date')

    def data(self, obj):
        """Return decoded session data."""
        return obj.get_decoded()

    def user(self, obj):
        """Get the user from session data if available."""
        session_data = obj.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id:
            try:
                return CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                return None
        return None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Session, SessionAdmin)
