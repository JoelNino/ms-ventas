import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ventas.mongo import sales, sales_summary


@api_view(["POST"])
def register_sale(request):
    """
    COMMAND → Registra una venta en MongoDB y actualiza el read model.
    Espera:
    {
        "product_id": "P001",
        "city": "Bogotá",
        "quantity": 5,
        "unit_price": 10000
    }
    """

    # ----------------------------
    # 1. Validar datos de entrada
    # ----------------------------
    data = request.data

    required_fields = ["product_id", "city", "quantity", "unit_price"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return Response({"error": f"Faltan campos: {missing}"}, status=400)

    try:
        product_id = str(data["product_id"])
        city = str(data["city"])
        quantity = int(data["quantity"])
        unit_price = float(data["unit_price"])
    except Exception:
        return Response({"error": "Tipos de datos inválidos."}, status=400)

    if quantity <= 0:
        return Response({"error": "La cantidad debe ser mayor que 0."}, status=400)

    if unit_price <= 0:
        return Response({"error": "El precio debe ser mayor a 0."}, status=400)

    total_value = quantity * unit_price

    # ----------------------------
    # 2. Guardar venta cruda
    # ----------------------------
    sale_doc = {
        "product_id": product_id,
        "city": city,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_value": total_value
    }

    sales.insert_one(sale_doc)

    # ----------------------------
    # 3. Actualizar read-model
    # ----------------------------
    sales_summary.update_one(
        {"product_id": product_id, "city": city},
        {
            "$inc": {
                "total_quantity_sold": quantity,
                "total_value_sold": total_value
            }
        },
        upsert=True  # si no existe, lo crea
    )

    return Response({
        "message": "Venta registrada exitosamente.",
        "product_id": product_id,
        "city": city,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_value": total_value
    }, status=201)
