import requests
import json
from sshtunnel import SSHTunnelForwarder

def insert_droplet_ip():
    ip = input("Your droplets IP: ").strip()
    return ip

# ---------------- CONFIG ----------------
DROPLET_IP = insert_droplet_ip()
SSH_USER = "root"        # or your droplet user
SSH_KEY = "../ssh_key"   # path to your private key
REMOTE_OLLAMA_PORT = 11434
LOCAL_BIND_PORT = 11434
MODEL = "laptopparser"

PROMPTS = [
    "Eladó Lenovo Ideapad Pro 5 Notebook (83AS0034HV) 16-os kijelző-AMD Ryzen 5-7535HS-16GB ram-2,5K IPS 120Hz 350 nit /100% Srgb/ -512 SSD-Lpddr5-6400.Még van rá 23 Hónap garancia.Csak külön egérrel és billentyűzettel volt használva,hibamentes és karcmentes.Az egész burkolata fém.Dobozában tartozékaival, kihasználatlanság miatt eladó.",
    "BOMBA ÁRON ELADÓ! HP Elitebook 1040 G9 tipusú laptopi5-1245U, 16 GRAM, 256 GB NVME SSD, Intel Iris Xe Graphics....",
    "A képek szerinti szép állapotban eladó DELL LATITUDE üzleti laptop garanciával14\",i7-1185G7, 16 GB RAM, 512 GB SSD FHD+, IPS..."
]
# ----------------------------------------

def query_ollama(prompt: str, local_port: int):
    """Send a prompt to the Ollama API running on the Droplet (via tunnel)."""
    url = f"http://127.0.0.1:{local_port}/v1/completions"
    payload = {"model": MODEL, "prompt": prompt}

    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data.get("completion", "").strip()

def main():
    outputs = []

    # Open SSH tunnel
    with SSHTunnelForwarder(
        (DROPLET_IP, 22),
        ssh_username=SSH_USER,
        ssh_pkey=SSH_KEY,
        remote_bind_address=("127.0.0.1", REMOTE_OLLAMA_PORT),
        local_bind_address=("127.0.0.1", LOCAL_BIND_PORT),
    ) as tunnel:
        print(f"✅ SSH tunnel established on localhost:{tunnel.local_bind_port}") # type: ignore

        for prompt in PROMPTS:
            try:
                result = query_ollama(prompt, tunnel.local_bind_port) # type: ignore
                print(f"\nPrompt: {prompt}\nOutput: {result}\n{'-'*40}")
                outputs.append({"prompt": prompt, "output": result})
            except Exception as e:
                print(f"❌ Error with prompt '{prompt}': {e}")
                outputs.append({"prompt": prompt, "output": None})

    # Save results
    with open("ollama_outputs.json", "w", encoding="utf-8") as f:
        json.dump(outputs, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()