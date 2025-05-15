import mysql.connector
import os
from dotenv import load_dotenv

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
        if connection.is_connected():
            print(f"[MySQL] Connected successfully")
            db_info = connection.get_server_info()
            print(f"[MySQL] Server version: {db_info}")
            return connection
        else:
            print("[MySQL] Connection attempt returned no socket.")
            return None
    except mysql.connector.Error as e:
        print(f"[MySQL] Connection failed: {e}")
        return None

def check_sql_data():
    conn = connect_mysql()
    if not conn:
        print("Failed to connect to MySQL database")
        return
        
    cursor = conn.cursor(dictionary=True)
    
    tables = ['Users', 'Addresses', 'Carts', 'CartItems', 'Inventory']
    
    try:
        # First check if tables exist
        cursor.execute("SHOW TABLES")
        existing_tables = cursor.fetchall()
        print("\n=== Existing Tables ===")
        print([table['Tables_in_' + os.getenv("MYSQL_DATABASE", "ecommerce_db")] for table in existing_tables])
        
        for table in tables:
            print(f"\n=== First 5 rows from {table} ===")
            try:
                cursor.execute(f"SELECT * FROM {table} LIMIT 5")
                rows = cursor.fetchall()
                if not rows:
                    print(f"No data found in {table}")
                for row in rows:
                    print(row)
            except mysql.connector.Error as e:
                print(f"Error querying {table}: {e}")
                
        # Check specific relationships
        print("\n=== Checking Cart-CartItems relationship ===")
        try:
            cursor.execute("""
                SELECT c.cartId, c.userId, ci.productId, ci.quantity 
                FROM Carts c 
                LEFT JOIN CartItems ci ON c.cartId = ci.cartId 
                LIMIT 5
            """)
            rows = cursor.fetchall()
            if not rows:
                print("No cart relationships found")
            for row in rows:
                print(row)
        except mysql.connector.Error as e:
            print(f"Error checking cart relationships: {e}")
            
        # Check User-Address relationship
        print("\n=== Checking User-Address relationship ===")
        try:
            cursor.execute("""
                SELECT u.userId, u.name, a.street, a.city, a.isDefault 
                FROM Users u 
                LEFT JOIN Addresses a ON u.userId = a.userId 
                LIMIT 5
            """)
            rows = cursor.fetchall()
            if not rows:
                print("No user-address relationships found")
            for row in rows:
                print(row)
        except mysql.connector.Error as e:
            print(f"Error checking user-address relationships: {e}")
            
    finally:
        cursor.close()
        conn.close()

def create_tables():
    conn = connect_mysql()
    if not conn:
        return
        
    cursor = conn.cursor()
    try:
        # Create ProductCatalog table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductCatalog (
            ProductID VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(255) NOT NULL,
            Description TEXT,
            Price DECIMAL(10,2) NOT NULL,
            Category VARCHAR(50)
        )
        """)
        
        # Insert some sample products if table is empty
        cursor.execute("SELECT COUNT(*) FROM ProductCatalog")
        count = cursor.fetchone()[0]
        
        if count == 0:
            products = [
                ('P1001', 'Gaming Laptop', 'High performance gaming laptop', 1299.99, 'Electronics'),
                ('P1002', 'Smartphone', 'Latest model smartphone', 899.99, 'Electronics'),
                ('P1003', 'Wireless Earbuds', 'Noise cancelling earbuds', 199.99, 'Electronics'),
                ('P1004', 'Smart Watch', 'Fitness tracking smartwatch', 299.99, 'Electronics'),
                ('P1005', 'Portable Charger', '20000mAh power bank', 39.99, 'Electronics')
            ]
            cursor.executemany(
                "INSERT INTO ProductCatalog (ProductID, Name, Description, Price, Category) VALUES (%s, %s, %s, %s, %s)",
                products
            )
            print("[MySQL] Inserted sample products")
            
        conn.commit()
        print("[MySQL] Tables verified/created successfully")
        
    except mysql.connector.Error as e:
        print(f"[MySQL] Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_sql_data()
    create_tables() 