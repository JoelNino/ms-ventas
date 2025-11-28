#ventas/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .mongo import sales_summary
import requests
import os

INVENTORY_MS_URL = os.getenv("INVENTORY_MS_URL", "http://127.0.0.1:8001")

@api_view(['GET'])
def resumen_producto(request, product_id):

    # 1. Obtener resumen de ventas desde Mongo
    resumen = list(sales_summary.find(
        {"product_id": product_id},
        {"_id": 0}
    ))

    # 2. Obtener stock desde inventory-ms
    r = requests.get(f"{INVENTORY_MS_URL}/productos/{product_id}/stock/")

    if r.status_code != 200:
        return Response({"error": "No se pudo obtener el stock"}, status=400)

    stock_por_ciudad = r.json()

    # 3. Combinar
    resultado = []
    for item in resumen:
        city = item["city"]
        resultado.append({
            "city": city,
            "total_quantity_sold": item["total_quantity_sold"],
            "total_value_sold": item["total_value_sold"],
            "stock_available": stock_por_ciudad.get(city, 0)
        })

    return Response(resultado)
