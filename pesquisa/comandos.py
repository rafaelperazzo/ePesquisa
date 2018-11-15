import os
import sys
import sqlite3
import click
from time import sleep

reload(sys)
sys.setdefaultencoding('utf-8')
#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('dados.db')
cursor  = conn.cursor()

consulta = "SELECT idlattes,siape,area,docente FROM docentes ORDER by docente"
cursor.execute(consulta)
print(len(cursor.fetchall()))



with click.progressbar(range(317)) as bar:
    for i in bar:
        sleep(0.01)
        print(i)

for linha in cursor.fetchall():
    idlattes = linha[0]
    siape = linha[1]
    #print(linha[1])

conn.close()
