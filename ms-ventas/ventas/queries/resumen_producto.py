from rest_framework.response import Response
from rest_framework.decorators import api_view
from ventas.mongo import sales_summary
import requests
import os

# Leer URL del microservicio de inventario desde variable de entorno
INVENTORY_MS_URL = os.getenv("INVENTORY_MS_URL", "http://127.0.0.1:8001")

@api_view(["GET"])
def resumen_producto(request, product_id):

    resumen = list(sales_summary.find(
        {"product_id": product_id},
        {"_id": 0}
    ))

    r = requests.get(f"{INVENTORY_MS_URL}/api/inventario/stock/{product_id}/")

    if r.status_code != 200:
        return Response({"error": "No se pudo obtener el stock"}, status=400)

    stock_response = r.json()

    # FIX: usar quantity, no stock
    stock_dict = {
        item["city"]: item["quantity"]
        for item in stock_response.get("stock_por_ciudad", [])
    }

    resultado = []
    for item in resumen:
        city = item["city"]
        resultado.append({
            "city": city,
            "total_quantity_sold": item["total_quantity_sold"],
            "total_value_sold": item["total_value_sold"],
            "stock_available": stock_dict.get(city, 0)
        })

    return Response({
        "product_id": product_id,
        "resumen": resultado
    })
