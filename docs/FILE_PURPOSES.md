| File Path | Role & Responsibility | Primary Purpose |
| --- | --- | --- |
| `config.py` | Configuration Layer | Uses `pydantic-settings` to load and type-check environment variables (`.env`) safely. |
| `database.py` | Infrastructure Layer | Initializes the SQLAlchemy `Engine`, creates `SessionLocal` generator (`get_db`), and defines ORM `Base`. |
| `models/listing.py` | Data Persistence Layer | SQLAlchemy ORM model matching the SQLite `listings` table structure. |
| `schemas/listing.py` | Data Contract & Validation Layer | Pydantic models for parsing incoming HTTP requests and validating/cleaning outgoing JSON responses. |
| `services/listing_service.py` | Business & Query Logic Layer | Builds dynamic SQL queries and executes database interactions isolated from HTTP logic. |
| `api/v1/listings.py` | Controller / Endpoint Layer | Defines FastAPI routes (`GET /listings`), handles HTTP parameters, and returns response models. |
| `api/v1/router.py` | Route Aggregator | Combines sub-routers under the `/api/v1` namespace prefix. |
| `main.py` | Application Entrypoint | Initializes `FastAPI()`, registers middleware (CORS), mounts routers, and defines root health check. |
