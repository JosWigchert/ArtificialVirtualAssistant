import openai, json, time
from AVA.events import Event


class Conversation:
    def __init__(
        self,
        engine: str = "gpt-3.5-turbo-1106",
        max_tokens: int = 4096,
        temperature: float = 0.2,
        stream: bool = False,
        system_message: None | str = None,
    ) -> None:
        self.engine = engine
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.stream = stream

        self.event = Event()

        self.messages = []

        if system_message is not None:
            self.messages.append({"role": "system", "content": system_message})

    def add_message(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model=self.engine, messages=self.messages, stream=self.stream
        )

        if self.stream:
            self.handle_stream_response(response)
        else:
            self.handle_response(response)

    def handle_response(self, response):
        self.event.publish(response["choices"][0])
        reply = response["choices"][0]["message"]
        self.messages.append(
            {
                "role": reply["role"],
                "content": reply["content"],
            }
        )

    def handle_stream_response(self, response):
        obj = {"content": ""}
        for chunk in response:
            self.event.publish(chunk["choices"][0])
            if "delta" in chunk["choices"][0]:
                reply = chunk["choices"][0]["delta"]
                if "role" in reply:
                    obj["role"] = reply["role"]
                if "content" in reply:
                    obj["content"] += reply["content"]
                if "finish_reason" in chunk["choices"][0]:
                    if chunk["choices"][0]["finish_reason"] == "stop":
                        self.messages.append(obj)
