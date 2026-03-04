import { useMemo } from 'react';
import ChatHeader from './components/ChatHeader.jsx';
import MessageComposer from './components/MessageComposer.jsx';
import MessageList from './components/MessageList.jsx';
import { CHAT_CONTACT } from './constants/chat.js';
import { useChat } from './hooks/useChat.js';
import { formatTime } from './utils/time.js';

export default function App() {
  const { text, setText, messages, sendMessage } = useChat();

  const lastSeen = useMemo(() => formatTime(new Date()), []);

  return (
    <main className="chat-page">
      <section className="chat-card" aria-label={`Chat with ${CHAT_CONTACT.name}`}>
        <ChatHeader
          name={CHAT_CONTACT.name}
          avatarInitial={CHAT_CONTACT.avatarInitial}
          lastSeen={lastSeen}
        />
        <MessageList messages={messages} />
        <MessageComposer
          text={text}
          onTextChange={setText}
          onSend={sendMessage}
          contactName={CHAT_CONTACT.name}
        />
      </section>
    </main>
  );
}
