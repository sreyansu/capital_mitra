import { Check } from 'lucide-react';

interface ProgressBarProps {
  currentStage: number;
}

const stages = [
  { id: 1, name: 'Inquiry', label: 'Initial Inquiry' },
  { id: 2, name: 'Sales', label: 'Loan Offer' },
  { id: 3, name: 'Verification', label: 'KYC & Verification' },
  { id: 4, name: 'Underwriting', label: 'Credit Check' },
  { id: 5, name: 'Sanction', label: 'Approved' },
];

export default function ProgressBar({ currentStage }: ProgressBarProps) {
  return (
    <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
      <h3 className="text-white font-semibold mb-6 text-center">Loan Progress</h3>
      <div className="space-y-4">
        {stages.map((stage, index) => {
          const isCompleted = currentStage > stage.id;
          const isCurrent = currentStage === stage.id;
          const isPending = currentStage < stage.id;

          return (
            <div key={stage.id} className="flex items-center space-x-4">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                  isCompleted
                    ? 'bg-orange-600'
                    : isCurrent
                    ? 'bg-orange-600 ring-4 ring-orange-600 ring-opacity-30'
                    : 'bg-gray-700'
                }`}
              >
                {isCompleted ? (
                  <Check size={20} className="text-white" />
                ) : (
                  <span className="text-white font-semibold">{stage.id}</span>
                )}
              </div>
              <div className="flex-1">
                <p
                  className={`font-medium ${
                    isCompleted || isCurrent ? 'text-white' : 'text-gray-500'
                  }`}
                >
                  {stage.label}
                </p>
                <p className="text-xs text-gray-400">{stage.name}</p>
              </div>
              {index < stages.length - 1 && (
                <div
                  className={`w-px h-8 ml-5 ${
                    isCompleted ? 'bg-orange-600' : 'bg-gray-700'
                  }`}
                ></div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
