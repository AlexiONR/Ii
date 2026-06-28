import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

function Navigation({ isDarkMode, toggleDarkMode }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">🛡️</span>
          <span className="brand-text">Cybersecurity Scanner</span>
        </Link>

        <div className="nav-menu">
          <Link to="/" className="nav-link">
            Dashboard
          </Link>
          <Link to="/scan-url" className="nav-link">
            Scan URL
          </Link>
          <Link to="/scan-file" className="nav-link">
            Scan File
          </Link>
          <Link to="/history" className="nav-link">
            History
          </Link>
          <Link to="/threat-database" className="nav-link">
            Threats
          </Link>
          <Link to="/alerts" className="nav-link">
            Alerts
          </Link>
        </div>

        <button className="dark-mode-toggle" onClick={toggleDarkMode}>
          {isDarkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </nav>
  );
}

export default Navigation;
