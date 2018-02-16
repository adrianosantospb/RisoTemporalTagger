import sys
from RisoTemporalTagger import *

if (len(sys.argv) != 3 and len(sys.argv) != 4):
    print "Uso: Main.py <ARQUIVO_DE_ENTRADA> <METODO> [<ARQUIVO_DE_CONFIGURACAO>]\n"
    print "Parametros:"
    print "ARQUIVO_DE_ENTRADA eh o arquivo a ser processado"
    print "METODO pode ser TAG, LIST ou NORM"
    print "ARQUIVO_DE_CONFIGURACAO eh o path para o arquivo de configuracao"
    sys.exit(-1)

path_entrada = sys.argv[1]
metodo = sys.argv[2]

riso = RisoTemporalTagger() if len(sys.argv) == 3 else RisoTemporalTagger(sys.argv[3])

try:
	if metodo == "TAG":   
		print riso.tag(path_entrada)
	
	if metodo == "LIST":
		print riso.list(path_entrada)
	
	if metodo == "NORM":
		print riso.normalization(path_entrada)
		
except (KeyboardInterrupt):
    print "Operacao interrompida pelo usuario."
    sys.exit(-1)

#python Main.py WikiWars_20120218_v104\in\01_WW2.sgm LIST config.xml
#python Main.py WikiWars_20120218_v104\in\01_WW2.sgm TAG config.xml > SAIDA.TXT
#python Main.py WikiWars_20120218_v104\in\01_WW2.sgm NORM config.xml > SAIDA.TXT