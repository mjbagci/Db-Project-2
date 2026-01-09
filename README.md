# Bookstore API

Full-stack web application with Flask REST API backend and vanilla JavaScript frontend, connected to Azure Cosmos DB (MongoDB API).

## Live Demo

**Application is currently deployed and accessible at:** `http://172.168.184.222`

Available for testing for a limited time. Includes:
- Complete CRUD operations
- Azure Kubernetes Service deployment
- RESTful API endpoints
- Modern frontend interface

**Note:** For security reasons, the cluster will be decommissioned after the evaluation period.

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

## License

This project was created for educational purposes.

## Author

mjb - 2026

