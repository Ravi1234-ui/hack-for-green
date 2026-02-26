import Hero from '../components/landing/Hero.jsx'
import FeatureGrid from '../components/landing/FeatureGrid.jsx'
import BeforeAfter from '../components/landing/BeforeAfter.jsx'
import TrustSection from '../components/landing/TrustSection.jsx'
import CTASection from '../components/landing/CTASection.jsx'
import s from './Landing.module.css'

export default function Landing({ onNavigate }) {
  return (
    <div className={s.page}>
      <Hero onNavigate={onNavigate} />
      <FeatureGrid />
      <BeforeAfter />
      <TrustSection />
      <CTASection onNavigate={onNavigate} />

      <footer className={s.footer}>
        <span className={s.footerBrand}>FinIntel</span>
        <span className={s.footerMid}>© 2026 Financial Intelligence Platform · All rights reserved</span>
        <span className={s.footerRight}>Built with React + CSS Modules</span>
      </footer>
    </div>
  )
}
