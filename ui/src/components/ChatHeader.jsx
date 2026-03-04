export default function ChatHeader({ name, avatarInitial, subtitle, onContextClick }) {
  return (
    <header className="chat-header">
      <div className="avatar" aria-hidden="true">
        {avatarInitial}
      </div>
      <div className="chat-title">
        <h1>{name}</h1>
        <p>{subtitle}</p>
      </div>
      <button type="button" className="context-toggle" onClick={onContextClick}>
        Update Context
      </button>
    </header>
  );
}
