'use client';
import { useState } from 'react';
import Link from 'next/link';

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside style={{
      width: isCollapsed ? '64px' : '240px',
      transition: 'width var(--transition-normal)',
      backgroundColor: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border-color)',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }}>
      <div className="flex items-center justify-between" style={{ padding: '16px', borderBottom: '1px solid var(--border-color)', height: '64px' }}>
        {!isCollapsed && <span className="font-bold text-accent" style={{ fontSize: '1.25rem' }}>AgentPassport</span>}
        <button onClick={() => setIsCollapsed(!isCollapsed)} style={{ color: 'var(--text-secondary)' }}>
          {isCollapsed ? '►' : '◄'}
        </button>
      </div>

      <nav style={{ flex: 1, padding: '16px 8px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        <NavItem href="#" icon="⌂" label="Dashboard" isCollapsed={isCollapsed} isActive />
        <NavItem href="#" icon="◷" label="Analytics" isCollapsed={isCollapsed} />
        <NavItem href="#" icon="⚙" label="Settings" isCollapsed={isCollapsed} />
      </nav>

      <div style={{ padding: '16px', borderTop: '1px solid var(--border-color)' }}>
        <div className="flex items-center gap-2">
          <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--accent-primary)' }} />
          {!isCollapsed && (
            <div className="flex flex-col">
              <span className="text-sm font-medium">Aryan</span>
              <span className="text-xs text-secondary">Admin</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}

function NavItem({ href, icon, label, isCollapsed, isActive = false }: { href: string, icon: string, label: string, isCollapsed: boolean, isActive?: boolean }) {
  return (
    <Link href={href} className="flex items-center" style={{
      padding: '8px',
      borderRadius: 'var(--radius-md)',
      background: isActive ? 'var(--bg-tertiary)' : 'transparent',
      color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
      gap: '12px',
      textDecoration: 'none',
      transition: 'background var(--transition-fast)'
    }}
    onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = 'var(--bg-tertiary)'; }}
    onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
    >
      <span style={{ fontSize: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'center', width: '24px' }}>{icon}</span>
      {!isCollapsed && <span className="text-sm font-medium">{label}</span>}
    </Link>
  );
}
