export default function MessageComposer({ text, onTextChange, onSend, contactName }) {
  return (
    <form
      className="composer"
      onSubmit={(event) => {
        event.preventDefault();
        onSend();
      }}
    >
      <input
        type="text"
        value={text}
        placeholder={`Message ${contactName}...`}
        onChange={(event) => onTextChange(event.target.value)}
        aria-label="Type message"
      />
      <button type="submit">Send</button>
    </form>
  );
}
