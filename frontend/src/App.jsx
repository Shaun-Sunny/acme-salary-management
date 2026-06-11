import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import './App.css'
import Analytics from './pages/Analytics.jsx'
import Employees from './pages/Employees.jsx'

function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">ACME</span>
          <span className="brand-text">Salary Management</span>
        </div>

        <nav className="nav-links" aria-label="Primary">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Employees
          </NavLink>
          <NavLink to="/analytics" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            Analytics
          </NavLink>
        </nav>
      </header>

      <main className="app-content">
        <Routes>
          <Route path="/" element={<Employees />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
