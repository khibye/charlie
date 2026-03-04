import { MANZOURI_REPLY_URL } from '../constants/chat.js';

const DEBUG_API = import.meta.env.VITE_DEBUG_API === 'true';

function debugLog(label, data) {
  if (!DEBUG_API) {
    return;
  }

  console.log(`[manzouri-api] ${label}`, data);
}

function extractReply(payload) {
  if (typeof payload === 'string') {
    const normalized = payload.trim();
    return normalized ? normalized : null;
  }

  if (!payload || typeof payload !== 'object') {
    return null;
  }

  if (typeof payload.summarize === 'string') {
    const summarizeText = payload.summarize.trim();
    if (summarizeText) {
      return summarizeText;
    }
  }

  const fallbackReply = payload.reply ?? payload.message ?? payload.text;
  return typeof fallbackReply === 'string' && fallbackReply.trim()
    ? fallbackReply
    : null;
}

export async function fetchManzouriReply(requestPayload) {
  const url = new URL(MANZOURI_REPLY_URL);
  Object.entries(requestPayload).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });

  debugLog('request', {
    method: 'GET',
    url: url.toString(),
    query: requestPayload,
  });

  const response = await fetch(url, {
    method: 'GET',
  });

  debugLog('response-meta', {
    status: response.status,
    ok: response.ok,
    contentType: response.headers.get('content-type') ?? '',
  });

  if (!response.ok) {
    throw new Error(`Manzouri API returned status ${response.status}`);
  }

  const contentType = response.headers.get('content-type') ?? '';

  if (contentType.includes('application/json')) {
    const payload = await response.json();
    debugLog('response-json', payload);

    const reply = extractReply(payload);
    debugLog('resolved-reply', reply);
    return reply;
  }

  const textPayload = await response.text();
  debugLog('response-text', textPayload);

  const reply = extractReply(textPayload);
  debugLog('resolved-reply', reply);
  return reply;
}
