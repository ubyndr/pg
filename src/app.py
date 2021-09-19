import time
from flask import Flask
from flask_restplus import Resource, Api, reqparse
from utils import queryUtils as qu
import rdflib

# Flask app initialization
app = Flask(__name__)
api = Api(version='1.0', title='Wine API',
          description='Swagger Interface for Wine API')
api.init_app(app)

# Wine ontology is loaded into graph object. Namespace added to ease the query process
graph = rdflib.Graph()
graph.parse('src/resources/wine_rdf.owl', format='application/rdf+xml')
ns = rdflib.Namespace('http://www.semanticweb.org/davidos/ontologies/2020/9/untitled-ontology-21#')
graph.bind('', ns)

wine_query = api.namespace('/', description='Wine query services')


@wine_query.route('/list_regions')
class list_regions(Resource):
    @api.response(200, 'Regions are listed successfully')
    def get(Self):
        # Lists all grape growing regions
        start = time.time()
        result = qu.get_result(graph, qu.region_list_query())
        print('Regions are listed in ', time.time() - start, 'seconds')
        return result, 200


@wine_query.route('/list_varietals')
class list_varietals(Resource):
    @api.response(200, 'Varietals are listed successfully')
    def get(Self):
        # List all varietals
        start = time.time()
        result = qu.get_result(graph, qu.varietal_list_query())
        print('Varietals are listed in ', time.time() - start, ' seconds')
        return result, 200


@wine_query.route('/list_wines')
class list_wines(Resource):
    @api.response(200, 'Wines are listed successfully')
    def get(Self):
        # List all types of wine
        start = time.time()
        result = qu.get_result(graph, qu.wine_list_query())
        print('Wines are listed in ', time.time() - start, ' seconds')
        return result, 200


# Request parser is added for faceted wine query
parser = reqparse.RequestParser()
parser.add_argument('region', required=False, help='Wine region, can be empty')
parser.add_argument('colour', required=False, help='Wine colour, can be empty')
parser.add_argument('varietal', required=False, help='Varietal type, can be empty')


@wine_query.route('/wine_query')
class wine_search(Resource):
    @api.expect(parser)
    @api.response(200, 'Wine/s retrieved successfully')
    def get(Self):
        # Query for wine types and individual wines by: region, colour, varietal
        args = parser.parse_args()
        start = time.time()
        result = qu.get_result(graph, qu.wine_query(args['colour'], args['varietal'], args['region']))
        print('Wine query completed in ', time.time() - start, ' seconds')
        return result, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
