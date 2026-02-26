// src/components/auth/AuthModal.jsx
import { useState, useEffect, useCallback } from 'react'
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  sendPasswordResetEmail,
  updateProfile,
} from 'firebase/auth'
import { auth, provider } from '../../firebase/config.js'
import s from './AuthModal.module.css'

/* ── Google SVG ── */
const GoogleIcon = () => (
  <svg className={s.googleIcon} viewBox="0 0 24 24">
    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
  </svg>
)

function friendlyError(code) {
  const MAP = {
    'auth/user-not-found':         'No account found with this email.',
    'auth/wrong-password':         'Incorrect password. Please try again.',
    'auth/invalid-credential':     'Invalid email or password.',
    'auth/email-already-in-use':   'This email is already registered.',
    'auth/invalid-email':          'Please enter a valid email address.',
    'auth/weak-password':          'Password must be at least 6 characters.',
    'auth/too-many-requests':      'Too many attempts. Please wait a moment.',
    'auth/network-request-failed': 'Network error. Check your connection.',
    'auth/popup-blocked':          'Popup blocked — please allow popups for this site.',
    'auth/popup-closed-by-user':   null, // silent
  }
  return MAP[code] || 'Something went wrong. Please try again.'
}

export default function AuthModal({ onClose, onSuccess, defaultTab = 'login' }) {
  const [view,        setView]        = useState('auth')     // 'auth' | 'forgot' | 'success'
  const [tab,         setTab]         = useState(defaultTab) // 'login' | 'signup'
  const [name,        setName]        = useState('')
  const [email,       setEmail]       = useState('')
  const [password,    setPassword]    = useState('')
  const [showPass,    setShowPass]    = useState(false)
  const [error,       setError]       = useState('')
  const [loading,     setLoading]     = useState(false)
  const [resetSent,   setResetSent]   = useState(false)

  // Lock body scroll
  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = '' }
  }, [])

  // Escape key closes
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const resetFields = () => {
    setName(''); setEmail(''); setPassword('')
    setError(''); setShowPass(false)
  }

  const switchTab = (t) => { setTab(t); resetFields() }

  /* ── Email / Password submit ── */
  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (tab === 'signup' && !name.trim()) return setError('Full name is required.')
    if (!email.includes('@'))            return setError('Enter a valid email address.')
    if (password.length < 6)            return setError('Password must be at least 6 characters.')

    setLoading(true)
    try {
      if (tab === 'login') {
        await signInWithEmailAndPassword(auth, email, password)
      } else {
        const cred = await createUserWithEmailAndPassword(auth, email, password)
        await updateProfile(cred.user, { displayName: name.trim() })
      }
      setView('success')
      setTimeout(() => onSuccess?.(), 1400)
    } catch (err) {
      const msg = friendlyError(err.code)
      if (msg) setError(msg)
    } finally {
      setLoading(false)
    }
  }

  /* ── Google ── */
  const handleGoogle = async () => {
    setError('')
    setLoading(true)
    try {
      await signInWithPopup(auth, provider)
      setView('success')
      setTimeout(() => onSuccess?.(), 1400)
    } catch (err) {
      const msg = friendlyError(err.code)
      if (msg) setError(msg)
    } finally {
      setLoading(false)
    }
  }

  /* ── Password reset ── */
  const handleReset = async (e) => {
    e.preventDefault()
    setError('')
    if (!email.includes('@')) return setError('Enter a valid email address.')
    setLoading(true)
    try {
      await sendPasswordResetEmail(auth, email)
      setResetSent(true)
    } catch (err) {
      const msg = friendlyError(err.code)
      if (msg) setError(msg)
    } finally {
      setLoading(false)
    }
  }

  /* ─────────────────────────────
     RENDER — Success
  ───────────────────────────── */
  const renderSuccess = () => (
    <div className={s.successBox}>
      <div className={s.successRing}>✓</div>
      <div className={s.successTitle}>Access Granted</div>
      <div className={s.successSub}>
        Redirecting you to your<br />AI financial dashboard…
      </div>
    </div>
  )

  /* ─────────────────────────────
     RENDER — Forgot Password
  ───────────────────────────── */
  const renderForgot = () => (
    <div className={s.forgotView}>
      <button className={s.backBtn} onClick={() => { setView('auth'); setResetSent(false); setError('') }}>
        ← Back to login
      </button>

      {resetSent ? (
        <div className={s.successBox}>
          <div className={s.successRing}>✉</div>
          <div className={s.successTitle}>Email Sent</div>
          <div className={s.successSub}>Check your inbox for the password reset link.</div>
        </div>
      ) : (
        <>
          <h2 className={s.heading}>Reset <span className={s.headingAccent}>Password</span></h2>
          <p className={s.subheading}>Enter your email and we'll send a secure reset link.</p>

          {error && (
            <div className={s.errorMsg}>
              <span className={s.errorIcon}>⚠</span>{error}
            </div>
          )}

          <form className={s.form} onSubmit={handleReset} noValidate>
            <div className={s.fieldGroup}>
              <label className={s.label}>Email Address</label>
              <div className={s.inputWrap}>
                <span className={s.inputIcon}>✉</span>
                <input
                  className={s.input}
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  autoFocus
                  required
                />
              </div>
            </div>
            <button className={s.submitBtn} type="submit" disabled={loading}>
              <span className={s.btnInner}>
                {loading ? <><span className={s.spinner} /> Sending…</> : 'Send Reset Link →'}
              </span>
            </button>
          </form>
        </>
      )}
    </div>
  )

  /* ─────────────────────────────
     RENDER — Main Auth
  ───────────────────────────── */
  const renderAuth = () => (
    <>
      {/* Status */}
      <div className={s.statusRow}>
        <span className={s.statusDot} />
        <span className={s.statusLabel}>Secure · 256-bit encrypted</span>
      </div>

      {/* Heading */}
      <h2 className={s.heading}>
        {tab === 'login'
          ? <><span className={s.headingAccent}>Welcome</span> Back</>
          : <>Create <span className={s.headingAccent}>Account</span></>
        }
      </h2>
      <p className={s.subheading}>
        {tab === 'login'
          ? 'Sign in to access your AI financial dashboard.'
          : 'Join 50,000+ users optimizing their finances with AI.'}
      </p>

      {/* Tabs */}
      <div className={s.tabs}>
        <button className={`${s.tab} ${tab === 'login'  ? s.tabActive : ''}`} onClick={() => switchTab('login')}>
          Login
        </button>
        <button className={`${s.tab} ${tab === 'signup' ? s.tabActive : ''}`} onClick={() => switchTab('signup')}>
          Sign Up
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className={s.errorMsg}>
          <span className={s.errorIcon}>⚠</span>{error}
        </div>
      )}

      {/* Form */}
      <form className={s.form} onSubmit={handleSubmit} noValidate>
        {tab === 'signup' && (
          <div className={s.fieldGroup}>
            <label className={s.label}>Full Name</label>
            <div className={s.inputWrap}>
              <span className={s.inputIcon}>◈</span>
              <input
                className={`${s.input} ${error && !name.trim() ? s.inputErr : ''}`}
                type="text"
                placeholder="Your full name"
                value={name}
                onChange={e => setName(e.target.value)}
                autoComplete="name"
                autoFocus
              />
            </div>
          </div>
        )}

        <div className={s.fieldGroup}>
          <label className={s.label}>Email Address</label>
          <div className={s.inputWrap}>
            <span className={s.inputIcon}>✉</span>
            <input
              className={s.input}
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
              autoComplete="email"
              autoFocus={tab === 'login'}
            />
          </div>
        </div>

        <div className={s.fieldGroup}>
          <label className={s.label}>Password</label>
          <div className={s.inputWrap}>
            <span className={s.inputIcon}>⬡</span>
            <input
              className={s.input}
              type={showPass ? 'text' : 'password'}
              placeholder={tab === 'signup' ? 'Min 6 characters' : '••••••••'}
              value={password}
              onChange={e => setPassword(e.target.value)}
              autoComplete={tab === 'login' ? 'current-password' : 'new-password'}
              style={{ paddingRight: '40px' }}
            />
            <button
              type="button"
              className={s.eyeBtn}
              onClick={() => setShowPass(p => !p)}
              aria-label={showPass ? 'Hide password' : 'Show password'}
            >
              {showPass ? '◎' : '◉'}
            </button>
          </div>
        </div>

        {tab === 'login' && (
          <div className={s.forgotRow}>
            <button
              type="button"
              className={s.forgotBtn}
              onClick={() => { setView('forgot'); setError('') }}
            >
              Forgot password?
            </button>
          </div>
        )}

        <button className={s.submitBtn} type="submit" disabled={loading}>
          <span className={s.btnInner}>
            {loading
              ? <><span className={s.spinner} /> Processing…</>
              : tab === 'login' ? 'Launch Dashboard →' : 'Create Account →'
            }
          </span>
        </button>
      </form>

      <div className={s.divider}>
        <div className={s.divLine} /><span className={s.divText}>or</span><div className={s.divLine} />
      </div>

      <button className={s.googleBtn} onClick={handleGoogle} disabled={loading} type="button">
        <GoogleIcon />
        Continue with Google
      </button>

      <p className={s.footNote}>
        Protected by Firebase Auth · No credit card required
      </p>
    </>
  )

  return (
    <div className={s.backdrop}>
      {/* Decorative rings */}
      <div className={s.backdropRingA} />
      <div className={s.backdropRingB} />

      {/* Click-outside closes */}
      <div className={s.closeArea} onClick={onClose} />

      <div className={s.modal} role="dialog" aria-modal="true">
        {/* Decorative elements */}
        <div className={s.sweep} />
        <div className={s.corner + ' ' + s.cornerTL} />
        <div className={s.corner + ' ' + s.cornerTR} />
        <div className={s.corner + ' ' + s.cornerBL} />
        <div className={s.corner + ' ' + s.cornerBR} />

        {/* Close button */}
        {view !== 'success' && (
          <button className={s.closeBtn} onClick={onClose} aria-label="Close">✕</button>
        )}

        {/* Brand */}
        <div className={s.brand}>
          <div className={s.brandMark}>FI</div>
          <div>
            <span className={s.brandName}>FinIntel</span>
            <span className={s.brandSub}>AI Intelligence Platform</span>
          </div>
        </div>

        <div className={s.content}>
          {view === 'success' && renderSuccess()}
          {view === 'forgot'  && renderForgot()}
          {view === 'auth'    && renderAuth()}
        </div>
      </div>
    </div>
  )
}
