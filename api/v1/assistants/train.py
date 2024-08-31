# use a sample of combined questions to fine tune a model on answering for a particular grade
import pathlib
import sys

import openai
import os
from dotenv import load_dotenv

load_dotenv()


client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))


class Assistant:
    file_id: str
    assistant_id: str

    def __init__(self, path: str) -> None:
        path = pathlib.Path(path)

        if not path.exists() and not path.is_absolute():
            self.path = None

        else:
            self.path = path.absolute()

    def _run(self) -> str:

        file = client.files.create(
            file=open(self.path, "rb"),
            purpose='assistants'
        )

        self.file_id = file.id

        assistant_obj = client.beta.assistants.create(
            name="grade assistant",
            model="gpt-3.5-turbo",
            instructions="You are an intelligent student assistant you are going to answer my questions with the tone and detail provided in the sample below for any question only respond with required response and maybe some explanation",
            tools=[{"type": "code_interpreter"}],
            tool_resources={
                "code_interpreter": {
                    "file_ids": [self.file_id]
                }
            }
        )

        self.assistant_id = assistant_obj.id

        return assistant_obj.id

    def train(self):
        self._run()

        print(self.file_id, '\n', self.assistant_id)


if __name__ == "__main__":
    print(sys.argv[0])


    assistant = Assistant("./")
    print(assistant.assistant_id)




# pick the full file directory

# collect all the pdf files in it

# analyze the pdf files and use it to create an assistant fine tune
