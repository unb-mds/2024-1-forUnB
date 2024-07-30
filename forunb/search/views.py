from django.shortcuts import render, redirect
from django.urls import reverse
from main.models import Forum

def search_forum(request):
    query = request.GET.get('search', '')  # Obtém o parâmetro de pesquisa da URL
    if query:
        try:
            forum = Forum.objects.get(title__icontains=query)  # Busca o fórum que contém o texto da pesquisa
            return redirect(reverse('forum_detail', args=[forum.id]))  # Redireciona para a página do fórum
        except Forum.DoesNotExist:
            return render(request, 'search/not_found.html', {'query': query})  # Página de não encontrado
    return redirect('forum_list')
