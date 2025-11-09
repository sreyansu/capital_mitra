import { HelpCircle, Mail } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-black border-b border-gray-800 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center space-x-2">
        <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-xl">CM</span>
        </div>
        <h1 className="text-white text-xl font-semibold">CapitalMitra</h1>
      </div>
      <div className="flex items-center space-x-6">
        <button className="flex items-center space-x-2 text-gray-400 hover:text-orange-500 transition-colors">
          <HelpCircle size={20} />
          <span className="hidden md:inline text-sm">Help</span>
        </button>
        <button className="flex items-center space-x-2 text-gray-400 hover:text-orange-500 transition-colors">
          <Mail size={20} />
          <span className="hidden md:inline text-sm">Contact</span>
        </button>
      </div>
    </nav>
  );
}
