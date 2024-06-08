from flask import Flask 
from flask_restful import Api, Resource,reqparse
from model import predict_class



app = Flask(__name__)
api = Api()

class Main(Resource):
    def get(self):
        return {"info":"Some info"}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text",type=str)
        text = parser.parse_args()['text']
        prediction = predict_class(text)
        return prediction

api.add_resource(Main, "/api/main")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000,host='127.0.0.1')