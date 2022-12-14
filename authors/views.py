from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.base import SessionBase
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import RegisterForm, LoginForm


def register_view(request: HttpRequest) -> render:
    register_form_data: SessionBase = request.session.get('register_form_data',
                                                          None,
                                                          )
    form: RegisterForm = RegisterForm(register_form_data)

    return render(request, 'authors/pages/author.html', context={
        'form': form,
        'form_title': 'Register',
        'form_action': reverse('authors:register_create'),
    })


def register_create(request: HttpRequest) -> dict:
    if not request.POST:
        raise Http404()

    post: dict = request.POST
    request.session['register_form_data'] = post
    form: RegisterForm = RegisterForm(post)

    if form.is_valid():  # checa se o formulário é válido
        user: User = form.save(commit=False)  # captura os dados do form em um commit falso  # noqa: E501
        user.set_password(user.password)  # criptografa a senha
        user.save()  # salva na base de dados
        messages.success(request, 'Usuário criado com sucesso.')  # informa que o usuário foi criado  # noqa: E501

        del request.session['register_form_data']  # deleta os dados dos campos
        return redirect(reverse('authors:login'))  # direciona para a página de login  # noqa: E501

    return redirect('authors:register')


def login_view(request) -> render:
    form: LoginForm = LoginForm()

    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_title': 'Login',
        'form_action': reverse('authors:login_create'),
    })


def login_create(request) -> None:
    if not request.POST:
        raise Http404

    form: LoginForm = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Login realizado com sucesso')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return redirect('authors:login')


@login_required(redirect_field_name='next', login_url='authors:login')
def logout_view(request) -> None:
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)  # faz o logout
    messages.success(request, 'Logout realizado com sucesso')
    return redirect(reverse('authors:login'))  # redireciona para a página de login  # noqa: E501
