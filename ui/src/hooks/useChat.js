import { useCallback, useState } from 'react';
import { fetchManzouriReply } from '../api/manzouri.js';
import { CHAT_CONTACT, MANZOURI_REQUEST_PAYLOAD } from '../constants/chat.js';
import { createMessage } from '../utils/chat.js';

export function useChat() {
  const [text, setText] = useState('');
  const [messages, setMessages] = useState([
    createMessage({
      sender: 'manzouri',
      content: CHAT_CONTACT.introMessage,
    }),
  ]);
  const sendMessage = useCallback(async () => {
    const content = text.trim();
    if (!content) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      createMessage({ sender: 'you', content }),
    ]);
    setText('');

    try {
      const replyFromApi = await fetchManzouriReply(MANZOURI_REQUEST_PAYLOAD);
      const reply = replyFromApi ?? 'Manzouri did not return a message.';

      setMessages((previous) => [
        ...previous,
        createMessage({ sender: 'manzouri', content: reply }),
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        createMessage({
          sender: 'manzouri',
          content: 'Could not reach Manzouri right now. Please try again.',
        }),
      ]);
    }
  }, [text]);

  return {
    text,
    setText,
    messages,
    sendMessage,
  };
}
