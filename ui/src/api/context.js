import { API_BASE_URL, CONTEXT_ENDPOINTS } from '../constants/chat.js';

const DEBUG_API = import.meta.env.VITE_DEBUG_API === 'true';

function debugLog(label, data) {
  if (!DEBUG_API) {
    return;
  }

  console.log(`[context-api] ${label}`, data);
}

function buildUrl(path, params) {
  const url = new URL(path, API_BASE_URL);
  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.set(key, String(value));
  });
  return url;
}

function extractContext(payload) {
  if (!payload || typeof payload !== 'object') {
    return null;
  }

  const contextValue = payload.context ?? payload.content;
  return typeof contextValue === 'string' && contextValue.trim() ? contextValue : null;
}

export async function fetchCurrentContext(requestParams) {
  const errors = [];

  for (const path of CONTEXT_ENDPOINTS.get) {
    const url = buildUrl(path, requestParams);
    debugLog('get-context-request', url.toString());

    try {
      const response = await fetch(url, { method: 'GET' });
      debugLog('get-context-response-meta', {
        path,
        status: response.status,
        ok: response.ok,
      });

      if (!response.ok) {
        errors.push(`${path}: ${response.status}`);
        continue;
      }

      const payload = await response.json();
      debugLog('get-context-response-json', payload);

      const context = extractContext(payload);
      if (context) {
        return context;
      }

      errors.push(`${path}: response missing context field`);
    } catch (error) {
      errors.push(`${path}: ${String(error)}`);
    }
  }

  throw new Error(`Could not fetch context. ${errors.join(' | ')}`);
}

export async function manualImproveContext(requestParams, newContext) {
  const url = new URL(CONTEXT_ENDPOINTS.manualImprove, API_BASE_URL);
  const body = {
    ...requestParams,
    new_context: newContext,
  };

  debugLog('manual-improve-request', { url: url.toString(), body });

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  debugLog('manual-improve-response-meta', {
    status: response.status,
    ok: response.ok,
  });

  if (!response.ok) {
    throw new Error(`Manual improve failed with status ${response.status}`);
  }
}

export async function llmImproveContext(requestParams, clarification) {
  const url = new URL(CONTEXT_ENDPOINTS.llmImprove, API_BASE_URL);
  const body = {
    ...requestParams,
    context_request_clarification: clarification,
  };

  debugLog('llm-improve-request', { url: url.toString(), body });

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  debugLog('llm-improve-response-meta', {
    status: response.status,
    ok: response.ok,
  });

  if (!response.ok) {
    throw new Error(`LLM improve failed with status ${response.status}`);
  }
}
