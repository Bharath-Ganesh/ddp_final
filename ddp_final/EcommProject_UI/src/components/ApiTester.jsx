import React, { useState } from "react";
import axios from "axios";

const ApiTester = () => {
  // State management
  const [userId, setUserId] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [productId, setProductId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [responses, setResponses] = useState({});
  const [loading, setLoading] = useState({});

  // Base URL for API calls
  const API_BASE_URL = "http://localhost:5000";

  // Helper to update responses
  const updateResponse = (key, data) => {
    setResponses((prev) => ({
      ...prev,
      [key]: data,
    }));
  };

  // Helper to manage loading states
  const withLoading = async (key, operation) => {
    setLoading((prev) => ({ ...prev, [key]: true }));
    try {
      await operation();
    } finally {
      setLoading((prev) => ({ ...prev, [key]: false }));
    }
  };

  // API Handlers
  const getCart = () =>
    withLoading("cart", async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/cart/${userId}`);
        updateResponse("cart", response.data);
      } catch (error) {
        updateResponse("cart", { error: error.message });
      }
    });

  const getOrders = () =>
    withLoading("orders", async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/orders/${userId}`);
        updateResponse("orders", response.data);
      } catch (error) {
        updateResponse("orders", { error: error.message });
      }
    });

  const getRecommendations = () =>
    withLoading("recommendations", async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/recommendations/${userId}`
        );
        updateResponse("recommendations", response.data);
      } catch (error) {
        updateResponse("recommendations", { error: error.message });
      }
    });

  const searchProducts = () =>
    withLoading("search", async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/search`, {
          params: { q: searchTerm, user_id: userId },
        });
        updateResponse("search", response.data);
      } catch (error) {
        updateResponse("search", { error: error.message });
      }
    });

  const addToCart = () =>
    withLoading("addToCart", async () => {
      try {
        const response = await axios.post(`${API_BASE_URL}/cart/add`, {
          user_id: userId,
          product_id: productId,
          quantity: quantity,
        });
        updateResponse("addToCart", response.data);
      } catch (error) {
        updateResponse("addToCart", { error: error.message });
      }
    });

  const placeOrder = () =>
    withLoading("placeOrder", async () => {
      try {
        const response = await axios.post(`${API_BASE_URL}/order/place`, {
          user_id: userId,
        });
        updateResponse("placeOrder", response.data);
      } catch (error) {
        updateResponse("placeOrder", { error: error.message });
      }
    });

  return (
    <div className="App">
      <header className="header">
        <h1>E-commerce API Tester</h1>
        <p>Test your hybrid SQL/NoSQL operations</p>
      </header>

      <div className="container">
        {/* Common Inputs */}
        <div className="input-group">
          <label>
            User ID:
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Enter user ID"
            />
          </label>
        </div>

        {/* Get Cart Section */}
        <div className="api-section" data-section="cart">
          <h3>Get Cart</h3>
          <button
            onClick={getCart}
            className={loading.cart ? "loading" : ""}
            disabled={loading.cart}
          >
            {loading.cart ? "Loading..." : "Get Cart Items"}
          </button>
          <div className="response-container">
            <pre className={responses.cart?.error ? "error-response" : ""}>
              {JSON.stringify(responses.cart, null, 2)}
            </pre>
          </div>
        </div>

        {/* Get Orders Section */}
        <div className="api-section" data-section="orders">
          <h3>Get Orders</h3>
          <button
            onClick={getOrders}
            className={loading.orders ? "loading" : ""}
            disabled={loading.orders}
          >
            {loading.orders ? "Loading..." : "Get Orders"}
          </button>
          <div className="response-container">
            <pre className={responses.orders?.error ? "error-response" : ""}>
              {JSON.stringify(responses.orders, null, 2)}
            </pre>
          </div>
        </div>

        {/* Get Recommendations Section */}
        <div className="api-section" data-section="recommendations">
          <h3>Get Recommendations</h3>
          <button
            onClick={getRecommendations}
            className={loading.recommendations ? "loading" : ""}
            disabled={loading.recommendations}
          >
            {loading.recommendations ? "Loading..." : "Get Recommendations"}
          </button>
          <div className="response-container">
            <pre
              className={
                responses.recommendations?.error ? "error-response" : ""
              }
            >
              {JSON.stringify(responses.recommendations, null, 2)}
            </pre>
          </div>
        </div>

        {/* Search Products Section */}
        <div className="api-section" data-section="search">
          <h3>Search Products</h3>
          <div className="input-group">
            <label>
              Search Term:
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Enter search term"
              />
            </label>
          </div>
          <button
            onClick={searchProducts}
            className={loading.search ? "loading" : ""}
            disabled={loading.search}
          >
            {loading.search ? "Searching..." : "Search"}
          </button>
          <div className="response-container">
            <pre className={responses.search?.error ? "error-response" : ""}>
              {JSON.stringify(responses.search, null, 2)}
            </pre>
          </div>
        </div>

        {/* Add to Cart Section */}
        <div className="api-section" data-section="cart">
          <h3>Add to Cart</h3>
          <div className="input-group">
            <label>
              Product ID:
              <input
                type="text"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
                placeholder="Enter product ID"
              />
            </label>
          </div>
          <div className="input-group">
            <label>
              Quantity:
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value) || 0)}
                min="1"
                placeholder="Enter quantity"
              />
            </label>
          </div>
          <button
            onClick={addToCart}
            className={loading.addToCart ? "loading" : ""}
            disabled={loading.addToCart}
          >
            {loading.addToCart ? "Adding..." : "Add to Cart"}
          </button>
          <div className="response-container">
            <pre className={responses.addToCart?.error ? "error-response" : ""}>
              {JSON.stringify(responses.addToCart, null, 2)}
            </pre>
          </div>
        </div>

        {/* Place Order Section */}
        <div className="api-section" data-section="orders">
          <h3>Place Order</h3>
          <button
            onClick={placeOrder}
            className={loading.placeOrder ? "loading" : ""}
            disabled={loading.placeOrder}
          >
            {loading.placeOrder ? "Processing..." : "Place Order"}
          </button>
          <div className="response-container">
            <pre
              className={responses.placeOrder?.error ? "error-response" : ""}
            >
              {JSON.stringify(responses.placeOrder, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApiTester;
