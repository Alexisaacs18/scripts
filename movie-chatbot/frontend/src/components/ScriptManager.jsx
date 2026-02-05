import { useRef } from 'react';
import { FiUpload, FiX, FiFile } from 'react-icons/fi';
import { useChat } from '../context/ChatContext';
import { uploadScript, deleteScript, fetchScripts } from '../services/api';
import './ScriptManager.css';

export default function ScriptManager() {
  const { state, dispatch } = useChat();
  const fileRef = useRef(null);

  const refresh = async () => {
    const scripts = await fetchScripts();
    dispatch({ type: 'SET_SCRIPTS', scripts });
  };

  const handleUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      await uploadScript(file);
      await refresh();
    } catch {
      alert('Failed to upload script');
    }
    e.target.value = '';
  };

  const handleDelete = async (name) => {
    try {
      await deleteScript(name);
      await refresh();
    } catch {
      alert('Failed to delete script');
    }
  };

  return (
    <div className="script-manager">
      <div className="script-list">
        {state.scripts.length === 0 && (
          <p className="empty-text">No reference scripts yet</p>
        )}
        {state.scripts.map((name) => (
          <div key={name} className="script-item">
            <FiFile size={12} />
            <span className="script-name">{name}</span>
            <button className="script-remove" onClick={() => handleDelete(name)}>
              <FiX size={12} />
            </button>
          </div>
        ))}
      </div>
      <input
        ref={fileRef}
        type="file"
        accept=".txt,.fountain,.fdx"
        hidden
        onChange={handleUpload}
      />
      <button className="upload-btn" onClick={() => fileRef.current?.click()}>
        <FiUpload size={13} />
        <span>Upload Script</span>
      </button>
    </div>
  );
}
