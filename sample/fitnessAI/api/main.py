from fastapi import FastAPI, Request

from api.s3.s3 import fetch_presigned_url
from api.script import main
import urllib.parse

import logging


def initialAppSetup():
    app = FastAPI()
    
    return app

app = initialAppSetup()

@app.get("/")
def root_path():
    return {"Fitcheck": "API"}


@app.post("/upload-url")
async def get_upload_url(request: Request):
    response = await request.body()
    key, file_name = response.decode("utf-8").split('=')
    url = fetch_presigned_url(str(file_name))
    
    # data = await request.json()
    # url = fetch_presigned_url(str(data.get("file_name")))
    if url:
        return url
    else:
        return {"error": "Something went wrong"}

@app.post("/begin-gemini")
async def start_script(request: Request):
    response = await request.body()
    fills = response.decode("utf-8").split('&')
    final = {fill.split('=')[0]: fill.split('=')[1] for fill in fills}
    encoded_url = final['url']
    response = main(urllib.parse.unquote(encoded_url), final['file_name'])
    
    if response: 
        return response
    else:
        return {"error": "Something went wrong"}

