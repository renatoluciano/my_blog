from django.shortcuts import render, get_object_or_404, redirect
from user.models import Friendship, User
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
    # Renderizar a página 'posts_list' passando os posts como contexto.
    
    posts = Post.objects.filter(published=True).order_by('-created_at')
    from_user_friendships = Friendship.objects.filter(from_user=request.user)
    to_user_friendships = []
    friends_posts = []

    for from_user_friendship in from_user_friendships:
        to_user_friendships.append(from_user_friendship.to_user)
    to_user_friendships = list(set(to_user_friendships))

    for post in posts:
        if post.author in to_user_friendships:
            friends_posts.append(post) 
    remaining_posts = [post for post in posts if post not in friends_posts]

    print(to_user_friendships)
    print(friends_posts)
    print(remaining_posts)
    
    return render(request, 'posts_list.html', {'friends_posts': friends_posts,
                                               'remaining_posts': remaining_posts})

@login_required
def post_detail(request, pk):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Pegar o post pelo ID (pk - chave primária) ou retornar 404 se não encontrado
    # Renderizar a página 'post_detail' passando o post como contexto

    post = get_object_or_404(Post, id=pk)
    user_friendships = Friendship.objects.filter(from_user=request.user)
    users_friends = []
    for user_friendship in user_friendships:
        users_friends.append(user_friendship.to_user)

    print(users_friends)

    print(post.author)

    return render(request, 'post_detail.html', {'post': post, 'users_friend': users_friends, 'user': request.user})

@login_required
def post_create(request):

    # Garantir que o usuário esteja autenticado (decorador @login_required)
    # Se a requisição for GET, renderizar o formulário de criação de um post
    # Se a requisição for POST, processar os dados do formulário e criar um novo post associado ao usuário logado
    # Redirecionar para a página de detalhes do post, 'post_detail', após a criação bem-sucedida

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