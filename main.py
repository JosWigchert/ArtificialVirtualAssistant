import sys
from AVA.database import PineconeDatabase
from AVA.utils import Environment
from AVA.ui import ChatbotGUI, create_app, exit_app

if __name__ == "__main__":
    env = Environment()
    db = PineconeDatabase(env.PINECONE_API_KEY, env.PINECONE_ENVIRONMENT)

    print("Starting chatbot...")
    app = create_app(sys.argv)
    chatbot = ChatbotGUI(env, db)
    chatbot.show()
    exit_app(app)
