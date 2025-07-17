# dbt Project: Shipping Data Product

This dbt project transforms raw Telegram message data into a clean, trusted data warehouse for analytics.

## Structure
- **models/staging/**: Staging models to clean and extract fields from raw JSON data.
- **models/marts/**: Data mart models implementing a star schema (fact and dimension tables).

## Star Schema
- **dim_channels**: Channel dimension
- **dim_dates**: Date dimension
- **fct_messages**: Message fact table

## How to Use
1. Load raw JSON data into the `raw.telegram_messages` table (see `scripts/load_raw_json_to_pg.py`).
2. Run dbt models:
   ```
   dbt run
   dbt test
   dbt docs generate
   dbt docs serve
   ```

## Testing
- Built-in dbt tests for uniqueness and not-null constraints
- Custom test to ensure no empty messages

## Documentation
- Run `dbt docs generate` and `dbt docs serve` to view project documentation.
