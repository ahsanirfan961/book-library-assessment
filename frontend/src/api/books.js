export async function fetchBooks(query) {
    const res = await fetch(`/api/books?q=${encodeURIComponent(query)}`);
    if (!res.ok) {
        throw new Error("Failed to fetch books");
    }
    return res.json();
}
