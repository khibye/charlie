import { useCallback, useState } from 'react';
import {
  fetchCurrentContext,
  llmImproveContext,
  manualImproveContext,
} from '../api/context.js';
import { CHARLIE_REQUEST_PAYLOAD } from '../constants/chat.js';

export function useContextManager() {
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [currentContext, setCurrentContext] = useState('');
  const [manualContext, setManualContext] = useState('');
  const [clarification, setClarification] = useState('');
  const [isLoadingContext, setIsLoadingContext] = useState(false);
  const [isSavingManual, setIsSavingManual] = useState(false);
  const [isSavingLlm, setIsSavingLlm] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const loadContext = useCallback(async () => {
    setIsLoadingContext(true);
    setErrorMessage('');

    try {
      const context = await fetchCurrentContext(CHARLIE_REQUEST_PAYLOAD);
      setCurrentContext(context);
      setManualContext(context);
      setStatusMessage('Context loaded.');
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Failed to load context.');
    } finally {
      setIsLoadingContext(false);
    }
  }, []);

  const openPanel = useCallback(async () => {
    setIsPanelOpen(true);
    await loadContext();
  }, [loadContext]);

  const closePanel = useCallback(() => {
    setIsPanelOpen(false);
    setStatusMessage('');
    setErrorMessage('');
  }, []);

  const applyManualUpdate = useCallback(async () => {
    const nextContext = manualContext.trim();
    if (!nextContext) {
      setErrorMessage('Manual context cannot be empty.');
      return;
    }

    setIsSavingManual(true);
    setErrorMessage('');

    try {
      await manualImproveContext(CHARLIE_REQUEST_PAYLOAD, nextContext);
      await loadContext();
      setStatusMessage('Manual context update completed.');
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Manual update failed.');
    } finally {
      setIsSavingManual(false);
    }
  }, [loadContext, manualContext]);

  const applyLlmUpdate = useCallback(async () => {
    const request = clarification.trim();
    if (!request) {
      setErrorMessage('Clarification request cannot be empty.');
      return;
    }

    setIsSavingLlm(true);
    setErrorMessage('');

    try {
      await llmImproveContext(CHARLIE_REQUEST_PAYLOAD, request);
      await loadContext();
      setStatusMessage('LLM context update completed.');
      setClarification('');
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'LLM update failed.');
    } finally {
      setIsSavingLlm(false);
    }
  }, [clarification, loadContext]);

  return {
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
  };
}
