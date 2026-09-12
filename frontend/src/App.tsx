import { useEffect, useState } from 'react';
import { Activity, ArrowRight, BarChart3, FileAudio, FileVideo, History, LockKeyhole, LogOut, Menu, ShieldCheck, Upload, UserRound, X } from 'lucide-react';
import { api, Scan } from './api';

type Page = 'dashboard' | 'voice' | 'video' | 'calls' | 'history' | 'settings';
const nav = [
	['dashboard', 'Overview', BarChart3], ['voice', 'Voice detection', FileAudio],
	['video', 'Video detection', FileVideo], ['calls', 'Incoming calls', Activity],
	['history', 'Scan history', History], ['settings', 'Settings', UserRound],
] as const;

function Risk({ level, score }: { level: string; score?: number }) {
	return <span className={`risk ${level.toLowerCase()}`}>{score !== undefined ? `${score}% · ` : ''}{level}</span>;
}

function Landing({ onAuth }: { onAuth: () => void }) {
	const features = [
		['01', 'AI voice detection', 'Spot acoustic patterns that may signal synthetic or converted speech.', FileAudio],
		['02', 'Deepfake video detection', 'Inspect facial consistency and temporal artifacts frame by frame.', FileVideo],
		['03', 'Incoming call protection', 'Connect authorized VoIP or mobile audio without hidden interception.', Activity],
	] as const;
	return <main className="landing">
		<nav className="topbar"><div className="brand"><span className="brand-mark"><ShieldCheck size={19} /></span> RedFlag AI</div><button className="text-button" onClick={onAuth}>Sign in <ArrowRight size={16} /></button></nav>
		<section className="hero"><div className="eyebrow">TRUST, VERIFIED</div><h1>Detect synthetic scams<br /><em>before you trust them.</em></h1><p>AI-assisted analysis for suspicious voices, manipulated video, and authorized call streams. Make a clearer decision when the stakes are high.</p><div className="hero-actions"><button className="primary" onClick={onAuth}>Analyze a file <ArrowRight size={17} /></button><button className="secondary" onClick={onAuth}>Explore the workspace</button></div><div className="trust-note"><LockKeyhole size={15} /> Your media is analyzed privately and is never used to train models.</div></section>
		<section className="feature-row">{features.map(([number, title, description, Icon]) => <article className="feature" key={number}><small>{number}</small><Icon size={23} /><h3>{title}</h3><p>{description}</p></article>)}</section>
		<div className="disclaimer"><strong>Scam detection is probabilistic.</strong> Results are risk estimates, not guaranteed proof. Always verify sensitive requests through official channels.</div>
	</main>;
}

function Auth({ onDone }: { onDone: () => void }) {
	const [register, setRegister] = useState(false); const [email, setEmail] = useState(''); const [password, setPassword] = useState(''); const [error, setError] = useState('');
	const submit = async (event: React.FormEvent) => { event.preventDefault(); setError(''); try { const result = register ? await api.register(email, password) : await api.login(email, password); localStorage.setItem('token', result.access_token); localStorage.setItem('email', email); onDone(); } catch (err) { setError((err as Error).message); } };
	return <main className="auth-page"><div className="auth-card"><div className="brand"><span className="brand-mark"><ShieldCheck size={19} /></span> RedFlag AI</div><h1>{register ? 'Create your workspace' : 'Welcome back'}</h1><p>{register ? 'Start assessing suspicious media with a private, focused workspace.' : 'Sign in to review your latest risk assessments.'}</p>{error && <div className="error">{error}</div>}<form onSubmit={submit}><label>Email address<input type="email" required value={email} onChange={event => setEmail(event.target.value)} placeholder="you@example.com" /></label><label>Password<input type="password" minLength={8} required value={password} onChange={event => setPassword(event.target.value)} placeholder="8 characters minimum" /></label><button className="primary full">{register ? 'Create account' : 'Sign in'} <ArrowRight size={17} /></button></form><button className="switch" onClick={() => setRegister(!register)}>{register ? 'Already have an account? Sign in' : 'New to RedFlag AI? Create an account'}</button></div></main>;
}

function UploadPage({ kind, onResult }: { kind: 'voice' | 'video' | 'calls'; onResult: (result: any) => void }) {
	const [file, setFile] = useState<File | null>(null); const [busy, setBusy] = useState(false); const [error, setError] = useState('');
	const title = kind === 'voice' ? 'Voice detection' : kind === 'video' ? 'Video deepfake detection' : 'Incoming call protection';
	const analyze = async () => { if (!file) return; setBusy(true); setError(''); try { onResult(await api.analyze(kind, file)); } catch (err) { setError((err as Error).message); } finally { setBusy(false); } };
	return <div className="content"><div className="page-heading"><div><div className="eyebrow">ANALYSIS WORKSPACE</div><h1>{title}</h1><p>{kind === 'calls' ? 'Analyze audio explicitly supplied by an authorized VoIP, SIP, mobile, or call-center integration.' : 'Upload a file to receive a transparent, experimental risk assessment.'}</p></div><span className="prototype"><Activity size={14} /> Prototype detection model</span></div><div className="upload-panel"><input id="file-upload" type="file" accept={kind === 'video' ? '.mp4,.mov,.avi,.mkv,.webm' : '.wav,.mp3,.m4a,.ogg'} onChange={event => setFile(event.target.files?.[0] ?? null)} /><label htmlFor="file-upload" className="dropzone"><Upload size={28} /><strong>{file ? file.name : 'Choose a file to analyze'}</strong><span>{file ? 'Ready for analysis' : 'Drag and drop or browse from your device'}</span></label>{error && <div className="error">{error}</div>}<button className="primary" disabled={!file || busy} onClick={analyze}>{busy ? 'Analyzing…' : `Analyze ${kind === 'calls' ? 'call' : 'file'}`} <ArrowRight size={17} /></button></div><div className="privacy-line"><LockKeyhole size={15} /> Only files you explicitly provide are analyzed. Browser-based call detection cannot intercept ordinary cellular calls.</div></div>;
}

function Dashboard({ scans, onPick }: { scans: Scan[]; onPick: (scan: Scan) => void }) {
	const [data, setData] = useState<any>({}); useEffect(() => { api.dashboard().then(setData).catch(() => undefined); }, [scans]);
	const stats = [['Total scans', data.total_scans ?? scans.length], ['High risk', data.high_risk ?? 0], ['Medium risk', data.medium_risk ?? 0], ['Low risk', data.low_risk ?? 0]];
	return <div className="content"><div className="page-heading"><div><div className="eyebrow">YOUR SIGNAL CONSOLE</div><h1>Good afternoon.</h1><p>Review your latest assessments and stay ahead of suspicious requests.</p></div><div className="live"><span /> System operational</div></div><div className="stats">{stats.map(([label, value]) => <div className="stat" key={label as string}><span>{label}</span><strong>{value as number}</strong><small>Across your workspace</small></div>)}</div><section className="section-head"><h2>Recent assessments</h2></section><div className="table">{scans.length === 0 ? <div className="empty"><ShieldCheck size={28} /><strong>No assessments yet</strong><span>Upload a voice or video file to begin.</span></div> : scans.slice(0, 8).map(scan => <button className="table-row" key={scan.id} onClick={() => onPick(scan)}><span className="file-icon">{scan.type === 'video' ? <FileVideo size={17} /> : <FileAudio size={17} />}</span><span className="file-name"><strong>{scan.filename}</strong><small>{scan.type} · {new Date(scan.created_at).toLocaleDateString()}</small></span><Risk level={scan.risk_level} score={scan.risk_score} /><ArrowRight size={17} /></button>)}</div></div>;
}

function Result({ result, onClose }: { result: any; onClose: () => void }) {
	const probability = result.ai_probability ?? result.deepfake_probability ?? 0;
	return <div className="modal-backdrop"><div className="result-modal"><button className="close" onClick={onClose}><X size={19} /></button><div className="eyebrow">SCAN RESULT</div><h1>{result.risk_score}<small>/100</small></h1><Risk level={result.risk_level} /><p className="prototype-copy">Prototype detection model · Results are experimental and should not be treated as definitive proof.</p><div className="result-grid"><div><span>AI probability</span><strong>{Math.round(probability * 100)}%</strong></div><div><span>Scan ID</span><strong>{String(result.scan_id ?? result.id).slice(0, 8)}…</strong></div></div><h3>Why this was flagged</h3>{(result.indicators ?? []).map((indicator: string) => <div className="indicator" key={indicator}><ShieldCheck size={15} />{indicator}</div>)}<button className="primary full" onClick={onClose}>Return to workspace <ArrowRight size={17} /></button></div></div>;
}

export function App() {
	const [authenticated, setAuthenticated] = useState(!!localStorage.getItem('token')); const [showAuth, setShowAuth] = useState(!!localStorage.getItem('seen')); const [page, setPage] = useState<Page>('dashboard'); const [scans, setScans] = useState<Scan[]>([]); const [result, setResult] = useState<any>(null); const [mobile, setMobile] = useState(false);
	useEffect(() => { if (authenticated) api.scans().then(setScans).catch(() => undefined); }, [authenticated, result]);
	if (!authenticated && !showAuth) return <Landing onAuth={() => { localStorage.setItem('seen', '1'); setShowAuth(true); }} />;
	if (!authenticated) return <Auth onDone={() => setAuthenticated(true)} />;
	const logout = () => { localStorage.removeItem('token'); setAuthenticated(false); setShowAuth(true); };
	return <div className="app-shell"><aside className={mobile ? 'open' : ''}><div className="brand"><span className="brand-mark"><ShieldCheck size={19} /></span> ScamShield</div><div className="workspace"><span className="avatar">{(localStorage.getItem('email') ?? 'A')[0].toUpperCase()}</span><span><strong>Personal workspace</strong><small>Prototype mode</small></span></div><nav>{nav.map(([id, label, Icon]) => <button className={page === id ? 'active' : ''} key={id} onClick={() => { setPage(id); setMobile(false); }}><Icon size={18} />{label}</button>)}</nav><button className="logout" onClick={logout}><LogOut size={17} /> Sign out</button></aside><main className="main"><header className="mobile-header"><button onClick={() => setMobile(!mobile)}><Menu size={21} /></button><div className="brand"><span className="brand-mark"><ShieldCheck size={17} /></span> ScamShield</div></header>{page === 'dashboard' && <Dashboard scans={scans} onPick={setResult} />}{(page === 'voice' || page === 'video' || page === 'calls') && <UploadPage kind={page} onResult={setResult} />}{page === 'history' && <div className="content"><div className="page-heading"><div><div className="eyebrow">AUDIT TRAIL</div><h1>Scan history</h1><p>Every assessment in your private workspace.</p></div></div><div className="table">{scans.map(scan => <button className="table-row" key={scan.id} onClick={() => setResult(scan)}><span className="file-name"><strong>{scan.filename}</strong><small>{new Date(scan.created_at).toLocaleString()}</small></span><Risk level={scan.risk_level} score={scan.risk_score} /></button>)}</div></div>}{page === 'settings' && <div className="content"><div className="page-heading"><div><div className="eyebrow">WORKSPACE</div><h1>Settings</h1><p>Privacy and integration boundaries.</p></div></div><div className="settings-box"><LockKeyhole size={22} /><div><h3>Private by design</h3><p>Raw uploads are analyzed temporarily and removed after processing. Scan metadata stays in your account until you delete it.</p></div></div></div>}</main>{result && <Result result={result} onClose={() => setResult(null)} />}</div>;
}
