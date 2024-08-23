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
                    'created_answers', 'display_liked_questions', 'display_liked_answers'
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

    readonly_fields = ('display_liked_questions', 'display_liked_answers')
    search_fields = ('email', 'username')
    ordering = ('email',)


    def display_liked_questions(self, obj):
        """ Return a string with the titles of the questions liked by the. """
        return ", ".join([q.title for q in obj.upvoted_questions.all()])
    display_liked_questions.short_description = 'Liked Questions'

    def display_liked_answers(self, obj):
        """ 
        Return a string with the first 
        50 characters of the text of the answers liked by the user. """
        return ", ".join([a.text[:50] for a in obj.upvoted_answers.all()])
    display_liked_answers.short_description = 'Liked Answers'

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
                'created_answers', 'is_active', 'is_staff',
                'display_liked_questions', 'display_liked_answers'
            )
        return super().get_readonly_fields(request, obj)


admin.site.register(CustomUser, CustomUserAdmin)
