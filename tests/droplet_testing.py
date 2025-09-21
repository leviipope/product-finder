import requests

LOCAL_PORT = 11434  # SSH tunnel forwards to this port

def parse_product(text):
    url = f"http://localhost:{LOCAL_PORT}/v1/completions"
    payload = {
        "model": "laptopparser",
        "prompt": text,
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    sample_text = "Eladó Lenovo Ideapad Pro 5 Notebook (83AS0034HV) 16-os kijelző-AMD Ryzen 5-7535HS-16GB ram-2,5K IPS 120Hz 350 nit /100% Srgb/ -512 SSD-Lpddr5-6400.Még van rá 23 Hónap garancia.Csak külön egérrel és billentyűzettel volt használva,hibamentes és karcmentes.Az egész burkolata fém.Dobozában tartozékaival, kihasználatlanság miatt eladó."
    result = parse_product(sample_text)
    print(result)
