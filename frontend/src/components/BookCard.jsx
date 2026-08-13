export default function BookCard({ book, onClick }) {
    return (
        <div onClick={onClick} className="bg-white shadow rounded hover:shadow-lg transition-shadow cursor-pointer">
            {book.coverUrl && (
                <img src={book.coverUrl} alt={book.title} className="mb-2 rounded w-full h-64 object-cover"/>
            )}
            <div className="p-4">
                <h2 className="font-semibold">{book.title}</h2>
                <p className="text-sm text-gray-600">{book.author}</p>
                <p className="mt-2">⭐ {book.rating || "No rating"}</p>
            </div>
        </div>
    );
}
