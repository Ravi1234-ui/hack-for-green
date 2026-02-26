// src/components/chat/InsightPanel.jsx
import s from '../../styles/components/chat.module.css'

const MONTHS = ['Aug','Sep','Oct','Nov','Dec','Jan']

function sparkPath(data, w, h) {
  const max = Math.max(...data)
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w
    const y = h - (v / max) * (h * 0.88)
    return `${x},${y}`
  })
  return 'M ' + pts.join(' L ')
}

export default function InsightPanel({ metrics, advisory, open }) {
  const w = 240, h = 80
  const income  = [68, 72, 75, 74, 80, 83]
  const expense = [50, 54, 48, 46, 56, 52]
  const inPath  = sparkPath(income,  w, h)
  const exPath  = sparkPath(expense, w, h)
  const inArea  = inPath  + ` L ${w},${h} L 0,${h} Z`
  const exArea  = exPath  + ` L ${w},${h} L 0,${h} Z`

  const METRICS = metrics || [
    { label: 'Savings Rate',  value: '28%',   sub: '↑ 3.2% vs last month', color: 'green', fill: 28, bg: 'var(--green-neon)' },
    { label: 'EMI Load',      value: '34%',   sub: 'Income ratio · safe',   color: 'gold',  fill: 34, bg: 'var(--gold)' },
    { label: 'Risk Score',    value: '62',    sub: 'Moderate exposure',     color: 'gold',  fill: 62, bg: 'var(--gold)' },
    { label: 'Expense Ratio', value: '58%',   sub: 'of monthly income',     color: 'cyan',  fill: 58, bg: 'var(--cyan)' },
  ]

  const ADVISORY = advisory || []

  return (
    <aside className={`${s.insightPanel} ${open ? s.insightOpen : ''}`}>
      <div className={s.insightTitle}>Financial Overview</div>

      {METRICS.map((m, i) => (
        <div key={i} className={s.metricCard}>
          <div className={s.metricLabel}>{m.label}</div>
          <div className={`${s.metricValue} ${s[m.color]}`}>{m.value}</div>
          <div className={s.metricSub}>{m.sub}</div>
          <div className={s.metricBar}>
            <div
              className={s.metricBarFill}
              style={{
                '--fw': `${m.fill}%`,
                width: `${m.fill}%`,
                background: m.bg,
                boxShadow: `0 0 6px ${m.bg}66`,
              }}
            />
          </div>
        </div>
      ))}

      {/* Sparkline chart */}
      <div className={s.chartBox}>
        <div className={s.chartBoxTitle}>
          Cash Flow
          <div className={s.chartLegend}>
            <span className={s.legendItem}>
              <span className={s.legendDot} style={{ background: '#00f0ff' }} />Income
            </span>
            <span className={s.legendItem}>
              <span className={s.legendDot} style={{ background: '#ff4d6d' }} />Expense
            </span>
          </div>
        </div>
        <div className={s.chartArea}>
          <svg viewBox={`0 0 ${w} ${h}`} className={s.chartSvg} preserveAspectRatio="none">
            <defs>
              <linearGradient id="igChat" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   stopColor="#00f0ff" stopOpacity="0.18" />
                <stop offset="100%" stopColor="#00f0ff" stopOpacity="0" />
              </linearGradient>
              <linearGradient id="egChat" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"   stopColor="#ff4d6d" stopOpacity="0.14" />
                <stop offset="100%" stopColor="#ff4d6d" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path d={inArea}  fill="url(#igChat)" className={s.chartFill} />
            <path d={exArea}  fill="url(#egChat)" className={s.chartFill} />
            <path d={inPath}  stroke="#00f0ff" className={s.chartPath} />
            <path d={exPath}  stroke="#ff4d6d" className={s.chartPath} />
          </svg>
        </div>
        <div style={{ display:'flex', justifyContent:'space-between', marginTop:'6px' }}>
          {MONTHS.map(m => (
            <span key={m} style={{ fontFamily:'var(--font-mono)', fontSize:'8px', color:'var(--t-25)' }}>{m}</span>
          ))}
        </div>
      </div>

      {/* Advisory insight cards (populated by AI mode) */}
      {ADVISORY.map((adv, i) => (
        <div key={i} className={s.advisoryCard} style={{ animationDelay: `${i * 0.08}s` }}>
          <div className={s.advisoryTag}>{adv.tag}</div>
          <div className={s.advisoryText}>{adv.text}</div>
        </div>
      ))}
    </aside>
  )
}
