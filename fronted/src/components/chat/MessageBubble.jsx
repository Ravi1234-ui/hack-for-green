// src/components/chat/MessageBubble.jsx
import { useState } from 'react'
import s from '../../styles/components/chat.module.css'

function ParamForm({ fields, onSubmit }) {
  const [vals, setVals] = useState(
    Object.fromEntries(fields.map(f => [f, '']))
  )
  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(vals)
  }
  return (
    <form className={s.paramForm} onSubmit={handleSubmit}>
      <div className={s.paramFormTitle}>⚙ Required Parameters</div>
      <div className={s.paramFields}>
        {fields.map(field => (
          <div key={field} className={s.paramField}>
            <label className={s.paramLabel}>{field.replace(/_/g, ' ')}</label>
            <input
              className={s.paramInput}
              type="text"
              placeholder={`Enter ${field.replace(/_/g, ' ')}…`}
              value={vals[field]}
              onChange={e => setVals(v => ({ ...v, [field]: e.target.value }))}
              required
            />
          </div>
        ))}
      </div>
      <button className={s.paramSubmit} type="submit">Submit →</button>
    </form>
  )
}

export default function MessageBubble({ message, onParamSubmit }) {
  const { role, text, time, toolTag, missingParams, intent } = message
  const isUser = role === 'user'

  return (
    <div className={`${s.msgRow} ${isUser ? s.msgRowUser : s.msgRowAi}`}>
      <div className={`${s.msgAvatar} ${isUser ? s.userAvatar : s.aiAvatar}`}>
        {isUser ? 'AK' : '◈'}
      </div>
      <div>
        {toolTag && (
          <div className={s.toolTag}>⚙ {toolTag}</div>
        )}
        <div className={`${s.bubble} ${isUser ? s.bubbleUser : s.bubbleAi}`}>
          {text}
          {missingParams && missingParams.length > 0 && (
            <ParamForm
              fields={missingParams}
              onSubmit={(vals) => onParamSubmit && onParamSubmit(intent, vals)}
            />
          )}
        </div>
        <div className={s.bubbleMeta}>{time}</div>
      </div>
    </div>
  )
}
