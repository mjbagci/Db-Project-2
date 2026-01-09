"""
Database connection module for MongoDB/Cosmos DB
"""
from pymongo import MongoClient
import os


def get_mongo_uri():
    """
    Get MongoDB connection URI from environment variables.
    Supports MONGO_URI (preferred) or individual components.
    """
    # Prefer MONGO_URI if available
    mongo_uri = os.getenv('MONGO_URI')
    if mongo_uri:
        return mongo_uri
    
    # Fallback to individual components
    host = os.getenv('MONGO_HOST', 'localhost')
    port = os.getenv('MONGO_PORT', '27017')
    user = os.getenv('MONGO_USER')
    password = os.getenv('MONGO_PASS')
    database = os.getenv('MONGO_DB', 'BOOKSTORE')
    
    if user and password:
        return f"mongodb://{user}:{password}@{host}:{port}/{database}?authSource=admin"
    else:
        return f"mongodb://{host}:{port}/{database}"


# Global client instance
_client = None


def get_client():
    """Get or create MongoDB client"""
    global _client
    if _client is None:
        mongo_uri = get_mongo_uri()
        # SSL settings for Azure Cosmos DB
        _client = MongoClient(
            mongo_uri,
            tlsAllowInvalidCertificates=True  # For development only
        )
    return _client


def get_db():
    """Get database instance"""
    db_name = os.getenv('MONGO_DB', 'BOOKSTORE')
    client = get_client()
    return client[db_name]


def get_collection():
    """Get books collection"""
    collection_name = os.getenv('MONGO_COLLECTION', 'books')
    db = get_db()
    return db[collection_name]

