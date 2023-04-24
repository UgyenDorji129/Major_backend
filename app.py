from flask import Flask, request
from scripts.feature_extractor import extract_features,is_URL_accessible
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from model.predict import predict
import os


app = Flask(__name__)

@app.route('/',methods=['POST'])
def check_Url():
    data = request.get_json()
    
    isAccessible =  is_URL_accessible(data['url'])
    print("dha:",isAccessible)
    if(isAccessible[0] == True):
        result = extract_features(data['url'])
        isPhishing = predict(result)
        return str(isPhishing[0])
    else:
        return str(-1)
    

if __name__ == "__main__":
    asgi_app = WsgiToAsgi(app.run(debug=True, port=os.getenv("PORT", default=7000)))
    asyncio.run(serve(asgi_app, Config()))
