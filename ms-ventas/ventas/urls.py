from django.urls import path

# Commands
from ventas.commands.register_sale import register_sale

# Queries
from ventas.queries.resumen_producto import resumen_producto

urlpatterns = [
    # COMMANDS (POST)
    path("sales/register/", register_sale),

    # QUERIES (GET)
    path("sales/resumen/<str:product_id>/", resumen_producto),
]
