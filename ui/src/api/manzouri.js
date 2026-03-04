import { MANZOURI_REPLY_STREAM_URL } from '../constants/chat.js';

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
  const url = new URL(MANZOURI_REPLY_STREAM_URL);
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

  if (!response.body) {
    const textPayload = await response.text();
    debugLog('response-text-fallback', textPayload);
    return extractReply(textPayload);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullText = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    const chunk = decoder.decode(value, { stream: true });
    if (!chunk) {
      continue;
    }
    fullText += chunk;
  }

  const trailing = decoder.decode();
  if (trailing) {
    fullText += trailing;
  }

  debugLog('response-stream-complete', fullText);
  return extractReply(fullText);
}

export async function streamManzouriReply(requestPayload, onChunk, options = {}) {
  const url = new URL(MANZOURI_REPLY_STREAM_URL);
  Object.entries(requestPayload).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });

  debugLog('stream-request', {
    method: 'GET',
    url: url.toString(),
    query: requestPayload,
  });

  const response = await fetch(url, { method: 'GET', signal: options.signal });
  if (!response.ok) {
    throw new Error(`Manzouri API returned status ${response.status}`);
  }
  if (!response.body) {
    const text = await response.text();
    onChunk?.(text);
    return extractReply(text);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let fullText = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      break;
    }

    const chunk = decoder.decode(value, { stream: true });
    if (!chunk) {
      continue;
    }

    fullText += chunk;
    onChunk?.(chunk);
  }

  const trailing = decoder.decode();
  if (trailing) {
    fullText += trailing;
    onChunk?.(trailing);
  }

  return extractReply(fullText);
}
