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
        print("문장을 생성합니다.")
        data = request.json
        print(data)
        if "challenge" in data:
            return jsonify({"challenge": data["challenge"]})
        elif "event" in data:
            event = data["event"]
            if event["type"] == "message" and "bot_id" not in event:
                text = event["text"]
                channel_id = event["channel"]
                user_id = event["user"]
                # chatgpt_response = chatTest(text)
                try:
                    client.chat_postMessage(
                        channel=channel_id,
                        text=f"{text}"
                    )
                    print("문장 생성을 완료했습니다.")
                except SlackApiError as e:
                    print("Error sending message: {}".format(e))
                return jsonify({})
        return jsonify({})

api.add_resource(HelloWorld, '/')
api.add_resource(TestAPI, '/test')
api.add_resource(BotAPI, '/slack/events')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)