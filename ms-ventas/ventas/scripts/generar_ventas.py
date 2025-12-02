import requests
import random

VENTAS_URL = "http://127.0.0.1:8000/api/sales/register/"

# Generar productos de P001 a P500
productos = [f"P{str(i).zfill(3)}" for i in range(1, 501)]
ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"]

def generar_ventas():
    ventas_creadas = 0

    # 1. Crear al menos una venta por cada producto
    for product_id in productos:
        city = random.choice(ciudades)
        quantity = random.randint(1, 20)
        unit_price = random.randint(5000, 30000)

        data = {
            "product_id": product_id,
            "city": city,
            "quantity": quantity,
            "unit_price": unit_price
        }

        r = requests.post(VENTAS_URL, json=data)
        if r.status_code == 201:
            ventas_creadas += 1
        else:
            print(f"Error al registrar {product_id}: {r.text}")

    # 2. Opcional: crear ventas adicionales aleatorias (por ejemplo 500 más)
    for _ in range(500):
        product_id = random.choice(productos)
        city = random.choice(ciudades)
        quantity = random.randint(1, 20)
        unit_price = random.randint(5000, 30000)

        data = {
            "product_id": product_id,
            "city": city,
            "quantity": quantity,
            "unit_price": unit_price
        }

        r = requests.post(VENTAS_URL, json=data)
        if r.status_code == 201:
            ventas_creadas += 1
        else:
            print("Error:", r.text)

    print(f"✔ Ventas generadas: {ventas_creadas} registros")

if __name__ == "__main__":
    generar_ventas()
