weights = {
    'FORMACAO-ACADEMICA-TITULACAO' : {'POS-DOUTORADO': 0, 'LIVRE-DOCENCIA': 0, 'DOUTORADO': 0, 'MESTRADO': 0},
    'PROJETO-DE-PESQUISA' : {'PESQUISA': 0, 'DESENVOLVIMENTO': 0},
    'PRODUCAO-BIBLIOGRAFICA' : {
        'ARTIGOS-PUBLICADOS': {'A1': 1, 'A2': 1, 'B1': 1, 'B2': 1, 'B3': 1, 'B4': 1, 'B5': 1, 'C': 1, 'NAO-ENCONTRADO': 1},
        'TRABALHOS-EM-EVENTOS': {
            'INTERNACIONAL': { 'COMPLETO': 1, 'RESUMO_EXPANDIDO': 1, 'RESUMO': 1 },
            'NACIONAL': { 'COMPLETO': 1, 'RESUMO_EXPANDIDO': 1, 'RESUMO': 1 },
            'REGIONAL': { 'COMPLETO': 1, 'RESUMO_EXPANDIDO': 1, 'RESUMO': 1 },
            'LOCAL': { 'COMPLETO': 1, 'RESUMO_EXPANDIDO': 1, 'RESUMO': 1 },
            'NAO_INFORMADO': { 'COMPLETO': 1, 'RESUMO_EXPANDIDO': 1, 'RESUMO': 1 },
        },
        'LIVROS-E-CAPITULOS': {
            'LIVRO-PUBLICADO-OU-ORGANIZADO': {
                'LIVRO_PUBLICADO': 1,
                'LIVRO_ORGANIZADO_OU_EDICAO': 1,
                'NAO_INFORMADO': 1,
            },
            'CAPITULO-DE-LIVRO-PUBLICADO': 1,
        },
        'DEMAIS-TIPOS-DE-PRODUCAO-BIBLIOGRAFICA': { 'TRADUCAO': 0 },
    },
    'PRODUCAO-TECNICA': {
        'SOFTWARE': 0,
        'PATENTE': {'DEPOSITADA': 0, 'CONCEDIDA': 0},
        'PRODUTO-TECNOLOGICO': 0,
        'PROCESSOS-OU-TECNICAS': 0,
        'TRABALHO-TECNICO': 0,
    },
    'OUTRA-PRODUCAO': {
        'PRODUCAO-ARTISTICA-CULTURAL': {
            'APRESENTACAO-DE-OBRA-ARTISTICA': 0,
            'COMPOSICAO-MUSICAL': 0,
            'OBRA-DE-ARTES-VISUAIS': 0,
        },
        'ORIENTACOES-CONCLUIDAS': {
            'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO': 0,
            'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO': {'ORIENTADOR_PRINCIPAL': 0, 'CO_ORIENTADOR': 0},
            'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO': {'ORIENTADOR_PRINCIPAL': 0, 'CO_ORIENTADOR': 0},
            'OUTRAS-ORIENTACOES-CONCLUIDAS': {
                'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO': 0,
                'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO': 0,
                'INICIACAO_CIENTIFICA': 0,
                'ORIENTACAO-DE-OUTRA-NATUREZA': 0,
            },
        },
    },
}