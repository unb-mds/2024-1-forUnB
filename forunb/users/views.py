"""Views for handling user-related actions in the users application."""

from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import CustomUser


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # The form's save method handles user creation
            authenticated_user = authenticate(
                username=user.email, password=request.POST['password1']
            )
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('main:index')
            print("Falha na autenticação")
        else:
            print("Formulário inválido")
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register_unb_email.html', {'form': form})

@require_GET 
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        # Check if the email exists in the database
        email = request.POST.get('username')

        if not CustomUser.objects.filter(email=email).exists():
            form.add_error('username', "Este email não está cadastrado.")
        elif not form.is_valid():
            form.add_error('password', "Senha incorreta.")

        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next', "main:index"))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})


def profile(request):
    """Render the user's profile page."""
    return render(request, 'users/profile.html')


@login_required(login_url='/users/login')
def edit_profile(request):
    """Handle profile editing."""
    if request.method == 'POST':
        username = request.POST.get('username')
        photo = request.FILES.get('photo')

        if username:
            if CustomUser.objects.filter(username=username).exclude(
                id=request.user.id
            ).exists():
                return JsonResponse({
                    'success': False,
                    'errors': 'Este nome de usuário já está em uso.'
                })
            user = request.user
            user.username = username
            if photo:
                user.photo = photo
            user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': 'Nome de usuário não pode estar vazio.'})
    return JsonResponse({'success': False, 'error': 'Método de requisição inválido.'})
