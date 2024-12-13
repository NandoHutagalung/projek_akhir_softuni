from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    # Form untuk mengedit pengguna
    form = UserChangeForm
    # Form untuk membuat pengguna baru
    add_form = UserCreationForm

    # List of fields to display in the list view
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active', 'is_staff', 'is_superuser')

    # List of fields to be searchable
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # List of fields to filter by in the right sidebar
    list_filter = ('role', 'is_active', 'is_staff')

    # Fields to be displayed on the user detail/edit page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Password dihandle dengan hashing otomatis
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
    )

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role'),
        }),
    )

    # Define the ordering of users
    ordering = ('username',)

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
