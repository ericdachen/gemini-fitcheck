from fastapi import FastAPI

from api.s3.s3 import fetch_presigned_url


def initialAppSetup():
    app = FastAPI()

    return app

app = initialAppSetup()

@app.get("/")
def root_path():
    return {"Fitcheck": "API"}


@app.get("/upload-url")
def get_upload_url(file_name):
    url = fetch_presigned_url(str(file_name))

    if url:
        return url
    else:
        return {"error": "Something went wrong"}

