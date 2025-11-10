import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import Loader from './Loader';

interface Message {
  id: string;
  text: string;
  isBot: boolean;
  timestamp: string;
}

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-8 space-y-2 bg-white scrollbar-thin scrollbar-thumb-orange-300 scrollbar-track-gray-100 rounded-xl">
      {messages.length === 0 && (
        <div className="flex items-center justify-center h-full">
          <div className="text-center text-gray-400">
            <p className="text-lg font-medium">Welcome to CapitalMitra</p>
            <p className="text-sm mt-2">Your AI-powered personal loan assistant</p>
          </div>
        </div>
      )}
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message.text}
          isBot={message.isBot}
          timestamp={message.timestamp}
        />
      ))}
      {isLoading && <Loader />}
      <div ref={chatEndRef} />
    </div>
  );
}
