import { useMemo } from 'react';
import ChatHeader from './components/ChatHeader.jsx';
import ContextPanel from './components/ContextPanel.jsx';
import MessageComposer from './components/MessageComposer.jsx';
import MessageList from './components/MessageList.jsx';
import { CHAT_CONTACT } from './constants/chat.js';
import { useChat } from './hooks/useChat.js';
import { useContextManager } from './hooks/useContextManager.js';
import { formatTime } from './utils/time.js';

export default function App() {
  const { text, setText, messages, sendMessage } = useChat();
  const {
    isPanelOpen,
    currentContext,
    manualContext,
    clarification,
    isLoadingContext,
    isSavingManual,
    isSavingLlm,
    statusMessage,
    errorMessage,
    setManualContext,
    setClarification,
    openPanel,
    closePanel,
    loadContext,
    applyManualUpdate,
    applyLlmUpdate,
  } = useContextManager();

  const lastSeen = useMemo(() => formatTime(new Date()), []);

  return (
    <main className="chat-page">
      <section className="chat-card" aria-label={`Chat with ${CHAT_CONTACT.name}`}>
        <ChatHeader
          name={CHAT_CONTACT.name}
          avatarInitial={CHAT_CONTACT.avatarInitial}
          lastSeen={lastSeen}
          onContextClick={openPanel}
        />
        <ContextPanel
          isOpen={isPanelOpen}
          currentContext={currentContext}
          manualContext={manualContext}
          clarification={clarification}
          isLoadingContext={isLoadingContext}
          isSavingManual={isSavingManual}
          isSavingLlm={isSavingLlm}
          statusMessage={statusMessage}
          errorMessage={errorMessage}
          onManualContextChange={setManualContext}
          onClarificationChange={setClarification}
          onRefresh={loadContext}
          onManualUpdate={applyManualUpdate}
          onLlmUpdate={applyLlmUpdate}
          onClose={closePanel}
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
