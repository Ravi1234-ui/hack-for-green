// src/components/chat/ChatWindow.jsx
import { useState, useRef, useEffect, useCallback } from 'react'
import MessageBubble from './MessageBubble.jsx'
import TypingIndicator from './TypingIndicator.jsx'
import SuggestionBar from './SuggestionBar.jsx'
import { mockRespond } from './mockAI.js'
import s from '../../styles/components/chat.module.css'

const ts = () => new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

const SEED_MESSAGES = [
  {
    id: 1,
    role: 'ai',
    text: 'Your financial health score is 74/100. EMI load is within safe range at 34%. I detected 3 budget optimization opportunities this month. How can I help you today?',
    time: ts(),
    toolTag: null,
    missingParams: [],
  },
]

export default function ChatWindow({ onModeChange, onAdvisory, disabled }) {
  const [messages,  setMessages]  = useState(SEED_MESSAGES)
  const [input,     setInput]     = useState('')
  const [typing,    setTyping]    = useState(false)
  const [activeMode, setActiveMode] = useState(null)
  const endRef  = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typing])

  const send = useCallback(async (text) => {
    const msg = (text || input).trim()
    if (!msg || typing || disabled) return
    setInput('')

    const userMsg = { id: Date.now(), role: 'user', text: msg, time: ts(), toolTag: null, missingParams: [] }
    setMessages(prev => [...prev, userMsg])
    setTyping(true)

    try {
      const res = await mockRespond(msg)

      // Update mode badge
      if (res.mode && res.mode !== 'general') {
        const modeLabel = {
          calculation: 'Calculation Mode',
          advisory:    'Advisory Mode',
          onboarding:  'Onboarding Mode',
        }[res.mode] || res.mode
        setActiveMode(modeLabel)
        onModeChange && onModeChange(modeLabel)
      } else {
        setActiveMode(null)
        onModeChange && onModeChange(null)
      }

      // Push advisory insights to InsightPanel
      if (res.advisory_insights?.length) {
        onAdvisory && onAdvisory(res.advisory_insights)
      } else {
        onAdvisory && onAdvisory([])
      }

      const aiMsg = {
        id: Date.now() + 1,
        role: 'ai',
        text: res.message,
        time: ts(),
        toolTag: res.mode === 'calculation' ? `${res.intent?.replace(/_/g,' ')} · active` : null,
        missingParams: res.missing_parameters || [],
        intent: res.intent,
      }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'ai',
        text: '⚠ Could not reach the server. Please check your connection and try again.',
        time: ts(),
        toolTag: null,
        missingParams: [],
      }])
    } finally {
      setTyping(false)
    }
  }, [input, typing, disabled, onModeChange, onAdvisory])

  const handleParamSubmit = useCallback(async (intent, vals) => {
    const summary = Object.entries(vals).map(([k,v]) => `${k.replace(/_/g,' ')}: ${v}`).join(', ')
    await send(`Here are the parameters — ${summary}`)
  }, [send])

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() }
  }

  return (
    <div className={s.chatWindow}>
      {/* Header */}
      <div className={s.chatHeader}>
        <div className={s.chatHeaderLeft}>
          <div className={s.chatAiAvatar}>◈</div>
          <div>
            <div className={s.chatAiName}>FinIntel AI Advisor</div>
            <div className={s.chatAiStatus}>
              <span className={s.chatStatusDot} /> Analyzing your portfolio
            </div>
          </div>
        </div>
        {activeMode && (
          <div className={s.modeBadge}>
            <span className={s.modeBadgeDot} />
            {activeMode}
          </div>
        )}
      </div>

      {/* Messages */}
      <div className={s.messages}>
        {messages.map(msg => (
          <MessageBubble
            key={msg.id}
            message={msg}
            onParamSubmit={handleParamSubmit}
          />
        ))}
        {typing && <TypingIndicator />}
        <div ref={endRef} />
      </div>

      {/* Suggestions */}
      <SuggestionBar onSelect={send} disabled={typing || disabled} />

      {/* Input */}
      <div className={s.inputRow}>
        <textarea
          ref={inputRef}
          className={s.chatInput}
          placeholder={disabled ? 'Starting up…' : 'Ask your AI financial advisor…'}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          rows={1}
          disabled={disabled || typing}
        />
        <button
          className={s.sendBtn}
          onClick={() => send()}
          disabled={!input.trim() || typing || disabled}
        >
          →
        </button>
      </div>
    </div>
  )
}