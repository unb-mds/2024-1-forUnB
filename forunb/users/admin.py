from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from main.models import Forum  # Certifique-se de importar o modelo Forum

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # Excluindo 'date_joined' dos fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'followed_forums', 'created_questions', 'created_answers', 'liked_questions', 'liked_answers')}),  # Adiciona 'followed_forums'
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Adicionando 'followed_forums' aos campos de adição
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

    # Ajusta o formulário para incluir o campo 'followed_forums'
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['followed_forums'].queryset = Forum.objects.all()  # Ajusta a queryset
        return form

    # Torna o campo 'followed_forums' editável apenas se o usuário for um superusuário
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se o objeto existe, estamos na página de edição
            return ('email', 'username', 'date_joined', 'created_questions', 'created_answers', 'is_active', 'is_staff')
        return super().get_readonly_fields(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)
