import { useCallback, useState } from 'react';
import { streamCharlieReply } from '../api/charlie.js';
import { CHAT_CONTACT, CHARLIE_REQUEST_PAYLOAD } from '../constants/chat.js';
import { createMessage } from '../utils/chat.js';

export function useChat() {
  const [text, setText] = useState('');
  const [messages, setMessages] = useState([
    createMessage({
      sender: 'charlie',
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

    const replyMessage = createMessage({ sender: 'charlie', content: '' });
    setMessages((previous) => [...previous, replyMessage]);

    try {
      const replyFromApi = await streamCharlieReply(CHARLIE_REQUEST_PAYLOAD, (chunk) => {
        setMessages((previous) =>
          previous.map((message) =>
            message.id === replyMessage.id
              ? { ...message, content: `${message.content}${chunk}` }
              : message
          )
        );
      });

      setMessages((previous) => [
        ...previous.map((message) =>
            message.id === replyMessage.id
              ? {
                  ...message,
                  content:
                    replyFromApi ??
                    message.content ??
                    'Charlie did not return a message.',
                }
              : message
        ),
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous.map((message) =>
          message.id === replyMessage.id
            ? {
                ...message,
                content: 'Could not reach Charlie right now. Please try again.',
              }
            : message
        ),
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
