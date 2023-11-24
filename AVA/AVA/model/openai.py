import openai, json
from AVA.utils import parse_docstring, load_functions_from_folder
from AVA.events import Event
from AVA.model.conversation import Conversation


class OpenAI:
    def __init__(
        self,
        api_key: str,
        engine: str,
        embeddings: str,
        max_tokens: int = 4096,
        temperature: float = 0.2,
        stream: bool = False,
    ) -> None:
        openai.api_key = api_key
        self.engine = engine
        self.embeddings = embeddings
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.stream = stream

        self.available_functions = {}
        self.function_parameters = []

    def add_functions(self, folder_path: str):
        loaded_functions = load_functions_from_folder(folder_path)
        for _, functions in loaded_functions.items():
            for name, function in functions.items():
                self.available_functions[name] = function
                self.function_parameters.append(parse_docstring(function))

        # print(self.function_parameters)

    def start_conversation(self, type: str = "default") -> Conversation:
        return Conversation(
            self.engine,
            self.max_tokens,
            self.temperature,
            self.stream,
        )

    def generate_tts(self, text: str, voice: str = "nova"):
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        return response
