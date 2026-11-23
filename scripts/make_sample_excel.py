"""Create a sample Excel workbook (data/shop_data.xlsx) with customers and orders sheets.

Run once to generate practice data:
    python scripts/make_sample_excel.py
"""
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "data" / "shop_data.xlsx"

customers = pd.DataFrame(
    {
        "customer_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "first_name": ["Asha", "Ben", "Chen", "Diya", "Ethan", "Fatima", "Gabriel", "Hana"],
        "last_name": ["Rao", "Miller", "Wei", "Patel", "Brooks", "Khan", "Lopez", "Sato"],
        "email": [
            "asha@example.com", "ben@example.com", "chen@example.com", "diya@example.com",
            "ethan@example.com", "fatima@example.com", "gabriel@example.com", "hana@example.com",
        ],
        "city": ["Hyderabad", "Austin", "Seattle", "Chennai", "Denver", "Dallas", "Miami", "Boston"],
        "signup_date": pd.to_datetime([
            "2026-01-05", "2026-01-18", "2026-02-02", "2026-02-20",
            "2026-03-11", "2026-04-07", "2026-05-15", "2026-06-01",
        ]),
    }
)

orders = pd.DataFrame(
    {
        "order_id": list(range(1001, 1016)),
        "customer_id": [1, 2, 1, 3, 4, 2, 5, 1, 6, 3, 7, 4, 2, 8, 6],
        "order_date": pd.to_datetime([
            "2026-02-01", "2026-02-03", "2026-02-14", "2026-03-01", "2026-03-05",
            "2026-03-20", "2026-04-02", "2026-04-10", "2026-04-22", "2026-05-03",
            "2026-05-19", "2026-06-08", "2026-06-15", "2026-07-01", "2026-07-12",
        ]),
        "status": [
            "completed", "completed", "completed", "returned", "completed",
            "completed", "shipped", "completed", "completed", "completed",
            "placed", "completed", "returned", "shipped", "completed",
        ],
        "amount": [
            120.50, 45.00, 89.99, 230.00, 15.25,
            310.40, 75.00, 60.10, 199.99, 42.00,
            88.80, 150.00, 27.50, 99.95, 64.30,
        ],
    }
)

OUT.parent.mkdir(parents=True, exist_ok=True)
with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
    customers.to_excel(writer, sheet_name="customers", index=False)
    orders.to_excel(writer, sheet_name="orders", index=False)

print(f"Wrote {OUT} ({len(customers)} customers, {len(orders)} orders)")
