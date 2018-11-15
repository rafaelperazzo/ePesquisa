# _*_ coding:utf-8 _*_
import sqlite3
import logging
import os
import sys

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
# create a file handler
handler = logging.FileHandler('criarColunasUltimos5Anos.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

def update(cursor,consulta):
    cursor.execute(consulta)

reload(sys)
sys.setdefaultencoding('utf-8')
#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('dados.db')
cursor  = conn.cursor()

periodo = range(1,6)

for i in periodo:
    try:
        campo = "A1_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "A2_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "B1_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "B2_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "B3_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "B4_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "B5_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "C_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "SC_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "evento_completo_internacional_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "evento_completo_nacional_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "livro_publicado_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "livro_organizado_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
        campo = "capitulo_livro_" + str(i)
        update(cursor,"ALTER TABLE docentes ADD " + campo + " INTEGER")
    except:
        e = sys.exc_info()[0]
        logger.error(e)

#Mostando como ficou a tabela
meta = cursor.execute("PRAGMA table_info('docentes')")
for r in meta:
    print (r)


logger.info("Procedimento finalizado.")
conn.commit()
conn.close()
logger.info("FINAL")
