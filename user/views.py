from django.shortcuts import redirect, render 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from blog.models import Post

def register(request):

    # Se a requisição for GET, renderizar o formulário de registro
    # Se a requisição for POST, processar os dados do formulário e criar um novo usuário.
    # Verificar se as senhas coincidem e, em caso afirmativo, criar o usuário e redirecionar 
    # para a página de login. Caso contrário, redirecionar de volta para o formulário de registro.
    # Verificar se o nome de usuário já existe e, em caso afirmativo, redirecionar de volta para o formulário de registro.
    # Se o registro for bem-sucedido, redirecionar para a página de login.

    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return redirect('register.html')
        
        try:
            user = User.objects.create_user(
                first_name = first_name,
                username = username,
                email = email,
                password = password,
           )
        except:
            return redirect('register.html')
        return redirect('login.html')


def login_view(request):

    # Se a requisição for GET, renderizar o formulário de login
    # Se a requisição for POST, processar os dados do formulário e autenticar o usuário.
    # Se a autenticação for bem-sucedida, fazer login do usuário e redirecionar para a página de listagem de posts. 
    # Caso contrário, redirecionar de volta para o formulário de login.

    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('posts_list')
        else:
            return render(request, 'login.html')


def logout_view(request):
    
    # Fazer logout do usuário e redirecionar para a página de login ou para a página inicial.
    
    logout(request)
    return render(request, 'login.html')

@login_required
def profile(request, pk):

    # Renderizar a página de perfil do usuário, exibindo as informações do usuário e seus posts.
    # Garantir que o usuário esteja autenticado (decorador @login_required) antes de acessar esta página.
    
    posts = Post.objects.filter(author_id=pk)
    user =  User.objects.get(id=pk)

    return render(request, 'profile.html', {'posts': posts, 'user': user})  
