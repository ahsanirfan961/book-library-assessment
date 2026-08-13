export default function BookModal({ book, onClose }) {
  if (!book) return null;

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50 backdrop-blur-sm">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden relative">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 bg-white/80 hover:bg-gray-100 text-gray-800 rounded-full p-2 shadow z-10 transition-colors cursor-pointer"
          aria-label="Close modal"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div className="flex-1 overflow-y-auto">
          {book.coverUrl && (
            <img src={book.coverUrl} alt={book.title} className="w-full h-80 object-cover"/>
          )}
          
          <div className="p-6 space-y-4 font-gocake">
            <div>
              <h2 className="text-2xl md:text-3xl font-bold text-gray-900 leading-tight">{book.title}</h2>
              <p className="text-lg text-gray-600 mt-1">By {book.author}</p>
            </div>

            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
              <span className="text-yellow-600 font-semibold flex items-center gap-1">
                ⭐ {book.rating}
              </span>
              {book.firstPublishYear && (
                <span>• First Published: {book.firstPublishYear}</span>
              )}
              {book.editionCount > 0 && (
                <span>• Editions: {book.editionCount}</span>
              )}
              {book.language && (
                <span>• Language: {book.language.toUpperCase()}</span>
              )}
            </div>

            {book.subjects && book.subjects.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {book.subjects.map((sub, index) => (
                  <span 
                    key={index}
                    className="bg-blue-50 text-blue-600 text-xs px-2.5 py-1 rounded-full font-medium"
                  >
                    {sub.name}
                  </span>
                ))}
              </div>
            )}


            <hr className="border-gray-200" />

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-700 leading-relaxed whitespace-pre-line text-sm md:text-base">
                {book.description}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
