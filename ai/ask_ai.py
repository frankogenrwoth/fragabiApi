import os
import time
from dotenv import load_dotenv
import openai

load_dotenv()
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(query, grade):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=.5,
        messages=[{"role": "system",
                   "content": f"You are an intelligent tutor for a grade {grade} learner. carefully answer the question below give only the answer and some explanations and no other text"},
                  {"role": "user", "content": query}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(generate_response("what is a map", 5))
