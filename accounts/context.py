from django.conf import settings

from cadd.models import Perfil, Membro
from cadd.utils import tipo_usuario, periodo_atual, proximo_periodo

def context_processors(request):
    """
    Função para a inclusão de variáveis de contexto nos templates
    """

    ret = {}
    if request.user.is_authenticated:
        usuario = Perfil.objects.get(user=request.user.id)
        perAtual = periodo_atual()
        proxPer = proximo_periodo(1)
        ret['matricula'] = usuario.matricula
        ret['idusuario'] = usuario.idusuario
        ret['tipo'] = tipo_usuario(usuario.matricula, 0)
        ret['membro'] = Membro.objects.filter(
                            professor=usuario.idusuario
                        ).values_list('comissao')
        ret['ano'] = perAtual[0]
        ret['periodo'] = perAtual[1]
        ret['periodoatual'] = perAtual[2]
        ret['proxperiodo'] = proxPer[2]
    else:
        ret['matricula'] = ''
        ret['idusuario'] = ''
        ret['tipo'] = ''
        ret['membro'] = ''
        ret['ano'] = ''
        ret['periodo'] = ''
        ret['periodoatual'] = ''
        ret['proxperiodo'] = ''
    return ret
