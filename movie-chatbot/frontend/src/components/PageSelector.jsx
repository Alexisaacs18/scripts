import { useChat } from '../context/ChatContext';
import './PageSelector.css';

export default function PageSelector() {
  const { state, dispatch } = useChat();

  return (
    <div className="page-selector">
      <label htmlFor="page-select">Scene Length</label>
      <select
        id="page-select"
        value={state.pageCount}
        onChange={(e) =>
          dispatch({ type: 'SET_PAGE_COUNT', pageCount: parseInt(e.target.value) })
        }
      >
        <option value={1}>1 page</option>
        <option value={2}>2 pages</option>
        <option value={3}>3 pages</option>
        <option value={4}>4 pages</option>
        <option value={5}>5 pages</option>
      </select>
    </div>
  );
}
