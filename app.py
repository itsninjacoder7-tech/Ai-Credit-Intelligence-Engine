<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LoanSahayak — Smart Loan Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --gold: #C9A84C;
  --gold-light: #E8C97A;
  --gold-dim: rgba(201,168,76,0.12);
  --gold-glow: rgba(201,168,76,0.25);
  --bg-deep: #060A12;
  --bg-surface: #0C1220;
  --bg-card: rgba(255,255,255,0.032);
  --bg-card-hover: rgba(255,255,255,0.055);
  --border: rgba(201,168,76,0.18);
  --border-bright: rgba(201,168,76,0.45);
  --text-primary: #EDE8DC;
  --text-secondary: #8A8070;
  --text-muted: #4A4440;
  --success: #2ECC71;
  --danger: #E74C3C;
  --blue: #4EA1FF;
  --sidebar-w: 280px;
}

html { scroll-behavior: smooth; }

body {
  background: var(--bg-deep);
  color: var(--text-primary);
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  min-height: 100vh;
  display: flex;
}

/* ─── NOISE TEXTURE ─── */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
  pointer-events: none; z-index: 0; opacity: 0.5;
}

/* ─── SIDEBAR ─── */
.sidebar {
  width: var(--sidebar-w);
  min-height: 100vh;
  background: #070B14;
  border-right: 1px solid var(--border);
  position: fixed; left: 0; top: 0; bottom: 0;
  display: flex; flex-direction: column;
  padding: 28px 24px;
  z-index: 10;
  overflow-y: auto;
}

.sidebar-logo {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}

.sidebar-logo-name {
  font-family: 'Playfair Display', serif;
  font-size: 22px; font-weight: 700;
  color: var(--text-primary);
}

.sidebar-logo-sub {
  font-size: 10px; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--text-muted);
  margin-top: 4px;
}

.sidebar-info {
  background: rgba(78,161,255,0.07);
  border: 1px solid rgba(78,161,255,0.18);
  border-radius: 12px;
  padding: 14px 16px;
  color: #9CCBFF;
  font-size: 13px; line-height: 1.7;
  margin-bottom: 20px;
}

.sidebar-stats-label {
  font-size: 10px; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 8px;
}

.sidebar-stats { font-size: 13px; color: var(--text-primary); line-height: 1.9; }
.sidebar-stats span { color: var(--gold); }

.sidebar-divider {
  border: none; border-top: 1px solid var(--border);
  margin: 20px 0;
}

.sidebar-author-name {
  font-family: 'Playfair Display', serif;
  font-size: 19px; font-weight: 600; color: var(--text-primary);
  margin-bottom: 2px;
}
.sidebar-author-title { font-size: 12px; color: var(--text-secondary); }

.sidebar-links {
  display: flex; gap: 10px; margin-top: 16px;
}

.sidebar-icon-btn {
  width: 40px; height: 40px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  text-decoration: none;
  transition: opacity 0.2s;
}

.sidebar-icon-btn:hover { opacity: 0.75; }

.sidebar-footer {
  margin-top: auto; padding-top: 20px;
  font-size: 11px; color: var(--text-muted);
  text-align: center; line-height: 1.5;
}

/* ─── MAIN CONTENT ─── */
.main {
  margin-left: var(--sidebar-w);
  flex: 1;
  padding: 40px 48px 80px;
  max-width: calc(100vw - var(--sidebar-w));
  position: relative; z-index: 1;
}

/* ─── WELCOME BANNER ─── */
.welcome-banner {
  padding: 14px 20px;
  border-radius: 12px;
  background: rgba(201,168,76,0.07);
  border: 1px solid rgba(201,168,76,0.25);
  color: var(--gold-light);
  font-size: 15px;
  margin-bottom: 32px;
}

/* ─── HERO ─── */
.hero {
  position: relative;
  text-align: center;
  padding: 72px 40px 64px;
  border-radius: 24px;
  border: 1px solid var(--border);
  background:
    radial-gradient(ellipse 90% 50% at 50% 0%, rgba(201,168,76,0.09) 0%, transparent 65%),
    linear-gradient(180deg, #0C1525 0%, #070B14 100%);
  overflow: hidden;
  margin-bottom: 48px;
}

.hero::after {
  content: '';
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 55%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

/* Decorative corner glows */
.hero::before {
  content: '';
  position: absolute; top: -80px; right: -80px;
  width: 300px; height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(201,168,76,0.06) 0%, transparent 70%);
  pointer-events: none;
}

.hero-badge {
  display: inline-block;
  padding: 6px 18px;
  border: 1px solid var(--border-bright);
  border-radius: 100px;
  font-size: 10px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--gold);
  background: var(--gold-dim);
  margin-bottom: 28px; font-weight: 600;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 60px; font-weight: 700;
  color: var(--text-primary);
  line-height: 1.05; letter-spacing: -1px;
  margin-bottom: 16px;
}

.hero-title span { color: var(--gold); }

.hero-sub {
  font-size: 16px; color: var(--text-secondary);
  font-weight: 300; letter-spacing: 0.3px;
  max-width: 480px; margin: 0 auto 36px;
  line-height: 1.75;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
  padding-top: 28px;
  border-top: 1px solid var(--border);
}

.hero-stat-val {
  font-family: 'Playfair Display', serif;
  font-size: 30px; font-weight: 600;
  color: var(--gold-light);
}

.hero-stat-label {
  font-size: 10px; letter-spacing: 2px;
  text-transform: uppercase; color: var(--text-muted);
  margin-top: 4px;
}

/* ─── SECTION HEADER ─── */
.section-header {
  display: flex; align-items: center; gap: 12px;
  margin: 40px 0 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.section-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: var(--gold-dim);
  border: 1px solid rgba(201,168,76,0.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px;
}

.section-title {
  font-family: 'Playfair Display', serif;
  font-size: 20px; font-weight: 600;
  color: var(--text-primary);
}

.section-desc {
  font-size: 10px; color: var(--text-muted);
  letter-spacing: 1.5px; text-transform: uppercase;
  margin-left: auto;
}

/* ─── FORM GRID ─── */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px 32px; }
.form-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px 32px; }

.field { display: flex; flex-direction: column; gap: 7px; }

label {
  font-size: 11px; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--text-secondary);
  font-weight: 500;
}

input[type="number"],
input[type="text"],
select {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text-primary);
  padding: 11px 14px;
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  -webkit-appearance: none;
}

input[type="number"]:focus,
input[type="text"]:focus,
select:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 3px var(--gold-dim);
}

select {
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath fill='%238A8070' d='M1 1l5 5 5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 14px center;
  padding-right: 36px;
}

select option { background: #0C1220; }

/* Range slider */
.slider-wrap { display: flex; flex-direction: column; gap: 7px; }

.slider-row { display: flex; align-items: center; gap: 14px; }

input[type="range"] {
  -webkit-appearance: none;
  flex: 1; height: 6px;
  border-radius: 3px;
  background: rgba(255,255,255,0.08);
  outline: none; cursor: pointer;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px; height: 18px;
  border-radius: 50%;
  background: var(--gold);
  border: 2px solid var(--bg-deep);
  box-shadow: 0 0 0 2px var(--gold);
  transition: box-shadow 0.15s;
}

input[type="range"]::-webkit-slider-thumb:hover {
  box-shadow: 0 0 0 4px var(--gold-dim);
}

.slider-val {
  font-family: 'DM Mono', monospace;
  font-size: 14px; font-weight: 500;
  color: var(--gold-light);
  min-width: 52px; text-align: right;
}

/* ─── BUTTON ─── */
.btn-primary {
  background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%);
  color: #060A12;
  border: none;
  border-radius: 12px;
  height: 54px;
  font-size: 13px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.25s ease;
  box-shadow: 0 4px 24px rgba(201,168,76,0.2);
  padding: 0 36px;
  position: relative; overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute; inset: 0;
  background: rgba(255,255,255,0);
  transition: background 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 36px rgba(201,168,76,0.38);
}

.btn-primary:hover::before { background: rgba(255,255,255,0.07); }
.btn-primary:active { transform: translateY(0); }

/* ─── METRICS ─── */
.metrics-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0; }

.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 22px;
  transition: border-color 0.2s;
}

.metric-card:hover { border-color: var(--border-bright); }

.metric-label {
  font-size: 10px; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--text-muted);
  margin-bottom: 8px;
}

.metric-value {
  font-family: 'Playfair Display', serif;
  font-size: 26px; font-weight: 600;
  color: var(--text-primary);
}

/* ─── PROGRESS BAR ─── */
.progress-wrap { margin: 20px 0; }

.progress-label {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 8px; font-size: 13px; color: var(--text-secondary);
}

.progress-label strong { color: var(--gold-light); font-size: 15px; }

.progress-track {
  height: 8px;
  background: rgba(255,255,255,0.07);
  border-radius: 100px; overflow: hidden;
}

.progress-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--gold), var(--gold-light));
  transition: width 0.8s cubic-bezier(.4,0,.2,1);
}

/* ─── RESULT CARDS ─── */
.result-approved {
  padding: 32px 36px; border-radius: 20px;
  border: 1px solid rgba(46,204,113,0.28);
  background:
    radial-gradient(ellipse at top, rgba(46,204,113,0.07) 0%, transparent 70%),
    rgba(255,255,255,0.02);
  text-align: center; margin: 20px 0;
}

.result-rejected {
  padding: 32px 36px; border-radius: 20px;
  border: 1px solid rgba(231,76,60,0.28);
  background:
    radial-gradient(ellipse at top, rgba(231,76,60,0.07) 0%, transparent 70%),
    rgba(255,255,255,0.02);
  text-align: center; margin: 20px 0;
}

.result-icon { font-size: 48px; margin-bottom: 12px; }

.result-label {
  font-family: 'Playfair Display', serif;
  font-size: 34px; font-weight: 700; margin-bottom: 8px;
}

.result-sub { font-size: 14px; color: var(--text-secondary); letter-spacing: 0.5px; }

.result-conf {
  display: inline-block; margin-top: 16px;
  padding: 6px 22px; border-radius: 100px;
  font-size: 13px; font-weight: 600; letter-spacing: 1px;
}

.conf-approved {
  background: rgba(46,204,113,0.12); color: #2ECC71;
  border: 1px solid rgba(46,204,113,0.28);
}

.conf-rejected {
  background: rgba(231,76,60,0.12); color: #E74C3C;
  border: 1px solid rgba(231,76,60,0.28);
}

/* ─── ALERT BOXES ─── */
.alert {
  padding: 14px 18px; border-radius: 12px;
  font-size: 14px; line-height: 1.6; margin: 12px 0;
  border-left: 3px solid;
}

.alert-warning {
  background: rgba(234,179,8,0.08);
  border-color: #EAB308; color: #FDE047;
}

.alert-info {
  background: rgba(59,130,246,0.08);
  border-color: #3B82F6; color: #93C5FD;
}

.alert-success {
  background: rgba(46,204,113,0.08);
  border-color: #2ECC71; color: #86EFAC;
}

.alert-danger {
  background: rgba(231,76,60,0.08);
  border-color: #E74C3C; color: #FCA5A5;
}

/* ─── REJECTION REASONS ─── */
.reason-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 14px; color: var(--text-secondary);
}

.reason-item::before {
  content: '•';
  color: var(--danger); font-size: 18px; line-height: 1; flex-shrink: 0;
}

/* ─── EXPANDER ─── */
details {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px; margin: 16px 0;
  overflow: hidden;
}

summary {
  padding: 14px 18px;
  cursor: pointer;
  font-size: 13px; color: var(--text-secondary);
  letter-spacing: 0.3px;
  list-style: none; display: flex; align-items: center; gap: 8px;
}

summary::-webkit-details-marker { display: none; }

summary::after {
  content: '▸'; margin-left: auto;
  color: var(--text-muted); font-size: 12px;
  transition: transform 0.2s;
}

details[open] summary::after { transform: rotate(90deg); }

.details-body {
  padding: 16px 18px;
  border-top: 1px solid var(--border);
  background: rgba(255,255,255,0.018);
}

/* ─── DIVIDER ─── */
hr {
  border: none; border-top: 1px solid var(--border);
  margin: 28px 0;
}

/* ─── FOOTER ─── */
.footer {
  margin-top: 80px; padding: 24px 32px;
  border-radius: 16px;
  border: 1px solid rgba(201,168,76,0.1);
  background: rgba(255,255,255,0.015);
  display: flex; justify-content: space-between; align-items: center;
  font-size: 12px; letter-spacing: 1px; color: var(--text-muted);
}

.footer span { color: var(--gold); }

/* ─── HIDDEN / VISIBLE ─── */
.hidden { display: none !important; }

/* ─── AUTH OVERLAY ─── */
.auth-overlay {
  position: fixed; inset: 0;
  background: var(--bg-deep);
  display: flex; align-items: center; justify-content: center;
  z-index: 100;
}

.auth-card {
  width: 420px;
  background: #0C1220;
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 40px;
  position: relative;
}

.auth-card::before {
  content: '';
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 60%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.auth-title {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700;
  color: var(--text-primary); text-align: center;
  margin-bottom: 6px;
}

.auth-sub {
  text-align: center; font-size: 13px; color: var(--text-secondary);
  margin-bottom: 28px;
}

.auth-tabs {
  display: flex; border-radius: 10px; overflow: hidden;
  border: 1px solid var(--border); margin-bottom: 24px;
}

.auth-tab {
  flex: 1; padding: 10px;
  background: transparent; border: none;
  color: var(--text-secondary); font-size: 13px;
  font-family: 'DM Sans', sans-serif; font-weight: 500;
  cursor: pointer; letter-spacing: 0.5px;
  transition: all 0.2s;
}

.auth-tab.active {
  background: var(--gold-dim);
  color: var(--gold-light);
}

.auth-field { margin-bottom: 16px; }
.auth-field label {
  display: block; margin-bottom: 6px;
  font-size: 11px; letter-spacing: 1px;
  text-transform: uppercase; color: var(--text-secondary);
}

.auth-field input {
  width: 100%;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border); border-radius: 10px;
  color: var(--text-primary); padding: 11px 14px;
  font-size: 15px; font-family: 'DM Sans', sans-serif;
  outline: none; transition: border-color 0.2s;
}

.auth-field input:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 3px var(--gold-dim);
}

.auth-btn {
  width: 100%; height: 50px;
  background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%);
  color: #060A12; border: none; border-radius: 12px;
  font-size: 13px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.2s;
  box-shadow: 0 4px 20px rgba(201,168,76,0.2);
  margin-top: 8px;
}

.auth-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 28px rgba(201,168,76,0.35);
}

.auth-msg {
  padding: 10px 14px; border-radius: 8px;
  font-size: 13px; margin-top: 12px; display: none;
}

.auth-msg.error { background: rgba(231,76,60,0.1); color: #FCA5A5; border: 1px solid rgba(231,76,60,0.2); }
.auth-msg.success { background: rgba(46,204,113,0.1); color: #86EFAC; border: 1px solid rgba(46,204,113,0.2); }
.auth-msg.warning { background: rgba(234,179,8,0.08); color: #FDE047; border: 1px solid rgba(234,179,8,0.2); }

/* ─── DOWNLOAD BUTTON ─── */
.btn-download {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 24px; border-radius: 10px;
  background: rgba(201,168,76,0.1);
  border: 1px solid rgba(201,168,76,0.3);
  color: var(--gold-light); font-size: 13px; font-weight: 500;
  cursor: pointer; text-decoration: none; font-family: 'DM Sans', sans-serif;
  transition: all 0.2s; letter-spacing: 0.3px;
  margin-top: 16px;
}

.btn-download:hover {
  background: rgba(201,168,76,0.18);
  border-color: rgba(201,168,76,0.5);
  transform: translateY(-1px);
}

/* ─── PROCESSING STEPS ─── */
.processing-wrap { padding: 16px 0; }

.processing-step {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; font-size: 14px;
  color: var(--text-muted);
  transition: color 0.3s;
}

.processing-step.active { color: var(--gold); }
.processing-step.done { color: var(--success); }

.step-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--text-muted); flex-shrink: 0;
  transition: background 0.3s;
}

.processing-step.active .step-dot { background: var(--gold); animation: pulse-dot 0.8s infinite; }
.processing-step.done .step-dot { background: var(--success); }

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.progress-bar-wrap {
  height: 4px; background: rgba(255,255,255,0.06);
  border-radius: 100px; overflow: hidden; margin: 16px 0;
}

.progress-bar-fill {
  height: 100%; background: linear-gradient(90deg, var(--gold), var(--gold-light));
  border-radius: 100px; width: 0;
  transition: width 0.4s ease;
}

/* ─── RESPONSIVENESS ─── */
@media (max-width: 900px) {
  .sidebar { display: none; }
  .main { margin-left: 0; max-width: 100vw; padding: 24px 20px; }
  .form-grid, .form-grid-3 { grid-template-columns: 1fr; }
  .metrics-grid { grid-template-columns: 1fr 1fr; }
  .hero-title { font-size: 40px; }
  .hero-stats { gap: 28px; }
}
</style>
</head>
<body>

<!-- ═══════ AUTH OVERLAY ═══════ -->
<div class="auth-overlay" id="authOverlay">
  <div class="auth-card">
    <div class="auth-title">🏦 LoanSahayak</div>
    <div class="auth-sub">Sign in to access your loan intelligence dashboard</div>

    <div class="auth-tabs">
      <button class="auth-tab active" id="tabLogin" onclick="switchTab('login')">Login</button>
      <button class="auth-tab" id="tabSignup" onclick="switchTab('signup')">Sign Up</button>
    </div>

    <!-- LOGIN -->
    <div id="loginForm">
      <div class="auth-field">
        <label>Username</label>
        <input type="text" id="loginUser" placeholder="Enter username">
      </div>
      <div class="auth-field">
        <label>Password</label>
        <input type="password" id="loginPass" placeholder="Enter password">
      </div>
      <button class="auth-btn" onclick="doLogin()">Login</button>
      <div class="auth-msg" id="loginMsg"></div>
    </div>

    <!-- SIGNUP -->
    <div id="signupForm" style="display:none;">
      <div class="auth-field">
        <label>Create Username</label>
        <input type="text" id="signupUser" placeholder="4–20 chars (letters, numbers, _.)">
      </div>
      <div class="auth-field">
        <label>Password</label>
        <input type="password" id="signupPass" placeholder="Uppercase + lowercase + number">
      </div>
      <div class="auth-field">
        <label>Confirm Password</label>
        <input type="password" id="signupConfirm" placeholder="Repeat your password">
      </div>
      <button class="auth-btn" onclick="doSignup()">Create Account</button>
      <div class="auth-msg" id="signupMsg"></div>
    </div>
  </div>
</div>


<!-- ═══════ SIDEBAR ═══════ -->
<aside class="sidebar" id="sidebarEl">
  <div class="sidebar-logo">
    <div class="sidebar-logo-name">LoanSahayak</div>
    <div class="sidebar-logo-sub">Smart Loan Intelligence</div>
  </div>

  <div class="sidebar-info">
    AI-powered system that evaluates loan applications using:<br>
    • Financial indicators<br>
    • Credit score analysis<br>
    • Multi-factor risk assessment
  </div>

  <div class="sidebar-stats-label">System Stats</div>
  <div class="sidebar-stats">
    ✔ Accuracy: <span>83.4%</span><br>
    ✔ Decision Time: <span>&lt; 2s</span><br>
    ✔ Risk Factors: <span>16+</span>
  </div>

  <hr class="sidebar-divider">

  <div style="font-family: 'Playfair Display', serif; font-size: 20px; color: var(--text-primary); font-weight: 600; margin-bottom: 6px;">👤 Project Author</div>
  <div class="sidebar-author-name">Arnav Singh</div>
  <div class="sidebar-author-title">Machine Learning Enthusiast · Aspiring Data Scientist</div>

  <div class="sidebar-links">
    <a href="https://www.linkedin.com/in/arnav-singh-a87847351" target="_blank" class="sidebar-icon-btn" style="background: rgba(78,161,255,0.08); border: 1px solid rgba(78,161,255,0.2);">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="#4EA1FF">
        <path d="M4.98 3.5C4.98 4.88 3.87 6 2.49 6S0 4.88 0 3.5 1.11 1 2.49 1 4.98 2.12 4.98 3.5zM.22 8.98H4.75V24H.22V8.98zm7.76 0h4.34v2.06h.06c.66-1.18 2.28-2.41 4.66-2.41 5.04 0 5.96 3.25 5.96 7.5V24h-4.53v-6.79c0-1.75-.03-4.01-2.45-4.01-2.46 0-2.84 1.86-2.84 3.88V24H7.98V8.98z"/>
      </svg>
    </a>
    <a href="mailto:itsarnav.singh80@gmail.com" class="sidebar-icon-btn" style="background: rgba(0,255,150,0.07); border: 1px solid rgba(0,255,150,0.2);">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="#00FFAA">
        <path d="M2 4a2 2 0 012-2h16a2 2 0 012 2v16a2 2 0 01-2 2H4a2 2 0 01-2-2V4zm2 0v2l8 7 8-7V4L12 11 4 4zm16 4l-8 7-8-7v12h16V8z"/>
      </svg>
    </a>
    <a href="https://github.com/Arnav-Singh-5080" target="_blank" class="sidebar-icon-btn" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12);">
      <svg width="17" height="17" viewBox="0 0 16 16" fill="#9CCBFF">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.6.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-.46-1.34-.46-1.34-.1-.26-.5-1.02-.5-1.02-.4-.28.03-.27.03-.27.44.03.68.45.68.45.4.69.98.52.22.38-.09-.29-.12-.56-.04-.79C6.88 11 5 10.13 5 7.13c0-.86.31-1.56.82-2.11-.08-.2-.36-1 .08-2.08 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.03 2.2-.82 2.2-.82.44 1.08.16 1.88.08 2.08.51.55.82 1.25.82 2.11 0 3.01-1.88 3.67-3.67 3.89.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
      </svg>
    </a>
  </div>

  <div class="sidebar-footer">⭐ Star this project on GitHub</div>
</aside>


<!-- ═══════ MAIN ═══════ -->
<main class="main" id="mainContent">

  <!-- Welcome Banner -->
  <div class="welcome-banner" id="welcomeBanner">
    👋 Welcome!! <strong id="welcomeName">User</strong> — System status: Active. LoanSahayak is ready to transform your data into definitive financial insights.
  </div>

  <!-- HERO -->
  <div class="hero">
    <div class="hero-badge">✦ AI-Powered Lending Intelligence</div>
    <div class="hero-title">Loan<span>Sahayak</span></div>
    <div class="hero-sub">Sophisticated credit analysis and risk assessment — engineered for modern lending decisions.</div>
    <div class="hero-stats">
      <div>
        <div class="hero-stat-val">83.4%</div>
        <div class="hero-stat-label">Accuracy</div>
      </div>
      <div>
        <div class="hero-stat-val">&lt; 2s</div>
        <div class="hero-stat-label">Decision Time</div>
      </div>
      <div>
        <div class="hero-stat-val">16+</div>
        <div class="hero-stat-label">Risk Factors</div>
      </div>
    </div>
  </div>

  <!-- ── FINANCIAL PROFILE ── -->
  <div class="section-header">
    <div class="section-icon">💼</div>
    <div class="section-title">Financial Profile</div>
    <div class="section-desc">Income & Loan Details</div>
  </div>

  <div class="form-grid" style="margin-bottom:20px;">
    <div class="field">
      <label>Applicant Income (₹)</label>
      <input type="number" id="applicantIncome" min="0" step="1000" placeholder="0">
    </div>
    <div class="field">
      <label>Coapplicant Income (₹)</label>
      <input type="number" id="coapplicantIncome" min="0" step="1000" placeholder="0">
    </div>
    <div class="field">
      <label>Loan Amount (₹)</label>
      <input type="number" id="loanAmount" min="0" step="1000" placeholder="0">
    </div>
    <div class="field">
      <label>Savings (₹)</label>
      <input type="number" id="savings" min="0" step="1000" placeholder="0">
    </div>
    <div class="field">
      <label>Collateral Value (₹)</label>
      <input type="number" id="collateralValue" min="0" step="1000" placeholder="0">
    </div>
    <div class="field">
      <label>Number of Dependents</label>
      <input type="number" id="dependents" min="0" placeholder="0">
    </div>
    <div class="field">
      <label>Existing Active Loans</label>
      <input type="number" id="existingLoans" min="0" placeholder="0">
    </div>
  </div>

  <div class="form-grid-3">
    <div class="slider-wrap">
      <label>Credit Score</label>
      <div class="slider-row">
        <input type="range" id="creditScore" min="300" max="900" value="650" oninput="document.getElementById('creditScoreVal').textContent=this.value">
        <span class="slider-val" id="creditScoreVal">650</span>
      </div>
    </div>
    <div class="slider-wrap">
      <label>Loan Term (Months)</label>
      <div class="slider-row">
        <input type="range" id="loanTerm" min="6" max="360" value="60" oninput="document.getElementById('loanTermVal').textContent=this.value">
        <span class="slider-val" id="loanTermVal">60</span>
      </div>
    </div>
    <div class="slider-wrap">
      <label>Applicant Age</label>
      <div class="slider-row">
        <input type="range" id="applicantAge" min="18" max="70" value="30" oninput="document.getElementById('ageVal').textContent=this.value">
        <span class="slider-val" id="ageVal">30</span>
      </div>
    </div>
  </div>

  <!-- ── APPLICANT BACKGROUND ── -->
  <div class="section-header" style="margin-top:44px;">
    <div class="section-icon">👤</div>
    <div class="section-title">Applicant Background</div>
    <div class="section-desc">Demographic & Employment</div>
  </div>

  <div class="form-grid">
    <div class="field">
      <label>Employment Status</label>
      <select id="employmentStatus">
        <option value="0">Unemployed</option>
        <option value="1">Salaried</option>
        <option value="2">Self-Employed</option>
      </select>
    </div>
    <div class="field">
      <label>Property Area</label>
      <select id="propertyArea">
        <option value="0">Rural</option>
        <option value="1">Semi-Urban</option>
        <option value="2">Urban</option>
      </select>
    </div>
    <div class="field">
      <label>Loan Purpose</label>
      <select id="loanPurpose">
        <option value="0">Home Loan</option>
        <option value="1">Car Loan</option>
        <option value="2">Education Loan</option>
        <option value="3">Personal Loan</option>
      </select>
    </div>
    <div class="field">
      <label>Education Level</label>
      <select id="educationLevel">
        <option value="0">Not Graduate</option>
        <option value="1">Graduate</option>
      </select>
    </div>
    <div class="field">
      <label>Gender</label>
      <select id="gender">
        <option value="0">Female</option>
        <option value="1">Male</option>
      </select>
    </div>
    <div class="field">
      <label>Employer Category</label>
      <select id="employerCategory">
        <option value="0">Private Sector</option>
        <option value="1">Government</option>
        <option value="2">Business Owner</option>
      </select>
    </div>
  </div>

  <!-- ANALYSE BUTTON -->
  <div style="margin-top: 40px; display:flex; justify-content: flex-start;">
    <button class="btn-primary" onclick="analyseApplication()">
      ⬡ &nbsp; Analyse Loan Application
    </button>
  </div>

  <!-- ── RESULT AREA ── -->
  <div id="resultArea" style="display:none; margin-top: 32px;">

    <!-- Processing -->
    <div id="processingArea">
      <div class="section-header">
        <div class="section-icon">⚙️</div>
        <div class="section-title">Processing Application</div>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" id="procProgressFill"></div>
      </div>
      <div class="processing-wrap" id="procSteps"></div>
    </div>

    <!-- Final results (hidden until processing done) -->
    <div id="finalResults" style="display:none;">

      <hr>

      <!-- Summary -->
      <details open>
        <summary>📋 Application Summary</summary>
        <div class="details-body">
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-label">Total Household Income</div>
              <div class="metric-value" id="sumIncome">—</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Loan Amount Requested</div>
              <div class="metric-value" id="sumLoan">—</div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Credit Score</div>
              <div class="metric-value" id="sumCredit">—</div>
            </div>
          </div>
        </div>
      </details>

      <!-- Financial Analysis -->
      <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">Financial Analysis</div>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Monthly EMI</div>
          <div class="metric-value" id="resEMI">—</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Total Monthly Income</div>
          <div class="metric-value" id="resIncome">—</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">EMI / Income Ratio</div>
          <div class="metric-value" id="resRatio">—</div>
        </div>
      </div>

      <hr>

      <!-- Approval Probability -->
      <div class="progress-wrap">
        <div class="progress-label">
          <span>Approval Probability</span>
          <strong id="approvalPct">—</strong>
        </div>
        <div class="progress-track">
          <div class="progress-fill" id="approvalFill" style="width:0%"></div>
        </div>
      </div>

      <!-- Risk alerts -->
      <div id="riskAlerts"></div>

      <!-- Decision -->
      <div id="decisionCard"></div>

      <!-- Rejection reasons -->
      <div id="rejectionReasons" style="display:none;">
        <div class="section-header">
          <div class="section-icon">⚠️</div>
          <div class="section-title">Possible Reasons for Rejection</div>
          <div class="section-desc">Key Risk Factors</div>
        </div>
        <div id="reasonsList"></div>
      </div>

      <!-- Download -->
      <button class="btn-download" onclick="downloadReport()">
        📄 &nbsp; Download PDF Report
      </button>

    </div><!-- /finalResults -->
  </div><!-- /resultArea -->

  <!-- FOOTER -->
  <div class="footer">
    <div>© 2026 <span>LoanSahayak</span> — All Rights Reserved</div>
    <div style="text-transform:uppercase; letter-spacing:2px;">AI · Credit · Intelligence</div>
  </div>

</main>


<script>
// ───────────────────────────────
// AUTH
// ───────────────────────────────
const STORAGE_KEY = 'ls_users';

function getUsers() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
}

function saveUser(username, password) {
  const users = getUsers();
  users[username.toLowerCase()] = { username, password: hashStr(password) };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
}

function hashStr(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (Math.imul(31, h) + s.charCodeAt(i)) | 0;
  return h.toString(16);
}

function isValidUsername(u) { return /^[a-zA-Z0-9_.]{4,20}$/.test(u); }
function isValidPassword(p) {
  return p.length >= 6 && /[A-Z]/.test(p) && /[a-z]/.test(p) && /[0-9]/.test(p);
}

function showMsg(id, text, type) {
  const el = document.getElementById(id);
  el.textContent = text; el.className = 'auth-msg ' + type;
  el.style.display = 'block';
}

function switchTab(tab) {
  const isLogin = tab === 'login';
  document.getElementById('tabLogin').classList.toggle('active', isLogin);
  document.getElementById('tabSignup').classList.toggle('active', !isLogin);
  document.getElementById('loginForm').style.display = isLogin ? 'block' : 'none';
  document.getElementById('signupForm').style.display = isLogin ? 'none' : 'block';
}

function doLogin() {
  const u = document.getElementById('loginUser').value.trim();
  const p = document.getElementById('loginPass').value;
  if (!u || !p) { showMsg('loginMsg', 'Please fill in both fields.', 'warning'); return; }
  const users = getUsers();
  const rec = users[u.toLowerCase()];
  if (rec && rec.password === hashStr(p)) {
    document.getElementById('authOverlay').style.display = 'none';
    document.getElementById('welcomeName').textContent = rec.username;
    document.getElementById('welcomeBanner').style.display = 'block';
  } else {
    showMsg('loginMsg', 'Invalid username or password.', 'error');
  }
}

function doSignup() {
  const u = document.getElementById('signupUser').value.trim();
  const p = document.getElementById('signupPass').value;
  const c = document.getElementById('signupConfirm').value;
  if (!u || !p) { showMsg('signupMsg', 'Fields cannot be empty.', 'warning'); return; }
  if (!isValidUsername(u)) { showMsg('signupMsg', 'Username must be 4–20 chars (letters, numbers, _ . only).', 'error'); return; }
  if (!isValidPassword(p)) { showMsg('signupMsg', 'Password needs uppercase, lowercase & number.', 'error'); return; }
  if (p !== c) { showMsg('signupMsg', 'Passwords do not match.', 'error'); return; }
  const users = getUsers();
  if (users[u.toLowerCase()]) { showMsg('signupMsg', 'Username already exists.', 'warning'); return; }
  saveUser(u, p);
  showMsg('signupMsg', 'Account created! Please login.', 'success');
  setTimeout(() => switchTab('login'), 1200);
}

document.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    if (document.getElementById('loginForm').style.display !== 'none') doLogin();
    else doSignup();
  }
});

// ───────────────────────────────
// EMI CALCULATOR
// ───────────────────────────────
function calcEMI(principal, months, rate = 10) {
  if (!principal || !months) return 0;
  const mr = rate / 12 / 100;
  return (principal * mr * Math.pow(1 + mr, months)) / (Math.pow(1 + mr, months) - 1);
}

function fmt(n) { return '₹ ' + Math.round(n).toLocaleString('en-IN'); }

// ───────────────────────────────
// ANALYSIS LOGIC (client-side heuristic model)
// ───────────────────────────────
function analyseApplication() {
  const appIncome = +document.getElementById('applicantIncome').value || 0;
  const coIncome  = +document.getElementById('coapplicantIncome').value || 0;
  const loanAmt   = +document.getElementById('loanAmount').value || 0;
  const collateral= +document.getElementById('collateralValue').value || 0;
  const existLoans= +document.getElementById('existingLoans').value || 0;
  const credit    = +document.getElementById('creditScore').value;
  const term      = +document.getElementById('loanTerm').value;

  if (!appIncome || !loanAmt) {
    alert('Income and Loan Amount must be greater than zero.');
    return;
  }

  const totalIncome = appIncome + coIncome;
  const emi = calcEMI(loanAmt, term);
  const emiRatio = totalIncome > 0 ? emi / totalIncome : 999;

  // Heuristic decision
  let score = 0;
  if (credit >= 750) score += 3;
  else if (credit >= 650) score += 2;
  else if (credit >= 550) score += 1;

  if (emiRatio < 0.3) score += 3;
  else if (emiRatio < 0.5) score += 1;

  if (totalIncome >= 50000) score += 2;
  else if (totalIncome >= 25000) score += 1;

  if (existLoans === 0) score += 1;
  else if (existLoans > 3) score -= 2;

  if (collateral >= loanAmt * 0.5) score += 1;

  const approved = score >= 5;
  const approvalProb = Math.min(95, Math.max(5, approved ? 55 + score * 5 : 20 + score * 5));

  // Show result area & start processing animation
  document.getElementById('resultArea').style.display = 'block';
  document.getElementById('processingArea').style.display = 'block';
  document.getElementById('finalResults').style.display = 'none';

  const steps = [
    '🔍 Collecting financial data...',
    '📊 Analyzing income & liabilities...',
    '🧠 Running ML model inference...',
    '⚖️ Evaluating risk parameters...',
    '✅ Finalizing decision...'
  ];

  const stepsEl = document.getElementById('procSteps');
  const fillEl = document.getElementById('procProgressFill');
  stepsEl.innerHTML = steps.map((s, i) =>
    `<div class="processing-step" id="step${i}">
      <div class="step-dot"></div><span>${s}</span>
    </div>`
  ).join('');

  let i = 0;
  function nextStep() {
    if (i > 0) {
      document.getElementById('step' + (i-1)).className = 'processing-step done';
    }
    if (i < steps.length) {
      document.getElementById('step' + i).className = 'processing-step active';
      fillEl.style.width = ((i + 1) / steps.length * 100) + '%';
      i++;
      setTimeout(nextStep, 420);
    } else {
      // All done — show results
      setTimeout(() => {
        document.getElementById('processingArea').style.display = 'none';
        showResults({ emi, totalIncome, emiRatio, credit, loanAmt, collateral, existLoans, approved, approvalProb });
        document.getElementById('resultArea').scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
    }
  }

  nextStep();
}

function showResults({ emi, totalIncome, emiRatio, credit, loanAmt, collateral, existLoans, approved, approvalProb }) {
  const fr = document.getElementById('finalResults');
  fr.style.display = 'block';

  // Summary
  document.getElementById('sumIncome').textContent = fmt(totalIncome);
  document.getElementById('sumLoan').textContent = fmt(loanAmt);
  document.getElementById('sumCredit').textContent = credit;

  // Metrics
  document.getElementById('resEMI').textContent = fmt(emi);
  document.getElementById('resIncome').textContent = fmt(totalIncome);
  document.getElementById('resRatio').textContent = (emiRatio * 100).toFixed(2) + ' %';

  // Progress bar animate
  const pct = Math.round(approvalProb);
  document.getElementById('approvalPct').textContent = pct + '%';
  setTimeout(() => {
    document.getElementById('approvalFill').style.width = pct + '%';
  }, 100);

  // Risk alerts
  const alerts = document.getElementById('riskAlerts');
  alerts.innerHTML = '';
  if (emiRatio > 0.5) {
    alerts.innerHTML += '<div class="alert alert-warning">⚠ High EMI ratio — EMI exceeds 50% of monthly income</div>';
  }
  if (credit < 600) {
    alerts.innerHTML += '<div class="alert alert-warning">⚠ Low credit score — below 600 threshold</div>';
  }
  if (emiRatio <= 0.5 && credit >= 600) {
    alerts.innerHTML += '<div class="alert alert-info">✓ Stable profile — no immediate risk flags detected</div>';
  }

  // Decision card
  const dc = document.getElementById('decisionCard');
  if (approved) {
    dc.innerHTML = `
      <div class="result-approved">
        <div class="result-icon">✅</div>
        <div class="result-label" style="color: #2ECC71;">APPROVED</div>
        <div class="result-sub">Your application meets our lending criteria</div>
        <div class="result-conf conf-approved">Confidence: ${approvalProb.toFixed(2)}%</div>
      </div>`;
    document.getElementById('rejectionReasons').style.display = 'none';
  } else {
    dc.innerHTML = `
      <div class="result-rejected">
        <div class="result-icon">❌</div>
        <div class="result-label" style="color: #E74C3C;">REJECTED</div>
        <div class="result-sub">This application does not meet current lending criteria</div>
        <div class="result-conf conf-rejected">Confidence: ${(100 - approvalProb).toFixed(2)}%</div>
      </div>`;

    // Rejection reasons
    const reasons = [];
    if (totalIncome < 25000) reasons.push('Total household income is below the recommended threshold (₹25,000).');
    if (emiRatio > 0.5) reasons.push('EMI to income ratio is too high (greater than 50%).');
    if (credit < 600) reasons.push('Credit score is below the acceptable limit (600).');
    if (existLoans > 3) reasons.push('Too many active loans already.');
    if (collateral < loanAmt * 0.5) reasons.push('Collateral value is insufficient for the requested loan.');

    const rr = document.getElementById('rejectionReasons');
    const rl = document.getElementById('reasonsList');
    if (reasons.length > 0) {
      rr.style.display = 'block';
      rl.innerHTML = reasons.map(r => `<div class="reason-item">${r}</div>`).join('');
    } else {
      rr.style.display = 'block';
      rl.innerHTML = '<div class="reason-item">The application does not meet the bank approval criteria.</div>';
    }
  }
}

// ───────────────────────────────
// SIMPLE PDF REPORT (text-based)
// ───────────────────────────────
function downloadReport() {
  const name = document.getElementById('welcomeName').textContent;
  const income = document.getElementById('resIncome').textContent;
  const loan = document.getElementById('sumLoan').textContent;
  const credit = document.getElementById('sumCredit').textContent;
  const emi = document.getElementById('resEMI').textContent;
  const ratio = document.getElementById('resRatio').textContent;
  const decision = document.getElementById('decisionCard').querySelector('.result-label')?.textContent || '—';
  const conf = document.getElementById('decisionCard').querySelector('.result-conf')?.textContent || '';

  const content = `LOANSAHAYAK — AI LOAN ANALYSIS REPORT
========================================
Generated for: ${name}
Date: ${new Date().toLocaleDateString('en-IN')}

FINANCIAL SUMMARY
─────────────────
Total Monthly Income  : ${income}
Loan Amount           : ${loan}
Monthly EMI           : ${emi}
EMI / Income Ratio    : ${ratio}
Credit Score          : ${credit}

DECISION
────────
Status     : ${decision}
${conf}

DISCLAIMER
──────────
This report is generated by LoanSahayak AI for informational
purposes only and does not constitute a formal loan offer.
Final approval is subject to bank verification.

© 2026 LoanSahayak — All Rights Reserved
AI · Credit · Intelligence`;

  const blob = new Blob([content], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'LoanSahayak_Report.txt';
  a.click();
}
</script>
</body>
</html>
