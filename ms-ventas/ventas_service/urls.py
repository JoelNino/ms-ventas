from django.urls import path, include

urlpatterns = [
    path('ventas/', include('ventas.urls')),
]
