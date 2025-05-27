import { useState } from 'react';

/**
 * ChatInput component handles user text input and submits it via POST request.
 * Props:
 * - onSend(role: string, message: string): function to render a message in the chat UI.
 */
export default function ChatInput({ onSend }) {
  const [input, setInput] = useState('');

  // Send message to the backend and handle response
  const handleSubmit = async () => {
    if (!input.trim()) return;
    onSend('user', input);
    setInput('');

    const formData = new FormData();
    formData.append('prompt', input);

    const response = await fetch('/get_incident_report/', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    onSend('giga', data.solution || data.incident_summary || 'Ответ не получен.');
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Введите вопрос или загрузите файл"
        onKeyDown={e => e.key === 'Enter' && handleSubmit()}
      />
      <button onClick={handleSubmit}>Отправить</button>
    </div>
  );
}