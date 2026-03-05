import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { streamCharlieReply } from '../api/charlie.js';
import { CHARLIE_REQUEST_PAYLOAD } from '../constants/chat.js';
import { formatTime } from '../utils/time.js';

export function useSummaryGenerator() {
  const [summary, setSummary] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [generatedAt, setGeneratedAt] = useState(null);
  const abortControllerRef = useRef(null);

  const generatedAtLabel = useMemo(
    () => (generatedAt ? formatTime(generatedAt) : null),
    [generatedAt]
  );

  const generateSummary = useCallback(async () => {
    if (isGenerating) {
      return;
    }

    const controller = new AbortController();
    abortControllerRef.current = controller;

    setIsGenerating(true);
    setError('');
    setSummary('');

    try {
      const finalText = await streamCharlieReply(
        CHARLIE_REQUEST_PAYLOAD,
        (chunk) => {
          setSummary((previous) => previous + chunk);
        },
        { signal: controller.signal }
      );

      setSummary((previous) => finalText ?? previous ?? 'No summary was returned.');
      setGeneratedAt(new Date());
    } catch (requestError) {
      const wasAborted =
        requestError instanceof DOMException && requestError.name === 'AbortError';

      if (!wasAborted) {
        setError(
          requestError instanceof Error
            ? requestError.message
            : 'Failed to generate summary. Please try again.'
        );
      }
    } finally {
      abortControllerRef.current = null;
      setIsGenerating(false);
    }
  }, [isGenerating]);

  const stopSummary = useCallback(() => {
    abortControllerRef.current?.abort();
  }, []);

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  return {
    summary,
    isGenerating,
    error,
    generatedAtLabel,
    generateSummary,
    stopSummary,
  };
}
