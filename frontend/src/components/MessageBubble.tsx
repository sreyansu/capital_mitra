interface MessageBubbleProps {
  message: string;
  isBot: boolean;
  timestamp?: string;
}

export default function MessageBubble({ message, isBot, timestamp }: MessageBubbleProps) {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4 animate-fadeIn`}>
      <div
        className={`max-w-[80%] md:max-w-[70%] px-6 py-4 rounded-2xl ${
          isBot
            ? 'bg-gray-800 text-white rounded-tl-none'
            : 'bg-orange-600 text-white rounded-tr-none'
        } shadow-lg transition-all hover:shadow-xl`}
      >
        <p className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">{message}</p>
        {timestamp && (
          <span className="text-xs opacity-60 mt-2 block">{timestamp}</span>
        )}
      </div>
    </div>
  );
}
