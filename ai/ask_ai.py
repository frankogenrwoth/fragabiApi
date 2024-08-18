import os
from dotenv import load_dotenv
import openai

load_dotenv()
# client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

assistants_dict = eval(os.getenv("ASSISTANTS"))


def generate_response(query, grade) -> str:
    assistant = assistants_dict[grade]

    return ""