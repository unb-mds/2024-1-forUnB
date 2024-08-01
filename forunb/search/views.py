from django.shortcuts import render, get_object_or_404
from main.models import Question, Forum

def search_forum(request):
    query = request.GET.get('search', '')
    forum_id = request.GET.get('forum_id', None)  # Pega 'forum_id' ou None se não for passado

    if forum_id:
        forum = get_object_or_404(Forum, id=forum_id)
        questions = Question.objects.filter(forum=forum, title__icontains=query).order_by('-created_at')
        return render(request, 'main/forum_detail.html', {'forum': forum, 'questions': questions, 'query': query})
    else:
        forums = Forum.objects.filter(title__icontains=query)
        return render(request, 'main/forums.html', {'forums': forums, 'query': query})