import s from './TrustSection.module.css'

const PILLARS = [
  {
    icon: '🔒',
    title: '256-bit AES Encryption',
    desc: 'All financial data encrypted at rest and in transit. Zero-knowledge architecture ensures we never see your credentials.',
  },
  {
    icon: '🛡',
    title: 'RBI & SEBI Compliant',
    desc: 'Fully compliant with Indian financial regulations. Regular third-party security audits and penetration testing.',
  },
  {
    icon: '◈',
    title: 'AI with Zero Data Leakage',
    desc: 'Your financial patterns train only your model. Federated learning ensures insights without ever sharing raw data.',
  },
]

const BADGES = [
  { icon: '✓', label: 'ISO 27001 Certified' },
  { icon: '✓', label: 'SOC 2 Type II' },
  { icon: '✓', label: 'GDPR Ready' },
  { icon: '✓', label: 'RBI Compliant' },
  { icon: '✓', label: '99.9% SLA Uptime' },
  { icon: '✓', label: 'MFA Enforced' },
]

export default function TrustSection() {
  return (
    <section className={s.section}>
      <div className={s.glow} />

      <div className={s.header}>
        <span className={s.eyebrow}>Security &amp; Compliance</span>
        <h2 className={s.title}>Enterprise-Grade Protection</h2>
        <p className={s.subtitle}>
          Your financial data is guarded by the same security standards
          used by global tier-1 banking institutions.
        </p>
      </div>

      <div className={s.grid}>
        {PILLARS.map((p, i) => (
          <div key={i} className={s.card}>
            <span className={s.iconBig}>{p.icon}</span>
            <div className={s.cardTitle}>{p.title}</div>
            <div className={s.cardDesc}>{p.desc}</div>
          </div>
        ))}
      </div>

      <div className={s.badges}>
        {BADGES.map((b, i) => (
          <div key={i} className={s.badge}>
            <span className={s.badgeIcon}>{b.icon}</span>
            {b.label}
          </div>
        ))}
      </div>
    </section>
  )
}
