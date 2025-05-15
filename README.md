Readme.md

# Distributed Database Project - E-Commerce Platform

## Team Members (Group 14)

- Bharath Ganesh
- Alisha Rawat
- Juhi Khare

## Project Overview

This project implements a distributed database system for an e-commerce platform, combining both SQL and NoSQL databases to leverage their respective strengths. The system includes a backend API service built with Flask and a modern React-based frontend interface.

## Architecture

The project follows a distributed architecture with the following components:

- **Frontend**: React.js based UI with modern component architecture
- **Backend**: Flask-based RESTful API service
- **Databases**:
  - MySQL for transactional data (orders, users, inventory)
  - MongoDB for unstructured data (product details, reviews, recommendations)

## Features

- 🛒 Shopping Cart Management
- 📦 Order Processing and Tracking
- 🔍 Advanced Product Search
- ⭐ Product Recommendations
- 👤 User Authentication
- 📊 Inventory Management
- 💳 Transaction Processing
- 📝 Product Reviews and Ratings

## Technology Stack

### Frontend

- React.js
- React Router for navigation
- CSS3 with Custom Variables
- Axios for API communication

### Backend

- Python Flask
- MySQL Connector
- PyMongo
- RESTful API architecture

### Databases

- MySQL for structured data
- MongoDB for unstructured data

## Project Structure

```
project/
├── Frontend (React)
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   └── public/
│
├── Backend (Flask)
│   ├── app.py
│   ├── connectors.py
│   ├── hybrid_queries.py
│   └── check_data/
│
└── Database Scripts
    ├── setup_mysql.sql
    └── setup_mongodb.js
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- MySQL Server
- MongoDB
- Git

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd EcommProject_UI
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend Setup

1. Create a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure database connections:

   - Update MySQL connection settings in `connectors.py`
   - Update MongoDB connection settings in `connectors.py`

4. Run the Flask application:
   ```bash
   python app.py
   ```

### Database Setup

1. MySQL Setup:

   ```bash
   mysql -u root -p < setup_mysql.sql
   ```

2. MongoDB Setup:
   ```bash
   mongosh < setup_mongodb.js
   ```

## API Documentation

The backend provides the following RESTful endpoints:

### Products

- GET `/api/products` - List all products
- GET `/api/products/{id}` - Get product details
- POST `/api/products` - Add new product
- PUT `/api/products/{id}` - Update product

### Orders

- GET `/api/orders` - List user orders
- POST `/api/orders` - Create new order
- GET `/api/orders/{id}` - Get order details

### Cart

- GET `/api/cart` - View cart
- POST `/api/cart` - Add to cart
- DELETE `/api/cart/{id}` - Remove from cart

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing

- Frontend: `npm test`
- Backend: `python -m pytest tests/`
- Database: Run test scripts in `check_data/`

## Performance Considerations

- Implemented database indexing for faster queries
- Caching layer for frequently accessed data
- Optimized database queries for better performance
- Load balancing considerations for scalability

## Security Measures

- Input validation and sanitization
- SQL injection prevention
- Authentication and authorization
- Secure password hashing
- CORS configuration
- Rate limiting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Course Instructor: [Instructor Name]
- Teaching Assistants
- Database design principles and best practices
- Open source community

## Contact

For any queries regarding the project, please reach out to:

- Bharath Ganesh - [Add contact information]
- [Add other team members' contact information]
