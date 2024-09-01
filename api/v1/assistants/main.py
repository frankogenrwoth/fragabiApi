import os
from os.path import join, dirname
from pypdf import PdfReader  # Updated import
import re

from api.models import Question, Answer


def runnit():
    curr = dirname(__file__)
    path = join(curr, "sample_try.pdf")

    print(path)

    # Open the PDF file and create a PdfReader object
    reader = PdfReader(open(path, "rb"))

    raw_text = ""

    # Iterate through each page and print the content
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()  # Updated method
        # print(f"Page {page_num + 1}:\n{text}\n")

        raw_text += text


    qn_and_answers = raw_text[:raw_text.rindex("Note")].split("Aufgabe\n \n")[1:]


    # print(qn_and_answers)

    objects = []

    regex = r'\.((\n)|(\s{2,}))'

    for item in qn_and_answers:

        split_index = item.find("?")

        if split_index < 0 and (item.find('!\n') >= 0):
            split_index = item.find('!\n')

        if split_index == -1:
            match = re.search(regex, item)

            if match:
                split_index = match.start()

            else:
                split_index = item.find(".\n")

        question = item[:(split_index + 1)]
        answer = item[(split_index + 1):]
        if answer.find("___") != -1:
            answer = answer[:answer.index("___")]

        if answer.find("Glück!!") == -1:
            qn = question[2:].replace("\n", " ").strip()
            ans = answer.replace(" \n", " ").replace("\n", "\t").strip()

            if qn and ans:
                objects.append({
                    "question": qn,
                    "answer": ans,
                })

    print(objects)
    for item in objects:
        qn, _ = Question.objects.get_or_create(grade=5, text=item["question"])
        if _:
            Answer.objects.create(question=qn, text=item["answer"])
