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
    <div className="min-h-screen bg-gradient-to-br from-white via-orange-50 to-white flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8 animate-fadeIn">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-orange-500 rounded-full mb-6 shadow-lg">
            <CheckCircle size={48} className="text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Congratulations!
          </h1>
          <p className="text-xl text-gray-600">
            Your loan has been successfully sanctioned
          </p>
        </div>

        <div className="bg-white rounded-2xl p-8 shadow-2xl mb-6 animate-fadeIn">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">
            Loan Details
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-500">Loan Amount</span>
              <span className="text-gray-900 text-xl font-semibold">{loanAmount}</span>
            </div>
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-500">Interest Rate</span>
              <span className="text-gray-900 text-xl font-semibold">{interestRate}</span>
            </div>
            <div className="flex justify-between items-center py-3">
              <span className="text-gray-500">Tenure</span>
              <span className="text-gray-900 text-xl font-semibold">{tenure}</span>
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
            className="w-full bg-orange-500 hover:bg-orange-600 text-white py-4 rounded-xl font-semibold text-lg transition-all shadow-lg hover:shadow-xl flex items-center justify-center space-x-3"
          >
            <Download size={24} />
            <span>Download Sanction Letter</span>
          </button>

          <button
            onClick={onStartNew}
            className="w-full bg-gray-100 hover:bg-gray-200 text-gray-900 py-4 rounded-xl font-semibold transition-all flex items-center justify-center space-x-3 border border-gray-300"
          >
            <Home size={20} />
            <span>Start New Application</span>
          </button>
        </div>

        <p className="text-center text-gray-500 text-sm mt-8">
          Thank you for choosing CapitalMitra. Our team will contact you soon.
        </p>
      </div>
    </div>
  );
}
