import json
import ollama
from db import get_prompt, get_connection, get_non_enriched_listings
import time

ollama = ollama.Client()

def run_ollama(prompt: str, model="laptopparser") -> str:
    response = ollama.generate(model=model, prompt=prompt)

    return response.response

def parse_listing(id: int): 
    return run_ollama(get_prompt(id))

def clean_output(llm_output: str) -> str:
    cleaned_output = llm_output.strip("` \n")

    return cleaned_output
    
def load_json(cleaned_output: str):
    return json.loads(cleaned_output)
          
def output_to_json(data, id):
    output_file = f"parsed_listing_{id}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data written to {output_file}")

def enrich_listing(id: int, data: dict):
    enriched_brand = data.get("enriched_brand")
    enriched_model = data.get("enriched_model")
    enriched_specs = json.dumps(data.get("enriched_specs", {}), ensure_ascii=False)

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        '''
        UPDATE listings
        SET enriched_brand = ?,
            enriched_model = ?,
            enriched_specs = ?
        WHERE id = ?
        ''',
        (enriched_brand, enriched_model, enriched_specs, id),
    )

    conn.commit()
    conn.close()

    print(f"✅ Listing {id} enriched, updated in database")

def main():
    MAX_RETRIES = 3
    non_enriched_listing_ids = get_non_enriched_listings()
    start_total = time.time()

    for id in non_enriched_listing_ids:
        print(f"\n🔹 Processing listing {id}")
        start_listing = time.time()

        for attempt in range(1, MAX_RETRIES + 1):
            start_attempt = time.time()
            try:
                llm_output = parse_listing(id)
                cleaned_output = clean_output(llm_output)
                data = load_json(cleaned_output)
                # output_to_json(data, id)
                enrich_listing(id, data)

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

if __name__ == "__main__":
    main()
