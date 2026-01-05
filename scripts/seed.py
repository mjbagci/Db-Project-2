"""
Seed script to populate BOOKSTORE.books collection with sample data
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from dotenv import load_dotenv
from db import get_collection

# Load environment variables
load_dotenv(Path(__file__).parent.parent / 'app' / '.env')


def seed_books():
    """Seed the books collection with sample data"""
    collection = get_collection()
    
    sample_books = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '978-0-7432-7356-5',
            'price': 12.99,
            'stock': 50,
            'description': 'A classic American novel set in the Jazz Age.'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '978-0-06-112008-4',
            'price': 11.99,
            'stock': 35,
            'description': 'A gripping tale of racial injustice and childhood innocence.'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '978-0-452-28423-4',
            'price': 13.99,
            'stock': 40,
            'description': 'A dystopian social science fiction novel.'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '978-0-14-143951-8',
            'price': 10.99,
            'stock': 30,
            'description': 'A romantic novel of manners written in 1813.'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '978-0-316-76948-0',
            'price': 12.49,
            'stock': 25,
            'description': 'A controversial novel about teenage rebellion and alienation.'
        }
    ]
    
    print(f"Seeding {len(sample_books)} books into {collection.full_name}...")
    
    # Clear existing books (optional - comment out if you want to keep existing)
    # collection.delete_many({})
    
    # Insert books
    result = collection.insert_many(sample_books)
    print(f"✓ Successfully inserted {len(result.inserted_ids)} books")
    
    # Display inserted books
    print("\nInserted books:")
    for book in collection.find():
        print(f"  - {book['title']} by {book['author']} (ISBN: {book['isbn']})")


if __name__ == '__main__':
    try:
        seed_books()
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)

