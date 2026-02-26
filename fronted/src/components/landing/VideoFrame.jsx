import { useRef } from 'react'
import s from './VideoFrame.module.css'

export default function VideoFrame() {
  const wrapRef = useRef(null)

  const handleMouseMove = (e) => {
    const el = wrapRef.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const cx = rect.left + rect.width / 2
    const cy = rect.top + rect.height / 2
    const dx = (e.clientX - cx) / (rect.width / 2)
    const dy = (e.clientY - cy) / (rect.height / 2)
    el.style.transform = `perspective(1000px) rotateY(${dx * 4}deg) rotateX(${-dy * 3}deg) translateY(0px)`
  }

  const handleMouseLeave = () => {
    const el = wrapRef.current
    if (!el) return
    el.style.transform = 'perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(0px)'
  }

  return (
    <div className={s.outer}>
      {/* Corner bracket decorations */}
      <div className={`${s.corner} ${s.cornerTL}`} />
      <div className={`${s.corner} ${s.cornerTR}`} />
      <div className={`${s.corner} ${s.cornerBL}`} />
      <div className={`${s.corner} ${s.cornerBR}`} />

      {/* HUD top bar */}
      <div className={s.hudBar}>
        <div className={s.hudBarLeft}>
          <span className={s.hudDot} />
          <span className={s.hudDot} />
          <span className={s.hudDot} />
        </div>
        <span className={s.hudLabel}>FININTEL · LIVE ANALYSIS</span>
        <div className={s.hudBarRight}>
          <span className={s.statusPip} />
          <span className={s.statusText}>ACTIVE</span>
        </div>
      </div>

      {/* Main video frame */}
      <div
        className={s.frame}
        ref={wrapRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        {/* Outer glow ring */}
        <div className={s.glowRing} />

        {/* Glass container */}
        <div className={s.glass}>

          {/* Video */}
          <video
            className={s.video}
            src="/assets/finance-hologram.mp4"
            autoPlay
            muted
            loop
            playsInline
            preload="metadata"
          />

          {/* Dark gradient overlay */}
          <div className={s.overlay} />

          {/* Sweep light */}
          <div className={s.sweep} />

          {/* Scan line */}
          <div className={s.scanLine} />

          {/* HUD overlay elements */}
          <div className={s.hudOverlay}>
            {/* Top-left data badge */}
            <div className={s.dataBadge}>
              <span className={s.badgeLabel}>PORTFOLIO SCORE</span>
              <span className={s.badgeValue}>74 / 100</span>
            </div>

            {/* Bottom status bar */}
            <div className={s.bottomBar}>
              <div className={s.bottomStat}>
                <span className={s.bsVal}>+28%</span>
                <span className={s.bsKey}>Savings Rate</span>
              </div>
              <div className={s.bottomDivider} />
              <div className={s.bottomStat}>
                <span className={s.bsVal}>₹1.4L</span>
                <span className={s.bsKey}>Net Gain QTR</span>
              </div>
              <div className={s.bottomDivider} />
              <div className={s.bottomStat}>
                <span className={s.bsVal}>34%</span>
                <span className={s.bsKey}>EMI Load</span>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Bottom label strip */}
      <div className={s.footerStrip}>
        <span className={s.footerMono}>AI ENGINE · REAL-TIME ANALYSIS ACTIVE</span>
        <span className={s.footerPing} />
      </div>
    </div>
  )
}
