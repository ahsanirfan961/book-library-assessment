import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import BookGrid from "./components/BookGrid";
import BookModal from "./components/BookModal";
import Spinner, { BookLoadSkeleton } from "./components/Spinner";
import { fetchBooks, fetchCategories, fetchBooksByCategory, fetchBookDetail } from "./api/books";

export default function App() {
  const [allBooks, setAllBooks] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedBook, setSelectedBook] = useState(null);
  const [bookLoading, setBookLoading] = useState(false);

  useEffect(() => {
    async function initApp() {
      try {
        setLoading(true);
        const booksData = await fetchBooks();
        setAllBooks(booksData);
        setFilteredBooks(booksData);

        const catsData = await fetchCategories();
        setCategories(catsData);
      } catch (err) {
        setError("Could not load library data.");
      } finally {
        setLoading(false);
      }
    }
    initApp();
  }, []);

  async function handleCategoryClick(slug) {
    try {
      setLoading(true);
      setSelectedCategory(slug);
      const categoryBooks = await fetchBooksByCategory(slug);
      setFilteredBooks(categoryBooks);
      setError("");
    } catch (err) {
      setError(`Failed to fetch books for category "${slug}".`);
    } finally {
      setLoading(false);
    }
  }

  function handleClearCategory() {
    setSelectedCategory(null);
    setFilteredBooks(allBooks);
  }

  async function handleSearch(query) {
    setSelectedCategory(null);
    if (!query.trim()) {
      setFilteredBooks(allBooks);
      return;
    }
    try {
      setLoading(true);
      const data = await fetchBooks(query);
      setFilteredBooks(data);
      setError("");
    } catch (err) {
      setError("Failed to find books matching search query.");
    } finally {
      setLoading(false);
    }
  }

  async function handleBookClick(book) {
    if (!book || !book.id) return;
    setSelectedBook(book);
    setBookLoading(true);
    try {
      const detail = await fetchBookDetail(book.id);
      setSelectedBook(detail);
    } catch (err) {
      console.error("Failed to fetch book details:", err);
      setSelectedBook({
        ...book,
        description: "Failed to load detailed description from the server."
      });
    } finally {
      setBookLoading(false);
    }
  }

  return (
    <div className="min-h-screen" style={{ background: "#fff8e7" }}>
      <nav className="bg-blue-600 text-white px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4 shadow">
        <h1 className="text-3xl font-bold">📚 Book Library</h1>
        <div className="w-full md:max-w-md">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>
      </nav>

      <div className="p-6 max-w-6xl mx-auto">
        {error && <p className="text-red-600 text-center mb-4 bg-red-50 p-2 rounded">{error}</p>}

        <div className="flex flex-col md:flex-row gap-6">
          <aside className="md:w-56 bg-white rounded p-4 shadow-md">
            <div className="flex justify-between items-center md:block md:text-center">
              <h2 className="text-lg font-bold mb-2">Categories</h2>
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="md:hidden text-sm bg-gray-100 px-2 py-1 rounded"
              >
                {isSidebarOpen ? "Hide" : "Show"}
              </button>
            </div>
            <ul className={`${isSidebarOpen ? "block" : "hidden"} md:block mt-3 text-center text-gray-700`}>
              <li 
                onClick={handleClearCategory}
                className={`py-2 cursor-pointer rounded ${!selectedCategory ? 'bg-blue-100 text-blue-700 font-bold' : 'hover:bg-gray-100'}`}
              >
                All Books (Popular)
              </li>
              {categories.map((cats) => (
                <li key={cats.slug} onClick={() => handleCategoryClick(cats.slug)}
                  className={`py-2 cursor-pointer rounded ${selectedCategory === cats.slug ? 'bg-blue-100 text-blue-700 font-bold' : 'hover:bg-gray-100'}`}
                >
                  {cats.name}
                </li>
              ))}
            </ul>
          </aside>
          <main className="flex-1">
            {loading ? (
              <div>
                <div className="text-center py-4"><Spinner /></div>
                <BookLoadSkeleton />
              </div>
            ) : (
              <BookGrid books={filteredBooks} onBookClick={handleBookClick} />
            )}
          </main>
        </div>
      </div>
      <BookModal book={selectedBook} loading={bookLoading} onClose={() => setSelectedBook(null)} />
    </div>
  );
}
