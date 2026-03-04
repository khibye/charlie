import ChatHeader from './components/ChatHeader.jsx';
import ContextPanel from './components/ContextPanel.jsx';
import { CHAT_CONTACT } from './constants/chat.js';
import { useContextManager } from './hooks/useContextManager.js';
import { useSummaryGenerator } from './hooks/useSummaryGenerator.js';

export default function App() {
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
  const { summary, isGenerating, error, generatedAtLabel, generateSummary } =
    useSummaryGenerator();

  return (
    <main className="chat-page">
      <section className="chat-card" aria-label="Summary workspace">
        <ChatHeader
          name="Summary Generator"
          avatarInitial={CHAT_CONTACT.avatarInitial}
          subtitle={
            generatedAtLabel
              ? `Last generated today at ${generatedAtLabel}`
              : 'Generate a fluent summary from your current data and context'
          }
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
        <section className="summary-shell">
          <div className="summary-toolbar">
            <button
              type="button"
              className="generate-button"
              onClick={generateSummary}
              disabled={isGenerating}
            >
              {isGenerating ? 'Generating...' : 'Generate Summary'}
            </button>
          </div>

          <article className="summary-output" aria-live="polite">
            {summary ? (
              summary
            ) : isGenerating ? (
              <div className="thinking-state">
                <p className="thinking-title">Working on your summary</p>
                <p className="thinking-subtitle">
                  Reading data, extracting signals, and preparing a fluent response.
                </p>
                <div className="thinking-dots" aria-label="Generating summary">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            ) : (
              'No summary generated yet.'
            )}
          </article>

          {error ? <p className="status error">{error}</p> : null}
        </section>
      </section>
    </main>
  );
}
