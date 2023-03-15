from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('challenge')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class TestAPI(Resource):
    def get(self):
        return {'test': 'success'}
    def post(self):
        return {'post' : 'successToo!'}
    
class BotAPI(Resource):
    def post(self):
        args = parser.parse_args()
        value = args['challenge']
        print(value)
        return args,200

api.add_resource(HelloWorld, '/')
api.add_resource(TestAPI, '/test')
api.add_resource(BotAPI, '/slack/events')

if __name__ == '__main__':
    app.run(debug=True)