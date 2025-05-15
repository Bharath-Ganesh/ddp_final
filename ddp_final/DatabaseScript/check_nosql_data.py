import os
from pymongo import MongoClient
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def connect_mysql():
    """Establish and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            database=os.getenv("MYSQL_DATABASE", "ecommerce_db"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root")
        )
        return connection
    except mysql.connector.Error as e:
        print(f"[MySQL] Connection failed: {e}")
        return None

def connect_mongo():
    """Establish and return a connection to the MongoDB database."""
    try:
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_uri)
        # Test the connection
        client.server_info()
        db = client["ecommerce_db"]
        print(f"[MongoDB] Connected successfully to {mongo_uri}")
        return db
    except Exception as e:
        print(f"[MongoDB] Connection failed: {e}")
        return None

def check_nosql_data():
    try:
        mongo_db = connect_mongo()
        if mongo_db is None:
            print("Failed to connect to MongoDB")
            return
        
        # List all collections
        print("\n=== Available Collections ===")
        collections = mongo_db.list_collection_names()
        print(collections)
        
        expected_collections = ['product', 'orders', 'recommendation', 'productreview', 'searchhistory']
        
        for collection in expected_collections:
            print(f"\n=== First 5 documents from {collection} ===")
            try:
                docs = list(mongo_db[collection].find({}, {'_id': 0}).limit(5))
                if not docs:
                    print(f"No documents found in {collection}")
                for doc in docs:
                    print(doc)
            except Exception as e:
                print(f"Error querying {collection}: {e}")
        
        # Check Product-CartItems relationship
        print("\n=== Checking Product references in CartItems ===")
        try:
            # Get first 5 product IDs from CartItems
            mysql_conn = connect_mysql()
            if mysql_conn:
                cursor = mysql_conn.cursor(dictionary=True)
                cursor.execute("SELECT DISTINCT productId FROM CartItems LIMIT 5")
                product_ids = [row['productId'] for row in cursor.fetchall()]
                cursor.close()
                mysql_conn.close()
                
                print("Checking these products in MongoDB:", product_ids)
                for pid in product_ids:
                    product = mongo_db.product.find_one(
                        {'productId': pid},
                        {'_id': 0, 'name': 1, 'price': 1}
                    )
                    if product:
                        print(f"Found product {pid}: {product}")
                    else:
                        print(f"Product {pid} not found in MongoDB!")
        except Exception as e:
            print(f"Error checking Product-CartItems relationship: {e}")
    except Exception as e:
        print(f"Unexpected error during MongoDB validation: {e}")

if __name__ == "__main__":
    check_nosql_data() 