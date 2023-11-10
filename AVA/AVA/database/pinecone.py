import pinecone


class PineconeDatabase:
    def __init__(
        self,
        api_key,
        environment,
        index="ava-chatbot",
        dimension=1536,
        metric="euclidean",
    ):
        self.__api_key = api_key
        self.__environment = environment
        self.__index = index
        self.__dimension = dimension
        self.__metric = metric

    def initialize(self):
        self.client = pinecone.init(
            api_key=self.__api_key, environment=self.__environment
        )
        indices = pinecone.list_indexes()
        if self.__index not in indices:
            print(f"Creating index {self.__index}")
            pinecone.create_index(
                self.__index, dimension=self.__dimension, metric=self.__metric
            )
        description = pinecone.describe_index(self.__index)
        print(description)

    def insert(self, data):
        pass
