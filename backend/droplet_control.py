import requests
import time
import os
from dotenv import load_dotenv
from pydo import Client
from utils import loading_bar

# ---------------- CONFIG ----------------
load_dotenv()
DO_API_TOKEN = os.getenv("DO_API_TOKEN")
DROPLET_NAME = "LLM-JSON-parser"
REGION = "tor1"
# SIZE = "gpu-l40sx1-48gb" # currently not available in tor1
SIZE = "gpu-6000adax1-48gb"
IMAGE_ID = os.getenv("IMAGE_ID")
SSH_KEY_ID = os.getenv("SSH_KEY_ID")
SSH_KEY_FINGERPRINT = os.getenv("SSH_KEY_FINGERPRINT")
TAGS = ["gpu-controller"]
# ----------------------------------------

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DO_API_TOKEN}"
}

client = Client(token=DO_API_TOKEN) # type: ignore

def create_droplet():
    body = {
        "name": DROPLET_NAME,
        "region": REGION,
        "size": SIZE,
        "image": IMAGE_ID,
        "ssh_keys": [
            SSH_KEY_ID,
            SSH_KEY_FINGERPRINT
        ],
        "backups": False,
        "ipv6": False,
        "monitoring": True,
        "tags": TAGS
    }
    droplet_response = client.droplets.create(body=body)
    droplet_id = droplet_response["droplet"]["id"]
    print(f"Created Droplet '{DROPLET_NAME}' with ID {droplet_id}")
    status, ip = get_status(droplet_id, print_bool=False)
    print("Initializing Droplet...")
    loading_bar(total=60, duration=65)
    while True:
        status, ip = check_status(droplet_id)
        if ip != "No IP yet":
            print(f"Droplet {droplet_id} is ready to use, status: {status}! IP: {ip}")
            break
        print("Waiting for droplet to become active...")
        time.sleep(7)

    return droplet_id

def delete_droplet(droplet_id):
    client.droplets.destroy(droplet_id)
    print(f"Droplet {droplet_id} deleted successfully.")

def check_status(droplet_id):
    droplet = client.droplets.get(droplet_id)
    status = droplet["droplet"]["status"]
    ip = droplet["droplet"]["networks"]["v4"][0]["ip_address"] if droplet["droplet"]["networks"]["v4"] else "No IP yet"
    return status, ip

def get_status(droplet_id, print_bool=True):
    droplet = client.droplets.get(droplet_id)
    status = droplet["droplet"]["status"]
    ip = droplet["droplet"]["networks"]["v4"][0]["ip_address"] if droplet["droplet"]["networks"]["v4"] else "No IP yet"
    if print_bool:
        print(f"Droplet status: {status}, IP: {ip}")
    return status, ip

def list_snapshots():
    resp = client.snapshots.list(per_page=50)

    for snap in resp["snapshots"]:
        print(f"ID: {snap['id']}, Name: {snap['name']}, Resource: {snap['resource_type']}, Created: {snap['created_at']}")

if __name__ == "__main__":
    action = input("Enter action (create/delete/status/list/other): ").strip().lower()

    if action == "create":
        droplet_id = create_droplet()
        print(f"Save this Droplet ID for later: {droplet_id}")

    elif action == "delete":
        droplet_id = input("Enter Droplet ID to delete: ").strip()
        delete_droplet(int(droplet_id))

    elif action == "status":
        droplet_id = input("Enter Droplet ID to check status: ").strip()
        get_status(int(droplet_id))

    elif action == "list":
        client = Client(token=DO_API_TOKEN) # type: ignore
        response = client.droplets.list()
        droplets = response.get("droplets", [])
        if len(droplets) != 0:
            for droplet in droplets:
                print(f"ID: {droplet['id']}\nName: {droplet['name']}")
        else:
            print("No droplets.")

    elif action == "other":
        other_action = input("Enter action (ssh/snapshots): ").strip().lower()

        if other_action == "ssh":
            client = Client(token=DO_API_TOKEN) # type: ignore
            response = client.ssh_keys.list()
            keys = response.get("ssh_keys", [])
            [print(f"ID: {k['id']}\nFingerprint: {k['fingerprint']}\nName: {k['name']}\n") for k in keys]

        elif other_action == "snapshots":
            list_snapshots()
        else:
            print("Invalid action. Use 'ssh'")

    else:
        print("Invalid action. Use 'create', 'delete', 'status', 'list' or 'other'.")