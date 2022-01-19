import math


def ndcg(results, expected):
    """
    Compute the normalized discounted cumulative gain (NDCG) of the results
    against the expected results.

    The relevance grade is the inverse order of the list. E.g. [3, 2, 1]
    """
    len_expected = len(expected)

    dcg = 0.0
    for i, result in enumerate(results):
        if result in expected:
            relevance_grade = len_expected - expected.index(result)
            dcg += (2 ** relevance_grade - 1) / math.log(i + 2, 2)
    idcg = 0.0
    for i, result in enumerate(expected):
        relevance_grade = len_expected - i
        idcg += (2 ** relevance_grade - 1) / math.log(i + 2, 2)

    return dcg / idcg
