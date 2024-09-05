"""Views for the main app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.urls import reverse
from bs4 import BeautifulSoup
from main.models import Forum, Answer, Question, Notification  # pylint: disable=E1101
from main.forms import QuestionForm, AnswerForm, ReportForm


def index(request):
    """Render the index page with the latest questions."""
    filter_by = request.GET.get('filter_by', 'latest')

    if filter_by == 'followed':
        if request.user.is_authenticated:
            latest_questions = Question.objects.filter(  # pylint: disable=E1101
                forum__in=request.user.followed_forums.all(), reports__isnull=True
            ).order_by('-created_at')
        else:
            return redirect(f"{reverse('users:login')}?next={request.path}")
    else:
        latest_questions = Question.objects.filter(  # pylint: disable=E1101
            reports__isnull=True
        ).order_by('-created_at')

    return render(request, 'main/index.html', {'latest_questions': latest_questions})


def forum_detail(request, forum_id):
    """Render the forum detail page with the questions associated with the forum."""
    forum = get_object_or_404(Forum, id=forum_id)
    order_by = request.GET.get('order_by', 'date')
    questions = Question.objects.filter(  # pylint: disable=E1101, W0621
        forum=forum).annotate(total_upvotes=Count('upvoters'))
    if order_by == 'least_upvoted':
        questions = questions.order_by('total_upvotes')
    elif order_by == 'most_upvoted':
        questions = questions.order_by('-total_upvotes')
    elif order_by == 'oldest':
        questions = questions.order_by('created_at')
    else:
        questions = questions.order_by('-created_at')

    is_following = request.user.is_authenticated and request.user.followed_forums.filter(
        id=forum.id).exists()

    return render(request, 'main/forum_detail.html', {
        'forum': forum,
        'questions': questions,
        'is_following': is_following,
    })


def forum_list(request):
    """Render the forum list page with all forums."""
    forums = Forum.objects.all()  # pylint: disable=E1101
    return render(request, 'main/forums.html', {'forums': forums})


@login_required(login_url='/users/login')
def followed_forums(request):
    """Render the followed forums page with the forums that the user follows."""
    user = request.user
    follow_forums = user.followed_forums.all()
    return render(request, 'main/forums.html', {'forums': follow_forums})


def questions(request):
    """Render the questions page with all questions."""
    all_questions_list = Question.objects.all()  # pylint: disable=E1101
    return render(request, 'main/questions.html', {'questions': all_questions_list})


@login_required(login_url='/users/login')
def user_posts(request):
    """Render the user posts page with the questions and answers created by the user."""
    user = request.user
    user_questions = Question.objects.filter(author=user) # pylint: disable=E1101
    user_answers = Answer.objects.filter(author=user)  # pylint: disable=E1101
    context = {
        'questions': user_questions,
        'answers': user_answers,
    }
    return render(request, 'main/questions.html', context)


def question_detail(request, question_id):
    """Render the question detail page with the question and its answers."""
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()  # pylint: disable=E1101
    return render(request, 'main/question_detail.html', {'question': question, 'answers': answers})


def clean_html(text):
    """Remove HTML tags but preserve line breaks and basic formatting."""
    soup = BeautifulSoup(text, 'html.parser')
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all("p"):
        p.insert(0, "\n")
        p.insert(len(p.contents), "\n")
    cleaned_text = soup.get_text()
    return cleaned_text

@require_http_methods(["GET"])
def about(request):
    """Render the about page."""
    return render(request, 'main/about.html')

@login_required(login_url='/users/login')
def follow_forum(request, forum_id, action):
    """Follow or unfollow a forum."""
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
    """Create a new question"""
    forum = get_object_or_404(Forum, id=forum_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.forum = forum
            question.author = request.user
            question.description = clean_html(question.description)
            question.save()
            request.user.created_questions.add(question)
            return JsonResponse({'success': True, 'question_id': question.id})
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    form = QuestionForm()
    return render(request, 'main/new_question.html', {'form': form, 'forum': forum})


@login_required(login_url='/users/login')
def new_answer(request, question_id):
    """Create a new answer."""
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.text = clean_html(answer.text)
            answer.save()
            request.user.created_answers.add(answer)

            # Create notification for the question's author
            if question.author != request.user:
                Notification.objects.create(  # pylint: disable=E1101
                    user=question.author,
                    question=question,
                    answer=answer
                )

            return JsonResponse({'success': True, 'question_id': question.id})

        return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='/users/login')
def delete_question(request, pk):
    """Delete a question."""
    question = get_object_or_404(Question, pk=pk, author=request.user)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Pergunta deletada com sucesso.')
        return redirect('main:user_posts')
    return render(request, 'main/confirm_delete.html', {'object': question})


@login_required(login_url='/users/login')
def delete_answer(request, pk):
    """Delete an answer."""
    answer = get_object_or_404(Answer, pk=pk, author=request.user)
    if request.method == 'POST':
        answer.delete()
        messages.success(request, 'Resposta deletada com sucesso.')
        return redirect('main:user_posts')
    return render(request, 'main/confirm_delete.html', {'object': answer})


@login_required(login_url='/users/login')
def notifications(request):
    """Render the notifications page with the user's notifications."""
    user_notifications = Notification.objects.filter(  # pylint: disable=E1101
        user=request.user).order_by('-created_at')
    return render(request, 'main/notifications.html', {'notifications': user_notifications})


@login_required(login_url='/users/login')
@require_POST
def toggle_upvote_question(request, question_id):
    """Toggle the upvote of a question for a user."""
    question = get_object_or_404(Question, id=question_id)
    question.toggle_upvote(request.user)
    return JsonResponse({'upvotes': question.upvote_count})


@login_required(login_url='/users/login')
@require_POST
def toggle_upvote_answer(request, answer_id):
    """Toggle the upvote of an answer for a user."""
    answer = get_object_or_404(Answer, id=answer_id)
    answer.toggle_upvote(request.user)
    return JsonResponse({'upvotes': answer.upvote_count})


@login_required(login_url='/users/login')
def report(request, item_id, item_type):
    """Report a question or an answer."""
    try:
        if item_type == 'question':
            item = get_object_or_404(Question, id=item_id)
        elif item_type == 'answer':
            item = get_object_or_404(Answer, id=item_id)
        else:
            return JsonResponse({'success': False, 'error': 'Tipo de item inválido.'}, status=400)

        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                report_instance = form.save(commit=False)
                if item_type == 'question':
                    report_instance.question = item
                else:
                    report_instance.answer = item
                report_instance.user = request.user
                report_instance.save()
                return JsonResponse({'success': True})
            print(form.errors)  # Isso irá mostrar quais campos estão falhando
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
        return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)
    except Exception as e:  # pylint: disable=broad-except
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
