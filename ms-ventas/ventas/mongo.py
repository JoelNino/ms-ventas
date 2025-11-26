import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ms_ventas_db"]

sales = db["sales"]
sales_summary = db["sales_summary"]
