from fastapi import APIRouter
from api.s3.s3 import fetch_presigned_url

router = APIRouter(tags=["upload_url"])


@router.get("/upload-url")
def get_upload_url(file_name):
    url = fetch_presigned_url(str(file_name))

    if url:
        return url
    else:
        return {"error": "Something went wrong"}