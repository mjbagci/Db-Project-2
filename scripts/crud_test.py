"""
CRUD test script to verify all operations work correctly
"""
import os
import sys
import requests
import json
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from dotenv import load_dotenv
from db import get_collection

# Load environment variables
load_dotenv(Path(__file__).parent.parent / 'app' / '.env')

# API base URL (default to localhost:5001, can be overridden)
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5001')


def test_health():
    """Test health endpoint"""
    print("1. Testing GET /health...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_create():
    """Test book creation"""
    print("\n2. Testing POST /books...")
    new_book = {
        'title': 'Test Book',
        'author': 'Test Author',
        'isbn': '978-0-123456-78-9',
        'price': 19.99,
        'stock': 10,
        'description': 'This is a test book for CRUD operations'
    }
    response = requests.post(f"{API_BASE_URL}/books", json=new_book)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        book_id = response.json()['_id']
        print(f"   ✓ Created book with ID: {book_id}")
        return book_id
    return None


def test_list():
    """Test listing all books"""
    print("\n3. Testing GET /books...")
    response = requests.get(f"{API_BASE_URL}/books")
    print(f"   Status: {response.status_code}")
    books = response.json()
    print(f"   Found {len(books)} books")
    if books:
        print(f"   First book: {books[0]['title']} by {books[0]['author']}")
    return books


def test_get(book_id):
    """Test getting a specific book"""
    print(f"\n4. Testing GET /books/{book_id}...")
    response = requests.get(f"{API_BASE_URL}/books/{book_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_update(book_id):
    """Test updating a book"""
    print(f"\n5. Testing PUT /books/{book_id}...")
    update_data = {
        'price': 24.99,
        'stock': 15,
        'description': 'Updated description for test book'
    }
    response = requests.put(f"{API_BASE_URL}/books/{book_id}", json=update_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_delete(book_id):
    """Test deleting a book"""
    print(f"\n6. Testing DELETE /books/{book_id}...")
    response = requests.delete(f"{API_BASE_URL}/books/{book_id}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def run_crud_test():
    """Run full CRUD test cycle"""
    print("=" * 60)
    print("CRUD Test Suite")
    print("=" * 60)
    
    try:
        # Test health
        if not test_health():
            print("\n❌ Health check failed!")
            return False
        
        # Test CREATE
        book_id = test_create()
        if not book_id:
            print("\n❌ Create operation failed!")
            return False
        
        # Test LIST
        test_list()
        
        # Test GET
        if not test_get(book_id):
            print("\n❌ Get operation failed!")
            return False
        
        # Test UPDATE
        if not test_update(book_id):
            print("\n❌ Update operation failed!")
            return False
        
        # Test DELETE
        if not test_delete(book_id):
            print("\n❌ Delete operation failed!")
            return False
        
        print("\n" + "=" * 60)
        print("✓ All CRUD operations completed successfully!")
        print("=" * 60)
        return True
    
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to API at {API_BASE_URL}")
        print("   Make sure the Flask app is running!")
        return False
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False


if __name__ == '__main__':
    success = run_crud_test()
    sys.exit(0 if success else 1)

