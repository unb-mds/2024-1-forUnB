from django.shortcuts import render, get_object_or_404
from main.models import Question, Forum
from unidecode import unidecode

def search_forum(request):
    query = request.GET.get('search', '')
    query_normalized = unidecode(query)
    forum_id = request.GET.get('forum_id', None)

    if forum_id:
        forum = get_object_or_404(Forum, id=forum_id)
        questions = Question.objects.all()
        filtered_questions = [
            question for question in questions
            if query_normalized.lower() in unidecode(question.title).lower()
        ]
        filtered_questions = sorted(filtered_questions, key=lambda q: q.created_at, reverse=True)
        return render(request, 'main/forum_detail.html', {'forum': forum, 'questions': filtered_questions, 'query': query})
    else:
        forums = Forum.objects.all()
        filtered_forums = [
            forum for forum in forums
            if query_normalized.lower() in unidecode(forum.title).lower()
        ]
        return render(request, 'main/forums.html', {'forums': filtered_forums, 'query': query})
