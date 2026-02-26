// src/components/chat/SuggestionBar.jsx
import s from '../../styles/components/chat.module.css'

const SUGGESTIONS = [
  { icon: '⬡', label: 'Calculate EMI' },
  { icon: '◈', label: 'Analyze Spending' },
  { icon: '◎', label: 'Create 1-Year Plan' },
  { icon: '∑', label: 'Simulate Risk' },
  { icon: '≈', label: 'Optimize Budget' },
  { icon: '⊕', label: 'Goal Projection' },
]

export default function SuggestionBar({ onSelect, disabled }) {
  return (
    <div className={s.suggestionBar}>
      {SUGGESTIONS.map((sg, i) => (
        <button
          key={i}
          className={s.chip}
          onClick={() => !disabled && onSelect(sg.label)}
          disabled={disabled}
        >
          <span>{sg.icon}</span>
          {sg.label}
        </button>
      ))}
    </div>
  )
}
