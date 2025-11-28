import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId

from ventas.mongo import sales, sales_summary


@api_view(["POST"])
def register_sale(request):
    """
    Command → Registra una venta en MongoDB.
    Espera:
    {
        "product_id": "P01",
        "city": "Bogotá",
        "quantity": 5,
        "unit_price": 10000
    }
    """
    try:
        data = request.data
        product_id = data["product_id"]
        city = data["city"]
        quantity = int(data["quantity"])
        unit_price = float(data["unit_price"])
    except:
        return Response({"error": "Datos inválidos"}, status=400)

    total_value = quantity * unit_price

    # Insertar venta cruda
    sale_doc = {
        "product_id": product_id,
        "city": city,
        "quantity": quantity,
        "unit_price": unit_price,
        "total_value": total_value
    }

    sales.insert_one(sale_doc)

    # Actualizar el resumen (read model)
    summary = sales_summary.find_one({"product_id": product_id, "city": city})

    if summary:
        # Ya existe, acumular
        sales_summary.update_one(
            {"product_id": product_id, "city": city},
            {
                "$inc": {
                    "total_quantity_sold": quantity,
                    "total_value_sold": total_value
                }
            }
        )
    else:
        # No existe, crear
        sales_summary.insert_one({
            "product_id": product_id,
            "city": city,
            "total_quantity_sold": quantity,
            "total_value_sold": total_value
        })

    return Response({"message": "Venta registrada."}, status=201)
