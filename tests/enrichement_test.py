import ollama
from pydantic import BaseModel, Field

class LaptopSpecs(BaseModel):
    brand: str
    model: str
    resolution: str = Field(
        description="The screen resolution in pixel x pixel format only (e.g., '1920x1080', '3840x2160'). Exclude marketing terms like FHD or 4K."
    )
    screen_size_inches: float = Field(
            description="The diagonal screen size, returned as a clean floating-point number in inches (e.g., 15.6, 13.3). Exclude all units, text, or quotation marks."
    )
    panel_type: str = Field(
        description="The screen panel technology. Must only include the type (e.g., 'IPS', 'OLED', 'TN', 'VA')."
    )
    refresh_rate: int
    cpu_brand: str
    cpu_model: str
    gpu_brand: str
    gpu_model: str
    gpu_type: str = Field(
        description="Must be either 'Dedicated' (e.g., NVIDIA, AMD Radeon) or 'Integrated' (e.g., Intel Iris, AMD Vega). If unknown, use null."
    )
    ram: str = Field(
        description="The total RAM size in the format 'X GB' (e.g., '16 GB', '32 GB')."
    )
    storage_size: str = Field(
        description="The total accumulated storage size across all drives. All capacity must be summed and returned as a string (e.g., '512 GB', or '1256 GB' if 1TB and 256GB are found)."
    )

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
        Tárhely: 500 GB SSD és 1 TB HDD
        Operációs rendszer: Windows 11
        Kijelző: 15" prémium minőségű panel
        Videókártya: NVIDIA Quadro T2000
        Masszív, profi workstation ház, kiváló hűtés, megbízható teljesítmény
        A gép ideális fejlesztőknek, tervezőknek vagy bárkinek, aki stabil, nagy teljesítményű laptopot keres hosszú távra.
        Személyes átvétel és kipróbálás Budapesten belül megoldható.
        '''
    }],
    format=LaptopSpecs.model_json_schema(), # <--- This enforces the structure
)

print(response['message']['content'])