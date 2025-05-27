/**
 * Renders a list of chat messages.
 * @param {Array} messages - List of message objects with { role, content }
 */
export default function MessageList({ messages }) {
  return (
    <div className="response-container">
      {messages.map((msg, idx) => (
        <div key={idx} className={`message ${msg.role === 'user' ? 'user-message' : 'giga-message'}`}>
          {msg.content}
        </div>
      ))}
    </div>
  );
}