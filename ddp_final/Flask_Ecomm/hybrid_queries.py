# hybrid_queries.py
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
from connectors import connect_mysql, connect_mongo

# Establish DB connections
print("\n====== Initializing Database Connections ======")
mongo_db = connect_mongo()
if mongo_db is not None:
    print("MongoDB connection established successfully")
else:
    print("Failed to establish MongoDB connection")

# 1: Show items in user's cart with product details
def show_cart_items(user_id):
    print(f"\n====== Show Cart Items Function ======")
    print(f"Parameters: user_id={user_id}")
    
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    try:
        print("Executing MySQL query for cart items...")
        cursor.execute(
            """
            SELECT ci.productId, ci.quantity 
            FROM CartItems ci 
            JOIN Carts c ON ci.cartId = c.cartId 
            WHERE c.userId = %s
            """,
            (user_id,)
        )
        cart_rows = cursor.fetchall()
        print(f"Found {len(cart_rows)} items in cart")
        print(f"Cart rows: {cart_rows}")
        
        result = []
        for r in cart_rows:
            print(f"Looking up product {r['productId']} in MongoDB")
            prod = mongo_db.product.find_one(
                {'productId': r['productId']},
                {'name': 1, 'price': 1}
            )
            print(f"MongoDB result for {r['productId']}: {prod}")
            if prod:
                result.append({
                    'productId': r['productId'],
                    'quantity': r['quantity'],
                    'name': prod.get('name'),
                    'price': prod.get('price')
                })
        print(f"Final result: {result}")
        return result
    except Exception as e:
        print(f"Error in show_cart_items: {str(e)}")
        print(f"Full error details: ", e)
        raise
    finally:
        print("Closing MySQL connection")
        cursor.close()
        conn.close()

# 2: Get user's order history
def get_order_history(user_id):
    try:
        # Orders are now stored in MongoDB
        orders = list(mongo_db.orders.find(
            {'userId': user_id},
            {'_id': 0}  # Exclude MongoDB _id
        ).sort('orderDate', -1))  # Sort by order date descending
        
        # Enrich with address details from MySQL
        conn = connect_mysql()
        cursor = conn.cursor(dictionary=True)
        
        for order in orders:
            if 'addressId' in order:
                cursor.execute(
                    """
                    SELECT street, city, state, postalCode, country 
                    FROM Addresses 
                    WHERE addressId = %s
                    """,
                    (order['addressId'],)
                )
                address = cursor.fetchone()
                if address:
                    order['shippingAddress'] = address
                    
        return orders
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 3: Search products with filters
def search_products(query, filters=None):
    try:
        # Build the search query
        search_query = {
            '$text': {'$search': query}
        }
        
        if filters:
            for key, value in filters.items():
                if key == 'price':
                    if 'min' in value:
                        search_query['price'] = search_query.get('price', {})
                        search_query['price']['$gte'] = value['min']
                    if 'max' in value:
                        search_query['price'] = search_query.get('price', {})
                        search_query['price']['$lte'] = value['max']
                elif key == 'category':
                    search_query['category'] = value
                elif key == 'attributes':
                    for attr_key, attr_value in value.items():
                        search_query[f'attributes.{attr_key}'] = attr_value
        
        # Execute search
        results = list(mongo_db.product.find(
            search_query,
            {'_id': 0}  # Exclude MongoDB _id
        ))
        
        # Log search history
        if results:  # Only log successful searches
            mongo_db.searchhistory.insert_one({
                'userId': None,  # Can be updated if user is logged in
                'terms': query,
                'filters': filters,
                'searchedAt': datetime.utcnow()
            })
            
        return results
    except Exception as e:
        print(f"Error in search_products: {str(e)}")
        raise

# 4: Get product recommendations
def get_recommendations(user_id):
    try:
        # Get user's latest recommendation
        rec = mongo_db.recommendation.find_one(
            {'userId': user_id},
            sort=[('generatedAt', -1)]
        )
        
        if not rec:
            return []
            
        # Get full product details for recommended products
        recommended_products = []
        for candidate in rec.get('candidates', []):
            product = mongo_db.product.find_one(
                {'productId': candidate['productId']},
                {'_id': 0}  # Exclude MongoDB _id
            )
            if product:
                product['score'] = candidate['score']
                recommended_products.append(product)
                
        return recommended_products
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        raise

# 5: Add product review
def add_review(user_id, product_id, rating, comment):
    try:
        review = {
            'reviewId': f"R{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'userId': user_id,
            'productId': product_id,
            'rating': rating,
            'comment': comment,
            'createdAt': datetime.utcnow()
        }
        
        result = mongo_db.productreview.insert_one(review)
        return bool(result.inserted_id)
    except Exception as e:
        print(f"Error in add_review: {str(e)}")
        raise

# 6: Get product reviews
def get_product_reviews(product_id):
    try:
        reviews = list(mongo_db.productreview.find(
            {'productId': product_id},
            {'_id': 0}  # Exclude MongoDB _id
        ).sort('createdAt', -1))
        
        # Enrich with user names from MySQL
        conn = connect_mysql()
        cursor = conn.cursor(dictionary=True)
        
        for review in reviews:
            cursor.execute(
                "SELECT name FROM Users WHERE userId = %s",
                (review['userId'],)
            )
            user = cursor.fetchone()
            if user:
                review['userName'] = user['name']
                
        return reviews
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# 7: Check inventory
def check_inventory(product_id):
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT stockQty, reservedQty 
            FROM Inventory 
            WHERE productId = %s
            """,
            (product_id,)
        )
        inventory = cursor.fetchone()
        if inventory:
            inventory['availableQty'] = inventory['stockQty'] - inventory['reservedQty']
        return inventory or {'stockQty': 0, 'reservedQty': 0, 'availableQty': 0}
    finally:
        cursor.close()
        conn.close()

# Add these functions after the existing ones

def add_to_cart(user_id, product_id, quantity):
    """Add an item to user's cart."""
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get or create cart for user
        cursor.execute(
            "SELECT cartId FROM Carts WHERE userId = %s",
            (user_id,)
        )
        cart = cursor.fetchone()
        
        if not cart:
            cursor.execute(
                "INSERT INTO Carts (userId, createdAt, updatedAt) VALUES (%s, NOW(), NOW())",
                (user_id,)
            )
            cart_id = cursor.lastrowid
        else:
            cart_id = cart['cartId']
            
        # Add/update cart item
        cursor.execute("""
            INSERT INTO CartItems (cartId, productId, quantity) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """, (cart_id, product_id, quantity))
        
        conn.commit()
        return {"cartId": cart_id, "added": True}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def place_order(user_id, address_id):
    """Place an order for all items in user's cart."""
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get cart items
        cursor.execute("""
            SELECT ci.productId, ci.quantity, p.price 
            FROM CartItems ci 
            JOIN Carts c ON ci.cartId = c.cartId 
            JOIN product p ON ci.productId = p.productId
            WHERE c.userId = %s
        """, (user_id,))
        items = cursor.fetchall()
        
        if not items:
            raise Exception("Cart is empty")
            
        # Calculate total
        total_amount = sum(item['price'] * item['quantity'] for item in items)
        
        # Create order in MongoDB
        order_id = f"O{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        order = {
            "orderId": order_id,
            "userId": user_id,
            "addressId": address_id,
            "items": [
                {
                    "productId": item['productId'],
                    "quantity": item['quantity'],
                    "priceAtSale": item['price']
                }
                for item in items
            ],
            "totalAmount": total_amount,
            "orderDate": datetime.utcnow(),
            "paymentStatus": "PENDING",
            "statusHistory": [
                {
                    "status": "PLACED",
                    "at": datetime.utcnow()
                }
            ]
        }
        
        # Insert order to MongoDB
        mongo_db.orders.insert_one(order)
        
        # Update inventory
        for item in items:
            cursor.execute("""
                UPDATE Inventory 
                SET stockQty = stockQty - %s,
                    updatedAt = NOW()
                WHERE productId = %s AND stockQty >= %s
            """, (item['quantity'], item['productId'], item['quantity']))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise Exception(f"Not enough stock for product {item['productId']}")
        
        # Clear cart
        cursor.execute("""
            DELETE ci FROM CartItems ci
            JOIN Carts c ON ci.cartId = c.cartId
            WHERE c.userId = %s
        """, (user_id,))
        
        conn.commit()
        return {"orderId": order_id}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def check_order_status(order_id):
    """Check the status of an order."""
    try:
        # Find order in MongoDB
        order = mongo_db.orders.find_one(
            {'orderId': order_id},
            {
                '_id': 0,
                'orderId': 1,
                'paymentStatus': 1,
                'statusHistory': 1,
                'orderDate': 1
            }
        )
        
        if not order:
            raise Exception(f"Order {order_id} not found")
            
        # Get the latest status from status history
        current_status = order['statusHistory'][-1] if order['statusHistory'] else None
        
        return {
            'orderId': order['orderId'],
            'paymentStatus': order['paymentStatus'],
            'currentStatus': current_status['status'] if current_status else None,
            'statusUpdatedAt': current_status['at'] if current_status else None,
            'orderDate': order['orderDate']
        }
    except Exception as e:
        print(f"Error checking order status: {str(e)}")
        raise

def write_review(user_id, product_id, rating, comment):
    """Write a review for a product."""
    try:
        # First check if product exists
        product = mongo_db.product.find_one({'productId': product_id})
        if not product:
            raise Exception(f"Product {product_id} not found")
            
        # Check if user has already reviewed this product
        existing_review = mongo_db.productreview.find_one({
            'userId': user_id,
            'productId': product_id
        })
        
        if existing_review:
            raise Exception("User has already reviewed this product")
            
        # Create review document
        review = {
            'reviewId': f"R{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'userId': user_id,
            'productId': product_id,
            'rating': rating,
            'comment': comment,
            'createdAt': datetime.utcnow()
        }
        
        # Insert review
        result = mongo_db.productreview.insert_one(review)
        
        if not result.inserted_id:
            raise Exception("Failed to insert review")
            
        return {
            'reviewId': review['reviewId'],
            'status': 'success',
            'message': 'Review added successfully'
        }
    except Exception as e:
        print(f"Error writing review: {str(e)}")
        raise
