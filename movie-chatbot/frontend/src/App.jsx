import { useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { useChat } from './context/ChatContext';
import { fetchScripts } from './services/api';
import './App.css';

export default function App() {
  const { state, dispatch } = useChat();

  useEffect(() => {
    fetchScripts().then((scripts) => {
      dispatch({ type: 'SET_SCRIPTS', scripts });
    });
  }, [dispatch]);

  useEffect(() => {
    if (state.conversations.length === 0) {
      dispatch({ type: 'NEW_CONVERSATION' });
    }
  }, [state.conversations.length, dispatch]);

  return (
    <div className="app">
      <Sidebar />
      <ChatWindow />
    </div>
  );
}
