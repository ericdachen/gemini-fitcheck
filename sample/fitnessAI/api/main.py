from fastapi import FastAPI, Request

from s3.s3 import fetch_presigned_url



def initialAppSetup():
    app = FastAPI()
    
    return app

app = initialAppSetup()

@app.get("/")
def root_path():
    return {"Fitcheck": "API"}


@app.post("/upload-url")
async def get_upload_url(request: Request):
    data = await request.json()
    url = fetch_presigned_url(str(data.get("file_name")))

    if url:
        return url
    else:
        return {"error": "Something went wrong"}

