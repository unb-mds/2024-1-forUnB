from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Forum, Answer, Question
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test


def login_redirect(view_func):
    return user_passes_test(lambda u: u.is_authenticated, login_url='/accounts/login/')(view_func)

def index(request):
    latest_questions = Question.objects.all().order_by('-created_at')  # Ordenar por data de criação
    return render(request, 'main/index.html', {'latest_questions': latest_questions})

def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    questions = Question.objects.filter(forum=forum).order_by('-created_at')
    return render(request, 'main/forum_detail.html', {'forum': forum, 'questions': questions})

def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'main/forums.html', {'forums': forums})

def questions(request):
    questions = Question.objects.all()  # Ajuste conforme necessário para filtrar as perguntas desejadas
    return render(request, 'main/questions.html', {'questions': questions})


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()  # Supondo que você configurou related_name='answers' no modelo Answer
    forum = question.forum
    return render(request, 'main/question_detail.html', {'question': question, 'answers': answers})


@login_required
def new_question(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.forum = forum
            question.author = request.user
            question.save()
            return redirect('forum_detail', forum_id=forum.id)
    else:
        form = QuestionForm()
    return render(request, 'main/new_question.html', {'form': form, 'forum': forum})


@login_required
def new_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'main/new_answer.html', {'form': form, 'question': question})

