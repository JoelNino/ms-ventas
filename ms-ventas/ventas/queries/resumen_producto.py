from rest_framework.response import Response
from rest_framework.decorators import api_view
from ventas.mongo import sales_summary
import requests
import os

INVENTORY_MS_URL = os.getenv("INVENTORY_MS_URL", "http://127.0.0.1:8001")


@api_view(["GET"])
def resumen_producto(request, product_id):
    """
    Query → Retorna el resumen final del producto:
    - total vendido por ciudad
    - dinero total por ciudad
    - stock disponible por ciudad (viene del ms-inventory)
    """

    # 1. Leer el read-model desde Mongo
    resumen = list(sales_summary.find(
        {"product_id": product_id},
        {"_id": 0}
    ))

    # 2. Pedir stock al ms-inventory
    r = requests.get(f"{INVENTORY_MS_URL}/api/inventory/stock/{product_id}/")

    if r.status_code != 200:
        return Response({"error": "No se pudo obtener el stock"}, status=400)

    stock_response = r.json()  # {"sku": "P01", "stock_por_ciudad": [...]}  

    # Convertir stock a dict para usarlo fácil:
    stock_dict = {
        item["city"]: item["stock"]
        for item in stock_response.get("stock_por_ciudad", [])
    }

    # 3. Combinar ventas + inventario
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
