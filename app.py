from flask import Flask, request
from scripts.feature_extractor import extract_features,is_URL_accessible
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from model.predict import predict


app = Flask(__name__)

@app.route('/',methods=['POST'])
def hello_world():
    data = request.get_json()
    result = extract_features(data['url'])
    # result =  is_URL_accessible("http://rgipt.ac.in")
    isPhishing = predict(result)
    print("dha: ",isPhishing)
    return str(isPhishing[0])

if __name__ == "__main__":
    asgi_app = WsgiToAsgi(app)
    asyncio.run(serve(asgi_app, Config()))