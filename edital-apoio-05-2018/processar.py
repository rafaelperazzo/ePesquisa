# -*- coding: utf-8 -*-
from __future__ import division
import sqlite3
import funcoes
import logging
import sqlite3
import logging
import os
import sys

'''
Calcula a pontuação lattes para cada pesquisador
'''
def calcularScoreLattes(cursor,TABELA):
    consulta = "SELECT B.nome,A.idlattes,A.siape,B.capes from docentes as A,edital_05_2018 as B WHERE A.siape=B.siape ORDER BY nome"
    cursor.execute(consulta)
    i = 1
    for linha in cursor.fetchall():
        idlattes = linha[1]
        siape = linha[2]
        area = linha[3]
        nomeDocente = linha[0]
        logger.info(nomeDocente)
        try:
            #Preparando o parser XML
            tree = ET.parse("../pesquisa/docentes/" + str(idlattes) + ".xml")
            root = tree.getroot()
            score = Score(root,2013, 2018, area, 2016)
            print(score.get_score())
            logger.info(nomeDocente + " - [" + str(score.get_score()) + "]")
            update = "UPDATE " + TABELA + " SET scorelattes=" + str(score.get_score()) + " WHERE siape=" + str(siape)
            cursor.execute(update)
            update = "UPDATE " + TABELA + " SET id=" + str(i) + " WHERE siape=" + str(siape)
            cursor.execute(update)
            i = i + 1
        except:
            e = sys.exc_info()[0]
            logger.error(e)

'''
Faz a distribuição de recursos proporcional por grande área
'''
def distribuir_recursos(cursor, grande_area,recursos,total_projetos,TABELA):
    #print("**********************************")
    logger.info(grande_area)
    #print("**********************************")
    consumo = recursos[0]
    terceiros = recursos[1]
    estudantes = recursos[2]
    #ALOCACAO DE RECURSOS
    consulta = "SELECT COUNT(consumo) FROM " + TABELA + " WHERE grande_area=\"" + grande_area + "\""
    cursor.execute(consulta)
    total_area = cursor.fetchone()[0]
    percentual_disponivel = (total_area/total_projetos)
    consumo_disponivel = consumo*percentual_disponivel
    terceiros_disponivel = terceiros*percentual_disponivel
    estudantes_disponivel = estudantes*percentual_disponivel
    #DISTRIBUIÇÃO ENTRE OS PROJETOS DA ÁREA
    consulta = "SELECT nome,siape,consumo,terceiros,estudantes,scorelattes,id,projeto FROM " + TABELA + " WHERE grande_area=\"" + grande_area + "\"" + " ORDER BY scorelattes DESC"
    cursor.execute(consulta)
    for linha in cursor.fetchall():
        #print(linha)
        consumo_solicitado = linha[2]
        terceiros_solicitado = linha[3]
        estudantes_solicitado = linha[4]
        #MATERIAL DE CONSUMO
        if (consumo_disponivel-consumo_solicitado>=0): #Verifica se é possível atender a solicitação
            consumo_disponivel = consumo_disponivel-consumo_solicitado #Atende a solicitação
            consulta = "UPDATE " + TABELA + " SET consumo_concedido=" + str(consumo_solicitado) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (consumo_solicitado>0):
                logger.info("Contemplando " + str(consumo_solicitado) + " para: " + linha[0] + "(CONSUMO)INTEGRALMENTE")
        else:
            consulta = "UPDATE " + TABELA + " SET consumo_concedido=" + str(consumo_disponivel) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (consumo_disponivel>0):
                logger.info("Contemplando " + str(consumo_disponivel) + " para: " + linha[0] + "(CONSUMO)PARCIALMENTE")
            consumo_disponivel = 0
        #SERVIÇOS DE TERCEIROS
        if (terceiros_disponivel-terceiros_solicitado>=0): #Verifica se é possível atender a solicitação
            terceiros_disponivel = terceiros_disponivel-terceiros_solicitado #Atende a solicitação
            consulta = "UPDATE " + TABELA + " SET terceiros_concedido=" + str(terceiros_solicitado) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (terceiros_solicitado>0):
                logger.info("Contemplando " + str(terceiros_solicitado) + " para: " + linha[0] + "(TERCEIROS)INTEGRALMENTE")
        else:
            consulta = "UPDATE " + TABELA + " SET terceiros_concedido=" + str(terceiros_disponivel) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (terceiros_disponivel>0):
                logger.info("Contemplando " + str(terceiros_disponivel) + " para: " + linha[0] + "(TERCEIROS)PARCIALMENTE")
            terceiros_disponivel = 0

        #AUXÍLIO A ESTUDANTES
        if (estudantes_disponivel-estudantes_solicitado>=0): #Verifica se é possível atender a solicitação
            estudantes_disponivel = estudantes_disponivel-estudantes_solicitado #Atende a solicitação
            consulta = "UPDATE " + TABELA + " SET estudantes_concedido=" + str(estudantes_solicitado) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (estudantes_solicitado>0):
                logger.info("Contemplando " + str(estudantes_solicitado) + " para: " + linha[0] + "(ESTUDANTES)INTEGRALMENTE")
        else: #Tenta atender parcialmente
            consulta = "UPDATE " + TABELA + " SET estudantes_concedido=" + str(estudantes_disponivel) + " WHERE id=" + str(linha[6])
            cursor.execute(consulta)
            if (estudantes_disponivel>0):
                logger.info("Contemplando " + str(estudantes_disponivel) + " para: " + linha[0] + "(ESTUDANTES)PARCIALMENTE")
            estudantes_disponivel = 0

    conn.commit()
    return 0;

def distribuir_recursos_remanescentes(cursor,recursos,TABELA):

    consumo = recursos[0]
    terceiros = recursos[1]
    estudantes = recursos[2]

    #DISTRIBUIÇÃO ENTRE TODOS OS PROJETOS
    consulta = "SELECT nome,siape,consumo,terceiros,estudantes,consumo_concedido,terceiros_concedido,estudantes_concedido,scorelattes,id,projeto FROM " + TABELA + " ORDER BY scorelattes DESC"
    cursor.execute(consulta)
    for linha in cursor.fetchall():
        #print(linha)
        consumo_solicitado = float(linha[2])
        terceiros_solicitado = float(linha[3])
        estudantes_solicitado = float(linha[4])
        consumo_concedido = float(linha[5])
        terceiros_concedido = float(linha[6])
        estudantes_concedido = float(linha[7])
        #MATERIAL DE CONSUMO
        if (consumo_solicitado-consumo_concedido>0): #Verifica se ainda tem o que atender
            if (consumo_solicitado-consumo_concedido<consumo): #Se o que ainda resta atender for menor do que o disponível
                diferenca = consumo_solicitado-consumo_concedido #Atende a solicitação
                novovalor = diferenca + consumo_concedido
                consumo = consumo - diferenca
                consulta = "UPDATE " + TABELA + " SET consumo_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)
                logger.info("COMPLEMENTANDO com " + str(diferenca) + " para: " + linha[0] + "(CONSUMO)")
            else: #Se o que resta for menor do que o que resta atender
                novovalor = consumo_concedido+consumo
                consulta = "UPDATE " + TABELA + " SET consumo_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)

                consumo = 0

        #SERVICOS DE TERCEIROS
        if (terceiros_solicitado-terceiros_concedido>0): #Verifica se ainda tem o que atender
            if (terceiros_solicitado-terceiros_concedido<terceiros): #Se o que ainda resta atender for menor do que o disponível
                diferenca = terceiros_solicitado-terceiros_concedido #Atende a solicitação
                novovalor = diferenca + terceiros_concedido
                terceiros = terceiros - diferenca
                consulta = "UPDATE " + TABELA + " SET terceiros_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)
                logger.info("COMPLEMENTANDO com " + str(diferenca) + " para: " + linha[0] + "(TERCEIROS)")
            else: #Se o que resta for menor do que o que resta atender
                novovalor = terceiros_concedido+terceiros
                consulta = "UPDATE " + TABELA + " SET terceiros_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)
                terceiros = 0

        #AUXÍLIO A ESTUDANTES
        if (estudantes_solicitado-estudantes_concedido>0): #Verifica se ainda tem o que atender
            if (estudantes_solicitado-estudantes_concedido<estudantes): #Se o que ainda resta atender for menor do que o disponível
                diferenca = estudantes_solicitado-estudantes_concedido #Atende a solicitação
                novovalor = diferenca + estudantes_concedido
                estudantes = estudantes - diferenca
                consulta = "UPDATE " + TABELA + " SET estudantes_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)
                logger.info("COMPLEMENTANDO com " + str(diferenca) + " para: " + linha[0] + "(ESTUDANTES)")
            else: #Se o que resta for menor do que o que resta atender
                novovalor = estudantes_concedido+estudantes
                consulta = "UPDATE " + TABELA + " SET estudantes_concedido=" + str(novovalor) + " WHERE id=" + str(linha[9])
                cursor.execute(consulta)
                estudantes = 0
    conn.commit()
    return 0;

def gerarResultados(titulo,cursor):
    cursor.execute("SELECT nome,grande_area,scorelattes FROM edital_05_2018 ORDER BY grande_area,scorelattes DESC")
    docente_grande_area = cursor.fetchall()
    cursor.execute("SELECT grande_area,sum(consumo),sum(consumo_concedido),sum(terceiros),sum(terceiros_concedido),sum(estudantes),sum(estudantes_concedido) FROM edital_05_2018 GROUP BY grande_area")
    resumo_grande_area = cursor.fetchall()
    cursor.execute("SELECT a.nome,b.cpf,(a.consumo_concedido+a.terceiros_concedido+a.estudantes_concedido) as total FROM edital_05_2018 as a, docentes as b WHERE a.siape=b.siape AND total>0 ORDER BY total DESC,nome ASC")
    contemplados = cursor.fetchall()
    cursor.execute("SELECT printf(\'%s(%s)\',nome,scorelattes) as nome,consumo,consumo_concedido,terceiros,terceiros_concedido,estudantes,estudantes_concedido FROM edital_05_2018 ORDER BY grande_area,scorelattes DESC")
    resultados = cursor.fetchall()
    funcoes.gerarPDF(titulo,resultados,contemplados,resumo_grande_area,docente_grande_area)

    return 0

def getRecursosRemanescentes():
    pass

#INICIO DO PROGRAMA PRINCIPAL
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# create a file handler
handler = logging.FileHandler('processar.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
#CONECTANDO AO BANCO DE DADOS
sys.path.append("/home/rafael/Private/rafael/ufca/software/edital-apoio-05-2018/scoreLattes-master")
from scoreLattes import *
reload(sys)
sys.setdefaultencoding('utf-8')
#CONECTANDO AO BANCO DE DADOS
conn = sqlite3.connect('../pesquisa/dados.db')
cursor  = conn.cursor()
TABELA = "edital_05_2018"

#ZERANDO RECURSOS CONCEDIDOS
cursor.execute("UPDATE " + TABELA + " SET consumo_concedido=0, terceiros_concedido=0, estudantes_concedido=0")

#DEFINICAO DOS RECURSOS TOTAIS
consumo = 40000
terceiros = 30000
estudantes = 20000
teto = 10000
recursos = (consumo,terceiros,estudantes,teto)
#TOTAL DE PROJETOS
cursor.execute("SELECT count(*) FROM " + TABELA)
total_projetos = cursor.fetchone()[0]

#PROJETOS POR GRANDE ÁREA
consulta = "SELECT COUNT(consumo), grande_area FROM " + TABELA + " GROUP BY grande_area ORDER BY grande_area"
cursor.execute(consulta)

for linha in cursor.fetchall():
    print(linha[1])
    print ("%.2f" % ((linha[0]/total_projetos)*100))

#calcularScoreLattes(cursor,TABELA)


#DISTRIBUIÇÃO DOS RECURSOS ENTRE AS GRANDES ÁREAS

distribuir_recursos(cursor,"Ciências Biológicas",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Engenharias",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Ciências Exatas e da terra",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Ciências da Saúde",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Ciências Agrárias",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Ciências Sociais Aplicadas",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Ciências Humanas",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Linguística, Letras e Artes",recursos,total_projetos,TABELA)
distribuir_recursos(cursor,"Multidisciplinar",recursos,total_projetos,TABELA)
conn.commit()
#DISTRIBUIÇÃO DE RECURSOS QUE SOBRARAM
cursor.execute("SELECT SUM(consumo_concedido),SUM(terceiros_concedido),SUM(estudantes_concedido) FROM " + TABELA)
linha = cursor.fetchone()
consumo_ramanescente = consumo - linha[0]
terceiros_remanescentes = terceiros - linha[1]
estudantes_remanescentes = estudantes - linha[2]
recursos_remanescentes = (consumo_ramanescente,terceiros_remanescentes,estudantes_remanescentes)
logger.info("Recursos remanescentes")
logger.info("Material de consumo: " + str(recursos_remanescentes[0]))
logger.info("Serviços a terceiros: " + str(recursos_remanescentes[1]))
logger.info("Auxílio a estudantes: " + str(recursos_remanescentes[2]))

distribuir_recursos_remanescentes(cursor,recursos_remanescentes,TABELA)
conn.commit()

cursor.execute("SELECT SUM(consumo_concedido),SUM(terceiros_concedido),SUM(estudantes_concedido) FROM " + TABELA)
linha = cursor.fetchone()
consumo_ramanescente = consumo - linha[0]
terceiros_remanescentes = terceiros - linha[1]
estudantes_remanescentes = estudantes - linha[2]
recursos_remanescentes = (consumo_ramanescente,terceiros_remanescentes,estudantes_remanescentes)
logger.info("Recursos remanescentes")
logger.info("Material de consumo: " + str(recursos_remanescentes[0]))
logger.info("Serviços a terceiros: " + str(recursos_remanescentes[1]))
logger.info("Auxílio a estudantes: " + str(recursos_remanescentes[2]))

#GERAR FOLHA DE RESULTADOS
## TODO: Gerar PDF com RESULTADOS
gerarResultados("Resultado Final - Edital 05/2018/PRPI",cursor)
#GERAR TERMO DE OUTORGA
## TODO: Gerar Termo de Outorga

conn.commit()
conn.close()
