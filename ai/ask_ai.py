import os
from dotenv import load_dotenv
import openai

load_dotenv()

def generate_response(query, grade) -> str:
    assistants_dict = eval(os.getenv("ASSISTANTS"))
    # client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    assistant = assistants_dict[grade]

    return ""