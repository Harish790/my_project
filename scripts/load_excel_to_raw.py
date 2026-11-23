"""Load every sheet of an Excel workbook into the Postgres `raw` schema.

Each sheet becomes a table named after the sheet (lowercased, spaces -> underscores).
Existing tables are replaced, so rerun this whenever the Excel file changes.

Usage:
    python scripts/load_excel_to_raw.py                       # loads data/shop_data.xlsx
    python scripts/load_excel_to_raw.py path/to/other.xlsx    # loads another workbook

Connection settings come from environment variables (defaults match local Postgres.app):
    PGHOST=localhost PGPORT=5432 PGUSER=<your mac user> PGPASSWORD= PGDATABASE=dbt_dev
"""
import getpass
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_FILE = PROJECT_DIR / "data" / "shop_data.xlsx"
TARGET_SCHEMA = "raw"


def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("PGUSER", getpass.getuser()),
        password=os.getenv("PGPASSWORD") or None,
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        database=os.getenv("PGDATABASE", "dbt_dev"),
    )
    return create_engine(url)


def clean_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def main() -> None:
    excel_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FILE
    if not excel_path.exists():
        sys.exit(f"File not found: {excel_path}")

    sheets = pd.read_excel(excel_path, sheet_name=None)  # dict of {sheet_name: DataFrame}
    engine = get_engine()
    loaded_at = datetime.now(timezone.utc)

    with engine.begin() as conn:
        conn.execute(text(f"create schema if not exists {TARGET_SCHEMA}"))
        for sheet_name, df in sheets.items():
            table = clean_name(sheet_name)
            df.columns = [clean_name(str(c)) for c in df.columns]
            df["_loaded_at"] = loaded_at  # audit column: when this row was loaded
            # cascade also drops dbt views built on this table; `dbt build` recreates them
            conn.execute(text(f'drop table if exists {TARGET_SCHEMA}."{table}" cascade'))
            df.to_sql(table, conn, schema=TARGET_SCHEMA, if_exists="fail", index=False)
            print(f"Loaded {len(df):>5} rows -> {TARGET_SCHEMA}.{table}")

    print(f"Done: {len(sheets)} sheet(s) from {excel_path.name}")


if __name__ == "__main__":
    main()
