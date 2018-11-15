# _*_ coding:utf-8 _*_
from os import listdir
#import untangle
from xml.dom import minidom
import sys
erros = 0
acertos = 0
for filename in listdir("/home/rafael/Private/rafael/ufca/software/pesquisa/docentes/"):
    if (str(filename).find(".xml")!=-1):
        with open('/home/rafael/Private/rafael/ufca/software/pesquisa/docentes/' + filename) as currentFile:
            text = currentFile.read()

            try:
                mydoc = minidom.parse(filename)
                items = mydoc.getElementsByTagName('DADOS-GERAIS')
                nomeCompleto = (items[0].attributes['NOME-COMPLETO'].value)
                mydoc = minidom.parse(filename)
                items = mydoc.getElementsByTagName('CURRICULO-VITAE')
                idlattes = items[0].attributes['NUMERO-IDENTIFICADOR'].value
                print(nomeCompleto,idlattes)
                acertos = acertos + 1
            except:
                erros = erros + 1
                e = sys.exc_info()[0]
                print("Erro!",e)
                '''
                if (nomeCompleto in text):
                    if (str(filename).find(".py")==-1):
                        print(filename)
                        mydoc = minidom.parse(filename)
                        items = mydoc.getElementsByTagName('CURRICULO-VITAE')
                        print(items[0].attributes['NUMERO-IDENTIFICADOR'].value)
                '''
print('TERMINOU!')
print("Erros: ", erros)
print("Acertos: ", acertos)
