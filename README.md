# APICREATION

A simple Node.js-based API server demonstrating CRUD operations with MongoDB. This project is built for learning and experimenting with custom API development, database integration, and backend setup using Express and Mongoose.

## Features

- Create, Read, Update, and Delete (CRUD) API endpoints
- MongoDB Atlas integration
- Express.js server setup
- Organized project structure using MVC pattern

## Tech Stack

- Backend: Node.js, Express.js
- Database: MongoDB (hosted on Atlas)
- ODM: Mongoose

## Project Structure

APICREATION/
├── models/           # Mongoose data models
├── routes/           # API route handlers
├── controllers/      # Business logic
├── db.js             # MongoDB connection
├── server.js         # Entry point
├── package.json      # Project config & dependencies


## API Endpoints

| Method | Endpoint         | Description          |
|--------|------------------|----------------------|
| GET    | /api/items       | Get all items        |
| POST   | /api/items       | Add a new item       |
| PUT    | /api/items/:id   | Update item by ID    |
| DELETE | /api/items/:id   | Delete item by ID    |

## Sample Request (POST)

POST /api/items
Content-Type: application/json

{
  "name": "Notebook",
  "quantity": 10
}

