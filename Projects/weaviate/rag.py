import weaviate
from weaviate.classes.init import Auth
import os


weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
cohere_api_key = os.environ["COHERE_APIKEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                                    
    auth_credentials=Auth.api_key(weaviate_api_key),             
    headers={"X-Cohere-Api-Key": cohere_api_key},           
)

questions = client.collections.get("Question")

response = questions.generate.near_text(
    query="science",
    limit=2,
    grouped_task="Write a tweet with emojis about these facts."
)

print(response.generated)  

client.close()