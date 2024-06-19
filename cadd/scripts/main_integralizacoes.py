# coding=UTF-8

import collections
import glob, os
import sys, getopt

import plotly.graph_objs as go
import plotly.plotly as py

from plotly.offline import plot

from os.path import basename

from analisador_desempenho_academico import AnalisadorDesempenhoAcademico
from parametros import Parametros
import xlsxwriter

from periodo_letivo import PeriodoLetivo

def plot_agregado_integralizacoes(sigla_curso,
                                  outputdir,
                                  lista_qtd_periodos,
                                  lista_qtd_alunos_por_qtd_periodos_cursados,
                                  qtd_total_alunos,
                                  qtd_alunos_irregulares):
    trace_quantidades = go.Bar(
        x=lista_qtd_periodos,
        y=lista_qtd_alunos_por_qtd_periodos_cursados,
        name='# periodos cursados',
        marker=dict(
            color='rgb(55, 83, 109)'
        )
    )
    data_quantidades = [trace_quantidades]
    
    layout_quantidades = go.Layout(
        title='<b>Gráfico: "Quantidades de alunos" versus "Qtd. de períodos cursados"</b>' + 
            '\n Curso: ' + sigla_curso + 
            '\n Período base: ' + str(Parametros.ANO_BASE) + '.' + str(Parametros.PERIODO_BASE) + 
            '\n Total/irregulares: ' + str(qtd_total_alunos) + '/' + str(qtd_alunos_irregulares),
        xaxis=dict(
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis=dict(
            title='qtd de alunos',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )
    fig = go.Figure(data=data_quantidades, layout=layout_quantidades)
    plot(fig, filename=outputdir + '/' + sigla_curso + '-periodos-cursados.html')

def processar_integralizacoes(planilha, outputdir):
    sigla_curso = os.path.splitext(basename(planilha))[0]

    mapa_alunos = AnalisadorDesempenhoAcademico.construir_mapa_alunos(planilha)
    mapas = AnalisadorDesempenhoAcademico.construir_mapas_periodos(planilha, mapa_alunos)
    mapa_periodos_cursados_por_aluno = mapas[0]
    mapa_trancamentos_totais_por_aluno = mapas[1]

    # Create a workbook and add a worksheet.
    filename = os.path.splitext(planilha)[0] + '-periodos-cursados.xlsx'
    filename = outputdir + '/' + basename(filename)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('Detalhado')
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    
    # Write some data headers.
    worksheet.write('A1', 'matricula_aluno', bold)
    worksheet.write('B1', 'nome_aluno', bold)
    worksheet.write('C1', 'qtd_periodos_cursados', bold)
    worksheet.write('D1', 'qtd_trancamentos', bold)
    
    # Start from the first cell below the headers.
    row = 1
    col = 0
    
    width_coluna_nome = 0

    for matr_aluno, qtd_periodos_cursados in mapa_periodos_cursados_por_aluno.items():
        if matr_aluno in mapa_trancamentos_totais_por_aluno:
            qtd_trancamentos = mapa_trancamentos_totais_por_aluno[matr_aluno]
        else:
            qtd_trancamentos = 0
        worksheet.write(row, col, matr_aluno)

        aluno = mapa_alunos[matr_aluno]
        worksheet.write(row, col + 1, aluno.nome.decode('latin-1'))
        width_coluna_nome = max(width_coluna_nome, len(aluno.nome.decode('latin-1')))

        worksheet.write(row, col + 2, qtd_periodos_cursados)
        
        worksheet.write(row, col + 3, qtd_trancamentos)

        row += 1

    worksheet.set_column(col, col, len('matricula_aluno'))
    worksheet.set_column(col + 1, col + 1, width_coluna_nome)
    worksheet.set_column(col + 2, col + 2, len('qtd_periodos_cursados'))
    worksheet.set_column(col + 3, col + 3, len('qtd_trancamentos'))

    print 'Quantidade de alunos com matrícula ativa: %s' % len(mapa_periodos_cursados_por_aluno)

    mapa_qtd_alunos_por_qtd_periodos_cursados = {}
    for (matr_aluno, qtd_periodos_cursados) in mapa_periodos_cursados_por_aluno.iteritems():
        if qtd_periodos_cursados in mapa_qtd_alunos_por_qtd_periodos_cursados:
            mapa_qtd_alunos_por_qtd_periodos_cursados[qtd_periodos_cursados] = mapa_qtd_alunos_por_qtd_periodos_cursados[qtd_periodos_cursados] + 1
        else:
            mapa_qtd_alunos_por_qtd_periodos_cursados[qtd_periodos_cursados] = 1
    
    qtd_alunos_irregulares = 0
    qtd_total_alunos = 0
    for (lista_qtd_periodos, qtd_alunos) in mapa_qtd_alunos_por_qtd_periodos_cursados.iteritems():
        qtd_total_alunos = qtd_total_alunos + qtd_alunos
        if lista_qtd_periodos > Parametros.mapa_qtd_maxima_periodos_integralizacao[sigla_curso]:
            qtd_alunos_irregulares = qtd_alunos_irregulares + qtd_alunos

    print "Qtd. total alunos: %d." % qtd_total_alunos 
    print "Qtd. alunos irregulares: %d." % qtd_alunos_irregulares 

    worksheet = workbook.add_worksheet('Agregado')
    
    # Write some data headers.
    worksheet.write('A1', 'qtd_periodos_cursados', bold)
    worksheet.write('B1', 'qtd_alunos', bold)
    
    # Start from the first cell below the headers.
    row = 1
    col = 0

    for key, value in mapa_qtd_alunos_por_qtd_periodos_cursados.items():
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, value)
        row += 1
    
    worksheet.set_column(col, col, len('qtd_periodos_cursados'))
    worksheet.set_column(col + 1, col + 1, len('qtd_alunos'))
    workbook.close()
    
    mapa_qtd_alunos_por_qtd_periodos_cursados = collections.OrderedDict(sorted(mapa_qtd_alunos_por_qtd_periodos_cursados.items()))
    
    lista_qtd_periodos = mapa_qtd_alunos_por_qtd_periodos_cursados.keys();
    lista_qtd_alunos_por_qtd_periodos_cursados = mapa_qtd_alunos_por_qtd_periodos_cursados.values()

    plot_agregado_integralizacoes(sigla_curso, outputdir, lista_qtd_periodos, lista_qtd_alunos_por_qtd_periodos_cursados, qtd_total_alunos, qtd_alunos_irregulares)

def main(argv):
    
    print 'Período letivo base: %s/%s' % (Parametros.ANO_BASE, Parametros.PERIODO_BASE)
    
    inputdir = ''
    outputdir = ''
    
    try:
        opts, args = getopt.getopt(argv, "hp:i:o:", ["idir=", "odir="])
    except getopt.GetoptError:
        print 'main.py -i <inputdir> -o <outputdir>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -i <inputdir> -o <outputdir>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
        elif opt == "-p":
            componentes = arg.split('.')
            if len(componentes) == 2:
                Parametros.ANO_BASE = int(componentes[0])
                Parametros.PERIODO_BASE = int(componentes[1])
                print PeriodoLetivo.fromstring(arg)
            else:
                sys.exit()
    
    print 'Input dir: ', inputdir
    print 'Output dir:', outputdir
    
    py.sign_in('edubezerra', 'ljf3zy0ivj')

    os.chdir(inputdir)
    for planilha in glob.glob("*.csv"):
        print 'Iniciando processamento do arquivo %s...' % planilha    
        processar_integralizacoes(planilha, outputdir)

if __name__ == "__main__":
    main(sys.argv[1:])
