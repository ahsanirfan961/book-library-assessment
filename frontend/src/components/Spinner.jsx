export default function Spinner({ small }) {
  if (small) {
    return <div className="h-4 w-4 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin inline-block" />
  }
  return <div className="h-8 w-8 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin mx-auto" />
}

export function BookLoadSkeleton() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {[1,2,3,4,5,6].map(n => (
        <div key={n} className="bg-white rounded-lg shadow animate-pulse">
          <div className="h-56 bg-gray-300 rounded-t-lg" />
          <div className="p-3">
            <div className="h-4 bg-gray-300 rounded mb-2 w-3/4" />
            <div className="h-3 bg-gray-300 rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  )
}
