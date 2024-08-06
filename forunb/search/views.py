from django.shortcuts import render, get_object_or_404
from main.models import Question, Forum
from unidecode import unidecode

def normalize_string(s):
    '''Remove os espaços extras e junta as palavras com um espaço entre elas'''
    return ' '.join(s.split())

def search_forum(request):
    '''Busca por fóruns ou perguntas utilizando o unidecode para remover acentos e normaliza a string'''
    query = request.GET.get('search', '')
    query_normalized = unidecode(normalize_string(query))
    forum_id = request.GET.get('forum_id', None)

    if forum_id:
        forum = get_object_or_404(Forum, id=forum_id)
        questions = Question.objects.all()
        filtered_questions = [
            question for question in questions
            if query_normalized.lower() in unidecode(normalize_string(question.title)).lower()
        ]
        filtered_questions = sorted(filtered_questions, key=lambda q: q.created_at, reverse=True)
        return render(request, 'main/forum_detail.html', {'forum': forum, 'questions': filtered_questions, 'query': query})
    else:
        forums = Forum.objects.all()
        filtered_forums = [
            forum for forum in forums
            if query_normalized.lower() in unidecode(normalize_string(forum.title)).lower()
        ]
        return render(request, 'main/forums.html', {'forums': filtered_forums, 'query': query})
