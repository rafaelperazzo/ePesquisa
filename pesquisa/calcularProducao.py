# _*_ coding:utf-8 _*_
#Python 2
import os
from xml.dom import minidom
from unidecode import unidecode
import sys
from unicodedata import normalize
import sqlite3
import logging
import datetime

#Coletando o ano atual
now = datetime.datetime.now()
anoAtual = now.year

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
# create a file handler
handler = logging.FileHandler('calcularProducao.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

def update(cursor,consulta):
    cursor.execute(consulta)

sys.path.append("/home/rafael/Private/rafael/ufca/software/pesquisa/scoreLattes-master")
from scoreLattes import *
reload(sys)
sys.setdefaultencoding('utf-8')
#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('dados.db')
cursor  = conn.cursor()

#INICIANDO A CONTAGEM
consulta = "SELECT idlattes,siape,area,docente FROM docentes ORDER by docente"
cursor.execute(consulta)
logger.info("Iniciando o procedimento.")
for linha in cursor.fetchall():
    idlattes = linha[0]
    siape = linha[1]
    area = linha[2]
    nomeDocente = linha[3]
    logger.info(nomeDocente)
    try:
        tree = ET.parse("docentes/" + str(idlattes) + ".xml")
        root = tree.getroot()
        score = Score(root,2013, 2018, area, 2016)
        tabela = score.getTabelaQualificacao()
        a1 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['A1']
        a2 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['A2']
        b1 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['B1']
        b2 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['B2']
        b3 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['B3']
        b4 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['B4']
        b5 = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['B5']
        c = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['C']
        sc = tabela['PRODUCAO-BIBLIOGRAFICA']['ARTIGOS-PUBLICADOS']['NAO-ENCONTRADO']
        eventos_internacional = tabela['PRODUCAO-BIBLIOGRAFICA']['TRABALHOS-EM-EVENTOS']['INTERNACIONAL']['COMPLETO']
        eventos_nacional = tabela['PRODUCAO-BIBLIOGRAFICA']['TRABALHOS-EM-EVENTOS']['NACIONAL']['COMPLETO']
        livro_publicado = tabela['PRODUCAO-BIBLIOGRAFICA']['LIVROS-E-CAPITULOS']['LIVRO-PUBLICADO-OU-ORGANIZADO']['LIVRO_PUBLICADO']
        livro_organizado = tabela['PRODUCAO-BIBLIOGRAFICA']['LIVROS-E-CAPITULOS']['LIVRO-PUBLICADO-OU-ORGANIZADO']['LIVRO_ORGANIZADO_OU_EDICAO']
        capitulo_de_livro = tabela['PRODUCAO-BIBLIOGRAFICA']['LIVROS-E-CAPITULOS']['CAPITULO-DE-LIVRO-PUBLICADO']
        consulta = "UPDATE docentes SET A1=" + str(a1) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET A2=" + str(a2) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET B1=" + str(b1) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET B5=" + str(b5) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET B2=" + str(b2) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET B3=" + str(b3) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET B4=" + str(b4) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET C=" + str(c) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET SC=" + str(sc) + " WHERE siape=\"" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET evento_completo_internacional=" + str(eventos_internacional) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET evento_completo_nacional=" + str(eventos_nacional) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET livro_publicado=" + str(livro_publicado) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET livro_organizado=" + str(livro_organizado) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        consulta = "UPDATE docentes SET capitulo_livro=" + str(capitulo_de_livro) + " WHERE siape=" + str(siape)
        update(cursor,consulta)
        #print ("%d,%s,%f" % ( tabela['PRODUCAO-BIBLIOGRAFICA']['TRABALHOS-EM-EVENTOS']['INTERNACIONAL']['COMPLETO'], score.get_name().upper(), score.get_score() ))
    except:
        e = sys.exc_info()[0]
        logger.error(e)
logger.info("Procedimento finalizado.")
conn.commit()
conn.close()
logger.info("FINAL")
