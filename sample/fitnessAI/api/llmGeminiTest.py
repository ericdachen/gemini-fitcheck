import requests
import os
import json

def get_presigned_s3(file_full_path):
    base_name = os.path.basename(file_full_path)
    url = f'http://127.0.0.1:8000/upload-url?file_name={base_name}'
    response = requests.get(url=url)
    return response

def upload_file_to_s3(response, file_path):
    dct = json.loads(response.text)
    with open(file_path, 'rb') as f: # rb data open allows easier transfer
        content = dct['fields']
        content['file'] = (os.path.basename(file_path))
        response = requests.post(dct['url'], files=dct['fields'])
        return response.status_code, response.content

if __name__ == "__main__":
    # Get file name and path
    # Get presigned from server
    # Chunk and async upload, retain the uploaded link