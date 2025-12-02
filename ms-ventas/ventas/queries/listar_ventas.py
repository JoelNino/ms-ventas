from rest_framework.decorators import api_view
from rest_framework.response import Response
from ventas.mongo import sales




@api_view(["GET"])
def listar_ventas(request):
    """
    Query → Retorna TODAS las ventas registradas en MongoDB.
    """

    ventas = list(sales.find({}, {"_id": 0}))  # Quitamos _id para no molestar

    return Response({
        "total": len(ventas),
        "ventas": ventas
    })
