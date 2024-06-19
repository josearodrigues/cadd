#from django.forms import BaseFormSet

from django import forms
from django.forms import TextInput, Textarea, Select, CheckboxInput, \
                    HiddenInput, NumberInput, TimeInput, DateInput

from .models import Parametros, Comissao, Membro, Horario, ItemHorario, Plano, \
                    ItemPlanoAtual, Reuniao, Convocacao, Documento, Perfil
from sca.models import Curso, Professor, Turma, Disciplina, Aluno, Versaocurso
from cadd.utils import periodo_atual

class ParametrosForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de parâmetros de
    configuração do sistema
    """

    class Meta:
        model = Parametros
        exclude = (id, )
        widgets = {
            'reprovacurso8periodoslaranja': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1,
                    'max': 10,
                    'step': 1,
                    'empty_label': 'Selecione a quantidade de reprovações'
                }),
            'reprovacurso8periodosvermelha': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1,
                    'max': 10,
                    'step': 1,
                    'empty_label': 'Selecione a quantidade de reprovações'
                }),
            'reprovademaiscursoslaranja': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1,
                    'max': 10,
                    'step': 1,
                    'empty_label': 'Selecione a quantidade de reprovações'
                }),
            'reprovademaiscursosvermelha': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1, 'max': 10, 'step': 1,
                    'empty_label': 'Selecione a quantidade de reprovações'
                }),
            'qtdperiodosiniciallaranja': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a fórmula para cálculo'
                }),
            'qtdperiodosfinallaranja': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a fórmula para cálculo'
                }),
            'qtdperiodosvermelha': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a fórmula para cálculo'
                }),
            'mincreditosporperiodopreta': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1, 'max': 50, 'step': 1,
                    'empty_label': 'Selecione o mínimo de créditos por período'
                }),
            'maxcreditosporperiodo': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 1, 'max': 50, 'step': 1,
                    'empty_label': 'Selecione o máximo de créditos por período'
                }),
        }

    def clean(self):
        if (self.cleaned_data.get('reprovacurso8periodosvermelha') <=
                self.cleaned_data.get('reprovacurso8periodoslaranja')):
            raise forms.ValidationError(
                    "As reprovações da faixa vermelha para cursos com 8 ou " + \
                    "mais períodos devem ser maiores que as da faixa laranja!"
                )
        if (self.cleaned_data.get('reprovademaiscursosvermelha') <=
                self.cleaned_data.get('reprovademaiscursoslaranja')):
            raise forms.ValidationError(
                    "As reprovações da faixa vermelha para os demais cursos " + \
                    "devem ser maiores que as da faixa laranja!"
                )

        return self.cleaned_data


class PerfilForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário meu perfil do usuário logado
    """

    class Meta:
        model = Perfil
        exclude = (id, 'user', 'matricula', 'idusuario', )
        widgets = {
            'itenspagina': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione o máximo de itens por página'
                }),
        }


class ComissaoForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de comissões de apoio
    """

    def __init__(self, *args, **kwargs):
        super (ComissaoForm, self).__init__(*args, **kwargs) # popula o post
        self.fields['curso'].queryset = \
            Curso.objects.using('sca').distinct().order_by('nome')
        self.fields['curso'].empty_label = 'Selecione o curso'

    class Meta:
        model = Comissao
        exclude = (id, )
        widgets = {
            'curso': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'descricao': Textarea(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a descrição'
                })
        }


class MembroForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de membros de uma
    comissão de apoio
    """

    def __init__(self, *args, **kwargs):
        super (MembroForm, self).__init__(*args, **kwargs)
        self.fields['professor'].queryset = \
            Professor.objects.using('sca').distinct().order_by('nome')
        self.fields['professor'].empty_label = 'Selecione o professor'

    class Meta:
        model = Membro
        exclude = (id, 'ativo', 'comissao', )
        widgets = {
            'professor': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'portaria': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a portaria'
                }),
            'presidente': CheckboxInput(attrs={
                    'class': 'form-control'
                })
        }


class ReuniaoForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de reuniões
    """

    def __init__(self, *args, **kwargs):
        if 'professor' in kwargs:
            self.professor = kwargs.pop('professor')
        super(ReuniaoForm, self).__init__(*args, **kwargs)
        membro = Membro.objects.filter(
                            professor=self.professor
                        ).exclude(ativo=0).values_list('comissao')
        self.fields['comissao'].queryset = \
            Comissao.objects.distinct().order_by('descricao').filter(id__in=membro)
        self.fields['comissao'].empty_label = 'Selecione a comissão de apoio'

    class Meta:
        model = Reuniao
        exclude = (id, 'situacao', 'anotacao')
        widgets = {
            'data': DateInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a data'
                }),
            'inicio': TimeInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a hora de início'
                }),
            'local': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe o local'
                }),
            'tipo': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione o tipo'
                }),
#            'anotacao': Textarea(attrs={
#                    'class': 'form-control',
#                    'data-rules': 'required',
#                    'placeholder': 'Informe a anotação'
#                }),
            'comissao': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione a comissão'
                }),
        }


class ConvocadoForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de convocados
    """

    def __init__(self, *args, **kwargs):
        if 'professor' in kwargs:
            self.professor = kwargs.pop('professor')
        super (ConvocadoForm, self).__init__(*args, **kwargs)
        membro = Membro.objects.filter(
                            professor=self.professor
                        ).exclude(ativo=0).values_list('comissao')
        comissao = list(Comissao.objects.filter(
                            id__in=membro
                        ).distinct().values_list('curso'))
        versao = Versaocurso.objects.using('sca').filter(
                            curso__in=comissao
                        ).values_list('id')
        self.fields['aluno'].queryset = \
            Aluno.objects.using('sca').filter(
                            versaocurso__in=versao
                        ).distinct().order_by('nome')
        self.fields['aluno'].empty_label = 'Selecione o aluno'

    class Meta:
        model = Convocacao
        exclude = (id, 'reuniao', 'envioemail', 'presente', 'anotacao')
        widgets = {
#            'envioemail': CheckboxInput(attrs={
#                    'class': 'form-control'
#                }),
#            'presente': CheckboxInput(attrs={
#                    'class': 'form-control'
#                }),
#            'anotacao': Textarea(attrs={
#                    'class': 'form-control',
#                    'data-rules': 'required',
#                    'placeholder': 'Informe a anotação'
#                }),
            'aluno': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione o aluno'
                }),
        }


class HorarioForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de previsão de horários
    """

    def __init__(self, *args, **kwargs):
        if 'professor' in kwargs:
            self.professor = kwargs.pop('professor')
        super (HorarioForm, self).__init__(*args, **kwargs)
        curso = Horario.cursos_membros_sql(self.professor)
        self.fields['curso'].queryset = \
            Curso.objects.using('sca').order_by('nome').filter(id__in=curso)
        self.fields['curso'].empty_label = 'Selecione o curso'

    class Meta:
        model = Horario
        exclude = (id, )
        widgets = {
            'ano': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 2018, 'max': 2050, 'step': 1,
                    'empty_label': 'Selecione o ano'}
                ),
            'periodo': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'curso': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione o curso'
                }),
        }


class ItemHorarioForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de itens de uma
    previsão de horário
    """

    def __init__(self, *args, **kwargs):
        periodoAtual = periodo_atual()
        super (ItemHorarioForm, self).__init__(*args, **kwargs)
        self.fields['turma'].queryset = \
            Turma.objects.using('sca').filter(
                            ano=periodoAtual[0], periodo=periodoAtual[1] - 1
                        ).order_by('codigo')
        versoesativas = Versaocurso.objects.using('sca').exclude(situacao=0)
        self.fields['disciplina'].queryset = \
            Disciplina.objects.using('sca').filter(
                            versaocurso__in=versoesativas
                        ).order_by('nome').distinct()
        self.fields['professor'].queryset = \
            Professor.objects.using('sca').order_by('nome').distinct()
        self.fields['periodo'].empty_label = 'Selecione o período'
        self.fields['turma'].empty_label = 'Selecione a turma'
        self.fields['disciplina'].empty_label = 'Selecione a disciplina'
        self.fields['professor'].empty_label = 'Selecione o professor'
        self.fields['departamento'].empty_label = 'Selecione o departamento'

    class Meta:
        model = ItemHorario
        exclude = (id, 'horario', )
        widgets = {
            'periodo': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe o periodo'
                }),
            'turma': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'disciplina': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'professor': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'diasemana': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'inicio': TimeInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a hora de início'
                }),
            'fim': TimeInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a hora final'
                }),
            'departamento': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                })
        }


class AvaliaPlanoForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de avaliação plano de estudos
    """

    class Meta:
        model = Plano
        fields = ['avaliacao']
        widgets = {
            'avaliacao': Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Informe a avaliação'
                })
        }


class DocumentoForm(forms.ModelForm):
    """
    Classe de uso do sistema para o formulário de documentos
    """

    def __init__(self, *args, **kwargs):
        if 'professor' in kwargs:
            self.professor = kwargs.pop('professor')
        super (DocumentoForm, self).__init__(*args, **kwargs)
        membro = Membro.objects.filter(
                            professor=self.professor
                        ).exclude(ativo=0).values_list('comissao')
        comissao = list(Comissao.objects.filter(
                            id__in=membro
                        ).distinct().values_list('curso'))
        versao = Versaocurso.objects.using('sca').filter(
                            curso__in=comissao
                        ).values_list('id')
        self.fields['aluno'].queryset = \
            Aluno.objects.using('sca').filter(
                            versaocurso__in=versao
                        ).distinct().order_by('nome')
        self.fields['aluno'].empty_label = 'Selecione o aluno'

    class Meta:
        model = Documento
        exclude = (id, )
        widgets = {
            'ano': NumberInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'min': 2018, 'max': 2050, 'step': 1,
                    'empty_label': 'Selecione o ano'
                }),
            'periodo': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required'
                }),
            'descricao': TextInput(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'placeholder': 'Informe a descrição do documento'
                }),
            'aluno': Select(attrs={
                    'class': 'form-control',
                    'data-rules': 'required',
                    'empty_label': 'Selecione o aluno'
                }),
#            'indice': TextInput(attrs={
#                    'class': 'form-control',
#                    'data-rules': 'required',
#                    'placeholder': 'Informe o arquivo a ser upladed'
#                }),
        }
