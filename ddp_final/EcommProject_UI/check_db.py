import mysql.connector
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def check_mysql():
    print("\n=== Checking MySQL Database ===")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            database=os.getenv("MYSQL_DATABASE", "ecommerce_db"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root")
        )
        
        if not conn.is_connected():
            print("Failed to connect to MySQL")
            return
            
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\nExisting tables:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Sample each table
        for table in tables:
            table_name = table[0]
            print(f"\nSampling {table_name}:")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            row = cursor.fetchone()
            if row:
                print(row)
            else:
                print("(empty table)")
                
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def check_mongodb():
    print("\n=== Checking MongoDB Database ===")
    try:
        client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
        db = client.ecommerce_nosql
        
        # List collections
        collections = db.list_collection_names()
        print("\nExisting collections:")
        for coll in collections:
            print(f"- {coll}")
            
        # Sample each collection
        for coll in collections:
            print(f"\nSampling {coll}:")
            doc = db[coll].find_one()
            if doc:
                print(doc)
            else:
                print("(empty collection)")
                
    except Exception as e:
        print(f"MongoDB Error: {e}")

if __name__ == "__main__":
    check_mysql()
    check_mongodb() 