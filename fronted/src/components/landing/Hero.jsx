import { useEffect, useState } from 'react'
import VideoFrame from './VideoFrame.jsx'
import AuthModal from '../auth/AuthModal.jsx'
import s from '../../styles/hero.module.css'

const FEATURES = [
  { icon: '⬡', label: 'Intelligent Loan Planning' },
  { icon: '◈', label: 'AI Budget Optimization' },
  { icon: '⊕', label: 'Risk Intelligence Engine' },
  { icon: '∑', label: 'Financial Memory System' },
  { icon: '◎', label: 'Scenario Simulation' },
]

const FLOATERS = ['₿', '$', '%', '∑', '≈', '◈']

export default function Hero({ onNavigate }) {
  const [featureIdx, setFeatureIdx] = useState(0)
  const [exiting, setExiting] = useState(false)
  const [showAuth, setShowAuth] = useState(false)

  /* ── Feature rotation ── */
  useEffect(() => {
    const id = setInterval(() => {
      setExiting(true)
      setTimeout(() => {
        setFeatureIdx(i => (i + 1) % FEATURES.length)
        setExiting(false)
      }, 420)
    }, 4000)
    return () => clearInterval(id)
  }, [])

  return (
    <>
      <section className={s.hero}>
        <div className={s.grid} />
        <div className={s.scanLine} />
        <div className={s.ambientA} />
        <div className={s.ambientB} />

        {/* Floating finance glyphs */}
        <div className={s.floaters}>
          {FLOATERS.map((g, i) => (
            <span key={i} className={s.floater}>{g}</span>
          ))}
        </div>

        <div className={s.inner}>

          {/* ════ LEFT — Copy + CTA ════ */}
          <div className={s.copy}>

            <span className={s.eyebrow}>
              <span className={s.eyebrowDot} />
              Enterprise · AI-Powered · Real-Time
            </span>

            <h1 className={s.headline}>
              <span className={s.headlineLine1}>
                AI <span className={s.headlineAccent}>Financial</span><br />
                Intelligence System
              </span>
              <span className={s.headlineLine2}>
                Strategic Banking Optimization for 2026
              </span>
            </h1>

            <p className={s.tagline}>
              Analyze <span className={s.taglineSep}>◆</span>
              Simulate <span className={s.taglineSep}>◆</span>
              Optimize <span className={s.taglineSep}>◆</span>
              Predict
            </p>

            {/* Rotating feature ticker */}
            <div className={s.featureTicker}>
              <span className={s.tickerLabel}>Now analyzing:</span>
              <div className={s.tickerTrack}>
                <span className={`${s.tickerItem} ${exiting ? s.tickerOut : s.tickerIn}`}>
                  {FEATURES[featureIdx].icon} {FEATURES[featureIdx].label}
                </span>
              </div>
            </div>

            <p className={s.desc}>
              A holographic-grade financial intelligence platform that unifies your loans,
              budgets, investments, and risk profile — powered by adaptive AI that learns
              your financial behavior in real time.
            </p>

            {/* ✅ CTA now opens Auth Modal */}
            <div className={s.ctas}>
              <button
                className={s.btnPrimary}
                onClick={() => setShowAuth(true)}
              >
                Launch Financial Scan →
              </button>

              <button
                className={s.btnSecondary}
                onClick={() => setShowAuth(true)}
              >
                Explore Platform
              </button>
            </div>

            <div className={s.proof}>
              <div className={s.proofStat}>
                <span className={s.proofNum}>50K+</span>
                <span className={s.proofLabel}>Active Users</span>
              </div>

              <div className={s.proofDiv} />

              <div className={s.proofStat}>
                <span className={s.proofNum}>₹2.4Cr</span>
                <span className={s.proofLabel}>Avg Wealth Grown</span>
              </div>

              <div className={s.proofDiv} />

              <div className={s.proofStat}>
                <span className={s.proofNum}>99.9%</span>
                <span className={s.proofLabel}>Uptime SLA</span>
              </div>
            </div>

          </div>

          {/* ════ RIGHT — Video Frame ════ */}
          <div className={s.videoSide}>
            <VideoFrame />
          </div>

        </div>
      </section>

      {/* ✅ Auth Modal Rendered Outside Section */}
      {showAuth && (
        <AuthModal
          onClose={() => setShowAuth(false)}
          onSuccess={() => {
            setShowAuth(false)
            onNavigate && onNavigate('chat')
          }}
        />
      )}
    </>
  )
}
