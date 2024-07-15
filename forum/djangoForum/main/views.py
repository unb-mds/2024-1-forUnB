from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Forum, Answer
from .forms import ForumForm, AnswerForm
from django.urls import reverse
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'main/index.html')

def questions(request):
    questions = Forum.objects.all()
    context = {
        'questions': questions 
    }
    return render(request, 'main/questions.html', context)

def question(request, question_id):
    question = Forum.objects.get(id=question_id)
    context = {
        'question': question
    }
    return render(request, 'main/question.html', context) 

def new_question(request):
    if request.method != 'POST':
        form = ForumForm()
    else:
        form = ForumForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.save()
            form.save()
            return HttpResponseRedirect(reverse('questions'))
    context = {'form': form}
    return render(request, 'main/new_question.html', context) 
    
def new_answer(request, question_id):
    # forum = get_object_or_404(Forum, id=question_id)
    forum = Forum.objects.get(id=question_id)
    if request.method != 'POST':
        form = AnswerForm()
    else:
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.forum = forum
            new_answer.save()
            return HttpResponseRedirect(reverse('question', args=[question_id, ]))
    context = {'forum': forum, 'form': form}
    return render(request, 'main/new_answer.html', context)