import { useState, useEffect } from "react";
import axios from "axios";
import { BASE_URL } from "./config";
import Navbar from "./components/Navbar";
import ChatWindow from "./components/ChatWindow";
import FileUpload from "./components/FileUpload";
import ProgressBar from "./components/ProgressBar";
import SanctionView from "./components/SanctionView";
import LandingPage from "./components/LandingPage";
import { Paperclip, Send } from "lucide-react";

import { toast, Toaster } from "react-hot-toast"; // add for user notifications

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
  sanctionLetterUrl?: string;
}

type ViewState = "landing" | "chat" | "sanction";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [currentStage, setCurrentStage] = useState(1);
  const [viewState, setViewState] = useState<ViewState>("landing");
  const [loanDetails, setLoanDetails] = useState<LoanDetails>({
    amount: "",
    interestRate: "",
    tenure: "",
  });

  // --- Load previous chat ---
  useEffect(() => {
    if (viewState === "chat") {
      const saved = localStorage.getItem("capitalmitra_chat");
      if (saved) {
        setMessages(JSON.parse(saved));
      } else {
        addBotMessage(
          "👋 Hi! I’m CapitalMitra, your personal AI loan assistant. I’ll help you apply, verify, and get your loan sanctioned — step by step. How can I help you today?"
        );
      }
    }
  }, [viewState]);

  // --- Persist chat state ---
  useEffect(() => {
    if (messages.length > 0)
      localStorage.setItem("capitalmitra_chat", JSON.stringify(messages));
  }, [messages]);

  // ========================
  // 📤 MESSAGE HELPERS
  // ========================
  const addBotMessage = (text: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        text,
        isBot: true,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  const addUserMessage = (text: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        text,
        isBot: false,
        timestamp: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      },
    ]);
  };

  // ========================
  // 🤖 GET BACKEND RESPONSE
  // ========================
  const getBotResponse = async (userMessage: string) => {
    setIsLoading(true);
    try {
      const res = await axios.post(`${BASE_URL}/chat/`, { message: userMessage });
      const data = res.data;

      if (data?.message) addBotMessage(data.message);

      // ✅ Dynamic: If backend returns sanction info, go to Sanction View
      if (data?.approved || data?.sanction_letter) {
        setTimeout(() => {
          setLoanDetails({
            amount: `₹${data.approved?.approved_amount?.toLocaleString() || "—"}`,
            interestRate: `${data.approved?.rate || 0}%`,
            tenure: `${data.approved?.tenure || 0} months`,
            sanctionLetterUrl: data.sanction_letter ? `${BASE_URL}${data.sanction_letter}` : "#",
          });
          setViewState("sanction");
        }, 2000);
      }

      // Optional: handle structured AI advice
      if (data?.advisor) {
        addBotMessage(
          data.advisor.summary_lines.join("\n• ")
        );
      }
    } catch (err) {
      console.error(err);
      toast.error("⚠️ Unable to connect to CapitalMitra backend. Please retry.");
      addBotMessage("Sorry, I couldn’t reach the backend. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  // ========================
  // ✉️ SEND MESSAGE
  // ========================
  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;
    const msg = inputValue.trim();
    setInputValue("");
    addUserMessage(msg);
    await getBotResponse(msg);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ========================
  // 📎 FILE UPLOAD
  // ========================
  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    await new Promise((res) => setTimeout(res, 2000)); // simulate verification
    setIsUploading(false);
    setShowFileUpload(false);

    addUserMessage(`[Uploaded: ${file.name}]`);
    addBotMessage("📁 Your document has been received and verified successfully.");

    // Move to next logical stage
    setCurrentStage(5);
    addBotMessage("✅ All checks complete! Your loan is being finalized...");
    setTimeout(() => setViewState("sanction"), 2500);
  };

  // ========================
  // 🔄 NEW SESSION
  // ========================
  const handleStartNew = () => {
    setMessages([]);
    setLoanDetails({ amount: "", interestRate: "", tenure: "" });
    setCurrentStage(1);
    setViewState("landing");
    localStorage.removeItem("capitalmitra_chat");
  };

  // ========================
  // 🌐 VIEW SWITCHES
  // ========================
  if (viewState === "landing") {
    return (
      <>
        <LandingPage onGetStarted={() => setViewState("chat")} />
        <Toaster position="bottom-center" />
      </>
    );
  }

  if (viewState === "sanction") {
    return (
      <>
        <SanctionView
          loanAmount={loanDetails.amount}
          interestRate={loanDetails.interestRate}
          tenure={loanDetails.tenure}
          sanctionLetterUrl={loanDetails.sanctionLetterUrl}
          onStartNew={handleStartNew}
        />
        <Toaster position="bottom-center" />
      </>
    );
  }

  // ========================
  // 💬 CHAT SCREEN
  // ========================
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-white via-orange-50 to-white">
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        <div className="flex flex-col flex-1 max-w-5xl mx-auto w-full">
          {/* New Chat Button */}
          <div className="flex justify-end px-6 py-3">
            <button
              onClick={handleStartNew}
              className="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-xl shadow transition-all"
            >
              New Chat
            </button>
          </div>

          <ChatWindow messages={messages} isLoading={isLoading} />

          {/* Chat Input */}
          <div className="border-t border-gray-200 bg-white/90 backdrop-blur-md px-4 py-4 sticky bottom-0">
            <div className="flex items-center space-x-3 max-w-4xl mx-auto">
              <button
                onClick={() => setShowFileUpload(true)}
                className="p-3 text-gray-400 hover:text-orange-500 hover:bg-orange-100 rounded-lg transition-all"
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
                className="flex-1 bg-gray-100 text-gray-900 px-6 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 placeholder-gray-400"
              />

              <button
                onClick={handleSend}
                disabled={inputValue.trim() === "" || isLoading}
                className="bg-orange-600 hover:bg-orange-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white p-3 rounded-xl transition-all shadow-lg hover:shadow-xl"
              >
                <Send size={22} />
              </button>
            </div>
          </div>
        </div>

        {/* Right Progress Bar */}
        <div className="hidden lg:block w-80 border-l border-gray-200 bg-white/80 backdrop-blur-md p-6 overflow-y-auto">
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

      <Toaster position="bottom-center" />
    </div>
  );
}