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
    
    Default system: You are a fitness instructor with 15 years of experience. Given a 
                    video or images, you know exactly what fitness activity you're 
                    seeing. You are also great at pointing out if a workout form is 
                    incorrect.

    model: Storing a model object from GenAi library
    """
    model: genai.GenerativeModel

    def __init__(self, model_version=None, system_instruction=None) -> None:
        if not system_instruction:
            default_instruction = """
                You are a fitness instructor with 15 years of experience. Given a 
                video or images, you know exactly what fitness activity you're 
                seeing. You are also great at pointing out if a workout form is 
                incorrect.
                """
        else:
            default_instruction=system_instruction

        self.model = self._model_initialize(system_instruction=default_instruction) # Default 
        pass

    def _model_initialize(self, system_instruction, model_version='gemini-1.5-pro-latest') -> None:
        """Initializes Gemini model. Default: gemini-1.5-pro-latest
        """
        model = genai.GenerativeModel(
            model_name=model_version,
            system_instruction=system_instruction
        )
        return model
    
    def generate_analysis(self, prompt, file_timestamp_list):
        """Generates content based on prompt. Prompt will come after file_timestamp_list
        """
        compiled_prompt = file_timestamp_list + [prompt]
        return self.model.generate_content(compiled_prompt)

    def upload_file(self, path):
        return genai.upload_file(path=path)





