export default function ChatHeader({ name, avatarInitial, lastSeen }) {
  return (
    <header className="chat-header">
      <div className="avatar" aria-hidden="true">
        {avatarInitial}
      </div>
      <div>
        <h1>{name}</h1>
        <p>Last seen today at {lastSeen}</p>
      </div>
    </header>
  );
}
