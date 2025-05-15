from connectors import connect_mongo

def check_nosql_data():
    mongo_db = connect_mongo()
    
    # List all collections
    print("\n=== Available Collections ===")
    collections = mongo_db.list_collection_names()
    print(collections)
    
    # Check Product collection
    print("\n=== First 5 Products ===")
    products = list(mongo_db.Product.find().limit(5))
    for product in products:
        print(product)
    
    # Check Order collection
    print("\n=== First 5 Orders ===")
    orders = list(mongo_db.Order.find().limit(5))
    for order in orders:
        print(order)
    
    # Check Recommendation collection
    print("\n=== First 5 Recommendations ===")
    recommendations = list(mongo_db.Recommendation.find().limit(5))
    for rec in recommendations:
        print(rec)
    
    # Check Review collection
    print("\n=== First 5 Reviews ===")
    reviews = list(mongo_db.Review.find().limit(5))
    for review in reviews:
        print(review)
    
    # Check SearchHistory collection
    print("\n=== First 5 Search History Records ===")
    searches = list(mongo_db.SearchHistory.find().limit(5))
    for search in searches:
        print(search)

if __name__ == "__main__":
    check_nosql_data() 