from datetime import datetime
import os

from .models import Parametros, Perfil
from sca.models import Users, UserProfile, Useruserprofile, Aluno, Curso, \
                    Itemhistoricoescolar, Disciplinasoriginais, \
                    Blocoequivalencia, Disciplinasequivalentes, Versaocurso

# Funções úteis
# Função para se saber o tipo do usuário logado
def tipo_usuario(matricula, registro):
    """
    Função que retorna o tipo de usuário por meio da ROLE do SCA e
    usuário logado
    """

    # Pesquisa na tabela de usuários do SCA o usuário a ser registrado
    usuario = Users.objects.using('sca').get(login__iexact=matricula)
    # Caso seja realizado um get na tabela N:N o resultado já sai para a tabela
    # apropriada. Nesse caso, necessitou saber quais são as ids das roles do SCA
    idProfProfile = UserProfile.objects.using('sca').get(
                        type__iexact='ROLE_PROFESSOR'
                    )
    idAlunoProfile = UserProfile.objects.using('sca').get(
                        type__iexact='ROLE_ALUNO'
                    )
    idAdminProfile = UserProfile.objects.using('sca').get(
                        type__iexact='ROLE_SECAD'
                    )
    # Caso seu perfil no SCA seja de role SECAD e não seja para registro...
    if registro == 0:
        if Useruserprofile.objects.using('sca').filter(
                        user=usuario, userprofile=idAdminProfile
                    ).exists():
            return 'Admin'
    # Caso seu perfil no SCA seja de role Professor
    if Useruserprofile.objects.using('sca').filter(
                        user=usuario, userprofile=idProfProfile
                    ).exists():
        return 'Prof'
    # Caso seu perfil no SCA seja de role Aluno
    if Useruserprofile.objects.using('sca').filter(
                        user=usuario, userprofile=idAlunoProfile
                    ).exists():
        return 'Aluno'

    return ''

# Funções para valores de parâmetros
def reprovacoes_faixa_laranja_cursos_8_periodos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de 8 períodos ou mais para que esteja na
    faixa de criticidade laranja
    """

    reprovacoes = 2
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        reprovacoes = registros.reprovacurso8periodoslaranja

    return reprovacoes

def reprovacoes_faixa_vermelha_cursos_8_periodos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de 8 períodos ou mais para que esteja na
    faixa de criticidade vermelha
    """

    reprovacoes = 3
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        reprovacoes = registros.reprovacurso8periodosvermelha

    return reprovacoes

def reprovacoes_faixa_laranja_demais_cursos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de menos de 8 períodos para que esteja na
    faixa de criticidade laranja
    """

    reprovacoes = 1
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        reprovacoes = registros.reprovademaiscursoslaranja

    return reprovacoes

def reprovacoes_faixa_vermelha_demais_cursos():
    """
    Função que retorna a quantidade de reprovações em uma mesma disciplina
    de um aluno em um curso de menos de 8 períodos para que esteja na
    faixa de criticidade vermelha
    """

    reprovacoes = 2
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        reprovacoes = registros.reprovademaiscursosvermelha

    return reprovacoes

def formula_inicial_faixa_laranja():
    """
    Função que retorna a fórmula do valor inicial para cálculo das
    integralizações dos cursos para que esteja na faixa de
    criticidade laranja
    """

    formula = '2 * N'
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        formula = registros.qtdperiodosiniciallaranja

    return formula

def formula_final_faixa_laranja():
    """
    Função que retorna a fórmula do valor final para cálculo das
    integralizações dos cursos para que esteja na faixa de
    criticidade laranja
    """

    formula = '2 * N'
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        formula = registros.qtdperiodosfinallaranja

    return formula

def formula_faixa_vermelha():
    """
    Função que retorna a fórmula para cálculo das integralizações dos
    cursos para que esteja na faixa de criticidade vermelha
    """

    formula = '4 * N - 3'
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        formula = registros.qtdperiodosvermelha

    return formula

def min_creditos_preta():
    """
    Função que retorna a quantidade mínima de créditos por semana para um
    aluno que esteja na faixa de criticidade preta
    """

    creditos = 20
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        creditos = registros.mincreditosporperiodopreta

    return creditos

def max_creditos():
    """
    Função que retorna a quantidade máxima de créditos por semana para
    qualquer aluno
    """

    creditos = 28
    registros = Parametros.objects.get(pk=1)
    if registros != 0:
        creditos = registros.maxcreditosporperiodo

    return creditos

def linhas_por_pagina(id_usuario):
    """
    Função que retorna a quantidade de linhas por página cadastrada na
    tabela perfil do usuário
    """

    linhas = 5
    registros = Perfil.objects.get(idusuario=id_usuario)
    if registros != 0:
        linhas = registros.itenspagina

    return linhas

# Funções gerais
def periodo_atual():
    """
    Função que retorna o ano e período atual
    """

    agora = datetime.now()
    ano = agora.year
    mes = agora.month
    # Mês de início das aulas do semestre
    if mes in [2, 3, 4, 5, 6, 7]:
        periodo = 1
    else:
        periodo = 2
    retorno = ano, periodo, str(ano) + "." + str(periodo)

    return retorno

def proximo_periodo(periodos):
    """
    Função que retorna o ano e periodo conforme a quantidade de semestres
    selecionados
    """

    temp = periodo_atual()
    ano = temp[0]
    tperiodos = temp[1] + periodos
    if tperiodos % 2 == 0:
        periodo = 2
        ano = ano + (tperiodos // 2) - 1
    else:
        periodo = 1
        ano = ano + (tperiodos // 2)
    retorno = ano, periodo,  str(ano) + "." + str(periodo)

    return retorno

def versao_curso(id_aluno):
    """
    Função que retorna a versão do curso do aluno logado
    """

    aluno = Aluno.objects.using('sca').get(id=id_aluno)
    versaocurso = aluno.versaocurso.numero
    cargahorariaoptativas = aluno.versaocurso.cargahorariaoptativas
    cargahorariaativcomp = aluno.versaocurso.cargahorariaativcomp
    retorno = versaocurso, cargahorariaoptativas, cargahorariaativcomp

    return retorno

def nome_sigla_curso(id_aluno):
    """
    Função que retorna o nome do curso do aluno logado
    """

    aluno = Aluno.objects.using('sca').get(id=id_aluno)
    t_curso = Curso.objects.using('sca').get(id=aluno.versaocurso.curso.id)
    nomecurso = t_curso.nome + " (" + t_curso.sigla + ")"
    retorno = nomecurso, t_curso.sigla, t_curso.id

    return retorno

def excluir_arquivo(documento):
    """
    Função que exclui o documento cadastrado e enviado para a pasta de
    mídias de documentos do projeto
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    try:
        os.remove('{}/{}'.format(MEDIA_ROOT, documento))
    except:
        messages.error(request, 'o arquivo não existe!')

    return None

# Função
def vida_academica(id_aluno):
    """
    Função que retorna a quantidade máxima de reprovações em uma disciplina
    para cálculo da faixa de criticidade do aluno logado

    TODO: Falta filtrar o item por ano e periodo nos itens de historico
    """

    # Variáveis
    t_aprovadas = []
    t_equivalentes = []
    t_original = []
    t_reprovacoes = []
    t_reprovadas = []
    t_discreprovadas = []
    periodo = -1
    periodos = 0
    trancamentos = 0
    maxreprovacoes = 0
    reprovacoest = 0
    integralizacaot = 0
    numcriticidade = 0
    cargaeletivas = 0
    mincreditos = 0
    maxcreditos = 28

    aluno = Aluno.objects.using('sca').get(id=id_aluno)
    nomeAluno = aluno.nome
    # TODO
    historico = Itemhistoricoescolar.objects.using('sca').filter(
                            historico_escolar=aluno.historico
                        )
    for h in historico:
        disc = h.disciplina.id
        # Verificação dos períodos cursados
        if periodo != h.periodo:
            periodo = h.periodo
            periodos = periodos + 1

        # Verificação das disciplinas cursadas, matriculadas e aprovadas
        if h.situacao in (0, 4, 7, 8, 9, 10, 12):
            t_aprovadas.append(disc)
            # Verifica se a disciplina é optativa e calcula a carga horária
            # O campo optativa é do tipo bit
            if h.disciplina.optativa == b'\x01':
                cargaeletivas += h.disciplina.cargahoraria
            # Verificação das disciplinas equivalentes (original -> equivalente)
            original = Disciplinasoriginais.objects.using('sca').filter(
                            disciplinasoriginais=disc
                        )
            bloco = Blocoequivalencia.objects.using('sca').filter(id__in=original)
            t_equivalentes = list(Disciplinasequivalentes.objects.using(
                            'sca').filter(bloco__in=bloco).values_list(
                            'disciplinasequivalentes', flat=True)
                        )
            t_aprovadas.extend(t_equivalentes)
            # Verificação das disciplinas equivalentes (equivalente -> original)
            t_equivalentes = Disciplinasequivalentes.objects.using(
                            'sca').filter(disciplinasequivalentes=disc)
            bloco = Blocoequivalencia.objects.using('sca').filter(
                            id__in=t_equivalentes
                        )
            t_original = list(Disciplinasoriginais.objects.using('sca').filter(
                            bloco__in=bloco).values_list(
                            'disciplinasoriginais', flat=True)
                        )
            t_aprovadas.extend(t_original)

        # Verificação das disciplinas reprovadas e reprovações
        elif h.situacao in (1, 2, 11):
            try:
                t_reprovacoes[t_reprovadas.index(disc)] = \
                            t_reprovacoes[t_reprovadas.index(disc)] + 1
            except:
                t_reprovadas.append(disc)
                t_discreprovadas.append(h.disciplina.nome + " (" +
                            h.disciplina.codigo + ")")
                t_reprovacoes.append(1)

        # Verificação dos trancamentos totais
        elif h.situacao == 6:
            trancamentos = trancamentos + 1

    # Ordenação das disciplinas
    t_aprovadas.sort()

    # Visualização das disciplinas reprovadas e qtd de reprovações
    for x in range(len(t_discreprovadas)):
        t_discreprovadas[x] = t_discreprovadas[x] + " - " + str(t_reprovacoes[x])

    # Parâmetros e cálculo para reprovações por disciplina
    periodomin = Versaocurso.objects.using('sca').get(
                            id=aluno.versaocurso.id).qtdperiodominimo
    if periodomin < 8:
        reprovacoeslaranja = reprovacoes_faixa_laranja_demais_cursos()
        reprovacoesvermelha = reprovacoes_faixa_vermelha_demais_cursos()
    else:
        reprovacoeslaranja = reprovacoes_faixa_laranja_cursos_8_periodos()
        reprovacoesvermelha = reprovacoes_faixa_vermelha_cursos_8_periodos()
    if len(t_reprovacoes) != 0:
        maxreprovacoes = max(t_reprovacoes)
    if maxreprovacoes < reprovacoeslaranja:
        reprovacoest = 0
    elif maxreprovacoes >= reprovacoeslaranja and maxreprovacoes < reprovacoesvermelha:
        reprovacoest = 1
    elif maxreprovacoes == reprovacoesvermelha:
        reprovacoest = 2
    else:
        reprovacoest = 3

    # Parâmetros e cálculo para integralização
    formulainiciallaranja = formula_inicial_faixa_laranja()
    formulafinallaranja = formula_final_faixa_laranja()
    formulavermelha = formula_faixa_vermelha()
    periodos = periodos - trancamentos
    N = periodomin / 2
    if periodos < eval(formulainiciallaranja):      # 2 * N:
        integralizacaot = 0
    elif periodos <= eval(formulafinallaranja):     # 4 * N - 4:
        integralizacaot = 1
    elif periodos <= eval(formulavermelha):         # 4 * N - 3:
        integralizacaot = 2
    else:
        integralizacaot = 3

    # Verificação dos máximo de créditos por semana que o aluno poder cursar
    # no período
    numcriticidade = max(reprovacoest, integralizacaot)
    if numcriticidade == 3:
        mincreditos = min_creditos_preta()
    maxcreditos = max_creditos()

    if numcriticidade == 0:
        criticidade = 'AZUL'
    elif numcriticidade == 1:
        criticidade = 'LARANJA'
    elif numcriticidade == 2:
        criticidade = 'VERMELHA'
    else:
        criticidade = 'PRETA'

    retorno = t_aprovadas, t_reprovacoes, t_reprovadas, t_discreprovadas, \
                    criticidade, mincreditos, maxcreditos, periodos, nomeAluno, \
                    trancamentos, cargaeletivas

    return retorno
