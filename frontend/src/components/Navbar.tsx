import { HelpCircle, Mail } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-[#0A1A2F] border-b border-[#0073E6] px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-sm">
      <div className="flex items-center space-x-3">
        <img src="/logo.png" alt="Capital Mitra Logo" className="w-10 h-10 rounded-lg bg-white p-1" />
        <h1 className="text-white text-xl font-semibold tracking-wide">CapitalMitra</h1>
      </div>
      <div className="flex items-center space-x-6">
        <button className="flex items-center space-x-2 text-[#0073E6] hover:text-[#0060C7] transition-colors">
          <HelpCircle size={20} />
          <span className="hidden md:inline text-sm">Help</span>
        </button>
        <button className="flex items-center space-x-2 text-[#0073E6] hover:text-[#0060C7] transition-colors">
          <Mail size={20} />
          <span className="hidden md:inline text-sm">Contact</span>
        </button>
      </div>
    </nav>
  );
}
