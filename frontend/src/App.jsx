import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import BookGrid from "./components/BookGrid";
import BookModal from "./components/BookModal";
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
    try {
      const detail = await fetchBookDetail(book.id);
      setSelectedBook(detail);
    } catch (err) {
      console.error("Failed to fetch book details:", err);
      setSelectedBook({
        ...book,
        description: "Failed to load detailed description from the server."
      });
    }
  }

  return (
    <div className="min-h-screen md:h-screen md:min-h-0 bg-gray-100 flex flex-col md:overflow-hidden">
      <nav className="bg-blue-600 text-white px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4 shadow-md shrink-0">
        <h1 className="text-2xl md:text-3xl font-gocake font-bold text-white text-center md:text-left">Book Library</h1>
        <div className="w-full md:max-w-md">
          <SearchBar onSearch={handleSearch} />
        </div>
      </nav>

      <div className="flex-1 p-6 md:overflow-hidden min-h-0">
        {loading && <div className="text-center py-4 text-blue-600 font-semibold">Loading books...</div>}
        {error && <div className="text-center py-4 text-red-500 font-semibold">{error}</div>}

        <div className="grid grid-cols-12 gap-6 md:h-full">
          <aside className="col-span-12 md:col-span-3 bg-white shadow rounded p-4 font-gocake flex flex-col md:h-full md:overflow-hidden">
            <div className="flex justify-between items-center md:block md:text-center shrink-0">
              <h2 className="font-semibold text-lg md:mb-4">Categories</h2>
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className="md:hidden bg-blue-50 text-blue-600 px-3 py-1 rounded text-sm font-semibold hover:bg-blue-100 transition-colors"
              >
                {isSidebarOpen ? "Hide" : "Show"}
              </button>
            </div>
            <ul className={`${isSidebarOpen ? "block" : "hidden"} md:block space-y-2 text-gray-700 mt-4 md:mt-0 text-center max-h-64 md:max-h-none overflow-y-auto pr-1 md:flex-1`}>
              <li 
                onClick={handleClearCategory}
                className={`hover:text-blue-500 cursor-pointer py-2 md:py-0 border-b border-gray-100 md:border-b-0 last:border-b-0 ${!selectedCategory ? 'text-blue-600 font-semibold' : ''}`}
              >
                All Books (Popular)
              </li>
              {categories.map((cats) => (
                <li key={cats.slug} onClick={() => handleCategoryClick(cats.slug)}
                  className={`hover:text-blue-500 cursor-pointer py-2 md:py-0 border-b border-gray-100 md:border-b-0 last:border-b-0 ${selectedCategory === cats.slug ? 'text-blue-600 font-semibold' : ''}`}
                >
                  {cats.name}
                </li>
              ))}
            </ul>
          </aside>
          <main className="col-span-12 md:col-span-9 font-gocake md:h-full md:overflow-y-auto md:pr-2">
            {!loading && <BookGrid books={filteredBooks} onBookClick={handleBookClick} />}
          </main>
        </div>
      </div>
      <BookModal book={selectedBook} onClose={() => setSelectedBook(null)} />
    </div>
  );
}
