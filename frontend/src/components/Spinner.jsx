export default function Spinner({ small }) {
  const cls = small ? "h-5 w-5" : "h-10 w-10"
  return <div className={`${cls} border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin`} />
}

export function BookLoadSkeleton() {
  return (
    <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-4">
      {[1,2,3,4,5,6].map(n => (
        <div key={n} className="w-full bg-white shadow rounded animate-pulse overflow-hidden">
          <div className="h-64 w-full bg-gray-200" />
          <div className="p-4 space-y-3">
            <div className="h-4 bg-gray-200 rounded w-3/4" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
            <div className="h-3 bg-gray-200 rounded w-1/4" />
          </div>
        </div>
      ))}
    </div>
  )
}
