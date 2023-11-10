import os
from dotenv import load_dotenv


class Environment:
    def __init__(self, env_file=".env"):
        # Load environment variables from the specified .env file
        load_dotenv(env_file)
        self.load_environment_variables()

    def load_environment_variables(self):
        # Get all environment variables from the .env file
        self.keys = []
        for key, value in os.environ.items():
            setattr(self, key, value)
            self.keys.append(key)
        # Add more environment variables as needed

    def get_variables(self):
        return self.keys
