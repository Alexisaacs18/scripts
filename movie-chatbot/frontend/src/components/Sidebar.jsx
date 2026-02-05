import { useState } from 'react';
import { FiPlus, FiMessageSquare, FiTrash2, FiFilm, FiChevronDown, FiChevronRight } from 'react-icons/fi';
import { useChat } from '../context/ChatContext';
import ScriptManager from './ScriptManager';
import './Sidebar.css';

export default function Sidebar() {
  const { state, dispatch } = useChat();
  const [scriptsOpen, setScriptsOpen] = useState(false);

  const handleNew = () => dispatch({ type: 'NEW_CONVERSATION' });

  const handleSelect = (id) => dispatch({ type: 'SET_ACTIVE_CONVERSATION', id });

  const handleDelete = (e, id) => {
    e.stopPropagation();
    dispatch({ type: 'DELETE_CONVERSATION', id });
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <FiFilm size={22} />
          <span>ScriptForge</span>
        </div>
      </div>

      <button className="new-chat-btn" onClick={handleNew}>
        <FiPlus size={16} />
        <span>New Script</span>
      </button>

      <nav className="conversation-list">
        <div className="section-label">Conversations</div>
        {state.conversations.map((conv) => (
          <div
            key={conv.id}
            className={`conversation-item ${conv.id === state.activeConversationId ? 'active' : ''}`}
            onClick={() => handleSelect(conv.id)}
          >
            <FiMessageSquare size={14} />
            <span className="conversation-title">{conv.title}</span>
            <button
              className="delete-btn"
              onClick={(e) => handleDelete(e, conv.id)}
              aria-label="Delete conversation"
            >
              <FiTrash2 size={13} />
            </button>
          </div>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <button
          className="scripts-toggle"
          onClick={() => setScriptsOpen(!scriptsOpen)}
        >
          {scriptsOpen ? <FiChevronDown size={14} /> : <FiChevronRight size={14} />}
          <span>Reference Scripts ({state.scripts.length})</span>
        </button>
        {scriptsOpen && <ScriptManager />}
      </div>
    </aside>
  );
}
