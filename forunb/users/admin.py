"""Admin module for managing custom user and related functionalities."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import Forum  # Certifique-se de importar o modelo Forum
from users.models import CustomUser
from users.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Admin class to manage CustomUser model."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal Info',
            {
                'fields': (
                    'username', 'followed_forums', 'created_questions',
                    'created_answers', 'liked_questions', 'liked_answers'
                )
            }
        ),
        (
            'Permissions', 
            {
                'fields': (
                    'is_staff', 'is_active', 'is_superuser',
                    'groups', 'user_permissions'
                )
            }
        ),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

    def get_form(self, request, obj=None, **kwargs):
        """Customize form to include the 'followed_forums' field with appropriate queryset."""
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['followed_forums'].queryset = Forum.objects.all() # pylint: disable=E1101
        return form

    def get_readonly_fields(self, request, obj=None):
        """Set readonly fields based on the user's permissions and object state."""
        if obj:  # Se o objeto existe, estamos na página de edição
            return (
                'email', 'username', 'date_joined', 'created_questions',
                'created_answers', 'is_active', 'is_staff'
            )
        return super().get_readonly_fields(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
