from django.contrib.auth.models import User
from django.db import models, connection, transaction
from collections import namedtuple

from django.utils import timezone

# Create your models here.

# Constante global para a lista dos períodos
# Utilizada pelas tabelas que possuem o campo periodo
PERIODO_CHOICES = (
    (None, 'Selecione o período'),
    (1, '1º semestre'),
    (2, '2º semestre'),
)

class Parametros(models.Model):
    """
    Classe de uso do sistema para a guarda dos parâmetros do sistema
    """

    # Armazena a quantidade máxima de reprovações em uma mesma disciplina
    # que um aluno na faixa de criticidade laranja pode ter oriundo de um
    # curso de 8 períodos ou mais
    reprovacurso8periodoslaranja = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=2
                )
    # Armazena a quantidade máxima de reprovações em uma mesma disciplina
    # que um aluno na faixa de criticidade laranja pode ter oriundo dos
    # demais cursos
    reprovademaiscursoslaranja = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=1
                )
    # Armazena a quantidade máxima de reprovações em uma mesma disciplina
    # que um aluno na faixa de criticidade vermelha pode ter oriundo de um
    # curso de 8 períodos ou mais
    reprovacurso8periodosvermelha = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=3
                )
    # Armazena a quantidade máxima de reprovações em uma mesma disciplina
    # que um aluno na faixa de criticidade vermelha pode ter oriundo dos
    # demais cursos
    reprovademaiscursosvermelha = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=2
                )
    # Armazena a fórmula para calcular a quantidade máxima de períodos para
    # integralização que um aluno na faixa de criticidade laranja pode cursar
    # (início da faixa)
    qtdperiodosiniciallaranja = models.CharField(
                    max_length=10,
                    blank=False,
                    null=False,
                    default='2 * N'
                )
    # Armazena a fórmula para calcular a quantidade máxima de períodos para
    # integralização que um aluno na faixa de criticidade laranja pode cursar
    # (final da faixa)
    qtdperiodosfinallaranja = models.CharField(
                    max_length=10,
                    blank=False,
                    null=False,
                    default='2 * N'
                )
    # Armazena a fórmula para calcular a quantidade máxima de períodos para
    # integralização que um aluno na faixa de criticidade vermelha pode cursar
    qtdperiodosvermelha = models.CharField(
                    max_length=10,
                    blank=False,
                    null=False,
                    default='4 * N - 3'
                )
    # Armazena a quantidade mínima de créditos das disciplinas por semana
    # que um aluno na faixa de criticidade preta pode ter
    mincreditosporperiodopreta = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=20
                )
    # Armazena a quantidade máxima de créditos das disciplinas por semana
    # que um aluno pode ter não estando na faixa de criticidade preta
    maxcreditosporperiodo = models.PositiveSmallIntegerField(
                    blank=False,
                    null=False,
                    default=28
                )

    class Meta:
        managed = True
        db_table = 'parametros'
        app_label = 'cadd'


class Perfil(models.Model):
    """
    Classe para estender a Model User padrão do Django adicionando alguns
    campos necessários e criando um perfil para o usuário logado

    TODO: Faltam os campos situacao e formaEvasao não contemplados no esquema
            mas visualizados nas planilhas
    """

    # Constante para a lista da quantidade de itens de uma lista a serem
    # visualizados por página
    ITENSPAGINA_CHOICES = (
        (None, 'Selecione o total de itens por página'),
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (25, 25),
        (30, 30),
        (35, 35),
        (40, 40),
        (45, 45),
        (50, 50),
    )

    # Armazena a id do usuário correspondente
    # Relacionamento com a tabela auth_user do Django
    user = models.OneToOneField(
                    User,
                    models.PROTECT,
                    unique=True,
                    related_name='profile'
                )
    # Armazena a matrícula seja do aluno ou professor
    matricula = models.CharField(
                    max_length=255,
                    blank=False,
                    null=False
                )
    # Armazena o identificador do usuário logado no banco de dados SCA, podendo
    # ser um aluno (campo id da tabela Aluno) ou um professor (campo id da
    # tabela Professor)
    idusuario = models.BigIntegerField(
                    blank=False,
                    null=False,
                )

    # Armazena a quantidade de itens por página um objeto pode ser listado
    # (paginação)
    itenspagina = models.PositiveSmallIntegerField(
                    choices=ITENSPAGINA_CHOICES,
                    blank=False,
                    null=False,
                    default=5
                )

    class Meta:
        managed = True
        db_table = 'perfil'
        app_label = 'cadd'


class Comissao(models.Model):
    """
    Classe de uso do sistema para o cadastro das comissões
    """

    # Armazena a descição da comissão
    descricao = models.CharField(
                    u'Descrição',
                    max_length=50,
                    blank=False,
                    null=False
                )
    # Armazena a id do curso correspondente
    # Relacionamento com a tabela Curso do banco de dados SCA
    curso = models.OneToOneField(
                    'sca.Curso',
                    models.DO_NOTHING,
                    blank=False,
                    null=False,
                    related_name='comissao_curso'
                )

    # Função que retorna uma descrição para cada objeto comissão
    def __str__(self):
        return self.descricao

    # Função que retorna uma consulta customizada entre as tabelas Comissao,
    # Membro e curso para que na visualização da lista de comissões o botão
    # de exclusão possa estar em uma das seguintes situações, conforme o campo
    # contagem:
    #    Habilitado: contagem == 0
    #    Desabilitado: contagem > 0
    def comissoes_membros_sql():

        # Criação do cursor e execução por meio da SQl customizada
        cursor = connection.cursor()
        cursor.execute(
            "SELECT	" + \
            "   c.id, c.descricao, cur.nome, count(m.id) as 'contagem'" + \
            "FROM " + \
            "   (" + \
            "       cadddb.comissao c " + \
            "       INNER JOIN scadb.curso cur " + \
            "       ON c.curso_id=cur.id" + \
            "   )" + \
            "   LEFT JOIN cadddb.membro m " + \
            "   ON c.id=m.comissao_id " + \
            "GROUP BY " + \
            "   c.curso_id " + \
            "ORDER BY " + \
            "   descricao"
        )

        # Retorna todas as linhas de um cursos como um tupla nomeada
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        row = [nt_result(*row) for row in cursor.fetchall()]

        return row

    class Meta:
        managed = True
        db_table = 'comissao'
        app_label = 'cadd'


class Membro(models.Model):
    """
    Classe de uso do sistema para o cadastro dos membros das CADDs
    """

    # Armazena se um membro está ativo ou não
    ativo = models.BooleanField(
                    u'Ativo'
                )
    # Armazena se um membro é presidente ou não
    presidente = models.BooleanField(
                    u'Presidente'
                )
    # Armazena a portaria de origem da função de um membro na comissão
    portaria = models.CharField(
                    u'Portaria',
                    max_length=50,
                    blank=False,
                    null=False
                )
    # Armazena a id da comissão correspondente
    # Relacionamento com a tabela Comissao
    comissao = models.ForeignKey(
                    'Comissao',
                    models.PROTECT,
                    blank=False,
                    null=False,
                    related_name='membro_comissao'
                )
    # Armazena a id do professor correspondente
    # Relacionamento com a tabela Professor do banco de dados SCA
    professor = models.ForeignKey(
                    'sca.Professor',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'membro'
        app_label = 'cadd'


class Reuniao(models.Model):
    """
    Classe de uso do sistema para o agendamento das reuniões
    """

    # Constante para a lista dos status das reuniões
    SITUACAO_CHOICES = (
        (None, 'Selecione a situação'),
        ('A', 'Agendada'),
        ('C', 'Cancelada'),
        ('E', 'Encerrada'),
    )
    # Constante para a lista dos tipos de reuniões
    TIPO_CHOICES = (
        (None, 'Selecione o tipo'),
        ('I', 'Informação'),
        ('C', 'Convocação'),
    )

    # Armazena a data agendada para a reunião
    data = models.DateField(
                    u'Data',
                    blank=False,
                    null=False
                )
    # Armazena o horário agendado para a reunião
    inicio = models.TimeField(
                    u'Início',
                    blank=False,
                    null=False
                )
    # Armazena o local da reunião
    local = models.CharField(
                    u'Local',
                    max_length=50,
                    blank=False,
                    null=False
                )
    # Armazena o status da reunião
    situacao = models.CharField(
                    u'Situação',
                    max_length=1,
                    choices=SITUACAO_CHOICES,
                    blank=False,
                    default='A'
                )
    # Armazena o tipo de reunião
    tipo = models.CharField(
                    u'Tipo',
                    max_length=1,
                    choices=TIPO_CHOICES,
                    blank=False,
                    default='I'
                )
    # Armazena as anotações referentes a uma reunião
    anotacao = models.TextField(
                    u'Anotação',
                    blank=True,
                    null=True
                )
    # Armazena a id do comissão correspondente
    # Relacionamento com a tabela Comissao
    comissao = models.ForeignKey(
                    'Comissao',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    # Função que retorna uma descrição para cada objeto reunião
    def __str__(self):
        return self.local.upper() + " em " + str(self.data.strftime('%d/%m/%Y')) + \
                    " às " + str(self.inicio.strftime('%H:%M')) + "h"

    class Meta:
        managed = True
        db_table = 'reuniao'
        app_label = 'cadd'


class Convocacao(models.Model):
    """
    Classe de uso do sistema para a guarda dos alunos convocados às reuniões
    """

    # Armazena se foi enviado ou não e-mail convocando o aluno
    envioemail = models.NullBooleanField(
                    u'Email',
                )
    # Armazena a presença do aluno na reunião
    presente = models.NullBooleanField(
                    u'Presente',
                )
    # Armazena as anotações/orientações passadas ao aluno
    anotacao = models.TextField(
                    u'Anotação',
                    blank=True,
                    null=True
                )
    # Armazena a id do reunião correspondente
    # Relacionamento com a tabela Reuniao
    reuniao = models.ForeignKey(
                    'Reuniao',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id do aluno convocado correspondente
    # Relacionamento com a tabela Aluno do banco de dados SCA
    aluno = models.ForeignKey(
                    'sca.Aluno',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'convocacao'
        app_label = 'cadd'


class Horario(models.Model):
    """
    Classe de uso do sistema para a guarda da prévia do horário do
    semestre subsequente
    """

    # Armazena o ano de referência ao horário salvaguardado
    ano = models.PositiveSmallIntegerField(
                    u'Ano',
                    blank=False,
                    null=False
                )
    # Armazena o perído de referência ao horário salvaguardado
    periodo = models.PositiveSmallIntegerField(
                    u'Período',
                    choices=PERIODO_CHOICES,
                    blank=False,
                    null=False
                )
    # Armazena a id do curso correspondente
    # Relacionamento com a tabela Curso do banco de dados SCA
    curso = models.ForeignKey(
                    'sca.Curso',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    # Função que retorna uma descrição para cada objeto horário
    def __str__(self):
        return str(self.ano) + '.' + str(self.periodo) + '-' + self.curso.sigla.upper()

    # Função que retorna uma consulta customizada entre as tabelas Comissao,
    # Membro e curso para que na visualização da lista de cursos sejam exibidos
    # somente os que um membro pode alterar
    def cursos_membros_sql(professor):

        # Criação do cursor e execução por meio da SQl customizada
        cursor = connection.cursor()
        cursor.execute(
            "SELECT	" + \
            "   c.curso_id as 'curso'" + \
            "FROM " + \
            "   (" + \
            "       cadddb.comissao c " + \
            "       INNER JOIN scadb.curso cur " + \
            "       ON c.curso_id=cur.id" + \
            "   )" + \
            "   LEFT JOIN cadddb.membro m " + \
            "   ON c.id=m.comissao_id " + \
            "WHERE " + \
            "   m.ativo=1 and " + \
            "   m.professor_id=" + str(professor)
        )

        # Retorna todas as linhas de cursos como uma lista
        desc = cursor.description
        row = [item[0] for item in cursor.fetchall()]

        return row

    class Meta:
        managed = True
        db_table = 'horario'
        app_label = 'cadd'


class ItemHorario(models.Model):
    """
    Classe de uso do sistema para a guarda dos itens da prévia do horário

    OBS: Possíveis horários das aulas (retirado do SCA):
        1 07:00 às 07:50
        2 07:55 às 08:45
        3 08:50 às 09:40
        4 09:55 às 10:45
        5 10:50 às 11:40
        6 11:45 às 12:35
        7 12:40 às 13:30
        8 13:35 às 14:25
        9 14:30 às 15:20
        10 15:35 às 16:25
        11 16:30 às 17:20
        12 17:25 às 18:15
        13 18:20 às 19:10
        14 19:10 às 20:00
        15 20:00 às 20:50
        16 21:00 às 21:50
        17 21:50 às 22:40
    """

    # Constante para a lista dos dias da semana
    DIASEMANA_CHOICES = (
        (None, 'Selecione o dia da semana'),
        (0, 'Domingo'),
        (1, 'Segunda-feira'),
        (2, 'Terça-feira'),
        (3, 'Quarta-feira'),
        (4, 'Quinta-feira'),
        (5, 'Sexta-feira'),
        (6, 'Sábado'),
        (7, 'Semipresencial'),
        (8, 'Horário variável'),
    )

    # Armazena a referência do período previsto da disciplina no curso
    periodo = models.CharField(
                    u'Período',
                    max_length=3,
                    blank=False,
                    null=False,
                    default=1
                )
    # Armazena a dia de semana que será ministrada a aula da disciplina
    diasemana = models.PositiveSmallIntegerField(
                    u'Dia da semana',
                    blank=False,
                    null=False,
                    choices=DIASEMANA_CHOICES
                )
    # Armazena o horário de início da aula
    inicio = models.TimeField(
                    u'Início',
                    blank=True,
                    null=True
                )
    # Armazena o horário de término da aula
    fim = models.TimeField(
                    u'Início',
                    blank=True,
                    null=True
                )
    # Armazena a id do horário correspondente
    # Relacionamento com a tabela Horario
    horario = models.ForeignKey(
                    'Horario',
                    models.PROTECT,
                    blank=False,
                    null=False
                )
    # Armazena a id do professor correspondente
    # Relacionamento com a tabela Professor do banco de dados SCA
    professor = models.ForeignKey(
                    'sca.Professor',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id do departamento correspondente
    # Relacionamento com a tabela Departamento do banco de dados SCA
    departamento = models.ForeignKey(
                    'sca.Departamento',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id da disciplina correspondente
    # Relacionamento com a tabela Disciplina do banco de dados SCA
    disciplina = models.ForeignKey(
                    'sca.Disciplina',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id da turma correspondente
    # Relacionamento com a tabela Turma do banco de dados SCA
    turma = models.ForeignKey(
                    'sca.Turma',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'item_horario'
        app_label = 'cadd'


class Documento(models.Model):
    """
    Classe de uso do sistema para a guarda dos documentos escaneados
    dos alunos
    """

    # Armazena o ano de referência à documentação salvaguardada
    ano = models.PositiveSmallIntegerField(
                    u'Ano',
                    blank=False,
                    null=False
                )
    # Armazena o perído de referência à documentação salvaguardada
    periodo = models.PositiveSmallIntegerField(
                    u'Período',
                    choices=PERIODO_CHOICES,
                    blank=False,
                    default=1,
                    null=False
                )
    # Armazena a descrição da documentação
    descricao = models.CharField(
                    u'Descrição',
                    max_length=50,
                    blank=False,
                    null=False
                )
    # Armazena o local do sistema de arquivos onde o documento está salvaguardado
    indice = models.FileField(
                    u'Índice',
                    max_length=50,
                    blank=False,
                    null=False,
                    upload_to='documentos/'
                )
    # Armazena o timestamp de upload do documento
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # Armazena a id do aluno convocado correspondente
    # Relacionamento com a tabela Aluno do banco de dados SCA
    aluno = models.ForeignKey(
                    'sca.Aluno',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    # Função que retorna uma descrição para cada objeto documento
    def __str__(self):
        return self.descricao.upper()

    class Meta:
        managed = True
        db_table = 'documento'
        app_label = 'cadd'


class Plano(models.Model):
    """
    Classe de uso do sistema para a guarda dos planos de estudo dos alunos
    """

    # Constante para a lista dos status dos planos
    SITUACAO_CHOICES = (
        (None, 'Selecione a situação'),
        ('M', 'Montado'),
        ('A', 'Avaliado'),
        ('E', 'Encerrado'),
    )

    # Armazena o ano de referência ao plano salvaguardado
    ano = models.PositiveSmallIntegerField(
                    u'Ano',
                    blank=False,
                    null=False
                )
    # Armazena o período de referência do plano salvaguardado
    periodo = models.PositiveSmallIntegerField(
                    u'Período',
                    choices=PERIODO_CHOICES,
                    blank=False,
                    null=False,
                    default=1
                )
    # Armazena o status do plano
    situacao = models.CharField(
                    u'Situação',
                    max_length=1,
                    choices=SITUACAO_CHOICES,
                    blank=False,
                    default='M'
                )
    # Armazena a avaliação de um membro de uma comissão para o plano
    avaliacao = models.TextField(
                    u'Anotação',
                    blank=True,
                    null=True
                )
    # Armazena a id do aluno correspondente
    # Relacionamento com a tabela Aluno do banco de dados SCA
    aluno = models.ForeignKey(
                    'sca.Aluno',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'plano'
        app_label = 'cadd'


class ItemPlanoAtual(models.Model):
    """
    Classe de uso do sistema para a guarda dos itens atuais dos planos de
    estudo dos alunos
    """

    # Armazena a id do plano correspondente
    # Relacionamento com a tabela Plano
    plano = models.ForeignKey(
                    'Plano',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id do item do horário correspondente
    # Relacionamento com a tabela ItemHorario
    itemhorario = models.ForeignKey(
                    'ItemHorario',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'item_plano_atual'
        app_label = 'cadd'


class PlanoFuturo(models.Model):
    """
    Classe de uso do sistema para a guarda dos planos de estudo futuro
    dos alunos
    """

    # Armazena o ano de referência ao plano futuro salvaguardado
    ano = models.PositiveSmallIntegerField(
                    u'Ano',
                    blank=False,
                    null=False
                )
    # Armazena o período de referência ao plano futuro salvaguardado
    periodo = models.PositiveSmallIntegerField(
                    u'Período',
                    choices=PERIODO_CHOICES,
                    blank=False,
                    null=False,
                    default=1
                )
    # Armazena a id do plano correspondente
    # Relacionamento com a tabela Plano
    plano = models.ForeignKey(
                    'Plano',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'plano_futuro'
        app_label = 'cadd'


class ItemPlanoFuturo(models.Model):
    """
    Classe de uso do sistema para a guarda dos itens do plano de estudo futuro
    dos alunos
    """

    # Armazena a id do plano futuro correspondente
    # Relacionamento com a tabela PlanoFuturo
    planofuturo = models.ForeignKey(
                    'PlanoFuturo',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )
    # Armazena a id da disciplina correspondente
    # Relacionamento com a tabela Disciplina do banco de dados SCA
    disciplina = models.ForeignKey(
                    'sca.Disciplina',
                    models.DO_NOTHING,
                    blank=False,
                    null=False
                )

    class Meta:
        managed = True
        db_table = 'item_plano_futuro'
        app_label = 'cadd'
