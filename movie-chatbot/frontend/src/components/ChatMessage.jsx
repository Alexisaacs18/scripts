import { FiUser, FiCpu } from 'react-icons/fi';
import ScriptRenderer from './ScriptRenderer';
import './ChatMessage.css';

export default function ChatMessage({ message, isGenerating }) {
  const isUser = message.role === 'user';
  const isEmpty = !message.content;

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-row">
        <div className={`avatar ${isUser ? 'avatar-user' : 'avatar-assistant'}`}>
          {isUser ? <FiUser size={16} /> : <FiCpu size={16} />}
        </div>
        <div className="message-body">
          <div className="message-role">{isUser ? 'You' : 'ScriptForge'}</div>
          <div className="message-content">
            {isEmpty && isGenerating ? (
              <span className="typing-indicator">
                <span></span><span></span><span></span>
              </span>
            ) : isUser ? (
              <p className="user-text">{message.content}</p>
            ) : (
              <ScriptRenderer content={message.content} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
