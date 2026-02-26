import s from './FeatureGrid.module.css'

const CARDS = [
  {
    icon: '⬡',
    num: '01',
    title: 'Intelligent Loan Planning',
    desc: 'Dynamic EMI forecasting with real-time prepayment simulation, optimal tenure analysis, and rate comparison engine.',
    tag: 'Loans · EMI',
    accent: '#00f0ff',
    bg: 'rgba(0,240,255,0.08)',
  },
  {
    icon: '◈',
    num: '02',
    title: 'AI Budget Optimization',
    desc: 'Behavioral spend categorization with zero-sum budgeting, anomaly detection, and adaptive reallocation engine.',
    tag: 'Budget · AI',
    accent: '#00ffb3',
    bg: 'rgba(0,255,179,0.08)',
  },
  {
    icon: '◎',
    num: '03',
    title: 'Smart Goal Engineering',
    desc: 'Reverse-engineered savings milestones with SIP alignment, inflation modeling, and life-event scenario paths.',
    tag: 'Goals · SIP',
    accent: '#ffc940',
    bg: 'rgba(255,201,64,0.08)',
  },
  {
    icon: '∑',
    num: '04',
    title: 'Risk Intelligence Engine',
    desc: 'Multi-factor portfolio stress testing against macro events, with personal risk threshold calibration and alerts.',
    tag: 'Risk · Portfolio',
    accent: '#ff4d6d',
    bg: 'rgba(255,77,109,0.08)',
  },
  {
    icon: '≈',
    num: '05',
    title: 'Financial Memory System',
    desc: '60-month longitudinal pattern recognition with contextual recall, predictive nudges, and behavioral insight.',
    tag: 'Memory · AI',
    accent: '#8b5cf6',
    bg: 'rgba(139,92,246,0.08)',
  },
  {
    icon: '⊕',
    num: '06',
    title: 'Scenario Simulation',
    desc: 'Monte Carlo projections for life events — job switch, home purchase, early retirement — with probability scoring.',
    tag: 'Simulation · Monte Carlo',
    accent: '#ff8c42',
    bg: 'rgba(255,140,66,0.08)',
  },
]

export default function FeatureGrid() {
  return (
    <section className={s.section}>
      <div className={s.header}>
        <span className={s.eyebrow}>Core Intelligence Modules</span>
        <h2 className={s.title}>
          Six Engines of{' '}
          <span className={s.titleAccent}>Financial Clarity</span>
        </h2>
        <p className={s.subtitle}>
          Purpose-built intelligence modules that operate in concert,
          turning your raw financial data into strategic, actionable precision.
        </p>
      </div>

      <div className={s.grid}>
        {CARDS.map((c, i) => (
          <div
            key={i}
            className={s.card}
            style={{
              '--c': c.accent + '88',
              animationDelay: `${i * 0.07}s`,
            }}
          >
            <div
              className={s.cardGlow}
              style={{ background: `radial-gradient(ellipse at 50% 0%, ${c.accent}20, transparent 70%)` }}
            />

            <div
              className={s.iconWrap}
              style={{ background: c.bg, border: `1px solid ${c.accent}30`, color: c.accent }}
            >
              {c.icon}
              <span className={s.num}>{c.num}</span>
            </div>

            <div className={s.cardTitle}>{c.title}</div>
            <div className={s.cardDesc}>{c.desc}</div>

            <div
              className={s.cardTag}
              style={{
                background: c.bg,
                border: `1px solid ${c.accent}30`,
                color: c.accent,
              }}
            >
              {c.tag}
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
