const API_KEY = import.meta.env.VITE_APP_KEY;

async function apiFetch(url) {
    const res = await fetch(url, {
        headers: { "X-App-Key": API_KEY },
    });
    if (!res.ok) {
        throw new Error("Failed to fetch");
    }
    return res.json();
}

export async function fetchBooks(query) {
    const url = query ? `/api/v1/books/search?q=${encodeURIComponent(query)}` : `/api/v1/books/popular?limit=24`;
    const data = await apiFetch(url);
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
    const data = await apiFetch('/api/v1/subjects/');
    return data.items || [];
}

export async function fetchBooksByCategory(slug) {
    const data = await apiFetch(`/api/v1/subjects/${slug}/books?limit=24`);
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
    const book = await apiFetch(`/api/v1/books/${bookId}`);
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
