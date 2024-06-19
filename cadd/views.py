from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Paginação
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Models e Forms
from .forms import ParametrosForm, ComissaoForm, MembroForm, HorarioForm, \
                    ItemHorarioForm, AvaliaPlanoForm, ReuniaoForm, \
                    ConvocadoForm, DocumentoForm
from .models import Parametros, Comissao, Membro, Horario, ItemHorario, Plano, \
                    ItemPlanoAtual, PlanoFuturo, ItemPlanoFuturo, Reuniao, \
                    Convocacao, Documento, Perfil
from sca.models import Aluno, Disciplina, Itemhistoricoescolar, Versaocurso, \
                    Curso, Disciplinasoriginais, Blocoequivalencia, \
                    Disciplinasequivalentes, Curso

# Funções gerais
from .utils import max_creditos, min_creditos_preta, \
                    linhas_por_pagina, nome_sigla_curso, versao_curso, \
                    vida_academica, excluir_arquivo, periodo_atual, \
                    proximo_periodo

# Create your views here.

########################### Perfil Administrador ###############################
# Configurações do sistema
@login_required
def editar_parametros(request):
    """
    Função para a edição dos parâmetros do sistema
    """

    registros = Parametros.objects.filter(id=1).count()
    if request.method == 'POST':
        if registros != 0:
            parametros = get_object_or_404(Parametros, id=1)
            form = ParametrosForm(request.POST, instance=parametros)
        else:
            form = ParametrosForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Parâmetro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('home')
        else:
            # Verifica as críticas aos campos de reprovação
            if (request.POST.get('reprovacurso8periodosvermelha') <=
                    request.POST.get('reprovacurso8periodoslaranja')):
                messages.error(request,
                    "As reprovações da faixa vermelha para cursos com 8 ou " + \
                    "mais períodos devem ser maiores que as da faixa laranja!"
                )
            if (request.POST.get('reprovademaiscursosvermelha') <=
                    request.POST.get('reprovademaiscursoslaranja')):
                messages.error(request,
                    "As reprovações da faixa vermelha para os demais cursos " + \
                    "devem ser maiores que as da faixa laranja!"
                )
    else:
        if registros != 0:
            parametros = get_object_or_404(Parametros, id=1)
            form = ParametrosForm(instance=parametros)
        else:
            form = ParametrosForm()

    return render(request, 'cadd/configuracoes.html', {
                        'form': form,
                        'ativoConfiguracoes': True
                    })


# Comissões de apoio
@login_required
def nova_comissao(request):
    """
    Função para a criação de uma nova comissão de apoio
    """

    if request.method == 'POST':
        form = ComissaoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Comissão salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_comissoes')
        else:
            messages.error(request, 'A comissão para um curso é unica, ' + \
                        'utilize-se de outro curso para cadastro!')
    else:
        form = ComissaoForm()

    return render(request, 'cadd/nova_comissao.html', {
                        'form': form,
                        'ativoComissoes': True
                    })

@login_required
def lista_comissoes(request):
    """
    Função para a listagem das comissões de apoio cadastradas
    """

    usuario = Perfil.objects.get(user=request.user.id)
    # Paginação
    linhas = linhas_por_pagina(usuario.idusuario)
    # Verifica se há membros em uma Comissão, desabilitando o botão de exclusão
    comissoes_list = list(Comissao.comissoes_membros_sql())
    paginator = Paginator(comissoes_list, linhas)
    page = request.GET.get('page')
    comissoes = paginator.get_page(page)

    return render(request, 'cadd/lista_comissoes.html', {
                        'comissoes': comissoes,
                        'ativoComissoes': True,
                        'copiabotoes': len(comissoes_list) >= 10 and linhas >= 10
                    })

@login_required
def excluir_comissao(request, id_comissao):
    """
    Função para a exclusão de uma comissão de apoio
    """

    comissao = Comissao.objects.get(id=id_comissao)
    try:
        comissao.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'A exclusão não foi realizada! Para isso, ' + \
                        'exclua primeiramente seus membros.')

    return redirect('cadd:lista_comissoes')

@login_required
def editar_comissao(request, id_comissao):
    """
    Função para a edição de uma comissão de apoio
    """

    comissao = get_object_or_404(Comissao, id=id_comissao)
    if request.method == 'POST':
        form = ComissaoForm(request.POST, instance=comissao)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Comissão salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_comissoes')
    else:
        form = ComissaoForm(instance=comissao)

    return render(request, 'cadd/nova_comissao.html', {
                        'form': form,
                        'ativoComissoes': True
                    })


# Membros das Comissões de apoio
@login_required
def novo_membro(request, id_comissao):
    """
    Função para a criação de uma novo membro de uma comissão de apoio
    """

    if request.method == 'POST':
        form = MembroForm(request.POST)
        if form.is_valid():
            comissao = Comissao.objects.get(id=id_comissao)
            f = form.save(commit=False)
            f.comissao = comissao
            f.ativo = True
            try:
                form.save()
                messages.success(request, 'Membro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_membros', id_comissao)
    else:
        form = MembroForm()

    return render(request, 'cadd/novo_membro.html', {
                        'form': form,
                        'id_comissao': id_comissao,
                        'ativoComissoes': True
                    })

@login_required
def lista_membros(request, id_comissao):
    """
    Função para a listagem dos membros cadastrados de uma comissões de apoio
    """

    usuario = Perfil.objects.get(user=request.user.id)
    linhas = linhas_por_pagina(usuario.idusuario)
    membros_list = Membro.objects.all().filter(comissao=id_comissao)
    paginator = Paginator(membros_list, linhas) # Paginação
    page = request.GET.get('page')
    membros = paginator.get_page(page)
    # objeto comissão anteriormente requisitado
    comissao = Comissao.objects.get(id__exact=id_comissao)

    return render(request, 'cadd/lista_membros.html', {
                        'membros': membros,
                        'id_comissao': id_comissao,
                        'comissao': comissao,
                        'ativoComissoes': True,
                        'copiabotoes': membros_list.count() >= 10 and linhas >= 10
                    })

@login_required
def excluir_membro(request, id_membro, id_comissao):
    """
    Função para a desativação de um membro de uma comissão de apoio
    """

    membro = Membro.objects.get(id=id_membro)
    membro.ativo = False
    try:
        membro.save()
        messages.success(request, 'Membro desativado com sucesso!')
    except:
        messages.error(request, 'Houve algum problema técnico e o ' + \
                'desativamento não foi realizado!')

    return redirect('cadd:lista_membros', id_comissao)

@login_required
def editar_membro(request, id_membro, id_comissao):
    """
    Função para a edição de um membro de uma comissão de apoio
    """

    membro = get_object_or_404(Membro, id=id_membro)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Membro salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_membros', id_comissao)
    else:
        form = MembroForm(instance=membro)

    return render(request, 'cadd/novo_membro.html', {
                        'form': form,
                        'id_comissao': id_comissao,
                        'ativoComissoes': True
                    })


########################### Perfil Membro da CADD ##############################
# Reuniões
@login_required
def nova_reuniao(request):
    """
    Função para a criação de uma nova reuniao
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, professor=professor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reunião salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_reunioes')
    else:
        form = ReuniaoForm(professor=professor)

    return render(request, 'cadd/nova_reuniao.html', {
                        'form': form,
                        'ativoReunioes': True
                    })


@login_required
def lista_reunioes(request):
    """
    Função para a listagem das reuniões agendadas
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    linhas = linhas_por_pagina(professor)
    membro = Membro.objects.filter(
                            professor=professor
                        ).exclude(ativo=0).values_list('comissao')
    comissao = Comissao.objects.filter(id__in=membro)
    reunioes_list = Reuniao.objects.filter(comissao__in=comissao)
    paginator = Paginator(reunioes_list, linhas) # Paginação
    page = request.GET.get('page')
    reunioes = paginator.get_page(page)

    return render(request, 'cadd/lista_reunioes.html', {
                        'reunioes': reunioes,
                        'ativoReunioes': True,
                        'copiabotoes': reunioes_list.count() >= 10 and linhas >= 10
                    })

@login_required
def excluir_reuniao(request, id_reuniao):
    """
    Função para o cancelamento de uma reunião
    """

    reuniao = Reuniao.objects.get(id=id_reuniao)
    reuniao.situacao = 'C'
    try:
        reuniao.save()
        messages.success(request, 'Reunião cancelada com sucesso!')
    except:
        messages.error(request, 'Houve algum problema técnico e o ' + \
                    'cancelamento não foi realizado!')

    return redirect('cadd:lista_reunioes')

@login_required
def editar_reuniao(request, id_reuniao):
    """
    Função para a edição de uma reunião
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    reuniao = get_object_or_404(Reuniao, id=id_reuniao)
    if request.method == 'POST':
        form = ReuniaoForm(request.POST, instance=reuniao, professor=professor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Reunião salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_reunioes')
    else:
        form = ReuniaoForm(instance=reuniao, professor=professor)

    return render(request, 'cadd/nova_reuniao.html', {
                        'form': form,
                        'ativoReunioes': True
                    })


# Convocados às reuniões
@login_required
def novo_convocado(request, id_reuniao):
    """
    Função para a cadastro de um convocado para uma reunião específica
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    if request.method == 'POST':
        form = ConvocadoForm(request.POST, professor=professor)
        if form.is_valid():
            reuniao = Reuniao.objects.get(id=id_reuniao)
            f = form.save(commit=False)
            f.reuniao = reuniao
            f.envioemail = False
            f.presente = False
            try:
                f.save()
                messages.success(request, 'Convocado salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_convocados', id_reuniao)
    else:
        form = ConvocadoForm(professor=professor)

    return render(request, 'cadd/novo_convocado.html', {
                        'form': form,
                        'id_reuniao': id_reuniao,
                        'ativoReunioes': True
                    })

@login_required
def lista_convocados(request, id_reuniao):
    """
    Função para a listagem dos convidados para uma reunião específica
    """

    usuario = Perfil.objects.get(user=request.user.id)
    # Paginação
    linhas = linhas_por_pagina(usuario.idusuario)
    convocados_list = Convocacao.objects.filter(reuniao=id_reuniao)
    paginator = Paginator(convocados_list, linhas)
    page = request.GET.get('page')
    convocados = paginator.get_page(page)
    # objeto reunião anteriormente requisitado
    reuniao = Reuniao.objects.get(id__exact=id_reuniao)

    return render(request, 'cadd/lista_convocados.html', {
                        'convocados': convocados,
                        'id_reuniao': id_reuniao,
                        'reuniao': reuniao,
                        'ativoReunioes': True,
                        'copiabotoes': convocados_list.count() >= 10 and linhas >= 10
                    })

@login_required
def excluir_convocado(request, id_convocado, id_reuniao):
    """
    Função para a exclusão de um convocado de uma reunião específica
    """

    convocado = Convocacao.objects.get(id=id_convocado)
    try:
        convocado.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão ' + \
                        'não foi realizada!')

    return redirect('cadd:lista_convocados', id_reuniao)

@login_required
def editar_convocado(request, id_convocado, id_reuniao):
    """
    Função para a edição de um convocado para uma reuniao específica
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    convocado = get_object_or_404(Convocacao, id=id_convocado)
    if request.method == 'POST':
        form = ConvocadoForm(request.POST, instance=convocado, professor=professor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Convocado salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_convocados', id_reuniao)
    else:
        form = ConvocadoForm(instance=convocado, professor=professor)

    return render(request, 'cadd/novo_convocado.html', {
                        'form': form,
                        'id_reuniao': id_reuniao,
                        'ativoReunioes': True
                    })


# Horários
@login_required
def novo_horario(request):
    """
    Função para a criação de uma nova previsão de horário
    """

    # O comando abaixo foi retirado pois filtrava o horário conforme o próximo
    # período atual, devido à prévia do horário nem sempre sair antes do término
    # de um período
#    proxPeriodo = proximo_periodo(1)
    professor = Perfil.objects.get(user=request.user.id).idusuario
    if request.method == 'POST':
        form = HorarioForm(request.POST, professor=professor)
        if form.is_valid():
            # Idem explicação acima
#            f = form.save(commit=False)
#            f.ano = proxPeriodo[0]
#            f.periodo = proxPeriodo[1]
            try:
                form.save()
                messages.success(request, 'Horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_horarios')
    else:
        form = HorarioForm(professor=professor)

    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })

@login_required
def lista_horarios(request):
    """
    Função para a listagem das previsões de horário
    """

    # Retirada a restrição do semestre subsequente
#    proxPeriodo = proximo_periodo(1)
    professor = Perfil.objects.get(user=request.user.id).idusuario
    # Paginação
    linhas = linhas_por_pagina(professor)
    membro = Membro.objects.filter(
                        professor=professor
                    ).exclude(ativo=0).values_list('comissao')
    comissoes = Comissao.objects.filter(id__in=membro).values_list('curso')
    # Idem explicação acima
#    horarios_list = Horario.objects.filter(
#                        curso__in=comissoes, ano=proxPeriodo[0], \
#                        periodo=proxPeriodo[1])
    horarios_list = Horario.objects.filter(
                        curso__in=comissoes
                    ).order_by('ano', 'periodo')
    paginator = Paginator(horarios_list, linhas)
    page = request.GET.get('page')
    horarios = paginator.get_page(page)

    return render(request, 'cadd/lista_horarios.html', {
                        'horarios': horarios,
                        'ativoHorarios': True,
                        'copiabotoes': horarios_list.count() >= 10 and linhas >= 10
                    })


@login_required
def excluir_horario(request, id_horario):
    """
    Função para a exclusão de uma previsão de horário
    """

    horario = Horario.objects.get(id=id_horario)
    try:
        horario.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'A exclusão não foi realizada! Para isso, ' + \
                        'exclua primeiramente seus itens de horário.')

    return redirect('cadd:lista_horarios')

@login_required
def editar_horario(request, id_horario):
    """
    Função para a edição de uma previsão de horário
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    horario = get_object_or_404(Horario, id=id_horario)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario, professor=professor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_horarios')
    else:
        form = HorarioForm(instance=horario, professor=professor)

    return render(request, 'cadd/novo_horario.html', {
                        'form': form,
                        'ativoHorarios': True
                    })


# Itens de Horário
@login_required
def novo_itemhorario(request, id_horario):
    """
    Função para a criação de uma novo item em uma previsão de horário
    """

    if request.method == 'POST':
        form = ItemHorarioForm(request.POST)
        if form.is_valid():
            horario = Horario.objects.get(id=id_horario)
            f = form.save(commit=False)
            f.horario = horario
            try:
                f.save()
                messages.success(request, 'Item de horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm()

    return render(request, 'cadd/novo_itemhorario.html', {
                        'form': form,
                        'id_horario': id_horario,
                        'ativoHorarios': True
                    })

@login_required
def lista_itenshorario(request, id_horario):
    """
    Função para a listagem dos itens cadastrados em uma previsão de horário
    """

    usuario = Perfil.objects.get(user=request.user.id)
    # Paginação
    linhas = linhas_por_pagina(usuario.idusuario)
    itenshorario_list = ItemHorario.objects.filter(
                        horario=id_horario
                    ).order_by('periodo', 'id')
    paginator = Paginator(itenshorario_list, linhas)
    page = request.GET.get('page')
    itenshorario = paginator.get_page(page)
    # objeto horário anteriormente requisitado
    horario = Horario.objects.get(id__exact=id_horario)

    return render(request, 'cadd/lista_itenshorario.html', {
                        'itenshorario': itenshorario,
                        'id_horario': id_horario,
                        'horario': horario,
                        'ativoHorarios': True,
                        'copiabotoes': itenshorario_list.count() >= 10 and linhas >= 10
                    })

@login_required
def excluir_itemhorario(request, id_itemhorario, id_horario):
    """
    Função para a exclusão de um item de uma previsão de horário
    """

    itemhorario = ItemHorario.objects.get(id=id_itemhorario)
    try:
        itemhorario.delete()
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão ' + \
                        'não foi realizada!')

    return redirect('cadd:lista_itenshorario', id_horario)

@login_required
def editar_itemhorario(request, id_itemhorario, id_horario):
    """
    Função para a edição de item de uma previsão de horário
    """

    itemhorario = get_object_or_404(ItemHorario, id=id_itemhorario)
    if request.method == 'POST':
        form = ItemHorarioForm(request.POST, instance=itemhorario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Item de horário salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_itenshorario', id_horario)
    else:
        form = ItemHorarioForm(instance=itemhorario)

    return render(request, 'cadd/novo_itemhorario.html', {
                        'form': form,
                        'id_horario': id_horario,
                        'ativoHorarios': True
                    })


# Avaliação dos Planos de Estudo cadastrados
@login_required
def lista_planos_avaliar(request):
    """
    Função para a listagem dos alunos e seus planos de estudo cadastrados
    """

    usuario = Perfil.objects.get(user=request.user.id)
    periodoAtual = periodo_atual()
    proxperiodo = proximo_periodo(1)

    membro = Membro.objects.filter(
                                professor=usuario.idusuario, ativo=1
                            ).values_list('comissao', flat=True)
    # Para saber as comissões que o membro logado faz parte
    comissoes = list(Comissao.objects.filter(
                                id__in=membro
                            ).values_list('curso', flat=True))
    # Para saber os cursos que o membro logado pode atuar
    cursos = Curso.objects.using('sca').filter(
                                id__in=comissoes
                            ).values_list('id', flat=True)
    # Para saber as versões de cursos que o membro logado pode atuar
    versoes = Versaocurso.objects.using('sca').filter(curso__in=cursos)
    # Para saber os alunos que ainda estão cursando
    itens = Itemhistoricoescolar.objects.using('sca').filter(
                                ano=periodoAtual[0], periodo=periodoAtual[1] - 1
                            ).values_list('historico_escolar', flat=True)
    # Para saber os alunos cujo plano de estudos encontra-se cadastrado e em
    # situação 'Montado' para o próximo semestre
    planos = list(Plano.objects.using('default').filter(ano=proxperiodo[0],
                                periodo=proxperiodo[1], situacao='M'
                            ).values_list('aluno', flat=True))
    # Dados dos alunos com a junção das informações selecionadas
    alunos = Aluno.objects.using('sca').filter(historico__in=itens,
                                versaocurso__in=versoes, id__in=planos
                            ).order_by('nome')

    return render(request, 'cadd/lista_plano_estudos_avaliar.html', {
                        'ativoPlanos': True,
                        'alunos': alunos,
                    })

@login_required
def avalia_plano(request, id_aluno):
    """
    Função para a avaliação do plano de estudos dos alunos pelos membros
    das comissões
    """

    # Variáveis
    versaocurso = ""
    criticidade = ""
    periodos = ""
    trancamentos = ""
    cargaeletivas = ""
    reprovadas = ""
    planoAtual = ""
    itensAtual = ""
    planosFuturos = ""
    itensFuturos = ""
    avaliacao = ""
    # Processamento da vida acadêmica do aluno logado e obtidos o nome do aluno,
    # versão do curso, faixa de criticidade, periodos, disciplinas reprovadas
    vidaacademica = vida_academica(id_aluno)
    aluno = vidaacademica[8]
    criticidade = vidaacademica[4]
    periodos = vidaacademica[7]
    reprovadas = vidaacademica[3]
    versaocurso = versao_curso(id_aluno)
    trancamentos = vidaacademica[9]
    cargaeletivas = vidaacademica[10]
    proxperiodo = proximo_periodo(1)

    # Planos atual e futuro para visualização
    try:
        planoAtual = Plano.objects.get(aluno=id_aluno, ano=proxperiodo[0],
                        periodo=proxperiodo[1])
        if planoAtual:
            itensAtual = ItemPlanoAtual.objects.filter(plano=planoAtual)
            planosFuturos = PlanoFuturo.objects.filter(plano=planoAtual)
        if planosFuturos:
            itensFuturos = ItemPlanoFuturo.objects.filter(
                        planofuturo__in=planosFuturos)
    except:
        pass

    if planoAtual.avaliacao:
        avaliacao = planoAtual.avaliacao

    if request.method == 'POST':
        t_avaliacao = request.POST.get('avaliacao')
        if t_avaliacao:
            planoAtual.avaliacao = t_avaliacao
            planoAtual.situacao = 'A'
            try:
                planoAtual.save()
                messages.success(request, 'Avaliação salva com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')

    return render(request, 'cadd/avalia_plano_estudos.html', {
                        'aluno': aluno,
                        'versaocurso': versaocurso[0],
                        'periodos': periodos,
                        'trancamentos': trancamentos,
                        'cargaeletivas': cargaeletivas,
                        'totaleletivas': versaocurso[1],
                        'totalatividades': versaocurso[2],
                        'criticidade': criticidade,
                        'reprovadas': reprovadas,
                        'planoAtual': planoAtual,
                        'itensAtual': itensAtual,
                        'planosFuturos': planosFuturos,
                        'itensFuturos': itensFuturos,
                        'avaliacao': avaliacao,
                        'id_aluno': id_aluno,
                    })


# Documentos
@login_required
def novo_documento(request):
    """
    Função para o cadastro de um novo documento
    """

    professor = Perfil.objects.get(user=request.user.id).idusuario
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, professor=professor)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Documento salvo com sucesso!')
            except:
                messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            return redirect('cadd:lista_documentos')
    else:
        form = DocumentoForm(professor=professor)

    return render(request, 'cadd/novo_documento.html', {
                        'form': form,
                        'ativoDocumentos': True
                    })

@login_required
def lista_documentos(request):
    """
    Função para a listagem dos documentos cadastrados
    """

    usuario = Perfil.objects.get(user=request.user.id)
    # Paginação
    linhas = linhas_por_pagina(usuario.idusuario)
    documentos_list = Documento.objects.all()
    paginator = Paginator(documentos_list, linhas)
    page = request.GET.get('page')
    documentos = paginator.get_page(page)

    return render(request, 'cadd/lista_documentos.html', {
                        'documentos': documentos,
                        'ativoDocumentos': True,
                        'copiabotoes': documentos_list.count() >= 10 and linhas >= 10
                    })

@login_required
def excluir_documento(request, id_documento):
    """
    Função para a exclusão de um documento
    """

    documento = Documento.objects.get(id=id_documento)
    try:
        documento.delete()
        excluir_arquivo(documento.indice)
        messages.success(request, 'A exclusão foi realizada!')
    except:
        messages.error(request, 'Houve algum problema técnico e a exclusão ' + \
                'não foi realizada!')

    return redirect('cadd:lista_documentos')


# Relatórios
@login_required
def relatorio_situacao(request):

    return render(request, 'cadd/relatorio_situacao.html', {
                        'ativoRelatorios': True
                    })

@login_required
def relatorio_conflitos(request):

    return render(request, 'cadd/relatorio_conflitos.html', {
                        'ativoRelatorios': True
                    })

@login_required
def relatorio_ata(request):

    return render(request, 'cadd/relatorio_ata.html', {
                        'ativoRelatorios': True
                    })

@login_required
def relatorio_atendimentos(request):

    return render(request, 'cadd/relatorio_atendimentos.html', {
                        'ativoRelatorios': True
                    })

@login_required
def relatorio_ausencia(request):

    return render(request, 'cadd/relatorio_ausencia.html', {
                        'ativoRelatorios': True
                    })

@login_required
def relatorio_excepcionais(request):

    return render(request, 'cadd/relatorio_excepcionais.html', {
                        'ativoRelatorios': True
                    })


############################## Perfil Aluno ###################################
#Planos de estudo
@login_required
def lista_planos(request):
    """
    Função para a listagem dos planos de estudo cadastrados
    """

    planoAtual = ""
    itensAtual = ""
    planosFuturos = ""
    itensFuturos = ""
    avaliacao = ""

    proxPeriodo = proximo_periodo(1)
    usuario = Perfil.objects.get(user=request.user.id)
    try:
        planoAtual = Plano.objects.get(aluno=usuario.idusuario,
                        ano=proxPeriodo[0], periodo=proxPeriodo[1]
                    )
        if planoAtual:
            avaliacao = planoAtual.avaliacao
            itensAtual = ItemPlanoAtual.objects.filter(plano=planoAtual)
            planosFuturos = PlanoFuturo.objects.filter(plano=planoAtual)
        if planosFuturos:
            itensFuturos = ItemPlanoFuturo.objects.filter(
                        planofuturo__in=planosFuturos
                    )
    except:
        pass

    return render(request, 'cadd/lista_plano_estudos.html', {
                        'ativoPlanos': True,
                        'planoAtual': planoAtual,
                        'itensAtual': itensAtual,
                        'planosFuturos': planosFuturos,
                        'itensFuturos': itensFuturos,
                        'avaliacao': avaliacao,
                    })

@login_required
def novo_plano_previa(request):
    """
    Função para a criação de um novo plano de estudos para o
    próximo semestre

    TODO: Falta verificar os pré-requisitos na ajuda à criação do plano
    """

    prerequisitos = ''

    usuario = Perfil.objects.get(user=request.user.id)
    periodoAtual = periodo_atual()
    proxPeriodo = proximo_periodo(1)
    # processamento da vida acadêmica do aluno logado
    vidaacademica = vida_academica(usuario.idusuario)
    # Verificação do nome do curso, versão do curso e faixa de criticidade
    curso = nome_sigla_curso(usuario.idusuario)
    nomecurso = curso[0]
    versaocurso = versao_curso(usuario.idusuario)
    criticidade = vidaacademica[4]
    maxcreditos = vidaacademica[6]
    periodos = vidaacademica[7]
    continua = False

    # Prévias e afins
    horario = Horario.objects.filter(ano=proxPeriodo[0], periodo=proxPeriodo[1],
                            curso=curso[2]
                        )
    previas = list(ItemHorario.objects.filter(
                            horario__in=horario).values_list(
                            'disciplina', flat=True).exclude(
                            disciplina__in=vidaacademica[0])
                        )
    # Ordenação do resultado
    previas.sort()
    podeLecionar = ItemHorario.objects.filter(
                            disciplina__in=previas
                        ).order_by('diasemana', 'periodo')

    aluno = Aluno.objects.get(id=usuario.idusuario)

    plano = Plano.objects.filter(ano=proxPeriodo[0], periodo=proxPeriodo[1],
                            aluno=aluno
                        )
    if plano:
        continua = True
#        itenst = ItemPlanoAtual.objects.filter(plano=planot).values_list('id')

    if request.method == 'POST':
        disciplinas = request.POST.get('discip')
        if disciplinas:
            disciplinas = disciplinas.split("_")
            if continua:
                try:
                    plano = get_object_or_404(Plano, ano=proxPeriodo[0],
                            periodo=proxPeriodo[1], aluno=aluno
                        )
                    plano.situacao = 'M'
                    plano.avaliacao = ''
                    plano.save()
                    messages.success(request, 'Plano Atual salvo com sucesso!')
                except:
                    messages.error(request, 'Houve algum problema técnico e o ' + \
                        'salvamento não foi realizado!')
            else:
                try:
                    plano = Plano.objects.create(ano=proxPeriodo[0],
                            periodo=proxPeriodo[1], situacao='M', aluno=aluno
                        )
                    messages.success(request, 'Plano Atual criado com sucesso!')
                except:
                    messages.error(request, 'Houve algum problema técnico e a ' + \
                        'criação do plano não foi realizada!')
            for d in disciplinas:
                disc = int(d)
                itemhorario = ItemHorario.objects.get(id=disc)
                i = ItemPlanoAtual.objects.create(
                    plano=plano, itemhorario=itemhorario
                )
    # Realizada novamente a conferência quando da criação de um novo plano
    if plano:
        continua = True

    return render(request, 'cadd/novo_plano_estudos_atual.html', {
                        'ativoPlanos': True,
                        'ativoPlanos2': True,
                        'podeLecionar': podeLecionar,
                        'criticidade': criticidade,
                        'maxcreditos': maxcreditos,
                        'nomecurso': nomecurso,
                        'versaocurso': versaocurso[0],
                        'periodos': periodos,
                        'continua': continua,
                    })

@login_required
def novo_plano_futuro(request):
    """
    Função para a criação de um novo plano de estudos para os
    semestres subsequentes

    TODO: Falta ver as disciplinas da prévia e seus equivalentes
    """

    prerequisitos = ''

    usuario = Perfil.objects.get(user=request.user.id)
    # processamento da vida acadêmica do aluno logado
    vidaacademica = vida_academica(usuario.idusuario)
    # Verificação do nome do curso, versão do curso e faixa de criticidade
    versaocurso = versao_curso(usuario.idusuario)
    criticidade = vidaacademica[4]
    maxcreditos = vidaacademica[6]
    periodos = vidaacademica[7]
    proxPeriodo = proximo_periodo(1)
    plano = get_object_or_404(Plano, ano=proxPeriodo[0], periodo=proxPeriodo[1],
                            aluno=usuario.idusuario
                        )

    # Prévias e afins
    aluno = Aluno.objects.using('sca').get(nome__exact=request.user.username)
    aprovadas = vidaacademica[0]
    aLecionar = Disciplina.objects.using('sca').exclude(id__in=aprovadas).filter(
                            versaocurso=aluno.versaocurso
                        ).order_by('optativa', 'departamento')

    # Criação dos planos futuros conforme inclusão do aluno
    listaperiodos = [proximo_periodo(x + 2) for x in range(6)]

    if request.method == 'POST':
        disciplinas = request.POST.get('discip')
        if disciplinas:
            disciplinas = disciplinas.split("_")
            for d in disciplinas:
                ano = d[0:4]
                periodo = d[5:6]
                disc = d[7:]
                disciplina = Disciplina.objects.using('sca').get(id=disc)
                try:
                    planofuturo = PlanoFuturo.objects.get(
                            ano=ano, periodo=periodo, plano=plano
                        )
                except:
                    planofuturo = PlanoFuturo.objects.create(
                            ano=ano, periodo=periodo, plano=plano
                        )
                i = ItemPlanoFuturo.objects.create(
                            planofuturo=planofuturo, disciplina=disciplina
                        )

            return redirect('cadd:lista_planos')

    return render(request, 'cadd/novo_plano_estudos_futuro.html', {
                        'ativoPlanos': True,
                        'ativoPlanos3': True,
                        'aLecionar': aLecionar,
                        'plano': plano,
                        'listaperiodos': listaperiodos,
                    })
