from django.urls import path
from .views import resumen_producto

urlpatterns = [
    path('resumen/<str:product_id>/', resumen_producto),
]
