export async function fetchBooks(query) {
    const url = query ? `/api/v1/books/search?q=${encodeURIComponent(query)}` : `/api/v1/books/popular?limit=24`;
    const res = await fetch(url);
    if (!res.ok) {
        throw new Error("Failed to fetch books");
    }
    const data = await res.json();
    const items = data.items || [];
    return items.map(book => ({
        id: book.id,
        title: book.title,
        author: book.authors && book.authors.length > 0 ? book.authors.map(a => a.name).join(', ') : 'Unknown Author',
        coverUrl: book.coverUrl,
        rating: book.rating && typeof book.rating === 'object' ? book.rating.average : (book.rating || "No rating"),
        description: book.description || "" 
    }));
}

export async function fetchCategories() {
    const res = await fetch('/api/v1/subjects/');
    if (!res.ok) {
        throw new Error("Failed to fetch categories");
    }
    const data = await res.json();
    return data.items || [];
}

export async function fetchBooksByCategory(slug) {
    const res = await fetch(`/api/v1/subjects/${slug}/books?limit=24`);
    if (!res.ok) {
        throw new Error("Failed to fetch books for category");
    }
    const data = await res.json();
    const items = data.items || [];
    return items.map(book => ({
        id: book.id,
        title: book.title,
        author: book.authors && book.authors.length > 0 ? book.authors.map(a => a.name).join(', ') : 'Unknown Author',
        coverUrl: book.coverUrl,
        rating: book.rating && typeof book.rating === 'object' ? book.rating.average : (book.rating || "No rating"),
        description: book.description || ""
    }));
}

export async function fetchBookDetail(bookId) {
    const res = await fetch(`/api/v1/books/${bookId}`);
    if (!res.ok) {
        throw new Error("Failed to fetch book details");
    }
    const book = await res.json();
    return {
        id: book.id,
        title: book.title,
        author: book.authors && book.authors.length > 0 ? book.authors.map(a => a.name).join(', ') : 'Unknown Author', 
        coverUrl: book.coverUrlLarge || book.coverUrl,
        rating: book.rating && typeof book.rating === 'object' ? book.rating.average : (book.rating || "No rating"),
        description: book.description || "No description available.",
        firstPublishYear: book.firstPublishYear,
        editionCount: book.editionCount, 
        subjects: book.subjects || [],
        language: book.language
    };
}
