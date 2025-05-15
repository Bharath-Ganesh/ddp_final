# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from hybrid_queries import (
    show_cart_items,
    get_order_history,
    get_recommendations,
    search_products,
    add_review,
    get_product_reviews,
    check_inventory,
    add_to_cart,
    place_order,
    check_order_status,
    write_review
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        items = show_cart_items(user_id)
        return jsonify({"status": "success", "items": items})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    try:
        orders = get_order_history(user_id)
        return jsonify({"status": "success", "orders": orders})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/products/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    try:
        recommendations = get_recommendations(user_id)
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/products/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query', '')
        filters = {
            'category': request.args.get('category'),
            'price': {
                'min': float(request.args.get('minPrice', 0)),
                'max': float(request.args.get('maxPrice', float('inf')))
            },
            'attributes': {}  # Can be expanded based on query parameters
        }
        results = search_products(query, filters)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/cart/add', methods=['POST'])
def add_item_to_cart():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        product_id = data.get('productId')
        quantity = data.get('productId', 1)
        
        # First check inventory
        inventory = check_inventory(product_id)
        if inventory['availableQty'] < quantity:
            return jsonify({
                "status": "error",
                "message": "Not enough stock available"
            }), 400
            
        # Add to cart
        result = add_to_cart(user_id, product_id, quantity)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders/place', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        address_id = data.get('addressId')
        
        result = place_order(user_id, address_id)
        return jsonify({
            "status": "success",
            "orderId": result['orderId'],
            "message": "Order placed successfully"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/products/<product_id>/reviews', methods=['POST'])
def add_product_review(product_id):
    try:
        data = request.get_json()
        user_id = data.get('userId')
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not all([user_id, rating, comment]):
            return jsonify({
                "status": "error",
                "message": "Missing required fields"
            }), 400
            
        result = write_review(user_id, product_id, rating, comment)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/products/<product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    try:
        reviews = get_product_reviews(product_id)
        return jsonify({
            "status": "success",
            "reviews": reviews
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/orders/<order_id>/status', methods=['GET'])
def check_status(order_id):
    try:
        status = check_order_status(order_id)
        return jsonify({
            "status": "success",
            "orderStatus": status
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/review', methods=['POST'])
def api_write_review():
    print(f"\n====== API: Write Review ======")
    payload = request.json
    print(f"Request payload: {payload}")

    user_id = payload.get('user_id')
    product_id = payload.get('product_id')
    rating = payload.get('rating')
    comment = payload.get('comment')

    if not all([user_id, product_id, rating, comment]):
        print("Missing required fields in payload")
        return jsonify({'error': 'Missing fields'}), 400
    try:
        result = write_review(user_id, product_id, rating, comment)
        print(f"Review written successfully: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error in write_review: {str(e)}")
        print(f"Full error details: ", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, use_reloader=True, reloader_type='stat')
