import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.init import Auth
import os


client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.environ["WEAVIATE_URL"],
    auth_credentials=Auth.api_key(os.environ["WEAVIATE_API_KEY"]),
)


try:
    client.collections.delete("Testing")
except weaviate.exceptions.WeaviateError as e:
    print(f"Collection may not exist yet: {e}")


discreteMath = client.collections.create(
    name="discreteMath",
    vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
    generative_config=Configure.Generative.cohere(),
    properties=[
        Property(name="answer", data_type=DataType.TEXT, vectorize_property=True),
        Property(name="question", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT),
    ]
)

print("Collection 'discreteMath' created with vectorizer!")
client.close()