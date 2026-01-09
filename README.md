# Bookstore API

Full-stack web application with Flask REST API backend and vanilla JavaScript frontend, connected to Azure Cosmos DB (MongoDB API).

## 🎯 Quick Start for Professor

**Important:** Due to browser security (HTTPS/HTTP mixed content), please use the local frontend to test the live backend:

```bash
# 1. Clone and start frontend (30 seconds)
git clone https://github.com/mjbagci/Db-Project-2
cd Db-Project-2/frontend
python3 -m http.server 8000

# 2. Open in browser
# http://localhost:8000
```

**Live Backend API (Already Running on AKS):**
- API Endpoint: `http://172.168.184.222`
- Health Check: `http://172.168.184.222/health`
- Books: `http://172.168.184.222/books`

The frontend automatically connects to the live Azure backend. No backend setup needed!

## Live Backend API

**The backend is live and running on Azure Kubernetes Service (AKS):**
- Endpoint: `http://172.168.184.222`
- Health: `http://172.168.184.222/health`
- Database: Azure Cosmos DB (MongoDB API)

Test the API:
```bash
# Health check
curl http://172.168.184.222/health

# Get all books
curl http://172.168.184.222/books

# Create a book
curl -X POST http://172.168.184.222/books \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-1234567890",
    "title": "Test Book",
    "year": 2026,
    "price": 29.99,
    "page": 300,
    "category": "IT",
    "coverPhoto": "images/test.jpg",
    "publisher": {"id": 99, "name": "Test Publisher"},
    "author": {"identityNo": "99", "firstName": "John", "lastName": "Doe"}
  }'
```

## Frontend Demo

**To see the full application with UI:**

```bash
# 1. Clone repository
git clone https://github.com/mjbagci/Db-Project-2
cd Db-Project-2/frontend

# 2. Start local server
python3 -m http.server 8000

# 3. Open http://localhost:8000 in your browser
```

The frontend automatically connects to the live Azure backend. Full functionality with search, filters, and CRUD operations.

## Features

- RESTful API with full CRUD operations
- Modern responsive frontend interface
- Real-time search and filtering
- Azure Cosmos DB cloud database integration
- Docker containerization support
- Kubernetes deployment ready

## Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0
- PyMongo 4.6
- Flask-CORS

**Frontend:**
- HTML5, CSS3
- Vanilla JavaScript
- Custom gradient design

**Database:**
- Azure Cosmos DB (MongoDB API)

## Quick Start

### Prerequisites

- Python 3.11+
- Azure Cosmos DB account
- Modern web browser

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Db-Project-2
```

2. Install dependencies
```bash
cd app
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your Azure Cosmos DB connection string
```

4. Seed database (optional)
```bash
cd scripts
python3 seed_bookstore.py
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd app
python3 app.py
```
Backend runs on http://localhost:5001

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 8000
```
Frontend runs on http://localhost:8000

### Testing

Run CRUD tests:
```bash
cd scripts
python3 crud_test.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/books` | Get all books |
| GET | `/books/<id>` | Get book by ID |
| POST | `/books` | Create new book |
| PUT | `/books/<id>` | Update book |
| DELETE | `/books/<id>` | Delete book |

## Project Structure

```
Db-Project-2/
├── app/                    # Backend Flask API
│   ├── app.py             # Main application
│   ├── models.py          # Data models
│   ├── db.py              # Database connection
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Docker configuration
├── frontend/              # Frontend application
│   ├── index.html         # Main HTML
│   ├── styles.css         # Styling
│   ├── app.js             # JavaScript logic
│   └── images/            # Book cover images
├── scripts/               # Utility scripts
│   ├── seed_bookstore.py  # Database seeding
│   ├── crud_test.py       # API testing
│   └── bookstore.json     # Sample data
├── k8s/                   # Kubernetes configs
│   ├── api/               # API deployment
│   ├── mongo/             # MongoDB deployment
│   └── network/           # Network policies
└── docs/                  # Documentation
    └── README.md          # Deployment guide
```

## Environment Variables

Create `.env` file in `app/` directory:

```env
MONGO_URI=your_cosmos_db_connection_string
MONGO_DB=BOOKSTORE
MONGO_COLLECTION=books
PORT=5001
```

## Docker Support

Build and run with Docker:

```bash
cd app
docker build -t bookstore-api:latest .
docker run -d -p 5001:5000 --env-file .env bookstore-api:latest
```

## Kubernetes Deployment

See [docs/README.md](docs/README.md) for complete Azure Kubernetes Service (AKS) deployment guide.

## Development

The application includes:
- Book model with nested author and publisher objects
- Real-time search across title, author, and publisher
- Category-based filtering
- Modal forms for create/edit operations
- Toast notifications for user feedback
- Responsive design for all screen sizes


## Author

mjb - 2026

