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
import click

#Coletando o ano atual
now = datetime.datetime.now()
anoAtual = now.year

logging.basicConfig(level=logging.DEBUG)
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
#consulta = "SELECT idlattes,siape,area,docente FROM docentes WHERE siape=1570709 ORDER by ua,docente"
#cursor.execute(consulta)
periodo = range(1,6)
for i in periodo:
    consulta = "SELECT idlattes,siape,area,docente FROM docentes ORDER by ua,docente"
    cursor.execute(consulta)
    logger.info("INICIANDO o procedimento para o ano:[" + str(anoAtual) +"] - Passo:" + str(i))
    linhas = cursor.fetchall()
    logger.info("Numero de linhas para o ano: " + str(len(linhas)))
    for linha in linhas:
        idlattes = linha[0]
        siape = linha[1]
        area = linha[2]
        nomeDocente = linha[3]
        logger.info(nomeDocente)
        try:
            #Preparando o parser XML
            tree = ET.parse("docentes/" + str(idlattes) + ".xml")
            root = tree.getroot()
            score = Score(root,anoAtual, anoAtual, area, 2016)
            #Extraindo os dados de interesse
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
            #Iniciando as consultas de atualização
            consulta = "UPDATE docentes SET A1_" + str(i) +  "=" + str(a1) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET A2_" + str(i) +  "=" + str(a2) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET B1_" + str(i) +  "=" + str(b1) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET B2_" + str(i) +  "=" + str(b2) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET B3_" + str(i) +  "=" + str(b3) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET B4_" + str(i) +  "=" + str(b4) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET B5_" + str(i) +  "=" + str(b5) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET C_" + str(i) +  "=" + str(c) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET SC_" + str(i) +  "=" + str(sc) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET evento_completo_internacional_" + str(i) +  "=" + str(eventos_internacional) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET evento_completo_nacional_" + str(i) +  "=" + str(eventos_nacional) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET livro_organizado_" + str(i) +  "=" + str(livro_organizado) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET livro_publicado_" + str(i) +  "=" + str(livro_publicado) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
            consulta = "UPDATE docentes SET capitulo_livro_" + str(i) +  "=" + str(capitulo_de_livro) + " WHERE siape=" + str(siape)
            update(cursor,consulta)
        except:
            e = sys.exc_info()[0]
            logger.error(e)
            logger.error(str(i) + "##" + str(anoAtual))
            logger.error(consulta)
    logger.info("FINALIZANDO o procedimento para o ano:[" + str(anoAtual) +"]")
    anoAtual = anoAtual-1


logger.info("Procedimento finalizado.")
conn.commit()
conn.close()
logger.info("FINAL")
