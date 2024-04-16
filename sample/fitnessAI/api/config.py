import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Settings() :
    aws_access_key: str = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY")


def get_settings():
    settings = Settings()

    return settings

