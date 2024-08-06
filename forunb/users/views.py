from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

def register(request): 
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid(): 
            user = form.save()  # O método save do formulário já lida com a criação do usuário 
            authenticated_user = authenticate(username=user.email, password=request.POST['password1'])  # Autentica o usuário recém-criado 
            if authenticated_user is not None: 
                login(request, authenticated_user) 
                return redirect('main:index') 
            else: 
                print("Falha na autenticação") 
        else: 
            print("Formulário inválido") 
            print(form.errors) 
    else: 
        form = CustomUserCreationForm() 
 
    return render(request, 'users/register_unb_email.html', {'form': form})


def Logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

# nao esta sendo usado
# def login_redirect(view_func):
#     return user_passes_test(lambda u: u.is_authenticated, login_url='/users/login/')(view_func)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("main:index")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})

def profile(request):
    return render(request, 'users/profile.html')

# def register_unb_email(request):
#     if request.method == 'POST':
#         form = UnbEmailRegistrationForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             # Cria um novo usuário com o email e senha fornecidos
#             user = User.objects.create_user(username=email, email=email, password=password)
#             # Você pode adicionar outras lógicas aqui, como enviar um email de confirmação
#             return redirect('login')  # Redireciona para a página de login após o registro
#     else:
#         form = UnbEmailRegistrationForm()

#     return render(request, 'users/register_unb_email.html', {'form': form})

# def register(request):
#     if request.method != 'POST':
#         form = UnbEmailRegistrationForm()
#     else:
#         form = UnbEmailRegistrationForm(data=request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
#             login(request, authenticated_user)
#             return HttpResponseRedirect(reverse('index'))
#     context = {'form': form}
#     return render(request, 'users/register.html', context)
