from tuning import evaluation
from tuning import solr

values = solr.query('art 2 registo civil')
eval = evaluation.ndcg(values, [
    solr.build_article("Código do Registo Civil", 2,
                       "Diploma", "1995-06-06T00:00:00Z")
])

print(eval)