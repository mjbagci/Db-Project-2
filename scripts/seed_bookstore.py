"""
Seed script to populate BOOKSTORE.books collection with bookstore.json data
"""
import os
import sys
import json
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from dotenv import load_dotenv
from db import get_collection

# Load environment variables
load_dotenv(Path(__file__).parent.parent / 'app' / '.env')


def seed_bookstore():
    """Seed the books collection with bookstore.json data"""
    collection = get_collection()
    
    # Load books from JSON file
    json_file = Path(__file__).parent / 'bookstore.json'
    
    if not json_file.exists():
        print(f"❌ Error: {json_file} not found!")
        sys.exit(1)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        books = json.load(f)
    
    print(f"📚 Seeding {len(books)} books into {collection.full_name}...")
    
    # Clear existing books
    deleted_count = collection.delete_many({}).deleted_count
    print(f"🗑️  Deleted {deleted_count} existing books")
    
    # Insert books
    result = collection.insert_many(books)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} books")
    
    # Display inserted books
    print("\n📖 Inserted books:")
    for book in collection.find():
        author_name = f"{book['author']['firstName']} {book['author']['lastName']}"
        print(f"  • {book['title']}")
        print(f"    Author: {author_name}")
        print(f"    Publisher: {book['publisher']['name']}")
        print(f"    Category: {book['category']}")
        print(f"    Price: ${book['price']}")
        print()
    
    # Statistics
    print("\n📊 Statistics:")
    print(f"  Total books: {collection.count_documents({})}")
    
    # Count by category
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = list(collection.aggregate(pipeline))
    print("\n  Books by category:")
    for cat in categories:
        print(f"    {cat['_id']}: {cat['count']}")
    
    # Count by publisher
    pipeline = [
        {"$group": {"_id": "$publisher.name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    publishers = list(collection.aggregate(pipeline))
    print("\n  Books by publisher:")
    for pub in publishers:
        print(f"    {pub['_id']}: {pub['count']}")


if __name__ == '__main__':
    try:
        seed_bookstore()
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

