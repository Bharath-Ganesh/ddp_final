-- ===================================================================
-- E‑Commerce Hybrid DBMS Schema (SQL Portion) – Simplified Inventory
-- ===================================================================

-- 1) Database Setup
CREATE DATABASE IF NOT EXISTS ecommerce_db;
USE ecommerce_db;

-- 2) Roles Setup
DROP ROLE IF EXISTS admin_role;
DROP ROLE IF EXISTS customer_role;
CREATE ROLE admin_role;
CREATE ROLE customer_role;

-- 3) Drop existing tables to redefine
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS CartItems;
DROP TABLE IF EXISTS Carts;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Addresses;

-- 4) Core Tables

-- 4.1) Users
CREATE TABLE Users (
  userId      BIGINT       PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  email       VARCHAR(100) UNIQUE NOT NULL,
  password    VARCHAR(255) NOT NULL,
  createdAt   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4.2) Addresses
CREATE TABLE Addresses (
  addressId   BIGINT       PRIMARY KEY AUTO_INCREMENT,
  userId      BIGINT       NOT NULL,
  street      VARCHAR(255) NOT NULL,
  city        VARCHAR(100) NOT NULL,
  state       VARCHAR(100),
  postalCode  VARCHAR(20),
  country     VARCHAR(100) NOT NULL,
  isDefault   BOOLEAN      NOT NULL DEFAULT FALSE,
  FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- 4.3) Carts
CREATE TABLE Carts (
  cartId      BIGINT       PRIMARY KEY AUTO_INCREMENT,
  userId      BIGINT       NOT NULL,
  createdAt   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- 4.4) CartItems
CREATE TABLE CartItems (
  cartId      BIGINT       NOT NULL,
  productId   VARCHAR(50)  NOT NULL,   -- logical link to NoSQL Products
  quantity    INT          NOT NULL CHECK (quantity > 0),
  PRIMARY KEY (cartId, productId),
  FOREIGN KEY (cartId) REFERENCES Carts(cartId) ON DELETE CASCADE
);

-- 4.5) Inventory
CREATE TABLE Inventory (
  inventoryId BIGINT       PRIMARY KEY AUTO_INCREMENT,
  productId   VARCHAR(50)  NOT NULL,    -- logical link to NoSQL Products
  stockQty    INT          NOT NULL CHECK (stockQty >= 0),
  reservedQty INT          NOT NULL DEFAULT 0 CHECK (reservedQty >= 0),
  updatedAt   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5) Privileges
GRANT ALL PRIVILEGES ON ecommerce_db.* TO admin_role;
GRANT SELECT, INSERT, UPDATE ON Carts TO customer_role;
GRANT SELECT, INSERT, UPDATE ON CartItems TO customer_role;
GRANT SELECT, INSERT, UPDATE ON Addresses TO customer_role;
GRANT SELECT, UPDATE ON Users TO customer_role;
GRANT SELECT, UPDATE ON Inventory TO customer_role;

-- 6) Sample Data Insertion
INSERT INTO Users (name, email, password) VALUES
('Test User', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewfT.xkGxkbv8GZi'),
('Admin User', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewfT.xkGxkbv8GZi');

INSERT INTO Addresses (userId, street, city, state, postalCode, country, isDefault) VALUES
(1, '123 Main St', 'Springfield', 'IL', '62701', 'USA', true),
(2, '456 Oak Ave', 'Springfield', 'IL', '62702', 'USA', true);

INSERT INTO Carts (userId) VALUES (1), (2);

INSERT INTO Inventory (productId, stockQty, reservedQty) VALUES 
('P1234', 100, 0),
('P5678', 50, 0); 