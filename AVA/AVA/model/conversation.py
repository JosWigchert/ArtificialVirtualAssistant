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
        reply = response["choices"][0]["message"]
        print(f"Extracted reply: \n{reply}")

        reply_content = response["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": reply_content})

    def handle_stream_response(self, response):
        start_time = time.time()
        collected_chunks = []
        message = ""
        self.messages.append({"role": "assistant", "content": message})

        for chunk in response:
            chunk_time = (
                time.time() - start_time
            )  # calculate the time delay of the chunk
            collected_chunks.append(chunk)
            chunk_message = chunk["choices"][0]["delta"]  # extract the message
            message += chunk_message
            print(
                f"Message received {chunk_time:.2f} seconds after request: {chunk_message}"
            )  # print the delay and text
