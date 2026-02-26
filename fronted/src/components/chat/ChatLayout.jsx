// src/components/chat/ChatLayout.jsx
import { useState, useEffect } from 'react'
import Sidebar from './Sidebar.jsx'
import ChatWindow from './ChatWindow.jsx'
import InsightPanel from './InsightPanel.jsx'
import s from '../../styles/components/chat.module.css'

const ONBOARD_STEPS = [
  {
    icon: '◈',
    title: <>Welcome to your <span className={s.onboardAccent}>Financial Intelligence</span> System</>,
    sub: 'Your AI-powered advisor is ready. Analyzing your complete financial profile…',
  },
  {
    icon: '∑',
    title: <>I analyze your <span className={s.onboardAccent}>financial behavior</span> in real time</>,
    sub: 'Scanning 24 months of transaction history, EMI patterns, investment performance, and risk exposure.',
  },
  {
    icon: '⊕',
    title: <>I help you <span className={s.onboardAccent}>optimize</span> loans, budgets, and risks</>,
    sub: 'Ask me anything — EMI simulation, budget gaps, goal timelines, or risk scenarios.',
  },
]

export default function ChatLayout({ onNavigate }) {
  const [activeNav,    setActiveNav]    = useState('dashboard')
  const [sidebarOpen,  setSidebarOpen]  = useState(false)
  const [insightOpen,  setInsightOpen]  = useState(false)
  const [onboardStep,  setOnboardStep]  = useState(0)
  const [onboarding,   setOnboarding]   = useState(true)
  const [mode,         setMode]         = useState(null)
  const [advisory,     setAdvisory]     = useState([])

  // Auto-advance onboarding
  useEffect(() => {
    if (!onboarding) return
    if (onboardStep < ONBOARD_STEPS.length - 1) {
      const t = setTimeout(() => setOnboardStep(s => s + 1), 2800)
      return () => clearTimeout(t)
    } else {
      const t = setTimeout(() => setOnboarding(false), 2800)
      return () => clearTimeout(t)
    }
  }, [onboardStep, onboarding])

  const progress = ((onboardStep + 1) / ONBOARD_STEPS.length) * 100

  return (
    <div className={s.page}>
      <div className={s.bgGrid} />

      {/* Topbar */}
      <header className={s.topbar}>
        <div className={s.topbarBrand}>
          <button className={s.hamburger} onClick={() => setSidebarOpen(o => !o)}>
            <span /><span /><span />
          </button>
          <div className={s.topbarMark}>FI</div>
          <div>
            <span className={s.topbarName}>FinIntel</span>
            <span className={s.topbarSub}>AI Financial System</span>
          </div>
        </div>

        <div className={s.topbarCenter}>
          <span className={s.topbarDot} />
          AI Engine Active
        </div>

        <div className={s.topbarRight}>
          <button className={s.topbarBtn} onClick={() => setInsightOpen(o => !o)}>
            Insights
          </button>
          <button className={s.topbarBtn} onClick={() => onNavigate('landing')}>
            ← Home
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <div className={s.layout}>
        <Sidebar
          active={activeNav}
          onSelect={setActiveNav}
          open={sidebarOpen}
          onNavigate={onNavigate}
        />

        <ChatWindow
          onModeChange={setMode}
          onAdvisory={setAdvisory}
          disabled={onboarding}
        />

        <InsightPanel
          advisory={advisory}
          open={insightOpen}
        />
      </div>

      {/* Onboarding Overlay */}
      {onboarding && (
        <div className={s.onboardOverlay}>
          <div className={s.onboardStep} key={onboardStep}>
            <span className={s.onboardIcon}>{ONBOARD_STEPS[onboardStep].icon}</span>
            <h2 className={s.onboardTitle}>{ONBOARD_STEPS[onboardStep].title}</h2>
            <p className={s.onboardSub}>{ONBOARD_STEPS[onboardStep].sub}</p>
          </div>

          <div className={s.onboardDots}>
            {ONBOARD_STEPS.map((_, i) => (
              <div key={i} className={`${s.onboardDot} ${i === onboardStep ? s.dotActive : ''}`} />
            ))}
          </div>

          <div className={s.onboardProgress}>
            <div className={s.onboardProgressBar} style={{ width: `${progress}%` }} />
          </div>

          <button className={s.onboardSkip} onClick={() => setOnboarding(false)}>
            Skip Intro
          </button>
        </div>
      )}
    </div>
  )
}
