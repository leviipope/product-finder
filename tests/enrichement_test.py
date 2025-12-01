import ollama
from pydantic import BaseModel

# 1. Define your desired structure using Pydantic
class LaptopSpecs(BaseModel):
    brand: str
    model: str
    resoluton: str
    screen_size: str
    panel_type: str
    refresh_rate: str
    cpu_brand: str
    cpu_model: str
    gpu_brand: str
    gpu_model: str
    gpu_type: str
    ram: str
    storage_size: str
    storage_type: str

# 2. Call Ollama with the schema
response = ollama.chat(
    model='laptop-parser',
    messages=[{
        'role': 'user',
        'content': '''
        Title: 'Eladó HP ZBook Fury 15 G7 megkímélt, hibátlan állapotban!'
        Description: 'Eladásra kínálom használt, de kiváló állapotú HP ZBook Fury 15 G7 professzionális laptopomat.
        A gép teljesen hibátlanul működik. Az ár tartalmazza az eredeti töltőt is.

        Főbb specifikációk:
        Processzor: Intel® Core™ i7-10850H (2.70 GHz – 5.10 GHz)
        Memória: 32 GB RAM
        Tárhely: 500 GB SSD
        Operációs rendszer: Windows 11
        Kijelző: 15" prémium minőségű panel
        Videókártya: NVIDIA Quadro T2000
        Masszív, profi workstation ház, kiváló hűtés, megbízható teljesítmény
        A gép ideális fejlesztőknek, tervezőknek vagy bárkinek, aki stabil, nagy teljesítményű laptopot keres hosszú távra.
        Személyes átvétel és kipróbálás Budapesten belül megoldható.'''
    }],
    format=LaptopSpecs.model_json_schema(), # <--- This enforces the structure
)

print(response['message']['content'])