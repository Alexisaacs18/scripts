import { createContext, useContext, useReducer, useCallback } from 'react';

const ChatContext = createContext(null);

const initialState = {
  conversations: [],
  activeConversationId: null,
  pageCount: 2,
  scripts: [],
  isGenerating: false,
};

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function chatReducer(state, action) {
  switch (action.type) {
    case 'NEW_CONVERSATION': {
      const id = generateId();
      const conv = { id, title: 'New Scene', messages: [], generatedScript: null };
      return {
        ...state,
        conversations: [conv, ...state.conversations],
        activeConversationId: id,
      };
    }
    case 'SET_ACTIVE_CONVERSATION':
      return { ...state, activeConversationId: action.id };

    case 'DELETE_CONVERSATION': {
      const filtered = state.conversations.filter((c) => c.id !== action.id);
      return {
        ...state,
        conversations: filtered,
        activeConversationId:
          state.activeConversationId === action.id
            ? (filtered[0]?.id ?? null)
            : state.activeConversationId,
      };
    }
    case 'ADD_MESSAGE': {
      return {
        ...state,
        conversations: state.conversations.map((c) => {
          if (c.id !== action.conversationId) return c;
          const updated = { ...c, messages: [...c.messages, action.message] };
          if (c.messages.length === 0 && action.message.role === 'user') {
            updated.title = action.message.content.slice(0, 50) + (action.message.content.length > 50 ? '...' : '');
          }
          return updated;
        }),
      };
    }
    case 'UPDATE_LAST_ASSISTANT_MESSAGE': {
      return {
        ...state,
        conversations: state.conversations.map((c) => {
          if (c.id !== action.conversationId) return c;
          const msgs = [...c.messages];
          for (let i = msgs.length - 1; i >= 0; i--) {
            if (msgs[i].role === 'assistant') {
              msgs[i] = { ...msgs[i], content: action.content };
              break;
            }
          }
          return { ...c, messages: msgs };
        }),
      };
    }
    case 'SET_PAGE_COUNT':
      return { ...state, pageCount: action.pageCount };

    case 'SET_SCRIPTS':
      return { ...state, scripts: action.scripts };

    case 'SET_GENERATING':
      return { ...state, isGenerating: action.value };

    default:
      return state;
  }
}

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const getActiveConversation = useCallback(() => {
    return state.conversations.find((c) => c.id === state.activeConversationId) ?? null;
  }, [state.conversations, state.activeConversationId]);

  return (
    <ChatContext.Provider value={{ state, dispatch, getActiveConversation }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const ctx = useContext(ChatContext);
  if (!ctx) throw new Error('useChat must be used within ChatProvider');
  return ctx;
}
