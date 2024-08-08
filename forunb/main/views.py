from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Forum, Answer, Question
from .forms import *
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Login view vai passar para o app de users
# def login_redirect(view_func):
#     return user_passes_test(lambda u: u.is_authenticated, login_url='/accounts/login/')(view_func)


def index(request):
    latest_questions = Question.objects.all().order_by(
        '-created_at')  # Ordenar por data de criação
    return render(request, 'main/index.html', {'latest_questions': latest_questions})


def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
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
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.forum = forum
            question.author = request.user
            question.save()
            request.user.created_questions.add(question)
            return JsonResponse({'success': True, 'question_id': question.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    else:
        form = QuestionForm()
    return render(request, 'main/new_question.html', {'form': form, 'forum': forum})



@login_required(login_url='/users/login')
def new_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            request.user.created_answers.add(answer)

            # Create notification for the question's author
            if question.author != request.user:
                Notification.objects.create(
                    user=question.author,
                    question=question,
                    answer=answer
                )
            
            return JsonResponse({'success': True, 'question_id': question.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='/users/login')
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk, author=request.user)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Pergunta deletada com sucesso.')
        return redirect('main:user_posts')
    return render(request, 'main/confirm_delete.html', {'object': question})

@login_required(login_url='/users/login')
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk, author=request.user)
    if request.method == 'POST':
        answer.delete()
        messages.success(request, 'Resposta deletada com sucesso.')
        return redirect('main:user_posts')
    return render(request, 'main/confirm_delete.html', {'object': answer})

@login_required(login_url='/users/login')
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/notifications.html', {'notifications': user_notifications})


@login_required
@require_POST
def toggle_upvote_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.toggle_upvote(request.user)
    return JsonResponse({'upvotes': question.upvote_count})

@login_required
@require_POST
def toggle_upvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.toggle_upvote(request.user)
    return JsonResponse({'upvotes': answer.upvote_count})