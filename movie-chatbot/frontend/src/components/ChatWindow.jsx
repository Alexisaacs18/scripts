import { useCallback } from 'react';
import ChatMessage from './ChatMessage';
import InputBar from './InputBar';
import PageSelector from './PageSelector';
import { useChat } from '../context/ChatContext';
import { generateScript } from '../services/api';
import './ChatWindow.css';

export default function ChatWindow() {
  const { state, dispatch, getActiveConversation } = useChat();
  const conversation = getActiveConversation();

  const handleSend = useCallback(
    async (text) => {
      if (!conversation || state.isGenerating) return;

      const userMsg = { role: 'user', content: text };
      dispatch({
        type: 'ADD_MESSAGE',
        conversationId: conversation.id,
        message: userMsg,
      });

      const assistantPlaceholder = { role: 'assistant', content: '' };
      dispatch({
        type: 'ADD_MESSAGE',
        conversationId: conversation.id,
        message: assistantPlaceholder,
      });

      dispatch({ type: 'SET_GENERATING', value: true });

      try {
        const allMessages = [...conversation.messages, userMsg].map((m) => ({
          role: m.role,
          content: m.content,
        }));

        const data = await generateScript({
          messages: allMessages,
          pageCount: state.pageCount,
        });

        dispatch({
          type: 'UPDATE_LAST_ASSISTANT_MESSAGE',
          conversationId: conversation.id,
          content: data.script,
        });
      } catch (err) {
        dispatch({
          type: 'UPDATE_LAST_ASSISTANT_MESSAGE',
          conversationId: conversation.id,
          content: `Error: ${err.message}`,
        });
      } finally {
        dispatch({ type: 'SET_GENERATING', value: false });
      }
    },
    [conversation, state.pageCount, state.isGenerating, dispatch]
  );

  if (!conversation) {
    return <div className="chat-window empty">Select or start a conversation</div>;
  }

  return (
    <main className="chat-window">
      <div className="chat-header">
        <h2 className="chat-title">{conversation.title}</h2>
        <PageSelector />
      </div>

      <div className="messages-container">
        {conversation.messages.length === 0 && (
          <div className="welcome">
            <div className="welcome-icon">&#127916;</div>
            <h3>Describe your scene</h3>
            <p>
              Set the stage — who's in the scene, where it takes place, what
              happens, the mood. After the first draft you can ask for rewrites,
              dialogue changes, pacing tweaks, and more.
            </p>
          </div>
        )}
        {conversation.messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} isGenerating={state.isGenerating && i === conversation.messages.length - 1 && msg.role === 'assistant'} />
        ))}
      </div>

      <InputBar onSend={handleSend} disabled={state.isGenerating} />
    </main>
  );
}
