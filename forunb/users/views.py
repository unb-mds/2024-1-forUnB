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
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Gerar o código de verificação
            verification_code = get_random_string(4, allowed_chars='0123456789')
            
            # Armazenar o código e os dados do usuário na sessão
            request.session['verification_code'] = verification_code
            request.session['registration_data'] = request.POST

            # Enviar o código de verificação por e-mail usando a nova função
            user = form.save(commit=False)  # Não salvar ainda para enviar o e-mail primeiro
            send_verification_email(user, verification_code)

            return render(request, 'users/verify_email.html', {'email': user.email})
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

@login_required(login_url='/users/login')
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


def verify_email(request):
    if request.method == 'POST':
        if 'resend_code' in request.POST:
            # Obtenha o e-mail da sessão
            registration_data = request.session.get('registration_data')
            email = registration_data.get('email') if registration_data else None

            user = None
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                except CustomUser.DoesNotExist:
                    # Define user como None se o usuário não for encontrado
                    user = None

                # Gerar um novo código de verificação
                verification_code = get_random_string(4, allowed_chars='0123456789')
                request.session['verification_code'] = verification_code

                # Enviar o novo código de verificação
                send_verification_email(user, verification_code)

                messages.success(request, 'Um novo código foi enviado para seu e-mail.')
            else:
                messages.error(request, 'Ocorreu um erro na verificação. Por favor, tente novamente.')

        elif 'cancel' in request.POST:
            return redirect('users:register')

        else:
            code_entered = request.POST.get('verification_code')
            code_sent = request.session.get('verification_code')

            if not code_sent:
                messages.error(request, 'Ocorreu um erro na verificação. Por favor, tente novamente.')
                return render(request, 'users/verify_email.html')

            if code_entered == code_sent:
                form = CustomUserCreationForm(request.session.get('registration_data'))
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    del request.session['verification_code']
                    del request.session['registration_data']
                    return redirect('main:index')
            else:
                messages.error(request, 'Código de verificação incorreto.')

    return render(request, 'users/verify_email.html')


def send_verification_email(user, verification_code):
    subject = 'Confirme seu E-mail para Acessar o forUnB'

    # Se o usuário for None, o nome de usuário será uma string vazia
    username = user.username if user else ''

    message = render_to_string('emails/email_verification_template.txt', {
        'username': username,
        'verification_code': verification_code,
    })

    recipient_email = user.email if user else 'email_provided_some_other_way@example.com'
    
    send_mail(
        subject,
        message,
        'forunb.noreply@gmail.com',  # O e-mail verificado
        [recipient_email],  # Envia para o e-mail do usuário ou outro definido
    )
