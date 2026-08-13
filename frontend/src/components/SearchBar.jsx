import { useState } from "react";
import Spinner from "./Spinner";

export default function SearchBar({ onSearch, loading }) {
    const [query, setQuery] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        onSearch(query);
    }

    return (
        <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for books..."
                className="border p-2 flex-1 rounded"
            />
            <button
                type="submit"
                disabled={loading}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-60 flex items-center gap-2"
            >
                {loading ? <Spinner small /> : "Search"}
            </button>
        </form>
    );
}
