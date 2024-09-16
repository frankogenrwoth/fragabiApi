import openai
import os
from dotenv import load_dotenv

load_dotenv()

assistant_id = "asst_Aa3WppF38zcHHi1fpC9QdjeO"
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create()
