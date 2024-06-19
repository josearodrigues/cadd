# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
#        modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Alocacacaodisciplinasemdepartamento(models.Model):
    """
    Classe importada da tabela alocacacaodisciplinasemdepartamento
    do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    departamento = models.ForeignKey(
                    'Departamento',
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'alocacacaodisciplinasemdepartamento'
        app_label = 'sca'


class Aluno(models.Model):
    """
    Classe importada da tabela aluno do banco de dados SCA

    OBS: O campo endereco é o da salvaguarda do e-mail
    TODO: Faltam os campos situacao, faixa e formaEvasao não contemplados
          no esquema
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    matricula = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    cpf = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    endereco = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    datanascimento = models.DateTimeField(
                    db_column='dataNascimento',
                    blank=True,
                    null=True
                )
    historico = models.ForeignKey(
                    'Historicoescolar',
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    versaocurso = models.ForeignKey(
                    'Versaocurso',
                    models.DO_NOTHING,
                    db_column='versaoCurso_id',
                    blank=True,
                    null=True
                )

    def __str__(self):
        return self.nome.upper()

    class Meta:
        managed = False
        db_table = 'aluno'
        app_label = 'sca'


class Atividadecomplementar(models.Model):
    """
    Classe importada da tabela atividadecomplementar do banco de dados SCA

    TODO: Ainda não se sabe se será utilizada
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    cargahorariamax = models.TextField(
                    db_column='cargaHorariaMax',
                    blank=True,
                    null=True
                )
    cargahorariamin = models.TextField(
                    db_column='cargaHorariaMin',
                    blank=True,
                    null=True
                )
    tipo = models.ForeignKey(
                    'Tipoatividadecomplementar',
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'atividadecomplementar'
        app_label = 'sca'


class Blocoequivalencia(models.Model):
    """
    Classe importada da tabela blocoequivalencia do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )

    class Meta:
        managed = False
        db_table = 'blocoequivalencia'
        app_label = 'sca'


class Curso(models.Model):
    """
    Classe importada da tabela curso do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    sigla = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    coordenador = models.ForeignKey(
                    'Professor',
                    models.DO_NOTHING,
                    db_column='coordenador_id',
                    blank=True,
                    null=True,
                    related_name='coordenador'
                )
    coordenadoratividades = models.ForeignKey(
                    'Professor',
                    models.DO_NOTHING,
                    db_column='coordenadorAtividadesComplementares_id',
                    blank=True,
                    null=True,
                    related_name='coordenadoratividades'
                )

    def __str__(self):
        return self.nome.upper()

    class Meta:
        managed = False
        db_table = 'curso'
        app_label = 'sca'


class Cursodisciplina(models.Model):
    """
    Classe importada da tabela curso_disciplina do banco de dados SCA
    """

    curso = models.ForeignKey(
                    Curso,
                    models.DO_NOTHING,
                    db_column='Curso_id'
                )
    disciplinas = models.OneToOneField(
                    'Disciplina',
                    models.DO_NOTHING,
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'curso_disciplina'
        app_label = 'sca'


class Departamento(models.Model):
    """
    Classe importada da tabela departamento do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    sigla = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )

    def __str__(self):
        return self.nome.upper()

    class Meta:
        managed = False
        db_table = 'departamento'
        app_label = 'sca'


class Departamentodisciplina(models.Model):
    """
    Classe importada da tabela departamento_disciplina do banco de dados SCA
    """

    departamento = models.OneToOneField(
                    Departamento,
                    models.DO_NOTHING,
                    db_column='Departamento_id',
                    primary_key=True
                )
    disciplinas = models.OneToOneField(
                    'Disciplina',
                    models.DO_NOTHING,
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'departamento_disciplina'
        unique_together = (('departamento', 'disciplinas'),)
        app_label = 'sca'


class Departamentoprofessor(models.Model):
    """
    Classe importada da tabela departamento_professor do banco de dados SCA
    """

    departamento = models.OneToOneField(
                    Departamento,
                    models.DO_NOTHING,
                    db_column='Departamento_id',
                    primary_key=True
                )
    professores = models.OneToOneField(
                    'Professor',
                    models.DO_NOTHING,
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'departamento_professor'
        unique_together = (('departamento', 'professores'),)
        app_label = 'sca'


class Disciplina(models.Model):
    """
    Classe importada da tabela disciplina do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    codigo = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    quantidadecreditos = models.IntegerField(
                    db_column='quantidadeCreditos',
                    blank=True,
                    null=True
                )
    cargahoraria = models.IntegerField(
                    db_column='cargaHoraria'
                )
    optativa = models.NullBooleanField(
                    u'Optativa',
                    db_column='ehOptativa',
                    blank=True,
                    null=True
                )
    versaocurso = models.ForeignKey(
                    'Versaocurso',
                    models.DO_NOTHING,
                    db_column='versaoCurso_id',
                    blank=True,
                    null=True
                )
    departamento = models.ForeignKey(
                    Alocacacaodisciplinasemdepartamento,
                    models.DO_NOTHING,
                    db_column='ALOCACAO_DEPTO_ID',
                    blank=True,
                    null=True
                )

    def __str__(self):
        return self.nome.upper() + " (" + self.codigo + ")" # + \
#                " (versão do curso: " + self.versaocurso.numero + ")"

    class Meta:
        managed = False
        db_table = 'disciplina'
        app_label = 'sca'


class DisciplinaPrereqs(models.Model):
    """
    Classe importada da tabela disciplina_prereqs do banco de dados SCA
    """

    grade = models.OneToOneField(
                    Disciplina,
                    models.DO_NOTHING,
                    db_column='GRADE_ID',
                    primary_key=True,
                    related_name='grade'
                )
    disciplina = models.OneToOneField(
                    Disciplina,
                    models.DO_NOTHING,
                    db_column='DISCIPLINA_ID',
                    related_name='disciplina'
                )

    class Meta:
        managed = False
        db_table = 'disciplina_prereqs'
        unique_together = (('grade', 'disciplina'),)
        app_label = 'sca'


class Disciplinasequivalentes(models.Model):
    """
    Classe importada da tabela disciplinas_equivalentes do banco de dados SCA
    """

    bloco = models.OneToOneField(
                    Blocoequivalencia,
                    models.DO_NOTHING,
                    db_column='BLOCO_ID',
                    primary_key=True
                )
    disciplinasequivalentes = models.OneToOneField(
                    Disciplina,
                    models.DO_NOTHING,
                    db_column='DISCIPLINASEQUIVALENTES_ID'
                )

    class Meta:
        managed = False
        db_table = 'disciplinas_equivalentes'
        unique_together = (('bloco', 'disciplinasequivalentes'),)
        app_label = 'sca'


class Disciplinasoriginais(models.Model):
    """
    Classe importada da tabela disciplinas_originais do banco de dados SCA
    """

    bloco = models.OneToOneField(
                    Blocoequivalencia,
                    models.DO_NOTHING,
                    db_column='BLOCO_ID',
                    primary_key=True
                )
    disciplinasoriginais = models.OneToOneField(
                    Disciplina,
                    models.DO_NOTHING,
                    db_column='DISCIPLINASORIGINAIS_ID'
                )

    class Meta:
        managed = False
        db_table = 'disciplinas_originais'
        unique_together = (('bloco', 'disciplinasoriginais'),)
        app_label = 'sca'


class Historicoescolar(models.Model):
    """
    Classe importada da tabela historicoescolar do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    versaocurso = models.ForeignKey(
                    'Versaocurso',
                    models.DO_NOTHING,
                    db_column='versaoCurso_id',
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'historicoescolar'
        app_label = 'sca'


class Inscricao(models.Model):
    """
    Classe importada da tabela inscricao do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    aluno = models.ForeignKey(
                    Aluno,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    avaliacao = models.ForeignKey(
                    'Notafinal',
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    turma = models.ForeignKey(
                    'Turma',
                    models.DO_NOTHING,
                    db_column='TURMA_ID',
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'inscricao'
        app_label = 'sca'


class Itemhistoricoescolar(models.Model):
    """
    Classe importada da tabela itemhistoricoescolar do banco de dados SCA

    OBS: Possíveis valores para o campo situacao:
        0 APROVADO
        1 REPROVADO_POR_MEDIA
        2 REPROVADO_POR_FALTAS
        3 TRANCAMENTO_DISCIPLINA
        4 ISENTO_POR_TRANSFERENCIA
        5 INDEFINIDA
        6 TRANCAMENTO_TOTAL
        7 APROVEITAMENTO_CREDITOS
        8 ISENTO
        9 APROVEITAMENTO_POR_ESTUDOS
        10 MATRICULA
        11 REPROVADO_SEM_NOTA
        12 APROVADO_SEM_NOTA
        13 REAPROVADO_COM_DEPENDENCIA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    ano = models.IntegerField(
                    blank=True,
                    null=True
                )
    periodo = models.IntegerField(
                    blank=True,
                    null=True
                )
    situacao = models.IntegerField(
                    blank=True,
                    null=True
                )
    disciplina = models.ForeignKey(
                    Disciplina,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    historico_escolar = models.ForeignKey(
                    Historicoescolar,
                    models.DO_NOTHING,
                    db_column='HISTORICO_ESCOLAR_ID',
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'itemhistoricoescolar'
        app_label = 'sca'


class Notafinal(models.Model):
    """
    Classe importada da tabela notafinal do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    frequencia = models.DecimalField(
                    max_digits=19,
                    decimal_places=2,
                    blank=True,
                    null=True
                )
    notap1 = models.DecimalField(
                    db_column='notaP1',
                    max_digits=19,
                    decimal_places=2,
                    blank=True,
                    null=True
                )
    notap2 = models.DecimalField(
                    db_column='notaP2',
                    max_digits=19,
                    decimal_places=2,
                    blank=True,
                    null=True
                )
    notap3 = models.DecimalField(
                    db_column='notaP3',
                    max_digits=19,
                    decimal_places=2,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'notafinal'
        app_label = 'sca'


class Professor(models.Model):
    """
    Classe importada da tabela professor do banco de dados SCA

    OBS: O campo endereço é o da salvaguarda do e-mail
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    matricula = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    cpf = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    datanascimento = models.DateTimeField(
                    db_column='dataNascimento',
                    blank=True,
                    null=True
                )
    endereco = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )

    def __str__(self):
        return self.nome.upper()

    class Meta:
        managed = False
        db_table = 'professor'
        app_label = 'sca'


class Professordisciplina(models.Model):
    """
    Classe importada da tabela professor_disciplina do banco de dados SCA
    """

    professor = models.OneToOneField(
                    Professor,
                    models.DO_NOTHING,
                    db_column='PROFESSOR_ID',
                    primary_key=True
                )
    disciplina = models.OneToOneField(
                    Disciplina,
                    models.DO_NOTHING,
                    db_column='DISCIPLINA_ID'
                )

    class Meta:
        managed = False
        db_table = 'professor_disciplina'
        unique_together = (('professor', 'disciplina'),)
        app_label = 'sca'


class Registroatividadecomplementar(models.Model):
    """
    Classe importada da tabela registroatividadecomplementar do banco de
    dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    cargahoraria = models.TextField(
                    db_column='cargaHoraria',
                    blank=True,
                    null=True
                )
    dataanalise = models.DateTimeField(
                    db_column='dataAnalise',
                    blank=True,
                    null=True
                )
    descricao = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    estado = models.IntegerField(
                    blank=True,
                    null=True
                )
    atividade = models.ForeignKey(
                    Atividadecomplementar,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    aluno = models.ForeignKey(
                    Aluno,
                    models.DO_NOTHING,
                    db_column='ALUNO_ID',
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'registroatividadecomplementar'
        app_label = 'sca'


class Tabelaatividadescomplementares(models.Model):
    """
    Classe importada da tabela tabelaatividadescomplementares do banco de
    dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )

    class Meta:
        managed = False
        db_table = 'tabelaatividadescomplementares'
        app_label = 'sca'


class TabelaatividadescomplementaresAtividadecomplementar(models.Model):
    """
    Classe importada da tabela tabelaatividadescomplementares_atividadecomplementar
    do banco de dados SCA
    """

    tabelaatividadescomplementares = models.ForeignKey(
                    Tabelaatividadescomplementares,
                    models.DO_NOTHING,
                    db_column='TabelaAtividadesComplementares_id'
                )
    atividades = models.OneToOneField(
                    Atividadecomplementar,
                    models.DO_NOTHING,
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'tabelaatividadescomplementares_atividadecomplementar'
        app_label = 'sca'


class Tabelaequivalencias(models.Model):
    """
    Classe importada da tabela tabelaequivalencias do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    versaocursocorrespondente = models.ForeignKey(
                    'Versaocurso',
                    models.DO_NOTHING,
                    db_column='versaoCursoCorrespondente_id',
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'tabelaequivalencias'
        app_label = 'sca'


class TabelaequivalenciasBlocoequivalencia(models.Model):
    """
    Classe importada da tabela tabelaequivalencias_blocoequivalencia do
    banco de dados SCA
    """

    tabelaequivalencias = models.OneToOneField(
                    Tabelaequivalencias,
                    models.DO_NOTHING,
                    db_column='TabelaEquivalencias_id',
                    primary_key=True
                )
    blocosequivalencia = models.OneToOneField(
                    Blocoequivalencia,
                    models.DO_NOTHING,
                    db_column='blocosEquivalencia_id',
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'tabelaequivalencias_blocoequivalencia'
        unique_together = (('tabelaequivalencias', 'blocosequivalencia'),)
        app_label = 'sca'


class Tipoatividadecomplementar(models.Model):
    """
    Classe importada da tabela tipoatividadecomplementar do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    categoria = models.IntegerField(
                    blank=True,
                    null=True
                )
    descricao = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'tipoatividadecomplementar'
        app_label = 'sca'


class Turma(models.Model):
    """
    Classe importada da tabela turma do banco de dados SCA
    """

    id = models.BigAutoField(
                    primary_key=True
                )
    codigo = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    ano = models.IntegerField(
                    blank=True,
                    null=True
                )
    periodo = models.IntegerField(
                    blank=True,
                    null=True
                )
    disciplina = models.ForeignKey(
                    Disciplina,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    professor = models.ForeignKey(
                    Professor,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )

    def __str__(self):
        return self.codigo

    class Meta:
        managed = False
        db_table = 'turma'
        app_label = 'sca'


class UserProfile(models.Model):
    """
    Classe importada da tabela user_profile do banco de dados SCA
    """

    type = models.CharField(
                    db_column='TYPE',
                    unique=True,
                    max_length=30
                )

    def __str__(self):
        return self.type

    class Meta:
        managed = False
        db_table = 'user_profile'
        app_label = 'sca'


class Useruserprofile(models.Model):
    """
    Classe importada da tabela user_user_profile do banco de dados SCA
    """

    user = models.OneToOneField(
                    'Users',
                    models.DO_NOTHING,
                    db_column='USER_ID',
                    primary_key=True
                )
    userprofile = models.OneToOneField(
                    UserProfile,
                    models.DO_NOTHING,
                    db_column='USER_PROFILE_ID'
                )

    def __str__(self):
        return self.user

    class Meta:
        managed = False
        db_table = 'user_user_profile'
        unique_together = (('user', 'userprofile'),)
        app_label = 'sca'


class Users(models.Model):
    """
    Classe importada da tabela users do banco de dados SCA

    OBS: O campo email foi o utilizado para envio de e-mails
    """

    dob = models.DateTimeField(
                    blank=True,
                    null=True
                )
    email = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    login = models.CharField(
                    max_length=255,
                    unique=True
                )
    matricula = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    nome = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'users'
        app_label = 'sca'


class Versaocurso(models.Model):
    """
    Classe importada da tabela versaocurso do banco de dados SCA

    OBS: Possíveis valores para o campo situacao:
        0 INATIVO
        1 ATIVO
        2 CORRENTE
    TODO: os campos cargahorariaminativcomp e cargahorariaminoptativas
            estão serializados pelo java
    """

    id = models.BigAutoField(primary_key=True)
    cargahorariaativcomp = models.TextField(
                    db_column='cargaHorariaMinAitvComp',
                    blank=True,
                    null=True
                )
    cargahorariaoptativas = models.TextField(
                    db_column='cargaHorariaMinOptativas',
                    blank=True,
                    null=True
                )
    numero = models.CharField(
                    max_length=255,
                    blank=True,
                    null=True
                )
    qtdperiodominimo = models.IntegerField(
                    db_column='qtdPeriodoMinimo',
                    blank=True,
                    null=True
                )
    situacao = models.IntegerField(
                    blank=True,
                    null=True
                )
    atividades = models.ForeignKey(
                    Tabelaatividadescomplementares,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )
    curso = models.ForeignKey(
                    Curso,
                    models.DO_NOTHING,
                    blank=True,
                    null=True
                )

    class Meta:
        managed = False
        db_table = 'versaocurso'
        app_label = 'sca'


class VersaocursoTabelaequivalencias(models.Model):
    """
    Classe importada da tabela versaocurso_tabelaequivalencias do banco de
    dados SCA
    """

    versaocurso = models.OneToOneField(
                    Versaocurso,
                    models.DO_NOTHING,
                    db_column='VersaoCurso_id',
                    primary_key=True
                )
    tabelasequivalencias = models.OneToOneField(
                    Tabelaequivalencias,
                    models.DO_NOTHING,
                    db_column='tabelasEquivalencias_id',
                    unique=True
                )

    class Meta:
        managed = False
        db_table = 'versaocurso_tabelaequivalencias'
        unique_together = (('versaocurso', 'tabelasequivalencias'),)
        app_label = 'sca'
