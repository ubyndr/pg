def region_list_query():
    return 'SELECT DISTINCT ?s { ?s a :region . }'


def varietal_list_query():
    return 'SELECT DISTINCT ?s { ?s rdfs:subClassOf :varietal . }'


def wine_list_query():
    return """ SELECT DISTINCT ?s { { ?s owl:equivalentClass ?b0. ?b0 owl:intersectionOf ?b1. ?b1 rdf:first :wine . }
            UNION {?s rdfs:subClassOf :wine . } }"""


def wine_query(colour, varietal, region):
    c = ':' + colour if colour else '?colour'
    v = ':' + varietal if varietal else '?varietal'
    r = ':' + region if region else '?region'
    return """SELECT DISTINCT ?s {
           ?s rdfs:subClassOf ?cnode. ?cnode owl:onProperty :has_color. ?cnode owl:someValuesFrom %s.
           ?s rdfs:subClassOf ?vnode. ?vnode owl:onProperty :made_from. ?vnode owl:someValuesFrom %s.
           ?s rdfs:subClassOf ?rnode. ?rnode owl:onProperty :grown_in. ?rnode owl:hasValue %s.}""" % (c, v, r)


def get_result(graph, query):
    result = []
    query_result = graph.query(query)
    for row in query_result:
        result.append(row.s.n3(graph.namespace_manager))
    return result
