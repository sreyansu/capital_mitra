interface MessageBubbleProps {
  message: string;
  isBot: boolean;
  timestamp?: string;
}

export default function MessageBubble({ message, isBot, timestamp }: MessageBubbleProps) {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4 animate-fadeIn items-end`}>
      {isBot && (
        <div className="mr-2 flex-shrink-0 w-12 h-12 rounded-full bg-[#F9FAFB] flex items-center justify-center border border-[#0073E6]">
          <img src="/logo.png" alt="Bot" className="w-10 h-10" />
        </div>
      )}
      <div
        className={`max-w-[80%] md:max-w-[70%] px-5 py-4 rounded-3xl ${
          isBot
            ? 'bg-white text-[#1A1A1A] border border-[#0073E6] rounded-tl-none'
            : 'button-gradient text-white rounded-tr-none'
        } shadow transition-all hover:shadow-lg`}
      >
        <p className="text-base leading-relaxed whitespace-pre-wrap">{message}</p>
        {timestamp && (
          <span className="text-xs opacity-50 mt-2 block">{timestamp}</span>
        )}
      </div>
      {!isBot && (
        <div className="ml-2 flex-shrink-0 w-9 h-9 rounded-full bg-[#0073E6] flex items-center justify-center text-white font-bold text-lg">
          U
        </div>
      )}
    </div>
  );
}
