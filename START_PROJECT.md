# 🚀 Bookstore Project - Complete Startup Guide

## Prerequisites
- Python 3.11+
- MongoDB connection (Azure Cosmos DB)
- Modern web browser

---

## 📋 Step-by-Step Startup Instructions

### 1️⃣ **Backend API (Flask) Startup**

```bash
# Navigate to project root
cd "/Users/muhammetisabagci/Desktop/DB Project 2/Db-Project-2"

# Start Flask API
cd app
python3 app.py
```

**Expected Output:**
```
WARNING: This is a development server.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://YOUR_LOCAL_IP:5001
```

✅ **Backend is ready on:** `http://localhost:5001`

---

### 2️⃣ **Frontend Startup**

Open a **NEW TERMINAL** and run:

```bash
# Navigate to frontend folder
cd "/Users/muhammetisabagci/Desktop/DB Project 2/Db-Project-2/frontend"

# Start HTTP server
python3 -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

✅ **Frontend is ready on:** `http://localhost:8000`

---

### 3️⃣ **Open Application in Browser**

```bash
# Automatically open in browser
open http://localhost:8000
```

OR manually navigate to: **http://localhost:8000**

---

## 🧪 Testing & Demonstration

### **A) Visual Test (Frontend)**

1. ✅ Homepage loads with gradient background
2. ✅ Header shows "Bookstore by mjb" with statistics
3. ✅ 9 books displayed with real cover images
4. ✅ Search functionality works
5. ✅ Category filters work (All, IT, Sci-Fi)
6. ✅ Book cards show:
   - Cover image
   - Title, Author, Publisher
   - Year, Pages, ISBN
   - Price
   - Edit & Delete buttons

### **B) CRUD Operations Test**

#### **Create a New Book:**
1. Click "**+ Add New Book**" button
2. Fill in the form:
   - ISBN: `978-1234567890`
   - Title: `Test Book`
   - Year: `2026`
   - Price: `29.99`
   - Pages: `300`
   - Category: `IT`
   - Author: ID `10`, First Name `John`, Last Name `Doe`
   - Publisher: ID `6`, Name `Test Publisher`
3. Click "**Save**"
4. ✅ Success toast appears
5. ✅ New book appears in the list

#### **Edit a Book:**
1. Click "**Edit**" button on any book
2. Change the price (e.g., `19.99`)
3. Click "**Update**"
4. ✅ Success toast appears
5. ✅ Price is updated

#### **Delete a Book:**
1. Click "**Delete**" button on the test book
2. Confirm deletion
3. ✅ Success toast appears
4. ✅ Book is removed from list

#### **Search Test:**
1. Type "JavaScript" in search box
2. ✅ Only JavaScript books are shown
3. Clear search
4. ✅ All books return

#### **Filter Test:**
1. Click "**IT**" filter
2. ✅ Only IT books shown (7 books)
3. Click "**Sci-Fi**" filter
4. ✅ Only Sci-Fi books shown (2 books)
5. Click "**All**"
6. ✅ All books shown (9 books)

### **C) API Endpoints Test (Terminal)**

```bash
# Health Check
curl http://localhost:5001/health

# Get all books
curl http://localhost:5001/books

# Get specific book (replace with actual ID)
curl http://localhost:5001/books/<BOOK_ID>

# Create new book
curl -X POST http://localhost:5001/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-9876543210",
    "title": "API Test Book",
    "year": 2026,
    "price": 24.99,
    "page": 250,
    "category": "IT",
    "coverPhoto": "images/test.jpg",
    "publisher": {"id": 7, "name": "Test Publisher"},
    "author": {"identityNo": "11", "firstName": "Jane", "lastName": "Smith"}
  }'

# Update book
curl -X PUT http://localhost:5001/books/<BOOK_ID> \
  -H "Content-Type: application/json" \
  -d '{"price": 19.99}'

# Delete book
curl -X DELETE http://localhost:5001/books/<BOOK_ID>
```

---

## 🎯 Key Features to Demonstrate

### **Backend (Flask API)**
✅ RESTful API with full CRUD operations
✅ MongoDB/Azure Cosmos DB integration
✅ CORS enabled for frontend communication
✅ Proper error handling
✅ JSON responses
✅ Health check endpoint

### **Frontend (HTML/CSS/JavaScript)**
✅ Modern, responsive design
✅ Gradient color scheme
✅ Real-time search and filtering
✅ Modal forms for add/edit
✅ Toast notifications
✅ Live statistics
✅ Book cover images
✅ Smooth animations

### **Database (Azure Cosmos DB)**
✅ MongoDB API
✅ Cloud-hosted
✅ Persistent data storage
✅ Complex document structure (nested objects)

---

## 📊 Project Statistics

- **Total Books:** 9
- **Categories:** IT (7), Science Fiction (2)
- **Publishers:** O'Reilly (5), Packt (1), Ace (1), Manning (1), Del Rey (1)

---

## 🛑 Shutdown Instructions

```bash
# Stop Backend
pkill -f "python3 app.py"

# Stop Frontend
pkill -f "python3 -m http.server"
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Port 8000)            │
│   HTML + CSS + Vanilla JavaScript      │
│         http://localhost:8000           │
└──────────────┬──────────────────────────┘
               │
               │ HTTP/REST API
               │ (with CORS)
               ▼
┌─────────────────────────────────────────┐
│         Backend (Port 5001)             │
│      Flask REST API + CORS              │
│         http://localhost:5001           │
└──────────────┬──────────────────────────┘
               │
               │ PyMongo Driver
               │
               ▼
┌─────────────────────────────────────────┐
│      Azure Cosmos DB (MongoDB API)      │
│         Database: BOOKSTORE             │
│         Collection: books               │
└─────────────────────────────────────────┘
```

---

## ✨ Technologies Used

- **Backend:** Python 3.11, Flask, PyMongo, Flask-CORS
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** Azure Cosmos DB (MongoDB API)
- **Styling:** Custom CSS with gradients and animations
- **Fonts:** Google Fonts (Inter, Playfair Display)

---

## 📝 Notes

- Backend runs on port 5001 (to avoid macOS AirPlay conflict)
- Frontend runs on port 8000
- Database connection uses SSL with certificate validation disabled for development
- All book covers are stored locally in `frontend/images/`
- Project includes CRUD test suite in `scripts/crud_test.py`

---

**Project by: mjb**
**Date: January 2026**

