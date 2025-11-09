import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ChatWindow from './components/ChatWindow';
import FileUpload from './components/FileUpload';
import ProgressBar from './components/ProgressBar';
import SanctionView from './components/SanctionView';
import LandingPage from './components/LandingPage';
import { Paperclip, Send } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  isBot: boolean;
  timestamp: string;
}

interface LoanDetails {
  amount: string;
  interestRate: string;
  tenure: string;
}

type ViewState = 'landing' | 'chat' | 'sanction';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [currentStage, setCurrentStage] = useState(1);
  const [viewState, setViewState] = useState<ViewState>('landing');
  const [loanDetails, setLoanDetails] = useState<LoanDetails>({
    amount: '₹5,00,000',
    interestRate: '10.5%',
    tenure: '36 months',
  });

  useEffect(() => {
    if (viewState === 'chat') {
      const savedMessages = localStorage.getItem('capitalmitra_chat');
      if (savedMessages) {
        setMessages(JSON.parse(savedMessages));
      } else {
        addBotMessage(
          "Hello! I'm CapitalMitra, your personal loan assistant. I'll guide you through the entire loan process from inquiry to sanction. How can I help you today?"
        );
      }
    }
  }, [viewState]);

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('capitalmitra_chat', JSON.stringify(messages));
    }
  }, [messages]);

  const addBotMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      isBot: true,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const addUserMessage = (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      isBot: false,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const simulateBotResponse = async (userMessage: string) => {
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 1500));

    const lowerMessage = userMessage.toLowerCase();

    if (currentStage === 1) {
      if (lowerMessage.includes('loan') || lowerMessage.includes('need') || lowerMessage.includes('want')) {
        setCurrentStage(2);
        addBotMessage("Great! I'd be happy to help you with a personal loan. May I know the purpose of your loan?");
      } else {
        addBotMessage("I can help you with personal loans. Could you tell me more about your loan requirements?");
      }
    } else if (currentStage === 2) {
      if (lowerMessage.includes('wedding') || lowerMessage.includes('business') || lowerMessage.includes('education') || lowerMessage.includes('home')) {
        addBotMessage(`Perfect! Based on your requirements, you're pre-approved for up to ₹8,00,000 at 10.5% interest rate for up to 60 months. Would you like to proceed with this offer?`);
      } else {
        addBotMessage("Could you please specify the purpose? For example: wedding, business, education, or home renovation.");
      }
    } else if (currentStage === 2 && (lowerMessage.includes('yes') || lowerMessage.includes('proceed') || lowerMessage.includes('sure'))) {
      setCurrentStage(3);
      addBotMessage("Excellent! Now, let's verify your identity. I've sent a 6-digit OTP to your registered mobile number. Please enter it here.");
    } else if (currentStage === 3) {
      if (/^\d{6}$/.test(userMessage.trim())) {
        setCurrentStage(4);
        addBotMessage("OTP verified successfully! ✓\n\nNow I'm checking your credit score and evaluating your application. This will take just a moment...");

        setTimeout(() => {
          addBotMessage("Great news! Your credit score is 785 — that's excellent!\n\nTo complete the underwriting process, I'll need your latest salary slip. Please upload it using the attachment button below.");
          setShowFileUpload(true);
        }, 3000);
      } else {
        addBotMessage("Please enter a valid 6-digit OTP.");
      }
    } else if (currentStage === 5) {
      addBotMessage("Your loan has been approved and the sanction letter is being generated. You'll be redirected shortly...");
      setTimeout(() => {
        setViewState('sanction');
      }, 2000);
    } else {
      addBotMessage("I'm here to help. Please follow the prompts to complete your loan application.");
    }

    setIsLoading(false);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = inputValue;
    setInputValue('');
    addUserMessage(userMessage);

    await simulateBotResponse(userMessage);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);

    await new Promise((resolve) => setTimeout(resolve, 2000));

    setIsUploading(false);
    setShowFileUpload(false);
    addUserMessage(`[Uploaded: ${file.name}]`);

    setTimeout(() => {
      setCurrentStage(5);
      addBotMessage("Thank you! Your salary slip has been received and verified.\n\nAll checks complete! ✓\n\nYour loan of ₹5,00,000 at 10.5% interest for 36 months has been APPROVED! 🎉\n\nGenerating your sanction letter now...");

      setTimeout(() => {
        setViewState('sanction');
      }, 3000);
    }, 1500);
  };

  const handleStartNew = () => {
    setMessages([]);
    setCurrentStage(1);
    setViewState('landing');
    localStorage.removeItem('capitalmitra_chat');
  };

  const handleGetStarted = () => {
    setViewState('chat');
  };

  if (viewState === 'landing') {
    return <LandingPage onGetStarted={handleGetStarted} />;
  }

  if (viewState === 'sanction') {
    return (
      <SanctionView
        loanAmount={loanDetails.amount}
        interestRate={loanDetails.interestRate}
        tenure={loanDetails.tenure}
        sanctionLetterUrl="#"
        onStartNew={handleStartNew}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 flex flex-col">
      <Navbar />

      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full">
          <ChatWindow messages={messages} isLoading={isLoading} />

          <div className="border-t border-gray-800 bg-black px-4 py-4">
            <div className="flex items-center space-x-3 max-w-4xl mx-auto">
              <button
                onClick={() => setShowFileUpload(true)}
                className="p-3 text-gray-400 hover:text-orange-500 hover:bg-gray-800 rounded-lg transition-all"
                title="Upload document"
              >
                <Paperclip size={22} />
              </button>

              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 bg-gray-800 text-white px-6 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-gray-500"
              />

              <button
                onClick={handleSendMessage}
                disabled={inputValue.trim() === '' || isLoading}
                className="bg-orange-600 hover:bg-orange-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all shadow-lg hover:shadow-xl"
              >
                <Send size={22} />
              </button>
            </div>
          </div>
        </div>

        <div className="hidden lg:block w-80 border-l border-gray-800 bg-black p-6 overflow-y-auto">
          <ProgressBar currentStage={currentStage} />
        </div>
      </div>

      {showFileUpload && (
        <FileUpload
          onFileSelect={handleFileUpload}
          onClose={() => setShowFileUpload(false)}
          isUploading={isUploading}
        />
      )}
    </div>
  );
}

export default App;
