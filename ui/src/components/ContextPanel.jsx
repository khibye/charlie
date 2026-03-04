export default function ContextPanel({
  isOpen,
  currentContext,
  manualContext,
  clarification,
  isLoadingContext,
  isSavingManual,
  isSavingLlm,
  statusMessage,
  errorMessage,
  onManualContextChange,
  onClarificationChange,
  onRefresh,
  onManualUpdate,
  onLlmUpdate,
  onClose,
}) {
  if (!isOpen) {
    return null;
  }

  return (
    <section className="context-panel" aria-label="Context update panel">
      <header className="context-panel-header">
        <h2>Context Management</h2>
        <div className="context-panel-actions">
          <button type="button" className="secondary" onClick={onRefresh} disabled={isLoadingContext}>
            {isLoadingContext ? 'Loading...' : 'Refresh'}
          </button>
          <button type="button" className="secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </header>

      <div className="context-current">
        <h3>Current Context</h3>
        <p>{currentContext || 'No context available yet.'}</p>
      </div>

      <div className="context-grid">
        <section className="pipeline-card">
          <h3>Manual Pipeline</h3>
          <p>Directly replace the context with your edited version.</p>
          <textarea
            value={manualContext}
            onChange={(event) => onManualContextChange(event.target.value)}
            placeholder="Write the full context..."
            rows={5}
          />
          <button type="button" onClick={onManualUpdate} disabled={isSavingManual}>
            {isSavingManual ? 'Saving...' : 'Update Manually'}
          </button>
        </section>

        <section className="pipeline-card">
          <h3>LLM Pipeline</h3>
          <p>Write a natural-language clarification request for automatic improvement.</p>
          <textarea
            value={clarification}
            onChange={(event) => onClarificationChange(event.target.value)}
            placeholder="Example: focus more on user buying intent and pricing sensitivity"
            rows={5}
          />
          <button type="button" onClick={onLlmUpdate} disabled={isSavingLlm}>
            {isSavingLlm ? 'Improving...' : 'Improve with LLM'}
          </button>
        </section>
      </div>

      {statusMessage ? <p className="status success">{statusMessage}</p> : null}
      {errorMessage ? <p className="status error">{errorMessage}</p> : null}
    </section>
  );
}
