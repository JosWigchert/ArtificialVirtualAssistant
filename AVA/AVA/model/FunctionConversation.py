import openai, json

class FunctionConversation:
    def __init__(
        self,
        engine: str,
        function_parameters: list[str] = [],
        callable_functions: dict = {},
        max_tokens: int = 4096,
        temperature: float = 0.2,
        stream: bool = False,
        system_message: None | str = None,
    ) -> None:
        self.engine = engine
        self.function_parameters = function_parameters
        self.callable_functions = callable_functions
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.stream = stream

        self.message_done_event = Event()

        self.messages = []

        if system_message is not None:
            self.messages.append({"role": "system", "content": system_message})

    def add_message(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})

        while True:
            response = openai.ChatCompletion.create(
                model=self.engine,
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