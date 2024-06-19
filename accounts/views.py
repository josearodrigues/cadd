from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, \
                    update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re

from .forms import UsuarioForm
from sca.models import Users, Professor, Aluno
from cadd.models import Membro, Comissao, Convocacao, Reuniao, Perfil
from cadd.forms import PerfilForm
from cadd.utils import tipo_usuario, vida_academica, nome_sigla_curso, \
                    versao_curso

# Create your views here.

def usuario_registrar(request):
    """
    Função para o formulário de criação de usuários para o sistema
    """

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                # Pesquisa na tabela Users do SCA se o usuário é registrado
                usuario_login = Users.objects.using('sca').get(
                            login__iexact=request.POST.get('username')
                        )
                # Verifica se o usuário a ser criado é um professor ou um
                # usuário. Isto é necessário para saber o id do aluno ou o id
                # do professor nas consultas
                if 'Prof' in tipo_usuario(request.POST.get('username'), 0):
                    usuario = Professor.objects.using('sca').get(
                            matricula__iexact=request.POST.get('username')
                        )
                else:
                    usuario = Aluno.objects.using('sca').get(
                            matricula__iexact=request.POST.get('username')
                        )
                # Altera os campos necessários e salva o novo usuário
                u = form.save(commit=False)
                u.set_password(u.password)
                u.username = usuario_login.nome
                u.email = usuario_login.email
                u.save()
                # Cria o perfil do usuário (extensão de User)
                perfil = Perfil.objects.create(user=u, \
                        matricula=usuario.matricula, \
                        idusuario=usuario.id, itenspagina=5)

                messages.success(request, 'Usuário registrado com sucesso! ' + \
                        'Utilize o formulário abaixo para fazer login.')
                return redirect('accounts:usuario_login')
            except:
                messages.error(request, 'Usuário não cadastrado no sistema SCA!')
        else:
            # Verifica se o usuário a ser criado já existe na tabela User do
            # sistema (autenticação)
            if User.objects.filter(username=request.POST.get('username')):
                messages.error(request, 'Esta matrícula já está registrada!')
            # Verifica as críticas aos campos de senha
            if (request.POST.get('password') != request.POST.get('new_password1')):
                messages.error(request, 'As senhas digitadas são diferentes!')
            # Verificação do comprimento da senha com no mínimo 8 caracteres
            if len(request.POST.get('password')) < 8:
                messages.error(request,
                    'A senha não está com o comprimento mínimo de 8 caracteres!'
                )
            # Verificação de pelo menos 1 letra maiúscula
            if len(re.findall(r"[A-Z]", request.POST.get('password'))) < 1:
                messages.error(request,
                    'A senha deve possuir no mínimo 1 letra maiúscula!'
                )
            # Verificação de pelo menos 1 número
            if len(re.findall(r"[0-9]", request.POST.get('password'))) < 1:
                messages.error(request,
                    'A senha deve possuir no mínimo 1 número!'
                )
            # Verificação de pelo menos 1 caracter especial
#            if len(re.findall(r"[~`!@#$%^&*()_+=-{};:'><]",
#                        request.POST.get('password'))) < 1:
#                messages.error(request,
#                    'Senha tem que ter no mínimo 1 caracter especial'
#                )
    else:
        form = UsuarioForm()

    return render(request, 'accounts/registro.html', {'form': form})

def usuario_login(request):
    """
    Função para o formulário de entrada no sistema
    """

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = Perfil.objects.get(matricula=username)

        user = authenticate(username=usuario.user.username, password=password)
        if user is not None:
            if user.is_active:
                if Users.objects.using('sca').get(login__iexact=username):
                    login(request, user)
                    tipo = tipo_usuario(usuario.matricula, 0)
                    # Redirecione para a página inicial
                    return redirect(request.GET.get('next', '/'))
                else:
                    messages.error(request,
                            'Usuário não cadastrado ou senha inválida!'
                        )

            else:
                # Retorna uma mensagem de erro de 'conta desabilitada' .
                messages.error(request, 'Usuário desabilitado no sistema!')
        else:
            # Retorna uma mensagem de erro 'login inválido'.
            messages.error(request, 'Usuário não cadastrado ou senha inválida!')

    return render(request, 'accounts/login.html')

@login_required
def usuario_logout(request):
    """
    Função para a saída do sistema
    """

    logout(request)
    return redirect('accounts:usuario_login')

@login_required
def usuario_perfil(request):
    """
    Função para o formulário de troca de senha dos usuários do sistema
    """

    perfil = get_object_or_404(Perfil, user=request.user.id)
    if request.method == 'POST':
        # Formulário para a alteração da senha
        form = PasswordChangeForm(request.user, request.POST)
        # Formulário para a alteração da quantidade de linhas por página
        # da tabela Perfil
        form2 = PerfilForm(request.POST, instance=perfil)

        # Foi utilizada esta crítica abaixo para que não se misturasse as
        # mensagens de erro da alteração de senha e da alteração da
        # quantidade de linhas por página (por ser multiform)
        if form.is_valid():
            try:
                # Altera a nova senha
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('accounts:usuario_perfil')
            except:
                messages.error(request, 'Não foi possível alterar a sua senha!')

        elif form2.is_valid():
            try:
                outros = form2.save()
                messages.success(request, 'Parâmetro alterado com sucesso!')
                return redirect('accounts:usuario_perfil')
            except:
                messages.error(request, 'Não foi possível alterar o parãmetro!')

        elif not form.is_valid():
            # Verifica se o campo senha antiga está correto
            if not request.user.check_password(request.POST.get('old_password')):
                messages.error(request,
                        'A senha antiga digitada não é a correta!'
                    )
            # Verifica as críticas aos campos de senha
            if (request.POST.get('new_password1') !=
                    request.POST.get('new_password2')):
                messages.error(request,
                        'A nova senha e sua confirmação digitada são diferentes!'
                    )
            # Verificação do comprimento da senha com no mínimo 8 caracteres
            if len(request.POST.get('new_password1')) < 8:
                messages.error(request,
                    'A nova senha não está com o comprimento mínimo de 8 caracteres!'
                )
            # Verificação de pelo menos 1 letra maiúscula
            if len(re.findall(r"[A-Z]", request.POST.get('new_password1'))) < 1:
                messages.error(request,
                    'A nova senha deve possuir no mínimo 1 letra maiúscula!'
                )
            # Verificação de pelo menos 1 número
            if len(re.findall(r"[0-9]", request.POST.get('new_password1'))) < 1:
                messages.error(request,
                    'A nova senha deve possuir no mínimo 1 número!'
                )
            return redirect('accounts:usuario_perfil')

    else:
        form = PasswordChangeForm(request.user)
        form2 = PerfilForm(instance=perfil)

    return render(request, 'accounts/perfil.html', {
                        'form': form,
                        'form2': form2,
                    })

# Tela inicial
@login_required
def home(request):
    """
    Função de saída para a tela inicial do sistema
    """

    # Variáveis
    membro = ""
    comissoes = ""
    convocacao = ""
    reunioes = ""
    matricula = ""
    nomecurso = ""
    versaocurso = ""
    criticidade = ""
    periodos = ""
    reprovadas = ""
    trancamentos = ""
    cargaeletivas = ""
    totaleletivas = ""
    cargaatividades = ""
    totalatividades = ""

    usuario = Perfil.objects.get(user=request.user.id)
    # Verifica o tipo do usuário logado
    tipousuario = tipo_usuario(usuario.matricula,0)
    # Caso seja um professor
    if 'Prof' in tipousuario:
        membro = Membro.objects.filter(
                            professor=usuario.idusuario
                        ).exclude(ativo=0).values_list('comissao')
        if membro:
            comissoes = Comissao.objects.filter(id__in=membro)
        else:
            messages.error(request,
                    'Professor(a), o Sr(a) não está cadastrado(a) em nenhuma ' + \
                        'comissão de apoio!'
                )

    if 'Aluno' in tipousuario:
        convocacao = Convocacao.objects.filter(aluno=usuario.idusuario).values_list('reuniao')
        reunioes = Reuniao.objects.filter(id__in=convocacao)

        # processamento da vida acadêmica do aluno logado
        vidaacademica = vida_academica(usuario.idusuario)
        reprovadas = vidaacademica[3]
        # Verificação do nome do curso, versão, faixa de criticidade e periodos
        nomecurso = nome_sigla_curso(usuario.idusuario)[0]
        t_versaocurso = versao_curso(usuario.idusuario)
        versaocurso = t_versaocurso[0]
        totaleletivas = t_versaocurso[1]
        totalatividades = t_versaocurso[2]
        criticidade = vidaacademica[4]
        periodos = vidaacademica[7]
        trancamentos = vidaacademica[9]
        cargaeletivas = vidaacademica[10]
        # Convocação para alguma reunião
        if not convocacao:
            messages.error(request, 'Aluno(a), você não possui nenhuma reunião agendada!')

    return render(request, 'accounts/home.html', {
                    'home': home,
                    'ativoInicio': True,
                    'membro': membro,
                    'comissoes': comissoes,
                    'reunioes': reunioes,
                    'nomecurso': nomecurso,
                    'versaocurso': versaocurso,
                    'periodos': periodos,
                    'trancamentos': trancamentos,
                    'cargaeletivas': cargaeletivas,
                    'totaleletivas': totaleletivas,
                    'totalatividades': totalatividades,
                    'criticidade': criticidade,
                    'reprovadas': reprovadas,
                })
