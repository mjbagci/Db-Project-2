"""
Flask REST API for BOOKSTORE database on Azure Cosmos DB (MongoDB API)
"""
from flask import Flask, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest
import os
from db import get_db, get_collection
from models import Book

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Bookstore API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'list_books': 'GET /books',
            'create_book': 'POST /books',
            'get_book': 'GET /books/<id>',
            'update_book': 'PUT /books/<id>',
            'delete_book': 'DELETE /books/<id>'
        }
    }), 200


def serialize_book(book):
    """Convert MongoDB document to JSON-serializable dict"""
    if book is None:
        return None
    book_dict = dict(book)
    book_dict['_id'] = str(book_dict['_id'])
    return book_dict


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        db = get_db()
        # Test connection
        db.command('ping')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.route('/books', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'author', 'isbn']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            price=data.get('price'),
            stock=data.get('stock', 0),
            description=data.get('description')
        )
        
        collection = get_collection()
        result = collection.insert_one(book.to_dict())
        
        # Fetch the created book
        created_book = collection.find_one({'_id': result.inserted_id})
        return jsonify(serialize_book(created_book)), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/books', methods=['GET'])
def list_books():
    """List all books"""
    try:
        collection = get_collection()
        books = list(collection.find())
        return jsonify([serialize_book(book) for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    """Get a book by ID"""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid book ID format'}), 400
    
    try:
        collection = get_collection()
        book = collection.find_one({'_id': object_id})
        
        if book is None:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify(serialize_book(book)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    """Update a book by ID"""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid book ID format'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        collection = get_collection()
        
        # Check if book exists
        existing = collection.find_one({'_id': object_id})
        if existing is None:
            return jsonify({'error': 'Book not found'}), 404
        
        # Prepare update document (exclude _id)
        update_data = {k: v for k, v in data.items() if k != '_id'}
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        
        result = collection.update_one(
            {'_id': object_id},
            {'$set': update_data}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'No changes made'}), 400
        
        # Fetch updated book
        updated_book = collection.find_one({'_id': object_id})
        return jsonify(serialize_book(updated_book)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    """Delete a book by ID"""
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid book ID format'}), 400
    
    try:
        collection = get_collection()
        result = collection.delete_one({'_id': object_id})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # For development only
    port = int(os.getenv('PORT', 5001))  # Default to 5001 to avoid AirPlay conflict
    app.run(host='0.0.0.0', port=port, debug=True)
else:
    # Production mode with gunicorn
    pass

