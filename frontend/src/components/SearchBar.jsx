import { useState } from "react";
import Spinner from "./Spinner";

export default function SearchBar({ onSearch, loading }) {
    const [query, setQuery] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        onSearch(query);
    }

    return (
        <form onSubmit={handleSubmit} className="flex gap-2">
            <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Search for books..."
                className="border p-2 flex-1 rounded bg-white text-black"
            />
            <button
                type="submit"
                disabled={loading}
                className="bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 disabled:opacity-50"
            >
                {loading ? <Spinner small /> : "Search"}
            </button>
        </form>
    );
}
