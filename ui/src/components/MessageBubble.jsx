import { formatTime } from '../utils/time.js';

export default function MessageBubble({ message }) {
  const toneClass = message.sender === 'you' ? 'mine' : 'theirs';

  return (
    <summarize className={`bubble ${toneClass}`}>
      <p>{message.content}</p>
      <time>{formatTime(message.time)}</time>
    </summarize>
  );
}
