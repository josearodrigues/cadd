import main_faixas_criticidade
import main_integralizacoes
import main_reprovacoes

args = ['-p', '2017.1', '-i', '../data', '-o', '../resultados']

main_faixas_criticidade.main(args)
main_integralizacoes.main(args)
main_reprovacoes.main(args)
