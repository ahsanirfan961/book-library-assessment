import Spinner from "./Spinner";

export default function BookModal({ book, onClose, loading }) {
  if (!book) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-auto relative">
        {loading && (
          <div className="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center">
            <Spinner />
          </div>
        )}
        <button onClick={onClose} className="absolute top-3 right-3 text-gray-600 hover:text-black text-xl z-10">
          ✕
        </button>
        {book.coverUrl && (
          <img src={book.coverUrl} className="w-full h-64 object-cover"/>
        )}
        <div className="p-5">
          <h2 className="text-2xl font-bold">{book.title}</h2>
          <p className="text-gray-600 mt-1">By {book.author}</p>

          <div className="mt-3 text-sm text-gray-500 flex flex-wrap gap-3">
            <span>⭐ {book.rating}</span>
            {book.firstPublishYear && <span>{book.firstPublishYear}</span>}
            {book.editionCount > 0 && <span>{book.editionCount} editions</span>}
            {book.language && <span>{book.language.toUpperCase()}</span>}
          </div>

          {book.subjects && book.subjects.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1">
              {book.subjects.map((sub, index) => (
                <span key={index} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                  {sub.name}
                </span>
              ))}
            </div>
          )}

          <hr className="my-4"/>

          <h3 className="font-bold mb-2">Description</h3>
          <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
            {book.description}
          </p>
        </div>
      </div>
    </div>
  );
}
