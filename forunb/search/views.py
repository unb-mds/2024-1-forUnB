from django.shortcuts import render
from main.models import Forum

def search_forum(request):
    query = request.GET.get('search', '')  # Obtém o parâmetro de pesquisa da URL
    forums = Forum.objects.filter(title__icontains=query)  # Filtra os fóruns com base na pesquisa
    return render(request, 'main/forums.html', {'forums': forums, 'query': query})  # Renderiza a página de fóruns com os resultados
