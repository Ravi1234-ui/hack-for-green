// src/components/chat/TypingIndicator.jsx
import s from '../../styles/components/chat.module.css'

export default function TypingIndicator() {
  return (
    <div className={s.typingRow}>
      <div className={`${s.msgAvatar} ${s.aiAvatar}`}>◈</div>
      <div className={s.typingBubble}>
        <span className={s.typingDot} />
        <span className={s.typingDot} />
        <span className={s.typingDot} />
      </div>
    </div>
  )
}
