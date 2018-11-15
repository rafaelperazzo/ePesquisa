# -*- coding: utf-8 -*-
import os
import sqlite3
import click
from time import sleep
from unidecode import unidecode
import sys
from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

#reload(sys)
#sys.setdefaultencoding('utf-8')
#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('../pesquisa/dados.db')
cursor  = conn.cursor()

consulta = "SELECT nome,siape FROM edital_05_2018 ORDER by nome"
cursor.execute(consulta)

for linha in cursor.fetchall():
    nome = linha[0]
    siape = linha[1]
    nome = remover_acentos(nome)
    consulta = "UPDATE edital_05_2018 SET nome=\"" + nome + "\"" + " WHERE siape=" + str(siape)
    #print(consulta)
    cursor.execute(consulta)

conn.commit()
conn.close()
