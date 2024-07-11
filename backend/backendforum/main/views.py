from django.shortcuts import render, redirect
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
    question = get_object_or_404(Forum, id=question_id)
    answers = question.answer_set.all()
    context = {
        'question': question,
        'answers': answers
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
    question = get_object_or_404(Forum, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['text']
            new_answer = Answer(forum=question, text=answer_text)
            new_answer.save()
            return redirect('question', question_id=question_id)
    else:
        form = AnswerForm()
    
    context = {'form': form, 'question': question}
    return render(request, 'main/new_answer.html', context)