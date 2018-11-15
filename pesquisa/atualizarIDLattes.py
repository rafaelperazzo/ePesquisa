# _*_ coding:utf-8 _*_
#Python 3
from os import listdir
from xml.dom import minidom
from unidecode import unidecode
import sys
from unicodedata import normalize
import sqlite3

sys.path.insert(0, "/home/rafael/Private/rafael/ufca/software/pesquisa/scoreLattes/")

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

erros = 0
acertos = 0
caminho = "/home/rafael/Private/rafael/ufca/software/pesquisa/docentes/"

#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('dados.db')
cursor  = conn.cursor()

for filename in listdir(caminho):
    if (str(filename).find(".xml")!=-1):
        arquivo = caminho + filename
        try:
            mydoc = minidom.parse(arquivo)
            items = mydoc.getElementsByTagName('DADOS-GERAIS')
            nomeCompleto = (items[0].attributes['NOME-COMPLETO'].value)
            mydoc = minidom.parse(arquivo)
            items = mydoc.getElementsByTagName('CURRICULO-VITAE')
            idlattes = items[0].attributes['NUMERO-IDENTIFICADOR'].value
            nomeCompleto = str(nomeCompleto).encode("utf-8")
            nomeCompleto=remover_acentos(nomeCompleto.decode("utf-8").upper())
            print(nomeCompleto)
            acertos = acertos + 1
            consulta = "UPDATE docentes SET idlattes=\"" + str(idlattes) + "\" WHERE docente=\"" + nomeCompleto + "\""
            cursor.execute(consulta)
            print("Atualizado idlattes de " + nomeCompleto + " para " + str(idlattes))
        except:
            erros = erros + 1
            e = sys.exc_info()[0]
            print("Erro!",e)

print('TERMINOU!')
print("Erros: ", erros)
print("Acertos: ", acertos)
conn.commit()
conn.close()
