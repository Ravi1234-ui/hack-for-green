import s from './CTASection.module.css'

export default function CTASection({ onNavigate }) {
  return (
    <section className={s.section}>
      <div className={s.grid} />
      <div className={s.glowA} />

      <div className={s.content}>
        <span className={s.eyebrow}>Begin Your Financial Transformation</span>

        <h2 className={s.title}>
          Take Strategic Command<br />
          of Your{' '}
          <span className={s.accent}>Financial Future</span>
        </h2>

        <p className={s.desc}>
          Join 50,000+ users who have replaced financial anxiety with
          data-backed confidence. Full platform access, zero commitment.
        </p>

        <div className={s.ctas}>
          <button className={s.btnPrimary} onClick={() => onNavigate && onNavigate('dashboard')}>
            Launch Free Dashboard →
          </button>
          <button className={s.btnSecondary} onClick={() => onNavigate && onNavigate('dashboard')}>
            View Live Demo
          </button>
        </div>

        <p className={s.note}>
          Free forever · No credit card · Export anytime · Cancel never needed
        </p>
      </div>
    </section>
  )
}
