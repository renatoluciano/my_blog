from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required

@login_required
def LikePost(request, pk):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Pegar o post pelo ID (pk - chave primária) ou retornar 404 se não encontrado
    # Verificar se o usuário já curtiu o post
    # Se já curtiu, remover a curtida; caso contrário, adicionar a curtida
    # Redirecionar de volta para a página de detalhes do post após a ação de curtir/descurtir 

    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)   

@login_required
def posts_list(request):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Pegar todos os posts publicados, ordenados por data de criação (do mais recente para o mais antigo)
    # Render da a página 'posts_list' passando os posts como contexto

    posts = Post.objects.filter(published=True).order_by('-created_at')
    return render(request, 'posts_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Pegar o post pelo ID (pk - chave primária) ou retornar 404 se não encontrado
    # Render da a página 'post_detail' passando o post como contexto

    post = get_object_or_404(Post, id=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create(request):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Se a requisição for GET, renderizar o formulário de criação de post
    # Se a requisição for POST, processar os dados do formulário e criar um novo post associado ao usuário logado
    # Redirecionar para a página de detalhes do post recém-criado após a criação bem-sucedida

    if request.method == 'GET':
        return render(request, 'post_create.html')
    else:
        title = request.POST.get('title')
        content = request.POST.get('content')
        published = request.POST.get('published')

        try:
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                published=request.POST.get('published') == 'on'
            )
            return redirect('post_detail', pk=post.id)
        except: 
            return render(request, 'post_create.html')