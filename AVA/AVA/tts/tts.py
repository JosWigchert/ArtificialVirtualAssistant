from AVA.utils import Environment
from AVA.model import OpenAI

env = Environment()

llm = OpenAI(env.OPENAI_API_KEY, env.OPENAI_ENGINE, env.OPENAI_EMBEDD)
