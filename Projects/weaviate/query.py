import weaviate
from weaviate.classes.init import Auth
import os, json


weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                                    
    auth_credentials=Auth.api_key(weaviate_api_key),             
)

questions = client.collections.get("Question")

response = questions.query.near_text(
    query="Dorian Gray",
    limit=2,
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close() 