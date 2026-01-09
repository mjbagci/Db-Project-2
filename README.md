# Bookstore API - Cloud-Native Full-Stack Application

Full-stack web application with Flask REST API backend and vanilla JavaScript frontend, connected to Azure Cosmos DB (MongoDB API) and deployed on Azure Kubernetes Service (AKS).

## 🎯 Quick Start for Professor

The application is **fully deployed and running on Azure**. Follow these simple steps to test it:

### Step 1: Start Frontend (30 seconds)
```bash
git clone https://github.com/mjbagci/Db-Project-2
cd Db-Project-2/frontend
python3 -m http.server 8000
```

### Step 2: Open Browser
Open `http://localhost:8000` in your browser.

### What You'll See
- ✅ **9 books** with real cover images
- ✅ **Search, filter, CRUD operations** all functional
- ✅ **Modern responsive UI** with real-time updates
- ✅ **Live Azure backend** (already running on AKS)

### Architecture
```
Frontend (localhost:8000) → Backend API (AKS) → Azure Cosmos DB
                             ↓
                    http://172.168.184.222
```

**Note:** The frontend must run locally due to browser security (HTTPS/HTTP mixed content restrictions). The backend is live on Azure and requires no setup.

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

## Project Features

### Backend (Flask REST API)
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ RESTful API design with proper HTTP methods
- ✅ Nested object support (Author, Publisher)
- ✅ Health check endpoint
- ✅ CORS enabled for cross-origin requests
- ✅ Production-ready with Gunicorn

### Frontend (Modern Web UI)
- ✅ Responsive single-page application
- ✅ Real-time search across title, author, publisher
- ✅ Category filtering (All, IT, Science Fiction)
- ✅ Book cover images with Open Library integration
- ✅ Modal-based forms for add/edit operations
- ✅ Toast notifications for user feedback

### Cloud Infrastructure
- ✅ **Azure Cosmos DB** (MongoDB API) for database
- ✅ **Azure Kubernetes Service (AKS)** for container orchestration
- ✅ **Azure Container Registry (ACR)** for Docker images
- ✅ StatefulSet for MongoDB persistence
- ✅ Network policies for security
- ✅ ConfigMaps and Secrets for configuration

## Tech Stack

**Backend:**
- Python 3.11
- Flask 3.0 (Web framework)
- PyMongo 4.6 (MongoDB driver)
- Flask-CORS 4.0 (Cross-origin support)
- Gunicorn 21.2 (Production server)

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Custom responsive design with gradients
- Fetch API for async operations
- No frameworks - vanilla JavaScript

**Database:**
- Azure Cosmos DB (MongoDB API)
- 9 books with complete metadata

**Cloud & DevOps:**
- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Docker containerization
- Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Network policies for security

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

## Deployment Status

🟢 **LIVE AND READY FOR EVALUATION**

| Component | Status | Details |
|-----------|--------|---------|
| Backend API | ✅ Running | Azure Kubernetes Service (AKS) |
| Database | ✅ Connected | Azure Cosmos DB - 9 books loaded |
| Frontend | ✅ Ready | Clone and run locally (30 seconds) |
| CORS | ✅ Enabled | Cross-origin requests working |
| Images | ✅ Loaded | Real book covers from Open Library |

**Test URL:** Clone repo → `cd frontend && python3 -m http.server 8000` → Open `http://localhost:8000`

## Author

mjb - 2026

