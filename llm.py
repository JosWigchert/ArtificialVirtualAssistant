import sys
from AVA.utils import Environment
from AVA.model import OpenAI


if __name__ == "__main__":
    env = Environment()
    llm = OpenAI(env.OPENAI_API_KEY, env.OPENAI_ENGINE, env.OPENAI_EMBEDDINGS)
    llm.add_functions("AVA/AVA/model/functions")
    convo = llm.start_chat()

    # msg = "Can you create a todo list for my shopping today?"
    msg = "Can you create a todo list for my grocery shopping"
    response = convo.add_message(msg)
    print(msg)
    print(f"{response["role"]}: {response["content"]}")

    msg = "Okay i got the milk"
    response = convo.add_message(msg)
    print(msg)
    print(f"{response["role"]}: {response["content"]}")
