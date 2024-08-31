import asyncio
import os
from typing import List, Dict

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def evaluate_answer(question: str, user_answer: str, correct_answer: str, score: int) -> float:
    prompt = f"""
    Question: {question}
    User's Answer: {user_answer}
    Correct Answer: {correct_answer}

    Please evaluate the user's answer based on its correctness and completeness and award a score of maximum {score}

    Provide the score as a single number without any explanation.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that evaluates answers to questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1
        )
        score = float(response.choices[0].message.content.strip())
        return min(max(score, 0), 5)
    except Exception as e:
        print(f"Error evaluating answer: {str(e)}")
        return 0.0


async def process_answer(item: Dict) -> Dict:
    score = await evaluate_answer(item["question"], item["answer"], item["correct"], item["score"])

    return {
        "question": item["question"],
        "answer": item["answer"],
        "correct": item["correct"],
        "score": score,
        "id": item["id"],
    }


async def process_all_answers(answers: List[Dict]) -> List[Dict]:
    tasks = [process_answer(item) for item in answers]
    return await asyncio.gather(*tasks)


def evaluate_responses(quiz_responses) -> list[Dict]:
    results = asyncio.run(process_all_answers(quiz_responses))

    # return json.dumps(results, indent=2)
    return results
