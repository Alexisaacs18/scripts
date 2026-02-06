import { useChat } from '../context/ChatContext';
import './PageSelector.css';

const PAGE_OPTIONS = [1, 2, 3, 4, 5];

export default function PageSelector() {
  const { state, dispatch } = useChat();

  return (
    <div className="page-selector">
      <label htmlFor="page-select">Pages</label>
      <select
        id="page-select"
        value={state.pageCount}
        onChange={(e) =>
          dispatch({ type: 'SET_PAGE_COUNT', pageCount: parseInt(e.target.value) })
        }
      >
        {PAGE_OPTIONS.map((n) => (
          <option key={n} value={n}>
            {n}
          </option>
        ))}
      </select>
    </div>
  );
}
