from django.urls import path

from . import views

app_name = 'cadd'
urlpatterns = [
    ### Perfil Administrador ###
    # Configurações do sistema
    path('editar-parametros/', views.editar_parametros, name='editar_parametros'),

    # Manter Comissões
    path('lista-comissoes/', views.lista_comissoes, name='lista_comissoes'),
    path('nova-comissao/', views.nova_comissao, name='nova_comissao'),
    path('editar-comissao/?<id_comissao>', views.editar_comissao, name='editar_comissao'),
    path('excluir-comissao/?<id_comissao>', views.excluir_comissao, name='excluir_comissao'),

    path('lista-membros/?<id_comissao>', views.lista_membros, name='lista_membros'),
    path('novo-membro/?<id_comissao>', views.novo_membro, name='novo_membro'),
    path('editar-membro/?<id_membro>&<id_comissao>', views.editar_membro, name='editar_membro'),
    path('excluir-membro/?<id_membro>&<id_comissao>', views.excluir_membro, name='excluir_membro'),

    ### Perfil Membro da CADD ###
    # Agendar Reuniões
    path('lista-reunioes/', views.lista_reunioes, name='lista_reunioes'),
    path('nova-reuniao/', views.nova_reuniao, name='nova_reuniao'),
    path('editar-reuniao/?<id_reuniao>', views.editar_reuniao, name='editar_reuniao'),
    path('excluir-reuniao/?<id_reuniao>', views.excluir_reuniao, name='excluir_reuniao'),

    path('lista-convocados/?<id_reuniao>', views.lista_convocados, name='lista_convocados'),
    path('novo-convocado/?<id_reuniao>', views.novo_convocado, name='novo_convocado'),
    path('editar-convocado/?<id_convocado>&<id_reuniao>', views.editar_convocado, name='editar_convocado'),
    path('excluir-convocado/?<id_convocado>&<id_reuniao>', views.excluir_convocado, name='excluir_convocado'),

    # Manter Prévias de horário
    path('lista-horarios/', views.lista_horarios, name='lista_horarios'),
    path('novo-horario/', views.novo_horario, name='novo_horario'),
    path('editar-horario/?<id_horario>', views.editar_horario, name='editar_horario'),
    path('excluir-horario/?<id_horario>', views.excluir_horario, name='excluir_horario'),

    path('lista-itenshorario/?<id_horario>', views.lista_itenshorario, name='lista_itenshorario'),
    path('novo-itemhorario/?<id_horario>', views.novo_itemhorario, name='novo_itemhorario'),
    path('editar-itemhorario/?<id_itemhorario>&<id_horario>', views.editar_itemhorario, name='editar_itemhorario'),
    path('excluir-itemhorario/?<id_itemhorario>&<id_horario>', views.excluir_itemhorario, name='excluir_itemhorario'),

    # Avaliação dos planos de estudos
    path('avalia-plano/?<id_aluno>', views.avalia_plano, name='avalia_plano'),

    # Anexar documentos
    path('lista-documentos/', views.lista_documentos, name='lista_documentos'),
    path('novo-documento/', views.novo_documento, name='novo_documento'),
    path('excluir-documento/?<id_documento>', views.excluir_documento, name='excluir_documento'),

    # Relatórios
    path('relatorio-situacao/', views.relatorio_situacao, name='relatorio_situacao'),
    path('relatorio-conflitos/', views.relatorio_conflitos, name='relatorio_conflitos'),
    path('relatorio-ata/', views.relatorio_ata, name='relatorio_ata'),
    path('relatorio-atendimentos/', views.relatorio_atendimentos, name='relatorio_atendimentos'),
    path('relatorio-ausencia/', views.relatorio_ausencia, name='relatorio_ausencia'),
    path('relatorio-excepcionais/', views.relatorio_excepcionais, name='relatorio_excepcionais'),

    ### Perfil Aluno ###
    # Montar planos de estudos
    path('lista-planos/', views.lista_planos, name='lista_planos'),
    path('novo-plano-previa/', views.novo_plano_previa, name='novo_plano_previa'),
    path('novo-plano-futuro/', views.novo_plano_futuro, name='novo_plano_futuro'),
    path('lista_planos_avaliar/', views.lista_planos_avaliar, name='lista_planos_avaliar'),
]
