import os
from os.path import join, dirname
from dotenv import load_dotenv
import google.generativeai as genai

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_key=os.environ.get('GEMINI_KEY')
genai.configure(api_key=api_key)

class geminiFitCheck:
    """A interface to interact with Gemini, system instruction of fitness coach
    
    model
    prompt

    """

    def __init__(self, model, prompt) -> None:
        pass

    def _model_initialize() -> None:

        model = genai.GenerativeModel(
            model_name='gemini-1.5-pro-latest',
            system_instruction="""
            You are a fitness instructor with 15 years of experience. Given a 
            video or images, you know exactly what fitness activity you're 
            seeing. You are also great at pointing out if a workout form is 
            incorrect.
            """
        )


