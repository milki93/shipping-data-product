# Data Mart Models

This directory contains the final analytical tables for the data warehouse, organized in a star schema:

- **dim_channels**: Dimension table with information about each Telegram channel.
- **dim_dates**: Dimension table for time-based analysis.
- **fct_messages**: Fact table containing one row per message, with foreign keys to dimension tables and key metrics (e.g., message length, has_image).

These models are built from the staging models and are optimized for analytics and reporting. 