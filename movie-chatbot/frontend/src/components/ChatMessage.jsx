import { useState } from 'react';
import { FiUser, FiCpu, FiDownload } from 'react-icons/fi';
import ScriptRenderer from './ScriptRenderer';
import { exportPDF } from '../services/api';
import './ChatMessage.css';

export default function ChatMessage({ message, isGenerating }) {
  const isUser = message.role === 'user';
  const isEmpty = !message.content;
  const [downloading, setDownloading] = useState(false);

  const handleDownloadPDF = async () => {
    if (downloading || !message.content) return;
    setDownloading(true);
    try {
      const blob = await exportPDF({
        script: message.content,
        title: 'Scene',
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'scene.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF download failed:', err);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-row">
        <div className={`avatar ${isUser ? 'avatar-user' : 'avatar-assistant'}`}>
          {isUser ? <FiUser size={16} /> : <FiCpu size={16} />}
        </div>
        <div className="message-body">
          <div className="message-role">
            {isUser ? 'You' : 'ScriptForge'}
            {!isUser && message.content && !isGenerating && (
              <button
                className="pdf-download-btn"
                onClick={handleDownloadPDF}
                disabled={downloading}
                title="Download as PDF"
              >
                <FiDownload size={13} />
                {downloading ? 'Exporting...' : 'PDF'}
              </button>
            )}
          </div>
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
