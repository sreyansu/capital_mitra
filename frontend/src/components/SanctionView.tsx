import { Download, CheckCircle, Home } from 'lucide-react';

interface SanctionViewProps {
  loanAmount: string;
  interestRate: string;
  tenure: string;
  sanctionLetterUrl?: string;
  onStartNew: () => void;
}

export default function SanctionView({
  loanAmount,
  interestRate,
  tenure,
  sanctionLetterUrl,
  onStartNew,
}: SanctionViewProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8 animate-fadeIn">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-orange-600 rounded-full mb-6 shadow-lg">
            <CheckCircle size={48} className="text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Congratulations!
          </h1>
          <p className="text-xl text-gray-300">
            Your loan has been successfully sanctioned
          </p>
        </div>

        <div className="bg-gray-900 rounded-2xl p-8 shadow-2xl mb-6 animate-fadeIn">
          <h2 className="text-2xl font-semibold text-white mb-6 text-center">
            Loan Details
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-800">
              <span className="text-gray-400">Loan Amount</span>
              <span className="text-white text-xl font-semibold">{loanAmount}</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-gray-800">
              <span className="text-gray-400">Interest Rate</span>
              <span className="text-white text-xl font-semibold">{interestRate}</span>
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-400">Tenure</span>
              <span className="text-white text-xl font-semibold">{tenure}</span>
            </div>
          </div>
        </div>

        <div className="space-y-4 animate-fadeIn">
          <button
            onClick={() => {
              if (sanctionLetterUrl) {
                window.open(sanctionLetterUrl, '_blank');
              }
            }}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white py-4 rounded-xl font-semibold text-lg transition-all shadow-lg hover:shadow-xl flex items-center justify-center space-x-3"
          >
            <Download size={24} />
            <span>Download Sanction Letter</span>
          </button>

          <button
            onClick={onStartNew}
            className="w-full bg-gray-800 hover:bg-gray-700 text-white py-4 rounded-xl font-semibold transition-all flex items-center justify-center space-x-3"
          >
            <Home size={20} />
            <span>Start New Application</span>
          </button>
        </div>

        <p className="text-center text-gray-400 text-sm mt-8">
          Thank you for choosing CapitalMitra. Our team will contact you soon.
        </p>
      </div>
    </div>
  );
}
