import weaviate
from weaviate.classes.init import Auth
import json, os


weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                                    
    auth_credentials=Auth.api_key(weaviate_api_key),             
)

with open("data/basic_chapters.json", "r") as dataj:
    data = json.load(dataj)

discreteMath = client.collections.get("discreteMath")

with discreteMath.batch.fixed_size(batch_size=200) as batch:
    for category in data["topics"]:
        category_name = category["category"]  
        for question_data in category["terms"]:  #
            batch.add_object(
                {
                    "answer": question_data["definition"],
                    "question": question_data["term"],
                    "category": category_name,
                }
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

failed_objects = discreteMath.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close() 