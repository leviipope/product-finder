import json
import ollama
import time
from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from notifier import run_notifier
from db import get_prompt, get_connection, get_non_enriched_ids_by_product_type

class LaptopSpecs(BaseModel):
    brand: str
    model: str
    
    resolution: Union[Literal['FHD', 'FHD+', 'QHD', 'QHD+', '4k', 'Other', None], None] = Field(
        description="No other text or marketing terms allowed. If unknown, use null."
    )
    
    screen_size_inches: Union[float, None] = Field(
        description="Diagonal screen size in inches (e.g., 15.6, 13.3). Return as a clean number. Use null if unknown."
    )
    
    panel_type: Union[Literal['IPS', 'OLED', 'TN', 'VA'], None] = Field(
        description="Screen panel technology. Must be one of: 'IPS', 'OLED', 'TN', 'VA'. Use null if unknown."
    )
    
    refresh_rate: Union[float, None] = Field( 
        description="Screen refresh rate in Hz (e.g., 144.0, 60.0). Return as a clean float. Use null if unknown."
    )
    
    cpu_brand: str
    cpu_model: str
    
    gpu_brand: Union[Literal['NVIDIA', 'AMD', 'Intel'], None] = Field(description="Brand of the GPU (e.g., 'NVIDIA', 'AMD', 'Intel'). Use null if unknown.")
    gpu_model: Union[str, None] = Field(description="Model of the GPU (e.g., 'RTX 4070', 'Radeon 780M'). Use null if unknown, don't use 'integrated'.")
    
    gpu_type: Union[Literal['Dedicated', 'Integrated'], None] = Field(
        description="Must be either 'Dedicated' or 'Integrated'. Use null if unknown."
    )
    
    ram_gb: Union[int, None] = Field(
        description="Total RAM size in GB (e.g., 16, 32). Return as a clean integer. Use null if unknown."
    )
    
    storage_size_gb: Union[int, None] = Field(
        description="Total storage capacity (summed) in GB (e.g., 512, 1256). Return as a clean integer. Use null if unknown."
    )

class GPUSpecs(BaseModel):
    enriched_brand: Literal['NVIDIA', 'AMD', 'Intel'] = Field(
        ...,
        description="The primary manufacturer of the GPU chipset (NVIDIA, AMD, or Intel)."    )

    enriched_model: str = Field(
        ..., 
        description="The full model name including the series. Examples: 'GeForce RTX 4070 Ti', 'Radeon RX 7900 XTX', 'Arc A770'."
    )

    vram_gb: Optional[int] = Field(
            None, 
            ge=1, 
            le=48, 
            description="The total amount of Video RAM in GB. Extract as a clean integer (e.g., 8, 12, 16, 24)."
        )
    
def run_ollama(prompt: str, model, schema: type[BaseModel], product_type: str) -> str:

    context_instructions = f"Extract {product_type} specifications from the following text according to the provided schema:\n\n"

    response = ollama.chat(
        model=model, 
        messages=[{'role': 'user', 'content': context_instructions + prompt}], 
        format=schema.model_json_schema())

    return response['message']['content']

def parse_listing(id: int , model: str, schema: type[BaseModel], product_type: str) -> tuple[str, str]: 
    prompt, site = get_prompt(id, product_type)
    return run_ollama(prompt, model, schema, product_type), site

def clean_output(llm_output: str) -> str:
    cleaned_output = llm_output.strip("` \n")
    return cleaned_output
    
def load_json(cleaned_output: str):
    return json.loads(cleaned_output)
          
def output_to_json(data):
    output_file = f"parsed_listings.json"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n")
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data written to {output_file}")

def enrich_laptop(id: int, site: str, data: dict):
    brand = data.get("brand")
    model = data.get("model")
    resolution = data.get("resolution")
    screen_size_inches = data.get("screen_size_inches")
    panel_type = data.get("panel_type")
    refresh_rate = data.get("refresh_rate")
    cpu_brand = data.get("cpu_brand")
    cpu_model = data.get("cpu_model")
    gpu_brand = data.get("gpu_brand")
    gpu_model = data.get("gpu_model")
    gpu_type = data.get("gpu_type")
    ram_gb = data.get("ram_gb")
    storage_size_gb = data.get("storage_size_gb")
    storage_type = data.get("storage_type")

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        '''
        INSERT INTO enriched_specs_laptops (
            site, listing_id, enriched_brand, enriched_model, resolution, screen_size, panel_type, refresh_rate,
            cpu_brand, cpu_model, gpu_brand, gpu_model, gpu_type, ram, storage_size, storage_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            site, id, brand, model, resolution, screen_size_inches, panel_type, refresh_rate,
            cpu_brand, cpu_model, gpu_brand, gpu_model, gpu_type, ram_gb, storage_size_gb, storage_type
        )
    )

    conn.commit()
    conn.close()

    print(f"✅ Listing {id} enriched, updated in database")

def enrich_gpu(id: int, site: str, data: dict):
    enriched_brand = data.get("enriched_brand")
    enriched_model = data.get("enriched_model")
    vram_gb = data.get("vram_gb")

    with get_connection() as conn:
        c = conn.cursor()

        c.execute(
            '''
            INSERT INTO enriched_gpus (
                site, listing_id, enriched_brand, enriched_model, vram
            ) VALUES (?, ?, ?, ?, ?)
            ''',
            (
                site, id, enriched_brand, enriched_model, vram_gb
            )
        )

    print(f"✅ Listing {id} enriched, updated in database")

def local_enrichment(non_enriched_dict):
    MAX_RETRIES = 3
    start_total = time.time()

    for product_type, ids in non_enriched_dict.items():
        print(f"\n🔷 Processing product type: {product_type.upper()}")
        
        if not ids:
            print(f"No non-enriched listings found for {product_type}, skipping.")
            continue

        for id in ids:
            print(f"\n🔹 Processing listing {id}")
            start_listing = time.time()

            for attempt in range(1, MAX_RETRIES + 1):
                start_attempt = time.time()
                try:

                    if product_type == "laptop":
                        model = "laptop-parser"
                        schema = LaptopSpecs
                    elif product_type == "gpu":
                        model = "general-parser" # testing
                        schema = GPUSpecs

                    llm_output, site = parse_listing(id, model, schema, product_type)

                    cleaned_output = clean_output(llm_output)
                    data = load_json(cleaned_output)

                    if product_type == "laptop":
                        #output_to_json(data)
                        enrich_laptop(id, site, data)
                    elif product_type == "gpu":
                        enrich_gpu(id, site, data)

                    elapsed_attempt = time.time() - start_attempt
                    print(f"✅ Attempt {attempt} succeeded in {elapsed_attempt:.2f}s")
                    break
                except Exception as e:
                    elapsed_attempt = time.time() - start_attempt
                    print(f"⚠️ Attempt {attempt} failed in {elapsed_attempt:.2f}s: {e}")
                    if attempt == MAX_RETRIES:
                        print("❌ All retries failed, could not parse JSON")

            elapsed_listing = time.time() - start_listing
            print(f"⏱ Finished listing {id} in {elapsed_listing:.2f}s")

    elapsed_total = time.time() - start_total
    print(f"\n🏁 Total runtime: {elapsed_total:.2f}s")

def main():
    non_enriched_dict = get_non_enriched_ids_by_product_type()
    local_enrichment(non_enriched_dict)
    run_notifier(non_enriched_dict)

if __name__ == "__main__":
    main()
