export const CHAT_CONTACT = {
  name: 'Charlie',
  avatarInitial: 'M',
  introMessage: 'Hey, this is Charlie. Send me a message when you are ready.',
};

export const API_BASE_URL = 'http://localhost:8000';
export const CHARLIE_REPLY_URL = `${API_BASE_URL}/summarize`;
export const CHARLIE_REPLY_STREAM_URL = `${API_BASE_URL}/summarize-stream`;
export const CONTEXT_ENDPOINTS = {
  get: ['/context'],
  manualImprove: '/manual-improve-context',
  llmImprove: '/llm-improve-context',
};
export const USER_ID = 'user-001';
export const COUNTRY = 'Israel';
export const CITY = 'Tel Aviv';

export const CHARLIE_REQUEST_PAYLOAD = {
  user_id: USER_ID,
  country: COUNTRY,
  city: CITY,
};

export const AUTO_REPLIES = [
  'I hear you. Tell me more.',
  'Interesting point, I am following.',
  'Let us break it down step by step.',
  'Sounds good. What is the next move?',
  'I am with you on this.',
];
