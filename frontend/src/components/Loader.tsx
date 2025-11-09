export default function Loader() {
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-gray-800 px-6 py-4 rounded-2xl rounded-tl-none shadow-lg">
        <div className="flex space-x-2">
          <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  );
}
