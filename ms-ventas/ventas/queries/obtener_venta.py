from rest_framework.decorators import api_view
from rest_framework.response import Response
from ventas.mongo import sales

@api_view(["GET"])
def obtener_venta(request, product_id):
    """
    Retorna todas las ventas registradas de un producto dado.
    """
    # Buscar ventas del producto en MongoDB
    ventas_producto = list(sales.find(
        {"product_id": product_id},
        {"_id": 0}  # Excluir el _id de MongoDB
    ))

    if not ventas_producto:
        return Response({"message": f"No hay ventas registradas para el producto {product_id}"}, status=404)

    return Response({
        "product_id": product_id,
        "ventas": ventas_producto
    })
