from flask import Flask, abort, request, jsonify
from slack import WebClient
from slack.errors import SlackApiError
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('challenge')
parser.add_argument('event')

# config
app.config.from_object('config.Config')
client = WebClient(token=app.config['OAUTH_TOKEN'])
openai_key = app.config['OPENAI_KEY']
SLACK_BOT_TOKEN = app.config['OAUTH_TOKEN']

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class TestAPI(Resource):
    def get(self):
        data = request.get_json()
        print(data['challenge'])
        return {'test': 'success'}
    def post(self):
        data = request.get_json()
        print(data['challenge'])
        return {'post' : 'successToo!'}
    
class SlackBot(Resource):
    def post(self):
        data = request.get_json()
        print(data['token'])
        if 'challenge' in data:
            return {'challenge' : data['challenge']}
        text = data['text']
        response = "Hello, " + text
        return {'text': response}
    def get(self):
        data = request.get_json()
        print(data['token'])
        if 'challenge' in data:
            return {'challenge' : data['challenge']}
        text = data['text']
        response = "Hello, " + text
        return {'text': response}

api.add_resource(HelloWorld, '/')
api.add_resource(TestAPI, '/test')
api.add_resource(SlackBot, '/slack/events')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)