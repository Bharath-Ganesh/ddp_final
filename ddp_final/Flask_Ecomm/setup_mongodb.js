// Switch to ecommerce database
db = db.getSiblingDB('ecommerce_db');

// Drop existing collections
db.product.drop();
db.searchhistory.drop();
db.recommendation.drop();
db.productreview.drop();
db.orders.drop();

// Create collections with validators
db.createCollection("product", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["productId", "name", "category", "price"],
            properties: {
                productId: { bsonType: "string" },
                name: { bsonType: "string" },
                category: { bsonType: "string" },
                description: { bsonType: "string" },
                price: { bsonType: "double" },
                attributes: { bsonType: "object" },
                createdAt: { bsonType: "date" },
                updatedAt: { bsonType: "date" }
            }
        }
    }
});

db.createCollection("searchhistory", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["userId", "terms", "searchedAt"],
            properties: {
                searchHistoryId: { bsonType: "string" },
                userId: { bsonType: "long" },
                terms: { bsonType: "string" },
                filters: { bsonType: "object" },
                searchedAt: { bsonType: "date" }
            }
        }
    }
});

db.createCollection("recommendation", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["userId", "candidates", "generatedAt"],
            properties: {
                recommendationId: { bsonType: "string" },
                userId: { bsonType: "long" },
                candidates: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["productId", "score"],
                        properties: {
                            productId: { bsonType: "string" },
                            score: { bsonType: "double" }
                        }
                    }
                },
                generatedAt: { bsonType: "date" }
            }
        }
    }
});

db.createCollection("productreview", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["userId", "productId", "rating", "createdAt"],
            properties: {
                reviewId: { bsonType: "string" },
                userId: { bsonType: "long" },
                productId: { bsonType: "string" },
                rating: { bsonType: "int" },
                comment: { bsonType: "string" },
                createdAt: { bsonType: "date" }
            }
        }
    }
});

db.createCollection("orders", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["orderId", "userId", "items", "totalAmount", "orderDate"],
            properties: {
                orderId: { bsonType: "string" },
                userId: { bsonType: "long" },
                addressId: { bsonType: "long" },
                paymentStatus: { bsonType: "string" },
                totalAmount: { bsonType: "double" },
                orderDate: { bsonType: "date" },
                items: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["productId", "quantity", "priceAtSale"],
                        properties: {
                            productId: { bsonType: "string" },
                            quantity: { bsonType: "int" },
                            priceAtSale: { bsonType: "double" }
                        }
                    }
                },
                statusHistory: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["status", "at"],
                        properties: {
                            status: { bsonType: "string" },
                            at: { bsonType: "date" }
                        }
                    }
                }
            }
        }
    }
});

// Create indexes
db.product.createIndex({ "productId": 1 }, { unique: true });
db.product.createIndex({ "category": 1 });
db.product.createIndex({ "name": "text", "description": "text" });

db.searchhistory.createIndex({ "userId": 1 });
db.searchhistory.createIndex({ "searchedAt": 1 });

db.recommendation.createIndex({ "userId": 1 });
db.recommendation.createIndex({ "generatedAt": 1 });

db.productreview.createIndex({ "productId": 1 });
db.productreview.createIndex({ "userId": 1 });
db.productreview.createIndex({ "createdAt": 1 });

db.orders.createIndex({ "userId": 1 });
db.orders.createIndex({ "orderDate": 1 });
db.orders.createIndex({ "orderId": 1 }, { unique: true });

// Insert sample data
db.product.insertMany([
    {
        productId: "P1234",
        name: "Wireless Earbuds",
        category: "Audio",
        description: "Noise-cancelling over-ear earbuds.",
        price: 79.99,
        attributes: {
            color: "Black",
            batteryLife: "8h",
            waterResistant: true
        },
        createdAt: new Date("2025-05-01T00:00:00Z"),
        updatedAt: new Date("2025-05-01T00:00:00Z")
    },
    {
        productId: "P5678",
        name: "Smart Watch",
        category: "Wearables",
        description: "Fitness tracking smartwatch with heart rate monitor.",
        price: 149.99,
        attributes: {
            color: "Silver",
            batteryLife: "5d",
            waterResistant: true
        },
        createdAt: new Date("2025-05-01T00:00:00Z"),
        updatedAt: new Date("2025-05-01T00:00:00Z")
    }
]); 