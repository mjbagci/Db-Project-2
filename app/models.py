"""
Data models for the bookstore application
"""
from datetime import datetime


class Book:
    """Book model"""
    
    def __init__(self, title, author, isbn, price=None, stock=0, description=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.stock = stock
        self.description = description
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert Book instance to dictionary"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'price': self.price,
            'stock': self.stock,
            'description': self.description,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Book instance from dictionary"""
        return cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            price=data.get('price'),
            stock=data.get('stock', 0),
            description=data.get('description')
        )

