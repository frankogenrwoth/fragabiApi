import os
from os.path import join, dirname
from pypdf import PdfReader  # Updated import

# Get the current directory and path to the PDF file
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

for q in qn_and_answers:
    print(q)