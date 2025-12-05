import os
import requests
import time
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ventas.mongo import sales_summary

# Leer URL del microservicio de inventario desde variable de entorno (si no existe usa la fija)
INVENTORY_MS_URL = os.getenv("INVENTORY_MS_URL", "http://13.221.18.236:8001")


@api_view(["GET"])
def resumen_producto(request, product_id):
    start_time = time.time()  # Inicia medición de tiempo

    # Consultar resumen de ventas en MongoDB
    resumen = list(
        sales_summary.find(
            {"product_id": product_id},
            {"_id": 0}
        )
    )

    # Consultar stock en el microservicio de inventario
    try:
        r = requests.get(f"{INVENTORY_MS_URL}/api/inventario/stock/{product_id}/")
    except requests.exceptions.RequestException:
        return Response({"error": "Error al conectar con el microservicio de inventario"}, status=500)

    if r.status_code != 200:
        return Response({"error": "No se pudo obtener el stock"}, status=400)

    stock_response = r.json()

    # Crear diccionario con stock por ciudad
    stock_dict = {
        item["city"]: item["quantity"]
        for item in stock_response.get("stock_por_ciudad", [])
    }

    # Unir ventas con stock
    resultado = []
    for item in resumen:
        city = item["city"]
        resultado.append({
            "city": city,
            "total_quantity_sold": item.get("total_quantity_sold", 0),
            "total_value_sold": item.get("total_value_sold", 0),
            "stock_available": stock_dict.get(city, 0)
        })

    end_time = time.time()
    elapsed_ms = int((end_time - start_time) * 1000)  # Tiempo en milisegundos

    return Response({
        "product_id": product_id,
        "resumen": resultado,
        "tiempo_ms": elapsed_ms
    })
