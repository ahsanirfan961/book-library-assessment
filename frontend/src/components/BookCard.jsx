export default function BookCard({ book }) {
    return (
        <div className="bg-white shadow p-4 rounded hover:shadow-lg transition-shadow">
            {book.coverUrl && (
                <img
                    src={book.coverUrl}
                    alt={book.title}
                    className="mb-2 rounded"
                />
            )}
            <h2 className="font-semibold">{book.title}</h2>
            <p className="text-sm text-gray-600">{book.author}</p>
            <p className="mt-2">⭐ {book.rating || "No rating"}</p>
        </div>
    );
}
