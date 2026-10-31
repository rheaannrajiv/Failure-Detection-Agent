'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Activity, ArrowUp, Bot, BookOpen, Check, ChevronDown, CircleHelp, Cpu, Database, FileText, Gauge, History, Loader2, LogIn, LogOut, Menu, Paperclip, Plus, Radio, Send, Settings2, ShieldCheck, Sparkles, Upload, Wrench, X, SlidersHorizontal, Factory, ClipboardList } from 'lucide-react';
import { createGuestSession, createUserSession, generateReport, getHealth, investigateWithSensor, readSession, sendChat, SessionInfo } from '@/lib/api';
import { getSupabase } from '@/lib/supabase';

type Message = { role: 'user' | 'assistant'; content: string; meta?: string; tools?: Array<Record<string,unknown>> };

export default function Home() {
  const [messages,setMessages] = useState<Message[]>([]);
  const [input,setInput] = useState('');
  const [session,setSession] = useState<SessionInfo|null>(null);
  const [accessToken,setAccessToken] = useState<string|undefined>();
  const [busy,setBusy] = useState(false);
  const [status,setStatus] = useState<'checking'|'online'|'offline'>('checking');
  const [error,setError] = useState('');
  const [authOpen,setAuthOpen] = useState(false);
  const [email,setEmail] = useState('');
  const [password,setPassword] = useState('');
  const [authMode,setAuthMode] = useState<'login'|'signup'>('login');
  const [userEmail,setUserEmail] = useState('');
  const [mobileMenu,setMobileMenu] = useState(false);
  const [featurePanel,setFeaturePanel] = useState<'machines'|'history'|'knowledge'|'settings'|'tools'|null>(null);
  const [reportBusy,setReportBusy] = useState(false);
  const [selectedFile,setSelectedFile] = useState<File|null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let alive = true;
    getHealth().then(()=>alive&&setStatus('online')).catch(()=>alive&&setStatus('offline'));
    const existing = readSession(); if (existing) setSession(existing);
    try {
      const sb = getSupabase();
      sb.auth.getSession().then(async ({data}) => {
        if (!alive) return;
        const token = data.session?.access_token;
        if (token) { setAccessToken(token); setUserEmail(data.session?.user.email || ''); try { const owned = await createUserSession(token); if (alive) setSession(owned); } catch (e) { if (alive) setError(e instanceof Error ? e.message : 'Could not create an authenticated session.'); } }
      }).catch(()=>{});
      const { data: listener } = sb.auth.onAuthStateChange((_event, authSession) => {
        setAccessToken(authSession?.access_token); setUserEmail(authSession?.user.email || '');
      });
      return () => { alive = false; listener.subscription.unsubscribe(); };
    } catch { return () => { alive = false; }; }
  }, []);
  useEffect(()=>{ bottomRef.current?.scrollIntoView({behavior:'smooth'}); },[messages,busy]);

  async function ensureSession() {
    if (session) return session;
    const created = await createGuestSession(); setSession(created); return created;
  }
  async function submit(text = input) {
    const clean = text.trim(); if (!clean || busy) return;
    setError(''); setInput(''); setBusy(true);
    const next = [...messages, {role:'user' as const,content:clean}]; setMessages(next);
    try {
      const active = await ensureSession();
      const history = messages.map(({role,content})=>({role,content}));
      const result = selectedFile ? await investigateWithSensor(clean, selectedFile, active, accessToken) : await sendChat(clean, history, active, accessToken);
      setMessages([...next,{role:'assistant',content:result.reply,meta:`${result.model || 'Failure Detective Agent'} · ${result.memory_mode || 'session'}`,tools:result.tool_calls || []}]);
      setSelectedFile(null); if (fileRef.current) fileRef.current.value='';
    } catch(e) { setError(e instanceof Error ? e.message : 'Request failed.'); setMessages(next); }
    finally { setBusy(false); }
  }
  async function authenticate() {
    setError(''); setBusy(true);
    try {
      const sb=getSupabase();
      const result = authMode==='signup' ? await sb.auth.signUp({email,password}) : await sb.auth.signInWithPassword({email,password});
      if (result.error) throw result.error;
      const session = result.data.session;
      const user = result.data.user;
      if (!session) { setError('Check your email to confirm your account, then sign in.'); return; }
      if (!user) throw new Error('Authentication succeeded without returning a user profile. Please try signing in again.');
      setAccessToken(session.access_token);
      setUserEmail(user.email ?? email);
      const created = await createUserSession(session.access_token);
      setSession(created);
      setAuthOpen(false);
      setPassword('');
    } catch(e) { setError(e instanceof Error ? e.message : 'Authentication failed.'); }
    finally { setBusy(false); }
  }
  async function logout() {
    try { await getSupabase().auth.signOut(); } catch {}
    setAccessToken(undefined); setUserEmail(''); setSession(null); sessionStorage.removeItem('fd_session'); setMessages([]);
  }
  async function downloadReport() {
    if (!messages.length) return;
    setReportBusy(true); setError('');
    try {
      const active = await ensureSession();
      const userMessages = messages.filter(m=>m.role==='user').map(m=>m.content);
      const assistantMessages = messages.filter(m=>m.role==='assistant').map(m=>m.content);
      const result = await generateReport({ machine: 'Machine under investigation (confirm machine type)', symptoms: userMessages, findings: assistantMessages, limitations: ['Report compiled from the current chat; verify all findings and machine-specific limits before acting.'] }, active, accessToken);
      const blob = new Blob([result.report_markdown], {type:'text/markdown;charset=utf-8'});
      const url = URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='failure-detective-investigation-report.md'; a.click(); URL.revokeObjectURL(url);
    } catch(e) { setError(e instanceof Error ? e.message : 'Could not generate report.'); } finally { setReportBusy(false); }
  }
  const greeting = useMemo(()=>new Intl.DateTimeFormat('en',{hour:'2-digit',minute:'2-digit'}).format(new Date()),[]);

  return <main className="shell">
    <aside className={`sidebar ${mobileMenu?'open':''}`}>
      <div className="brand"><div className="brand-mark"><Activity size={21}/></div><div><strong>FAILURE<span>DETECTIVE</span></strong><small>MECHANICAL INTELLIGENCE</small></div><button className="icon-btn mobile-close" onClick={()=>setMobileMenu(false)}><X size={18}/></button></div>
      <button className="new-chat" onClick={()=>{setMessages([]);setError('');setSession(null);sessionStorage.removeItem('fd_session');setMobileMenu(false)}}><Plus size={17}/> New investigation</button>
      <div className="side-label">WORKSPACE</div>
      <button className="nav-item active" onClick={()=>{setFeaturePanel(null);setMobileMenu(false)}}><Bot size={17}/> AI diagnostic agent <span className="live-dot"/></button>
      <button className="nav-item" onClick={()=>{setFeaturePanel('machines');setMobileMenu(false)}}><Factory size={17}/> Machine library <span className="side-feature-icon"><ChevronDown size={13}/></span></button>
      <button className="nav-item" onClick={()=>{setFeaturePanel('history');setMobileMenu(false)}}><History size={17}/> Investigation history <span className="side-feature-icon"><ChevronDown size={13}/></span></button>
      <button className="nav-item" onClick={()=>{setFeaturePanel('knowledge');setMobileMenu(false)}}><BookOpen size={17}/> Engineering knowledge <span className="side-feature-icon"><ChevronDown size={13}/></span></button>
      <button className="nav-item" onClick={()=>{setFeaturePanel('tools');setMobileMenu(false)}}><Activity size={17}/> Sensor workspace <span className="soon">OPEN</span></button>
      <button className="nav-item" onClick={()=>{setFeaturePanel('history');setMobileMenu(false)}}><FileText size={17}/> Reports <span className="soon">VIEW</span></button>
      <div className="side-label side-label-spaced">PREFERENCES</div>
      <button className="nav-item" onClick={()=>{setFeaturePanel('settings');setMobileMenu(false)}}><SlidersHorizontal size={17}/> Workspace settings</button>
      <div className="side-label side-label-spaced">SYSTEM</div>
      <div className="system-card"><div className="system-head"><span className={`status-dot ${status}`}/><b>Backend status</b><span className="status-text">{status==='checking'?'CHECKING':status==='online'?'OPERATIONAL':'UNAVAILABLE'}</span></div><p>FastAPI diagnostic engine</p><div className="system-foot"><span>RENDER CLOUD</span><span>v0.4 API</span></div></div>
      <div className="sidebar-bottom"><div className="privacy"><ShieldCheck size={16}/><span>Diagnostic sessions are protected by session tokens.</span></div><button className="account-btn" onClick={()=>userEmail?logout():setAuthOpen(true)}>{userEmail?<><div className="avatar">{userEmail[0].toUpperCase()}</div><span className="account-text"><b>{userEmail}</b><small>Sign out</small></span><LogOut size={16}/></>:<><div className="avatar guest"><LogIn size={16}/></div><span className="account-text"><b>Guest workspace</b><small>Sign in to use your account</small></span><ChevronDown size={16}/></>}</button></div>
    </aside>
    {mobileMenu&&<button className="scrim" onClick={()=>setMobileMenu(false)} aria-label="Close menu"/>}
    <section className="main-panel">
      <header className="topbar"><div className="top-left"><button className="icon-btn menu-btn" onClick={()=>setMobileMenu(true)}><Menu size={19}/></button><div className="breadcrumb">WORKSPACE <span>/</span> <b>DIAGNOSTIC AGENT</b></div></div><div className="top-right"><div className="secure"><ShieldCheck size={14}/> SECURE SESSION</div><button className="help-btn" title="Engineering knowledge" onClick={()=>setFeaturePanel('knowledge')}><CircleHelp size={17}/></button><button className="help-btn" title="Quick tools" onClick={()=>setFeaturePanel('tools')}><Sparkles size={17}/></button><button className="sign-in" onClick={()=>userEmail?logout():setAuthOpen(true)}>{userEmail?'Sign out':'Sign in'} <LogIn size={15}/></button></div></header>
      <div className="content">
        {messages.length===0 ? <div className="welcome"><div className="eyebrow"><span className="pulse"/> AGENT ONLINE <span className="eyebrow-divider"/> {greeting}</div><div className="hero-icon"><div className="hero-ring ring-one"/><div className="hero-ring ring-two"/><div className="hero-core"><Cpu size={32}/></div></div><h1>Diagnose with<br/><em>engineering intelligence.</em></h1><p className="hero-copy">Describe a machine fault, share operating data or upload a sensor recording. Your diagnostic agent investigates the evidence and guides the next step.</p><div className="capabilities"><span><Wrench size={14}/> Mechanical diagnosis</span><span><Radio size={14}/> Sensor-assisted analysis</span><span><Gauge size={14}/> Evidence-led findings</span></div><div className="prompt-grid"><button onClick={()=>submit('My centrifugal pump is vibrating excessively and its discharge flow is fluctuating. Help me investigate possible causes.') }><span className="prompt-icon"><Activity size={17}/></span><span><b>Investigate a pump fault</b><small>Vibration, noise and flow instability</small></span><ArrowUp size={15}/></button><button onClick={()=>submit('Explain how to distinguish rotor imbalance from shaft misalignment using vibration measurements.') }><span className="prompt-icon"><Gauge size={17}/></span><span><b>Interpret vibration symptoms</b><small>Compare possible rotating machinery faults</small></span><ArrowUp size={15}/></button><button onClick={()=>submit('A rolling element bearing is overheating. Help me build a systematic inspection plan.') }><span className="prompt-icon"><Settings2 size={17}/></span><span><b>Build an inspection plan</b><small>Bearing temperature and lubrication</small></span><ArrowUp size={15}/></button><button onClick={()=>fileRef.current?.click()}><span className="prompt-icon"><Upload size={17}/></span><span><b>Analyse sensor data</b><small>Upload a CSV, TXT or MAT recording</small></span><ArrowUp size={15}/></button></div><div className="welcome-note"><ShieldCheck size={14}/> Diagnostic scores are evidence rankings, not confirmed probabilities.</div></div> : <div className="conversation"><div className="conversation-heading"><div><div className="eyebrow"><span className="pulse"/> INVESTIGATION ACTIVE</div><h2>Diagnostic investigation</h2></div><div className="conversation-actions"><span className="session-chip">{session?.mode==='authenticated'?'ACCOUNT SESSION':'GUEST SESSION'}</span><button className="report-download" onClick={downloadReport} disabled={reportBusy}>{reportBusy?<Loader2 className="spin" size={14}/>:<FileText size={14}/>} Export report</button></div></div>{messages.map((m,i)=><div className={`message-row ${m.role}`} key={i}><div className={`message-avatar ${m.role}`}>{m.role==='assistant'?<Bot size={17}/>:<span>YOU</span>}</div><div className="message-body"><div className="message-author">{m.role==='assistant'?'FAILURE DETECTIVE AI':'YOU'} {m.meta&&<small>{m.meta}</small>}</div><div className="message-content markdown-body"><ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown></div>{m.tools&&m.tools.length>0&&<details className="tool-details"><summary><Wrench size={14}/> Diagnostic tools used ({m.tools.length})</summary><pre>{JSON.stringify(m.tools,null,2)}</pre></details>}</div></div>)}{busy&&<div className="message-row assistant"><div className="message-avatar assistant"><Bot size={17}/></div><div className="message-body"><div className="message-author">FAILURE DETECTIVE AI</div><div className="thinking"><span/><span/><span/> Analysing evidence and selecting diagnostic tools…</div></div></div>}<div ref={bottomRef}/></div>}
      </div>
      <div className="composer-wrap"><div className="composer"><input ref={fileRef} type="file" accept=".csv,.txt,.mat" hidden onChange={e=>setSelectedFile(e.target.files?.[0]||null)}/>{selectedFile&&<div className="file-pill"><Paperclip size={13}/>{selectedFile.name}<button onClick={()=>{setSelectedFile(null);if(fileRef.current)fileRef.current.value=''}}><X size={13}/></button></div>}<textarea value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();submit()}}} placeholder="Describe the machine, symptoms or inspection findings…" rows={2}/><div className="composer-bottom"><div className="composer-tools"><button className="attach-btn" onClick={()=>fileRef.current?.click()}><Paperclip size={15}/> Attach sensor data</button><span className="file-hint">CSV · TXT · MAT · max 15 MB</span></div><button className="send-btn" onClick={()=>submit()} disabled={busy||!input.trim()}>{busy?<Loader2 className="spin" size={17}/>:<ArrowUp size={18}/>}</button></div></div><div className="disclaimer">AI-generated engineering guidance must be verified against machine-specific limits and qualified inspection procedures.</div>{error&&<div className="error-banner"><X size={15}/>{error}</div>}</div>
    </section>
    {featurePanel&&<div className="feature-backdrop" onClick={()=>setFeaturePanel(null)}><section className="feature-modal" onClick={e=>e.stopPropagation()}>
      <div className="feature-modal-head"><div><div className="feature-modal-kicker">FAILURE DETECTIVE / WORKSPACE</div>
      <h2>{featurePanel==='machines'?'Machine library':featurePanel==='history'?'Investigation & reports':featurePanel==='knowledge'?'Engineering knowledge':featurePanel==='settings'?'Workspace settings':'Diagnostic tools'}</h2>
      <p>{featurePanel==='machines'?'Choose a machine family to start a focused investigation. Confirm actual operating limits before diagnosis.':featurePanel==='history'?'Your current conversation is available in this session. Sign in to use account-linked sessions and memory features supported by the backend.':featurePanel==='knowledge'?'Quick reference topics for structured mechanical fault investigation. The agent can help explore these topics in the active chat.':featurePanel==='settings'?'Control the current workspace experience. Account and persistent memory controls depend on your sign-in and backend configuration.':'Launch a diagnostic workflow from the current investigation.'}</p></div><button className="feature-close" onClick={()=>setFeaturePanel(null)} aria-label="Close panel"><X size={17}/></button></div>
      {featurePanel==='machines'&&<div className="feature-grid">{['Centrifugal pumps','Electric motors','Rolling element bearings','Gearboxes','Compressors','Fans & blowers'].map(name=><button className="feature-tile" key={name} onClick={()=>{setFeaturePanel(null);submit(`Help me investigate a ${name.toLowerCase()}. Start by asking for the operating conditions, symptoms and available measurements.`)}}><Factory size={18}/><b>{name}</b><small>Start a guided machine investigation</small></button>)}</div>}
      {featurePanel==='history'&&<div className="feature-list"><div className="feature-list-item"><History size={18}/><div><b>Current investigation</b><small>{messages.length?`${messages.length} messages in this active conversation.`:'No active investigation yet. Start a new investigation to create a session.'}</small></div></div><div className="feature-list-item"><FileText size={18}/><div><b>Diagnostic report export</b><small>{messages.length?'Use Export report in the conversation to download findings.':'Start an investigation before generating a report.'}</small></div></div><div className="feature-note">Persistent cross-session history is not displayed here yet. This panel currently reflects the active conversation.</div></div>}
      {featurePanel==='knowledge'&&<div className="feature-grid">{['Vibration analysis','Cavitation & hydraulics','Bearing failure modes','Shaft alignment','Lubrication & wear','Thermal diagnostics'].map(name=><button className="feature-tile" key={name} onClick={()=>{setFeaturePanel(null);submit(`Explain ${name.toLowerCase()} in mechanical fault diagnosis. Give practical symptoms, evidence to collect and inspection checks.`)}}><BookOpen size={18}/><b>{name}</b><small>Ask the agent for an engineering explanation</small></button>)}</div>}
      {featurePanel==='tools'&&<div className="feature-grid"><button className="feature-tile" onClick={()=>{setFeaturePanel(null);fileRef.current?.click()}}><Upload size={18}/><b>Upload sensor recording</b><small>Attach a CSV, TXT or MAT file</small></button><button className="feature-tile" onClick={()=>{setFeaturePanel(null);submit('Help me plan a vibration measurement campaign for a rotating machine. Ask for machine speed, bearing type and available sensor locations.')}}><Activity size={18}/><b>Measurement planning</b><small>Build a vibration data collection plan</small></button><button className="feature-tile" onClick={()=>{setFeaturePanel(null);submit('Create a systematic inspection checklist for the machine under investigation.')}}><ClipboardList size={18}/><b>Inspection checklist</b><small>Generate practical inspection steps</small></button><button className="feature-tile" onClick={()=>{setFeaturePanel(null);downloadReport()}}><FileText size={18}/><b>Generate report</b><small>Export the current diagnostic conversation</small></button></div>}
      {featurePanel==='settings'&&<div className="feature-list"><div className="feature-list-item"><ShieldCheck size={18}/><div><b>Session security</b><small>{userEmail?`Signed in as ${userEmail}.`:'You are using guest access. Sign in for an account-linked session.'}</small></div></div><div className="feature-list-item"><Database size={18}/><div><b>Memory connection</b><small>{session?.mode==='authenticated'?'Authenticated session is active.':'Guest context may be session-scoped; sign in for account-linked memory where configured.'}</small></div></div><div className="feature-list-item"><SlidersHorizontal size={18}/><div><b>Appearance</b><small>Warm Prism · Syne display type · Manrope interface type · animated prism accents</small></div></div><button className="feature-tile" onClick={()=>{setFeaturePanel(null);userEmail?logout():setAuthOpen(true)}}><LogIn size={18}/><b>{userEmail?'Sign out':'Sign in / create account'}</b><small>Manage your account session</small></button></div>}
    </section></div>}
    {authOpen&&<div className="modal-backdrop" onClick={()=>setAuthOpen(false)}><div className="auth-modal" onClick={e=>e.stopPropagation()}><button className="modal-close" onClick={()=>setAuthOpen(false)}><X size={18}/></button><div className="modal-icon"><ShieldCheck size={22}/></div><div className="eyebrow">PERSONAL WORKSPACE</div><h2>{authMode==='login'?'Welcome back':'Create your account'}</h2><p>Sign in to create an authenticated diagnostic session. Guest investigations remain available without an account.</p><label>Email address</label><input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@example.com"/><label>Password</label><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="At least 6 characters"/><button className="auth-submit" disabled={busy||!email||password.length<6} onClick={authenticate}>{busy?<Loader2 className="spin" size={16}/>:authMode==='login'?'Sign in':'Create account'}</button><div className="auth-switch">{authMode==='login'?"New to Failure Detective?":"Already have an account?"} <button onClick={()=>setAuthMode(authMode==='login'?'signup':'login')}>{authMode==='login'?'Create account':'Sign in'}</button></div>{error&&<div className="error-banner">{error}</div>}</div></div>}
  </main>;
}
