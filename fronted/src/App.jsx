// src/App.jsx
// ─────────────────────────────────────────────────────────────────
//  Root router for FinIntel platform.
//
//  Pages:
//    landing    → public landing page (auth modal opens on CTA click)
//    chat       → AI chat interface (requires login)
//    dashboard  → alias for chat (same component)
//
//  Auth flow:
//    - Landing page is always public
//    - AuthModal opens from Hero CTAs / navbar buttons
//    - On successful login → navigates to 'chat'
//    - If logged-in user tries landing → redirect link to chat available
//    - If logged-out user tries to access chat directly → redirected to landing
//    - Logout from ChatInterface sidebar → returns to landing
//
//  Firebase:
//    - AuthProvider wraps everything in main.jsx
//    - useAuth() gives { user, loading, logout }
//    - loading state prevents flash of wrong page on refresh
// ─────────────────────────────────────────────────────────────────

import { useState, useEffect } from 'react'
import { useAuth }       from './context/AuthContext.jsx'
import Landing           from './pages/Landing.jsx'
import ChatInterface     from './pages/ChatInterface.jsx'

// ── Full-screen loading spinner shown while Firebase
//    resolves the auth state on initial page load ──
function LoadingScreen() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#030d1a',
      gap: '20px',
    }}>
      {/* Animated ring */}
      <div style={{
        width: '44px',
        height: '44px',
        borderRadius: '50%',
        border: '2px solid rgba(0,240,255,0.12)',
        borderTopColor: '#00f0ff',
        animation: 'spin 0.7s linear infinite',
      }} />
      {/* Inline keyframe for the spinner */}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      <span style={{
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: '10px',
        letterSpacing: '0.22em',
        textTransform: 'uppercase',
        color: 'rgba(0,240,255,0.4)',
      }}>
        Initializing…
      </span>
    </div>
  )
}

export default function App() {
  const { user, loading } = useAuth()
  const [page, setPage]   = useState('landing')

  // ── When Firebase resolves auth state:
  //    If user is already logged in on refresh → go to chat.
  //    If not logged in → stay on landing.
  useEffect(() => {
    if (!loading) {
      if (user && page === 'landing') setPage('chat')
    }
  }, [loading, user])

  // ── Guard: if a logged-out user somehow navigates to chat,
  //    push them back to landing.
  useEffect(() => {
    if (!loading && !user && (page === 'chat' || page === 'dashboard')) {
      setPage('landing')
    }
  }, [user, loading, page])

  // ── Show loading screen while Firebase checks session
  if (loading) return <LoadingScreen />

  return (
    <div>
      {/* ── Public landing page ──
           AuthModal is managed inside Hero.jsx.
           onNavigate prop lets any section trigger page change. */}
      {page === 'landing' && (
        <Landing onNavigate={setPage} />
      )}

      {/* ── Protected chat interface ──
           Both 'chat' and 'dashboard' render ChatInterface.
           ChatInterface sidebar has a logout + back-to-home option. */}
      {(page === 'chat' || page === 'dashboard') && (
        <ChatInterface onNavigate={setPage} />
      )}
    </div>
  )
}
