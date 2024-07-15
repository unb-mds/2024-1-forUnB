from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UnbEmailRegistrationForm

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

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UnbEmailRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UnbEmailRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=email, email=email, password=password)
            aunthenticated_user = authenticate(username=email, password=password)
            login(request, aunthenticated_user)
            return redirect('index')
    else:
        form = UnbEmailRegistrationForm()
    
    return render(request, 'users/register_unb_email.html', {'form': form})

def Logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

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



# Create your views here.
