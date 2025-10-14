import os
from pydo import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(token=os.getenv("DO_API_TOKEN"))  # type: ignore

# List all snapshots
resp = client.snapshots.list(per_page=50)

for snap in resp["snapshots"]:
    print(f"ID: {snap['id']}, Name: {snap['name']}, Resource: {snap['resource_type']}, Created: {snap['created_at']}")