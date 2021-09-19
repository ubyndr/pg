import unittest
import rdflib
from utils import queryUtils as qu


class TestQueryUtils(unittest.TestCase):
    def test_list_query_length(self):
        # Test list query length
        self.assertEqual(len(qu.region_list_query()), 37)
        self.assertEqual(len(qu.varietal_list_query()), 53)
        self.assertEqual(len(qu.wine_list_query()), 153)

    def test_wine_query_length(self):
        # Test wine_query length, check if the queries are not corrupted
        test_input = {'region': 'Kalecik', 'colour': 'red', 'varietal': 'Kalecik Karası'}
        self.assertEqual(len(qu.wine_query('', '', '')), 337)
        self.assertEqual(len(qu.wine_query(test_input['region'], '', '')), 338)
        self.assertEqual(len(qu.wine_query('', test_input['colour'], '')), 332)
        self.assertEqual(len(qu.wine_query('', '', test_input['varietal'])), 345)
        self.assertEqual(len(qu.wine_query(test_input['region'], test_input['colour'], test_input['varietal'])), 341)

    def test_wine_query_content(self):
        # Test wine_query content, check if query components are added correctly
        test_input = {'region': 'Kalecik', 'colour': 'red', 'varietal': 'KalecikKarası'}
        input_list = [':red', ':KalecikKarası', ':Kalecik']
        # add region, colour and varietal one by one and check if corresponding query components are added to the query
        self.assertIn(input_list[2], qu.wine_query('', '', test_input['region']))
        self.assertIn(input_list[0], qu.wine_query(test_input['colour'], '', ''))
        self.assertIn(input_list[1], qu.wine_query('', test_input['varietal'], ''))
        query = qu.wine_query(test_input['colour'], test_input['varietal'], test_input['region'])
        self.assertTrue(all(x in query for x in input_list))
        # add inputs in wrong order and check the unexpected behaviour
        self.assertFalse(input_list[1] in qu.wine_query('', '', test_input['region']))
        self.assertFalse(input_list[2] in qu.wine_query(test_input['colour'], '', ''))
        self.assertFalse(input_list[0] in qu.wine_query('', test_input['varietal'], ''))

    def test_get_result(self):
        # Test query execution on sparql api and result parsing
        graph = rdflib.Graph()
        graph.parse('src/resources/wine_rdf.owl', format='application/rdf+xml')
        ns = rdflib.Namespace('http://www.semanticweb.org/davidos/ontologies/2020/9/untitled-ontology-21#')
        graph.bind('', ns)
        result = qu.get_result(graph, 'SELECT DISTINCT ?s {?s ?p ?o} LIMIT 1')
        self.assertTrue(len(result), 1)


if __name__ == '__main__':
    unittest.main()
