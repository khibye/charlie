import { useCallback, useMemo, useState } from 'react';
import { streamManzouriReply } from '../api/manzouri.js';
import { MANZOURI_REQUEST_PAYLOAD } from '../constants/chat.js';
import { formatTime } from '../utils/time.js';

export function useSummaryGenerator() {
  const [summary, setSummary] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  const [generatedAt, setGeneratedAt] = useState(null);

  const generatedAtLabel = useMemo(
    () => (generatedAt ? formatTime(generatedAt) : null),
    [generatedAt]
  );

  const generateSummary = useCallback(async () => {
    setIsGenerating(true);
    setError('');
    setSummary('');

    try {
      const finalText = await streamManzouriReply(MANZOURI_REQUEST_PAYLOAD, (chunk) => {
        setSummary((previous) => previous + chunk);
      });

      setSummary((previous) => finalText ?? previous ?? 'No summary was returned.');
      setGeneratedAt(new Date());
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : 'Failed to generate summary. Please try again.'
      );
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return {
    summary,
    isGenerating,
    error,
    generatedAtLabel,
    generateSummary,
  };
}
