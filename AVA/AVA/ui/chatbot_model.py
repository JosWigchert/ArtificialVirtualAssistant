from AVA.model import OpenAI
from AVA.utils import Environment, ObservableList
from AVA.events import Event


class ChatbotModel:
    def __init__(self):
        self.model = None
        self.intents = None

        self.chat_event = Event()
        self.messages = ObservableList()

        self.env = Environment()

        self.openai = OpenAI(
            self.env.OPENAI_API_KEY,
            self.env.OPENAI_ENGINE,
            self.env.OPENAI_EMBEDDINGS,
            stream=True,
        )

    def start_conversation(self):
        self.conversation = self.openai.start_conversation()
        self.conversation.event.subscribe(self.handle_response)

    def send_message(self, text):
        self.messages.append(
            {
                "is_user": True,
                "content": text,
            }
        )
        self.conversation.add_message(text)

    def search_message(self, text):
        print(f"Search: {text}")

    def handle_response(self, response):
        if "delta" in response:
            if "role" in response["delta"]:
                self.messages.append(
                    {
                        "is_user": False,
                        "content": "",
                    }
                )
            elif "content" in response["delta"]:
                obj = self.messages[-1]
                obj["content"] += response["delta"]["content"]
                self.messages[-1] = obj

        elif "message" in response:
            self.messages.append(
                {
                    "is_user": False,
                    "content": response["message"]["content"],
                }
            )
