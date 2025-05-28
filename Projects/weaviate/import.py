import weaviate
from weaviate.classes.init import Auth
import json, os


weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,                                    
    auth_credentials=Auth.api_key(weaviate_api_key),             
)

with open("data/jeopardy_extreme.json", "r") as dataj:
    data = json.load(dataj)

questions = client.collections.get("Question")

with questions.batch.fixed_size(batch_size=200) as batch:
    for category in data["categories"]:
        category_name = category["name"]
        for question_data in category["questions"]:
            batch.add_object(
                {
                    "answer": question_data["answer"],
                    "question": question_data["question"],
                    "category": category_name,
                    "value": question_data["value"]  
                }
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

failed_objects = questions.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close() 