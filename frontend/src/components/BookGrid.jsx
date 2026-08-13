import BookCard from "./BookCard";

export default function BookGrid({ books, onBookClick }) {
    if (!books.length) {
        return <p className="text-gray-600">No books found.</p>;
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {books.map(book => (
                <BookCard key={book.id} book={book} onClick={() => onBookClick(book)} />
            ))}
        </div>
    );
}
