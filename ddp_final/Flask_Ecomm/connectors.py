import os
import mysql.connector
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

# Default values if env vars are not set
host     = os.getenv("MYSQL_HOST", "localhost")
database = os.getenv("MYSQL_DATABASE", "ecommerce_db")
user     = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "root")

def connect_mysql():
    """Establish and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            print(f"[MySQL] Connected to {database}@{host} as {user}")
            return connection
        else:
            print("[MySQL] Connection attempt returned no socket.")
            return None
    except mysql.connector.Error as e:
        print(f"[MySQL] Connection failed: {e}")
        return None

def connect_mongo():
    """Establish and return a connection to the MongoDB database."""
    try:
        print("\n[DEBUG] ====== MongoDB Connection Started ======")
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        print(f"[DEBUG] Attempting connection to MongoDB at: {mongo_uri}")
        
        client = MongoClient(mongo_uri)
        # Test the connection
        server_info = client.server_info()
        print(f"[DEBUG] MongoDB server version: {server_info.get('version')}")
        
        db = client["ecommerce_db"]  # Using same database name as MySQL
        print(f"[DEBUG] Selected database: {db.name}")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"[DEBUG] Available collections: {collections}")
        
        # Ensure the database and required collections exist
        if "product" not in collections:
            print("[DEBUG] Product collection not found, creating with sample data...")
            # Create product collection and add sample data
            products = [
                {
                    "productId": "P1234",
                    "name": "Wireless Earbuds",
                    "category": "Audio",
                    "description": "Noise-cancelling over-ear earbuds.",
                    "price": 79.99,
                    "attributes": {
                        "color": "Black",
                        "batteryLife": "8h",
                        "waterResistant": True
                    },
                    "createdAt": datetime.utcnow(),
                    "updatedAt": datetime.utcnow()
                },
                {
                    "productId": "P5678",
                    "name": "Smart Watch",
                    "description": "Fitness tracking smartwatch with heart rate monitor.",
                    "price": 149.99,
                    "category": "Wearables",
                    "attributes": {
                        "color": "Silver",
                        "batteryLife": "5d",
                        "waterResistant": True
                    },
                    "createdAt": datetime.utcnow(),
                    "updatedAt": datetime.utcnow()
                }
            ]
            db.product.insert_many(products)
            print("[DEBUG] Sample products inserted successfully")
            
        print(f"[DEBUG] Product collection document count: {db.product.count_documents({})}")
        print(f"[DEBUG] ====== MongoDB Connection Completed ======\n")
        return db
    except Exception as e:
        print(f"[ERROR] MongoDB connection failed: {str(e)}")
        print(f"[ERROR] Full error details: ", e)
        return None

# Quick smoke‐test when run as a script
if __name__ == "__main__":
    mysql_db = connect_mysql()
    if mysql_db is not None:
        print("MySQL connection successful!")
        mysql_db.close()
    
    mongo_db = connect_mongo()
    if mongo_db is not None:
        print("MongoDB connection successful!")
