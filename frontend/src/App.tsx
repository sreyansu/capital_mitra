import { useState, useEffect } from 'react';
import axios from 'axios';
import { BASE_URL } from './config';
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

  const getBotResponseFromBackend = async (userMessage: string) => {
    setIsLoading(true);
    try {
      const res = await axios.post(`${BASE_URL}/chat/`, { message: userMessage });
      if (res.data && res.data.message) {
        addBotMessage(res.data.message);
      } else {
        addBotMessage("Sorry, I couldn't understand your request.");
      }
    } catch (error) {
      addBotMessage("Error connecting to backend. Please try again later.");
    }
    setIsLoading(false);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    const userMessage = inputValue;
    setInputValue('');
    addUserMessage(userMessage);

    await getBotResponseFromBackend(userMessage);
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

          <div className="flex justify-end items-center mb-4">
            <button
              onClick={handleStartNew}
              className="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-xl shadow transition-all"
              title="Start a new chat"
            >
              New Chat
            </button>
          </div>
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
