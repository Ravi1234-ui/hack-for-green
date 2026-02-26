// src/components/chat/Sidebar.jsx
import s from '../../styles/components/chat.module.css'

const NAV = [
  { icon: '◈', label: 'Dashboard',   id: 'dashboard' },
  { icon: '⬡', label: 'Loans',       id: 'loans',      badge: '2' },
  { icon: '◎', label: 'Goals',       id: 'goals' },
  { icon: '▦', label: 'Budget',      id: 'budget' },
  { icon: '∑', label: 'Investments', id: 'investments', badge: 'New' },
  { icon: '⊕', label: 'Risk Report', id: 'risk' },
  { icon: '⚙', label: 'Settings',    id: 'settings' },
]

export default function Sidebar({ active, onSelect, open, onNavigate }) {
  return (
    <aside className={`${s.sidebar} ${open ? s.sidebarOpen : ''}`}>
      <div className={s.sidebarLogo}>
        <div className={s.sidebarMark}>FI</div>
        <div>
          <span className={s.sidebarBrandName}>FinIntel</span>
          <span className={s.sidebarBrandSub}>AI Platform</span>
        </div>
      </div>

      <nav className={s.navSection}>
        <div className={s.navLabel}>Navigation</div>
        {NAV.map(item => (
          <div
            key={item.id}
            className={`${s.navItem} ${active === item.id ? s.navActive : ''}`}
            onClick={() => onSelect(item.id)}
          >
            <span className={s.navIcon}>{item.icon}</span>
            <span>{item.label}</span>
            {item.badge && <span className={s.navBadge}>{item.badge}</span>}
          </div>
        ))}
      </nav>

      <div className={s.sidebarFooter}>
        <div className={s.userCard}>
          <div className={s.avatar}>AK</div>
          <div>
            <div className={s.userName}>Arjun Kumar</div>
            <div className={s.userRole}>Pro Plan</div>
          </div>
        </div>
        <div className={s.navItem} onClick={() => onNavigate('landing')}>
          <span className={s.navIcon}>←</span>
          <span>Back to Home</span>
        </div>
      </div>
    </aside>
  )
}
