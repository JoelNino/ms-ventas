from django.urls import path

# Commands
from ventas.commands.register_sale import register_sale

# Queries
from ventas.queries.resumen_producto import resumen_producto
from ventas.queries.listar_ventas import listar_ventas
from ventas.queries.obtener_venta import obtener_venta

urlpatterns = [
    # COMMANDS (POST)
    path("sales/register/", register_sale),

    # QUERIES (GET)
    path("sales/resumen/<str:product_id>/", resumen_producto),

    path("sales/all/", listar_ventas),
    path("sales/product/<str:product_id>/", obtener_venta)
]
