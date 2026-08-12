import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import BookGrid from "./components/BookGrid";
import { fetchBooks } from "./api/books";

export default function App() {
  const [allBooks, setAllBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadBooks() {
      try {
        const data = await fetchBooks();
        setAllBooks(data);
        setFilteredBooks(data);
      } catch (err) {
        setError("Could not load books.");
      } finally {
        setLoading(false);
      }
    }
    loadBooks();
  }, []);

  function handleSearch(query) {
    if (!query.trim()) {
      setFilteredBooks(allBooks);
    } else {
      const lower = query.toLowerCase();
      setFilteredBooks(
        allBooks.filter(
          b =>
            b.title.toLowerCase().includes(lower) ||
            b.author.toLowerCase().includes(lower)
        )
      );
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-6">Book Library</h1>
      <div className="bg-red-500 text-white p-4">Tailwind works!</div>
      <SearchBar onSearch={handleSearch} />
      {loading && <p className="text-blue-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <BookGrid books={filteredBooks} />
    </div>
  );
}
