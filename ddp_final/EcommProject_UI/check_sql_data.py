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
        table_names = [list(table.values())[0] for table in existing_tables]
        print("\n=== Existing Tables ===")
        print(table_names)
        
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
                SELECT u.userId, u.name, u.defaultAddressId, a.street, a.city 
                FROM Users u 
                LEFT JOIN Addresses a ON u.defaultAddressId = a.addressId 
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

if __name__ == "__main__":
    check_sql_data() 