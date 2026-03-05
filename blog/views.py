from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment

def LikePost(request, pk):
    
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
