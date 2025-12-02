# Product Finder

Product Finder is a powerful tool designed to scrape used laptop listings from [HardverApró](https://hardverapro.hu/), store them in a local SQLite database, and enrich the listing data with detailed specifications using a local Large Language Model (LLM).

## Features

- **Automated Scraping**: Fetches laptop listings including price, seller info, location, and descriptions using Scrapy.
- **Data Persistence**: Stores all scraped data in a structured SQLite database.
- **AI-Powered Enrichment**: Uses **Ollama** with a custom **Llama 3** model to parse unstructured descriptions and extract key specs:
  - CPU (Brand, Model)
  - GPU (Brand, Model, Type)
  - RAM (Size)
  - Storage (Size, Type)
  - Screen (Resolution, Size, Panel Type, Refresh Rate)
- **Change Detection**: Tracks price changes and status updates (e.g., if a listing is "iced" or sold).

## Tech Stack

- **Core Language**: Python 3.8+
- **Web Scraping**: [Scrapy](https://scrapy.org/) - Efficient and fast web crawling framework.
- **Database**: [SQLite](https://www.sqlite.org/index.html) - Lightweight, serverless database for local storage.
- **AI & LLM**:
  - [Ollama](https://ollama.com/) - Run Llama 3 locally.
  - **Llama 3** - The underlying Large Language Model used for text extraction.
- **Cloud Infrastructure**:
  - [DigitalOcean API](https://docs.digitalocean.com/reference/api/) - Programmatic control of cloud droplets (VMs) for scalable LLM inference (via `pydo`).
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/) - Strict type checking and schema definition for LLM outputs.

## Prerequisites

- **Python 3.8+**
- **[Ollama](https://ollama.com/)**: Required for running the local LLM.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd product-finder
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Ollama Model**:
   Pull the base Llama 3 model and create the custom `laptop-parser` model defined in `Modelfile`.
   ```bash
   ollama pull llama3
   ollama create laptop-parser -f Modelfile
   ```

## Usage

### 1. Scraping Listings

To start scraping listings from HardverApró, navigate to the scraper directory and run the spider:

```bash
cd backend/scraper
scrapy crawl hardver
```

This will fetch listings and populate the `listings` table in `data/database.db`.

### 2. Enriching Data

Once you have scraped listings, you can run the enrichment script to extract specifications using the LLM. This script processes listings that haven't been enriched yet.

From the project root:

```bash
python backend/enrichment.py
```

This will read descriptions from the database, query the local Ollama model, and save the structured specs into the `enriched_specs_laptops` table.

## Project Structure

- **`backend/`**
  - **`scraper/`**: Scrapy project containing the spider (`hardver_spider.py`).
  - **`db.py`**: Database connection and schema management.
  - **`enrichment.py`**: Logic for communicating with Ollama and updating the database.
  - **`main.py`**: Entry point (currently used for maintenance/testing).
- **`data/`**: Stores the SQLite database (`database.db`).
- **`Modelfile`**: Definition of the custom Ollama model for JSON extraction.

## Database Schema

The project uses two main tables:
- `listings`: Raw data scraped from the website.
- `enriched_specs_laptops`: Structured data extracted by the LLM, linked to `listings` via `listing_id`.
