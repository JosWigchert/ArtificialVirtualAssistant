import openai, json
from AVA.utils import parse_docstring, load_functions_from_folder


class Conversation:
    def __init__(
        self,
        engine: str,
        function_parameters: list[str] = [],
        callable_functions: dict = {},
        max_tokens: int = 4096,
        temperature: float = 0.2,
        system_message: None | str = None,
    ) -> None:
        self.engine = engine
        self.function_parameters = function_parameters
        self.callable_functions = callable_functions
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.messages = []

        if system_message is not None:
            self.messages.append({"role": "system", "content": system_message})

    def add_message(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=self.messages,
                functions=self.function_parameters,
            )

            response_message = response["choices"][0]["message"]
            print(type(response_message))
            self.messages.append(response_message)

            if response_message.get("function_call"):
                function_name = response_message["function_call"]["name"]
                function_args = json.loads(
                    response_message["function_call"]["arguments"]
                )
                function_response = self.run_function(function_name, function_args)

                self.messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    }
                )

            if not response_message.get("function_call"):
                break

            print(self.messages)

        return response_message

    def run_function(self, name, args):
        function_to_call = self.callable_functions[name]
        a = []
        for f in self.function_parameters:
            if f["name"] == name:
                params = f["parameters"]
                if params is not None:
                    props = params["properties"]
                    for p in props.keys():
                        if p in args:
                            a.append(args[p])
        return function_to_call(*a)


class OpenAI:
    def __init__(
        self,
        api_key: str,
        engine: str,
        embeddings: str,
        max_tokens: int = 4096,
        temperature: float = 0.2,
    ) -> None:
        openai.api_key = api_key
        self.engine = engine
        self.embeddings = embeddings
        self.max_tokens = max_tokens
        self.temperature = temperature

        self.available_functions = {}
        self.function_parameters = []

    def add_functions(self, folder_path: str):
        loaded_functions = load_functions_from_folder(folder_path)
        for _, functions in loaded_functions.items():
            for name, function in functions.items():
                self.available_functions[name] = function
                self.function_parameters.append(parse_docstring(function))

        # print(self.function_parameters)

    def start_chat(self):
        return Conversation(
            self.engine,
            self.function_parameters,
            self.available_functions,
            self.max_tokens,
            self.temperature,
        )
