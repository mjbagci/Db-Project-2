// ===== Configuration =====
// Always use Azure backend for testing
const API_BASE_URL = 'http://172.168.184.222';

// Alternative: Auto-detect (uncomment to use local backend when testing locally)
// const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
//     ? 'http://localhost:5001'
//     : 'http://172.168.184.222';

// ===== State =====
let allBooks = [];
let filteredBooks = [];
let currentFilter = 'all';
let editingBookId = null;

// ===== DOM Elements =====
const elements = {
    booksGrid: document.getElementById('booksGrid'),
    loading: document.getElementById('loading'),
    emptyState: document.getElementById('emptyState'),
    searchInput: document.getElementById('searchInput'),
    filterButtons: document.querySelectorAll('.filter-btn'),
    addBookBtn: document.getElementById('addBookBtn'),
    bookModal: document.getElementById('bookModal'),
    bookForm: document.getElementById('bookForm'),
    closeModal: document.getElementById('closeModal'),
    cancelBtn: document.getElementById('cancelBtn'),
    modalTitle: document.getElementById('modalTitle'),
    submitBtnText: document.getElementById('submitBtnText'),
    toast: document.getElementById('toast'),
    toastMessage: document.getElementById('toastMessage'),
    totalBooks: document.getElementById('totalBooks'),
    totalCategories: document.getElementById('totalCategories')
};

// ===== Utility Functions =====
function showToast(message, type = 'success') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type} show`;
    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

function showLoading() {
    elements.loading.style.display = 'block';
    elements.booksGrid.style.display = 'none';
    elements.emptyState.style.display = 'none';
}

function hideLoading() {
    elements.loading.style.display = 'none';
}

function getCategoryIcon(category) {
    const icons = {
        'IT': 'IT',
        'Science Fiction': 'SCI-FI',
        'Fantasy': 'FANTASY',
        'Mystery': 'MYSTERY',
        'Romance': 'ROMANCE',
        'Thriller': 'THRILLER',
        'Biography': 'BIO',
        'History': 'HISTORY'
    };
    return icons[category] || 'BOOK';
}

function updateStats() {
    elements.totalBooks.textContent = allBooks.length;
    const categories = new Set(allBooks.map(book => book.category));
    elements.totalCategories.textContent = categories.size;
}

// ===== API Functions =====
async function fetchBooks() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/books`);
        if (!response.ok) throw new Error('Failed to fetch books');
        allBooks = await response.json();
        filteredBooks = [...allBooks];
        updateStats();
        renderBooks();
    } catch (error) {
        console.error('Error fetching books:', error);
        showToast('Error loading books', 'error');
    } finally {
        hideLoading();
    }
}

async function createBook(bookData) {
    try {
        const response = await fetch(`${API_BASE_URL}/books`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create book');
        }
        
        const newBook = await response.json();
        allBooks.push(newBook);
        applyFilters();
        updateStats();
        showToast('Book added successfully!', 'success');
        return newBook;
    } catch (error) {
        console.error('Error creating book:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

async function updateBook(id, bookData) {
    try {
        const response = await fetch(`${API_BASE_URL}/books/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update book');
        }
        
        const updatedBook = await response.json();
        const index = allBooks.findIndex(book => book._id === id);
        if (index !== -1) {
            allBooks[index] = updatedBook;
        }
        applyFilters();
        showToast('Book updated successfully!', 'success');
        return updatedBook;
    } catch (error) {
        console.error('Error updating book:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

async function deleteBook(id) {
    if (!confirm('Are you sure you want to delete this book?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/books/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete book');
        }
        
        allBooks = allBooks.filter(book => book._id !== id);
        applyFilters();
        updateStats();
        showToast('Book deleted successfully!', 'success');
    } catch (error) {
        console.error('Error deleting book:', error);
        showToast(error.message, 'error');
    }
}

// ===== Render Functions =====
function renderBooks() {
    elements.booksGrid.innerHTML = '';
    
    if (filteredBooks.length === 0) {
        elements.booksGrid.style.display = 'none';
        elements.emptyState.style.display = 'block';
        return;
    }
    
    elements.booksGrid.style.display = 'grid';
    elements.emptyState.style.display = 'none';
    
    filteredBooks.forEach((book, index) => {
        const bookCard = createBookCard(book, index);
        elements.booksGrid.appendChild(bookCard);
    });
}

function createBookCard(book, index) {
    const card = document.createElement('div');
    card.className = 'book-card';
    card.style.animationDelay = `${index * 0.05}s`;
    
    const authorName = `${book.author.firstName} ${book.author.lastName}`;
    const categoryIcon = getCategoryIcon(book.category);
    
    // Check if valid image URL exists
    const hasImage = book.coverPhoto && 
                     book.coverPhoto !== '' && 
                     (book.coverPhoto.startsWith('http') || book.coverPhoto.startsWith('images/'));
    
    let coverHtml = '';
    if (hasImage) {
        coverHtml = `<img src="${book.coverPhoto}" alt="${book.title}" class="book-cover-image">`;
    } else {
        coverHtml = `<div class="book-cover-fallback">${categoryIcon}</div>`;
    }
    
    card.innerHTML = `
        <div class="book-cover">
            ${coverHtml}
            <div class="book-category-badge">${book.category}</div>
        </div>
        <div class="book-info">
            <h3 class="book-title">${book.title}</h3>
            <p class="book-author">Author: ${authorName}</p>
            <p class="book-publisher">Publisher: ${book.publisher.name}</p>
            
            <div class="book-meta">
                <div class="book-meta-item">
                    <span class="meta-label">Year</span>
                    <span class="meta-value">${book.year}</span>
                </div>
                <div class="book-meta-item">
                    <span class="meta-label">Pages</span>
                    <span class="meta-value">${book.page}</span>
                </div>
                <div class="book-meta-item">
                    <span class="meta-label">ISBN</span>
                    <span class="meta-value">${book.isbn.substring(0, 10)}...</span>
                </div>
            </div>
            
            <div class="book-price">$${book.price.toFixed(2)}</div>
            
            <div class="book-actions">
                <button class="btn btn-edit" onclick="editBook('${book._id}')">
                    Edit
                </button>
                <button class="btn btn-delete" onclick="deleteBookById('${book._id}')">
                    Delete
                </button>
            </div>
        </div>
    `;
    
    return card;
}

// ===== Filter & Search Functions =====
function applyFilters() {
    let books = [...allBooks];
    
    // Apply category filter
    if (currentFilter !== 'all') {
        books = books.filter(book => book.category === currentFilter);
    }
    
    // Apply search filter
    const searchTerm = elements.searchInput.value.toLowerCase().trim();
    if (searchTerm) {
        books = books.filter(book => {
            const authorName = `${book.author.firstName} ${book.author.lastName}`.toLowerCase();
            return book.title.toLowerCase().includes(searchTerm) ||
                   authorName.includes(searchTerm) ||
                   book.publisher.name.toLowerCase().includes(searchTerm) ||
                   book.isbn.toLowerCase().includes(searchTerm);
        });
    }
    
    filteredBooks = books;
    renderBooks();
}

// ===== Modal Functions =====
function openModal(mode = 'create', book = null) {
    editingBookId = null;
    elements.bookForm.reset();
    
    if (mode === 'edit' && book) {
        editingBookId = book._id;
        elements.modalTitle.textContent = 'Edit Book';
        elements.submitBtnText.textContent = 'Update';
        
        // Fill form with book data
        document.getElementById('isbn').value = book.isbn;
        document.getElementById('title').value = book.title;
        document.getElementById('year').value = book.year;
        document.getElementById('price').value = book.price;
        document.getElementById('page').value = book.page;
        document.getElementById('category').value = book.category;
        document.getElementById('coverPhoto').value = book.coverPhoto || '';
        
        document.getElementById('authorId').value = book.author.identityNo;
        document.getElementById('authorFirstName').value = book.author.firstName;
        document.getElementById('authorLastName').value = book.author.lastName;
        
        document.getElementById('publisherId').value = book.publisher.id;
        document.getElementById('publisherName').value = book.publisher.name;
    } else {
        elements.modalTitle.textContent = 'Add New Book';
        elements.submitBtnText.textContent = 'Save';
    }
    
    elements.bookModal.classList.add('active');
}

function closeModal() {
    elements.bookModal.classList.remove('active');
    editingBookId = null;
    elements.bookForm.reset();
}

// ===== Event Handlers =====
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(elements.bookForm);
    const bookData = {
        isbn: formData.get('isbn'),
        title: formData.get('title'),
        year: parseInt(formData.get('year')),
        price: parseFloat(formData.get('price')),
        page: parseInt(formData.get('page')),
        category: formData.get('category'),
        coverPhoto: formData.get('coverPhoto') || `images/${formData.get('title').toLowerCase().replace(/ /g, '-')}.jpg`,
        author: {
            identityNo: formData.get('authorId'),
            firstName: formData.get('authorFirstName'),
            lastName: formData.get('authorLastName')
        },
        publisher: {
            id: parseInt(formData.get('publisherId')),
            name: formData.get('publisherName')
        }
    };
    
    try {
        if (editingBookId) {
            await updateBook(editingBookId, bookData);
        } else {
            await createBook(bookData);
        }
        closeModal();
    } catch (error) {
        // Error already handled in API functions
    }
}

function editBook(bookId) {
    const book = allBooks.find(b => b._id === bookId);
    if (book) {
        openModal('edit', book);
    }
}

function deleteBookById(bookId) {
    deleteBook(bookId);
}

// ===== Event Listeners =====
elements.addBookBtn.addEventListener('click', () => openModal('create'));
elements.closeModal.addEventListener('click', closeModal);
elements.cancelBtn.addEventListener('click', closeModal);
elements.bookForm.addEventListener('submit', handleFormSubmit);

// Close modal when clicking outside
elements.bookModal.addEventListener('click', (e) => {
    if (e.target === elements.bookModal) {
        closeModal();
    }
});

// Search input
elements.searchInput.addEventListener('input', applyFilters);

// Filter buttons
elements.filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        elements.filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.category;
        applyFilters();
    });
});

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    fetchBooks();
});

// Make functions available globally
window.editBook = editBook;
window.deleteBookById = deleteBookById;

