export default function BookCard({ book, onClick }) {
    return (
        <div onClick={onClick} className="bg-white rounded-lg shadow cursor-pointer hover:shadow-md">
            {book.coverUrl ? (
                <img src={book.coverUrl} className="w-full h-56 object-cover rounded-t-lg"/>
            ) : (
                <div className="w-full h-56 bg-blue-400 rounded-t-lg" />
            )}
            <div className="p-3">
                <h2 className="font-semibold text-gray-800">{book.title}</h2>
                <p className="text-sm text-gray-500 mt-1">{book.author}</p>
                <p className="mt-2 text-sm text-yellow-700 bg-yellow-50 inline-block px-2 py-0.5 rounded">
                    ⭐ {book.rating || "no rating yet"}
                </p>
            </div>
        </div>
    );
}
