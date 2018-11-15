# -*- coding: utf-8 -*-
from __future__ import division
from fpdf import FPDF
import datetime
from unicodedata import normalize

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def imprimirData():
    Meses=('janeiro','fevereiro','mar','abril','maio','junho',
       'julho','agosto','setembro','outubro','novembro','dezembro')
    agora = datetime.date.today()
    dia = agora.day
    mes=(agora.month-1)
    mesExtenso = Meses[mes]
    ano = agora.year
    resultado = str(dia) + " de " + mesExtenso + " de " + str(ano) + "."
    return resultado

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('cabecalho.png', 90, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 10)
        # Move to the right
        # Title
        self.ln(35)
        self.cell(70)
        self.cell(50, 5, u'MINISTÉRIO DA EDUCAÇÃO', 0, 1, 'C')
        self.cell(70)
        self.cell(50, 5, u'UNIVERSIDADE FEDERAL DO CARIRI', 0, 1, 'C')
        self.cell(70)
        # Line break
        self.cell(50, 5, u'PRÓ-REITORIA DE PESQUISA, PÓS-GRADUAÇÃO E INOVAÇÃO', 0, 1, 'C')
        self.cell(70)
        self.cell(50, 5, u'COORDENADORIA DE PESQUISA', 0, 1, 'C')

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-55)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        self.cell(0,5,u"Juazeiro do Norte, " + imprimirData(),0,1,'R')
        self.ln(5)
        self.image('rodape.png', 5, 250, 200)
        self.cell(0, 5, 'DOCUMENTO ASSINADO DIGITALMENTE ' , 0, 1, 'C')
        #self.cell(0, 5, 'Autenticidade pode ser verificada em: http://prpi.ufca.edu.br ' , 0, 1, 'C')

def imprimirTabela(pdf,linhas,header,sizes):
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    pdf.set_font('Times', 'B', 8)
    #header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    i=0
    for datum in header:
        pdf.cell(sizes[i], th, str(datum), border=1,align='C')
        i = i + 1
    pdf.ln(th)
    pdf.set_font('Times', '', 9)
    for linha in linhas:
        i=0
        for datum in linha:
            if isinstance(datum,unicode):
                pdf.cell(col_width*1.6, th, str(datum), border=1)
            else:
                pdf.cell(col_width/2.5, th, str("R$ {:0.2f}".format(datum)), border=1)
            i = i + 1
        pdf.ln(th)


def imprimirContemplatos(pdf,linhas,header,sizes):
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    pdf.set_font('Times', 'B', 8)
    #header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    '''i=0
    for datum in header:
        pdf.cell(sizes[i], th, str(datum), border=1,align='C')
        i = i + 1
    pdf.ln(th)'''
    pdf.set_font('Times', '', 9)
    for linha in linhas:
        i=0
        for datum in linha:
            if isinstance(datum,unicode):
                #datum = remover_acentos(datum)
                pdf.cell(col_width*1.6, th, str(datum), border=1)
            else:
                pdf.cell(col_width/2.5, th, str("R$ {:0.2f}".format(datum)), border=1)

            i = i + 1
        pdf.ln(th)

def imprimirResumoGrandeArea(pdf,linhas,header,sizes):
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    pdf.set_font('Times', 'B', 8)
    #header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    i=0
    for datum in header:
        pdf.cell(sizes[i], th, unicode(datum), border=1,align='C')
        i = i + 1
    pdf.ln(th)
    pdf.set_font('Times', '', 9)
    for linha in linhas:
        i=0
        for datum in linha:
            if isinstance(datum,unicode):
                pdf.cell(col_width*1.6, th, unicode(datum), border=1)
            else:
                pdf.cell(col_width/2.5, th, str("R$ {:0.2f}".format(datum)), border=1)

            i = i + 1
        pdf.ln(th)

def imprimirDocentesPorGrandeArea(pdf,linhas,header,sizes):
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    pdf.set_font('Times', 'B', 8)
    #header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    i=0
    for datum in header:
        pdf.cell(sizes[i], th, unicode(datum), border=1,align='C')
        i = i + 1
    pdf.ln(th)
    pdf.set_font('Times', '', 8)
    for linha in linhas:
        i=0
        for datum in linha:
            if isinstance(datum,unicode):
                pdf.cell(col_width*1.6, th, unicode(datum), border=1)
            else:
                pdf.cell(col_width/2.5, th, str("{:0.1f}".format(datum)), border=1)

            i = i + 1
        pdf.ln(th)

def gerarPDF(titulo,linhas,linhas2,linhas3,linhas4):
    pdf = PDF(orientation = 'P')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    ## TODO: Ajustar margens
    pdf.set_margins(7,7,7)
    pdf.ln(10)
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 10, titulo, 0, 1,'C')
    pdf.ln(1)
    pdf.set_font('Times', '', 12)
    pdf.ln(5)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    pdf.set_font('Times','B',14.0)
    #pdf.cell(epw, 0.0, u'Distribuição de recursos', align='C')
    pdf.set_font('Times','',10.0)
    pdf.ln(0.5)
    th = pdf.font_size

    #TABELA DE RESULTADOS
    pdf.set_font('Times', 'B', 8)
    header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    sizes = (col_width*1.6,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5)
    imprimirTabela(pdf,linhas,header,sizes)

    #header = ('Nome',u'Scorelattes',u'Grande Área')
    #sizes = (col_width*1.6,col_width/2.5,col_width/2.5)
    #imprimirTabela(pdf,linhas2,header,sizes)

    '''
    header = ('Nome','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Aux.Est(S)','Aux.Est(C)')
    sizes = (col_width*1.6,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5)
    imprimirTabela(pdf,linhas,header,sizes)
    '''
    #LEGENDA
    pdf.set_font('Times', '', 7)
    pdf.cell(0, 3, "Legenda: (S) - Solicitado; (C) - Concedido", 0, 1,'J')
    #pdf.cell(0, 3, u"Resultado sujeito a mudança após recursos.", 0, 1,'J')
    pdf.cell(0, 3, u"Tabela ordenada por Grande Área e pontuação lattes.", 0, 1,'J')
    pdf.cell(0, 3, u"Resultado gerado automaticamente via software. Software disponível em prpi.ufca.edu.br.", 0, 1,'J')

    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 10, "Lista de Contemplados - Edital 05/2018/PRPI", 0, 1,'C')
    pdf.ln(10)
    header = ('Nome','CPF','TOTAL')
    sizes = (col_width*1.6,col_width*1.6,col_width/2.5)
    imprimirContemplatos(pdf,linhas2,header,sizes)

    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 10, u"Docentes por grande área - Edital 05/2018/PRPI", 0, 1,'C')
    pdf.ln(10)
    header = (u'Docente',u'Grande Área','Scorelattes')
    sizes = (col_width*1.6,col_width*1.6,col_width/2.5)
    pdf.set_font('Times', '', 10)
    imprimirDocentesPorGrandeArea(pdf,linhas4,header,sizes)

    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 10, u"Resumo por grande área - Edital 05/2018/PRPI", 0, 1,'C')
    pdf.ln(10)
    header = (u'GRANDE ÁREA','Consumo(S)','Consumo(C)','Terceiros(S)','Terceiros(C)','Estudantes(S)','Estudantes(C)')
    sizes = (col_width*1.6,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5,col_width/2.5)
    imprimirResumoGrandeArea(pdf,linhas3,header,sizes)
    #LEGENDA
    pdf.set_font('Times', '', 7)
    pdf.cell(0, 3, "Legenda: (S) - Solicitado; (C) - Concedido", 0, 1,'J')
    pdf.cell(0, 3, u"Resultado gerado automaticamente via software. Disponível em prpi.ufca.edu.br.", 0, 1,'J')

    '''
    pdf.cell(0,5,u"Juazeiro do Norte, " + imprimirData(),0,1,'R')
    pdf.image('assinatura.jpg', 90, 220, 66)
    pdf.line(60,200,150,200)
    pdf.ln(20)
    pdf.cell(0,5,u"RAFAEL PERAZZO BARBOSA MOTA",0,1,'C')
    pdf.cell(0,5,u"COORDENADOR DE PESQUISA",0,1,'C')
    pdf.cell(0,5,u"SIAPE: 1570709",0,1,'C')
    '''
    pdf.output('resultados.pdf', 'F')
