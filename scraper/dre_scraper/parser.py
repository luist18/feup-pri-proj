import requests
import json

import dre_scraper.config.headers as request_headers
import dre_scraper.config.body as request_body
import dre_scraper.config.urls as request_urls
from dre_scraper.model import Article, Book

file = open("../../data.json")

body = json.loads(file.read())


def parse_books():
    headers = {
        'authority': 'dre.pt',
        'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40',
        'content-type': 'application/json; charset=UTF-8',
        'accept': 'application/json',
        'outsystems-request-token': '2734480502774848',
        'x-csrftoken': 'T6C+9iB49TLra4jEsMeSckDMNhQ=',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://dre.pt',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://dre.pt/dre/legislacao-consolidada-destaques',
        'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
        'cookie': 'COOKIE_SUPPORT=true; osVisitor=a9384b17-e10b-4e42-982f-fac7e1fbd247; nr1Users=lid%3dAnonymous%3btuu%3d0%3bexp%3d0%3brhs%3dXBC1ss1nOgYW1SmqUjSxLucVOAg%3d%3bhmc%3dJtcVf7R%2feKL81mKfj9zspoL6b6Q%3d; nr2Users=crf%3dT6C%2b9iB49TLra4jEsMeSckDMNhQ%3d%3buid%3d0%3bunm%3d; osVisit=446c9236-7b24-472c-8162-f19c3c125f8a',
    }

    data = '{"versionInfo":{"moduleVersion":"xe0bdohhZvclrbKCWScnvg","apiVersion":"iR7w6FNd0uMHUhmIEWU_Vg"},"viewName":"LegislacaoConsolidada.LegCons","screenData":{"variables":{"Search":"","IsRended":false,"RegimeJuridico":true,"ResultsCountAT":{"Took":"0","Timed_out":false,"shards":{"Total":"0","Successful":"0","Skipped":"0","Failed":"0"},"Hits":{"Total":{"Value":"0","Relation":""},"Max_score":"0","Hits":{"List":[],"EmptyListItem":{"index":"","type":"","id":"","score":"0","source":{"NumeroInt":"0","DataPublicacaoAJ":"1900-01-01","DocType":"","Visibility":"","Conteudo":false,"Vigencia":"","Title_bst_10k":"","TextoEntradaVigor":"","Type":"","TipoAssociacao":{"List":[],"EmptyListItem":""},"NumeroFonte":"","Descritor":{"List":[],"EmptyListItem":""},"Emissor":"","Ano":"","Paginas":"","TipoAJ":"","SerieNR":"","Suplemento":"","OrdemDR":"","Texto":"","ConteudoId":"0","EntidadePrincipal":"","DataPublicacao":"1900-01-01","EntidadeEmitente":"","DataDistribuicao":"1900-01-01","PaginaFinal":"0","Numero":"","FileId":"0","AjPublica":false,"TipoConteudo":"","Tratamento":false,"EntidadeResponsavel":"","NumeroAJ":"","DbId":"0","Nota":{"List":[],"EmptyListItem":""},"Thesaurus_descritor_eq":"","DataAssinatura":"1900-01-01","Thesaurus_descritor_np":{"List":[],"EmptyListItem":""},"WhenSearchable":"","Id":"","Fragmentado":false,"Title":"","Ordem":"0","ConteudoTitle":"","ClassName":"","NumeroDR":"","DataEntradaVigor":"1900-01-01T00:00:00","PaginaInicial":"0","Acronimo":"","TextoAssociacao":"","Serie":"","CreationDate":"1900-01-01T00:00:00","Descritor_texto":"","ResumoAJ":"","Sumario":"","Regional":false,"Views":"0","Fonte":"","Tipo":"","ModificationDate":"1900-01-01T00:00:00","Thesaurus_descritor":{"List":[],"EmptyListItem":""},"EmissorEN":"","Parte":"","TipoEN":"","TextoNota":"","resumo":"","resumoEN":"","Designacao":"","ConsolidacaoType":"","DiplomaBase":"","concelho":"","empresa":"","assunto":"","consolidacaoEstado":"","IsSelected":false},"Highlight":{"Title":{"List":[],"EmptyListItem":""},"Sumario":{"List":[],"EmptyListItem":""},"Designacao":{"List":[],"EmptyListItem":""},"Texto":{"List":[],"EmptyListItem":""}}}}},"aggregations":{"SerieAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"TipoAtoAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"TipoConteudoAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"EntidadeEmitenteAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"EntidadeProponenteAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"EntidadePrincipalAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"TipoConteudoAggOutros":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"EmissorAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"CalendarioAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"JurisprudenciaAgg":{"doc_count_error_upper_bound":"0","sum_other_doc_count":"0","buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}},"JurisAggs":{"buckets":{"List":[],"EmptyListItem":{"key":"","doc_count":"0","key_as_string":"","isActive":false}}}}}}},"clientVariables":{"NewUser":"https://dre.pt/dre/utilizador/registar","PesquisaAvancada":"https://dre.pt/dre/pesquisa-avancada","NIC":"","UtilizadorPortalIdOld":"0","Login":"https://dre.pt/dre/utilizador/entrar","TotalResultados":0,"Search":false,"DicionarioJuridicoId":"0","FullHTMLURL_EN":"https://dre.pt/dre/en","Name":"","ShowResult":false,"EntityId_Filter":0,"BookId_Filter":0,"Email":"","paginaJson":"","Pesquisa":"","CookiePath":"/dre/","DataInicial_Filter":"1900-01-01","Query_Filter":"","UtilizadorPortalId":"0","t":"","Session_GUID":"605771f4-558f-4237-8cd1-99d2e92f7e93","ActoLegislativoId_Filter":0,"FullHTMLURL":"https://dre.pt/dre/home","TipoDeUtilizador":"","DataFinal_Filter":"1900-01-01","GUID":"","IsColecaoLegislacaoFilter":true}}'

    response = requests.post(
        'https://dre.pt/dre/screenservices/DRE/LegislacaoConsolidada/LegCons/DataActionGetRegimesJuridicos', headers=headers, data=data)
    pass
