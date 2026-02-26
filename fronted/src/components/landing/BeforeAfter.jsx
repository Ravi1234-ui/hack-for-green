import s from './BeforeAfter.module.css'

const BEFORE = [
  'Finances scattered across 5+ disconnected apps',
  'Loan impact on cash flow is pure guesswork',
  'Goals set without data-backed timelines',
  'Reactive to financial events, never predictive',
  'No unified view of risk exposure',
  'Manual budget tracking lost within weeks',
]

const AFTER = [
  'Unified financial intelligence in one dashboard',
  'Precise EMI modeling with prepayment scenarios',
  'Goal roadmaps with adaptive monthly SIP plans',
  'AI proactively alerts and models future events',
  'Real-time risk score with mitigation playbooks',
  'Self-updating budgets powered by AI behavior engine',
]

const METRICS = [
  { val: '3.2×', label: 'Faster Financial Decisions' },
  { val: '₹1.8L', label: 'Avg Annual Savings Added' },
  { val: '94%', label: 'Users Achieved Goals Faster' },
  { val: '18 min', label: 'Weekly Review Time' },
]

export default function BeforeAfter() {
  return (
    <section className={s.section}>
      <div className={s.header}>
        <span className={s.eyebrow}>Transformation Impact</span>
        <h2 className={s.title}>The FinIntel Difference</h2>
      </div>

      <div className={s.layout}>
        <div className={s.panel}>
          <div className={`${s.panelHead} ${s.beforeHead}`}>
            <span>Before FinIntel</span>
            <span className={s.headBadge}>⊗</span>
          </div>
          {BEFORE.map((text, i) => (
            <div key={i} className={s.item}>
              <div className={`${s.itemBullet} ${s.beforeBullet}`} />
              <div className={s.itemText}>{text}</div>
            </div>
          ))}
        </div>

        <div className={s.divider}>
          <div className={s.divLine} />
          <div className={s.divBadge}>VS</div>
          <div className={s.divLine} />
        </div>

        <div className={s.panel}>
          <div className={`${s.panelHead} ${s.afterHead}`}>
            <span>After FinIntel</span>
            <span className={s.headBadge}>◉</span>
          </div>
          {AFTER.map((text, i) => (
            <div key={i} className={s.item}>
              <div className={`${s.itemBullet} ${s.afterBullet}`} />
              <div className={s.itemText}>{text}</div>
            </div>
          ))}
        </div>
      </div>

      <div className={s.metrics}>
        {METRICS.map((m, i) => (
          <div key={i} className={s.metric}>
            <div className={s.metricVal}>{m.val}</div>
            <div className={s.metricLabel}>{m.label}</div>
          </div>
        ))}
      </div>
    </section>
  )
}
