from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Forum, Answer, Question
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


# Login view vai passar para o app de users
# def login_redirect(view_func):
#     return user_passes_test(lambda u: u.is_authenticated, login_url='/accounts/login/')(view_func)


def index(request):
    latest_questions = Question.objects.all().order_by(
        '-created_at')  # Ordenar por data de criação
    return render(request, 'main/index.html', {'latest_questions': latest_questions})


def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    order_by = request.GET.get('order_by', 'date')
    # Vai ser implementado o upvote ainda
    # if order_by == 'likes':
    #     questions = Question.objects.filter(forum=forum).order_by('-likes')  # Ordenar por número de likes
    # elif order_by == 'dislikes':
    #     questions = Question.objects.filter(forum=forum).order_by('dislikes')  # Ordenar por número de dislikes
    if order_by == 'oldest':
        questions = Question.objects.filter(forum=forum).order_by('created_at')  
    else:
        questions = Question.objects.filter(forum=forum).order_by('-created_at') 
    
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.followed_forums.filter(id=forum.id).exists()
    
    return render(request, 'main/forum_detail.html', {
        'forum': forum,
        'questions': questions,
        'is_following': is_following,
    })


def forum_list(request):
    forums = Forum.objects.all()
    return render(request, 'main/forums.html', {'forums': forums})

@login_required(login_url='/users/login')
def followed_forums(request):
    user = request.user
    followed_forums = user.followed_forums.all()
    return render(request, 'main/forums.html', {'forums': followed_forums})

def questions(request):
    # Ajuste conforme necessário para filtrar as perguntas desejadas
    questions = Question.objects.all()
    return render(request, 'main/questions.html', {'questions': questions})

@login_required(login_url='/users/login')
def user_posts(request):
    user = request.user
    questions = Question.objects.filter(author=user)
    answers = Answer.objects.filter(author=user)
    context = {
        'questions': questions,
        'answers': answers,
    }
    return render(request, 'main/questions.html', context)


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # Supondo que você configurou related_name='answers' no modelo Answer
    answers = question.answers.all()
    forum = question.forum
    return render(request, 'main/question_detail.html', {'question': question, 'answers': answers})

@login_required(login_url='/users/login')
def follow_forum(request, forum_id, action):
    if request.method == 'POST':
        forum = get_object_or_404(Forum, id=forum_id)
        if action == 'follow':
            request.user.followed_forums.add(forum)
        elif action == 'unfollow':
            request.user.followed_forums.remove(forum)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required(login_url='/users/login')
def new_question(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.forum = forum
            question.author = request.user
            question.save()
            request.user.created_questions.add(question)
            return redirect('main:forum_detail', forum_id=forum.id)
    else:
        form = QuestionForm()
    return render(request, 'main/new_question.html', {'form': form, 'forum': forum})


@login_required(login_url='/users/login')
def new_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            request.user.created_answers.add(answer)
            return redirect('main:question_detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'main/new_answer.html', {'form': form, 'question': question})
