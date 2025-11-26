from .mongo import sales, sales_summary
from datetime import datetime
import requests
import os

INVENTORY_MS_URL = os.getenv("INVENTORY_MS_URL")

def registrar_venta(product_id, city, quantity, unit_price):
    total_value = quantity * unit_price
    now = datetime.utcnow()

    # 1. Guardar venta cruda
    sales.insert_one({
        "product_id": product_id,
        "city": city,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_value": total_value,
        "sale_timestamp": now,
    })

    # 2. Actualizar resumen
    sales_summary.update_one(
        {"product_id": product_id, "city": city},
        {
            "$inc": {
                "total_quantity_sold": quantity,
                "total_value_sold": total_value
            },
            "$set": {
                "last_sale_at": now
            }
        },
        upsert=True
    )
