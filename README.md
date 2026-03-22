<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="AI King - Aditya Raj ka Personal AI Assistant">
<title>AI King 👑 — Aditya Raj's AI</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>👑</text></svg>">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{--gold:#FFD700;--gold-dk:#B8860B;--gold-lt:#FFF8A0;--bg:#020408;--bg2:#050d15;--bg3:#071825;--cyan:#00f5ff;--text:#c8dce8;--dim:#4a6a7a;--border:rgba(0,245,255,0.12);}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html{font-size:16px;}
body{background:var(--bg);font-family:'Rajdhani',sans-serif;color:var(--text);min-height:100vh;overflow-x:hidden;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:rgba(0,245,255,.2);border-radius:4px;}
*{scrollbar-width:thin;scrollbar-color:rgba(0,245,255,.2) transparent;}

.bg-grid{position:fixed;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(rgba(0,245,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,245,255,.025) 1px,transparent 1px);background-size:44px 44px;animation:gridScroll 25s linear infinite;}
@keyframes gridScroll{to{background-position:0 44px;}}
.bg-glow{position:fixed;inset:0;z-index:0;pointer-events:none;background:radial-gradient(ellipse 60% 40% at 20% 20%,rgba(255,215,0,.04) 0%,transparent 60%),radial-gradient(ellipse 50% 50% at 80% 80%,rgba(0,245,255,.04) 0%,transparent 60%);}
.scanlines{position:fixed;inset:0;z-index:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.04) 2px,rgba(0,0,0,.04) 4px);}

.layout{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;max-width:840px;margin:0 auto;padding:0 20px;}

/* HEADER */
.hdr{display:flex;align-items:center;gap:14px;padding:18px 0 14px;border-bottom:1px solid var(--border);position:relative;flex-shrink:0;}
.hdr::after{content:'';position:absolute;bottom:-1px;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 0%,var(--gold) 30%,var(--cyan) 70%,transparent 100%);animation:shimmer 4s ease-in-out infinite;}
@keyframes shimmer{0%,100%{opacity:.4}50%{opacity:1}}
.logo svg{width:54px;height:54px;filter:drop-shadow(0 0 12px rgba(255,215,0,.7));animation:cpulse 3s ease-in-out infinite;}
@keyframes cpulse{0%,100%{filter:drop-shadow(0 0 8px rgba(255,215,0,.5))}50%{filter:drop-shadow(0 0 22px rgba(255,215,0,.9))}}
.htitle{font-family:'Orbitron',monospace;font-weight:900;font-size:clamp(17px,3vw,25px);background:linear-gradient(135deg,var(--gold),var(--gold-lt),var(--gold-dk));-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:4px;}
.hsub{font-size:11px;color:var(--dim);font-family:'Share Tech Mono',monospace;letter-spacing:2px;margin-top:3px;}
.hright{display:flex;flex-direction:column;align-items:flex-end;gap:7px;margin-left:auto;}
.spill{display:flex;align-items:center;gap:7px;background:rgba(0,255,136,.05);border:1px solid rgba(0,255,136,.2);border-radius:20px;padding:4px 12px;}
.sdot{width:7px;height:7px;border-radius:50%;background:#00ff88;box-shadow:0 0 8px #00ff88;animation:blink 2s ease-in-out infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.stxt{font-size:11px;color:#00ff88;font-family:'Share Tech Mono',monospace;letter-spacing:1px;}
.mctr{font-size:10px;color:var(--dim);font-family:'Share Tech Mono',monospace;}

/* PAGES */
.page{display:none;flex:1;flex-direction:column;}
.page.active{display:flex;}

/* SETUP */
#sp{align-items:center;justify-content:center;padding:32px 0;gap:22px;min-height:calc(100vh - 120px);}
.sh{text-align:center;}
.sc-emoji{font-size:60px;display:block;animation:float 3s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-10px) rotate(2deg)}}
.stag{font-family:'Share Tech Mono',monospace;font-size:12px;letter-spacing:3px;color:var(--dim);margin-top:8px;}
.scard{background:linear-gradient(135deg,rgba(255,215,0,.04),rgba(0,245,255,.03));border:1px solid rgba(255,215,0,.22);border-radius:16px;padding:28px 30px;width:100%;max-width:440px;position:relative;overflow:hidden;}
.scard::before{content:'';position:absolute;top:-2px;left:10%;right:10%;height:2px;background:linear-gradient(90deg,transparent,var(--gold),transparent);border-radius:2px;}
.sct{font-family:'Orbitron',monospace;font-size:14px;font-weight:700;color:var(--gold);letter-spacing:2px;margin-bottom:6px;}
.scd{font-size:14px;color:var(--dim);margin-bottom:20px;line-height:1.6;}
.flbl{font-size:11px;color:var(--gold-dk);font-family:'Share Tech Mono',monospace;letter-spacing:2px;display:block;margin-bottom:8px;}
.iw{position:relative;margin-bottom:14px;}
.iw input{width:100%;background:rgba(0,0,0,.3);border:1px solid var(--border);border-radius:10px;padding:12px 44px 12px 16px;color:var(--text);font-size:14px;font-family:'Share Tech Mono',monospace;outline:none;transition:border-color .2s,box-shadow .2s;letter-spacing:1px;}
.iw input:focus{border-color:rgba(255,215,0,.4);box-shadow:0 0 20px rgba(255,215,0,.08);}
.iw input::placeholder{color:var(--dim);font-size:12px;}
.tv{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--dim);cursor:pointer;font-size:15px;padding:4px;transition:color .2s;}
.tv:hover{color:var(--gold);}
.abtn{width:100%;background:linear-gradient(135deg,var(--gold-dk),var(--gold),var(--gold-lt));border:none;border-radius:12px;padding:14px;color:#000;font-family:'Orbitron',monospace;font-size:14px;font-weight:900;letter-spacing:3px;cursor:pointer;box-shadow:0 0 20px rgba(255,215,0,.35);transition:all .25s;position:relative;overflow:hidden;}
.abtn::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent 40%,rgba(255,255,255,.15) 50%,transparent 60%);transform:translateX(-100%);transition:transform .4s;}
.abtn:hover{box-shadow:0 0 35px rgba(255,215,0,.6);transform:translateY(-1px);}
.abtn:hover::after{transform:translateX(100%);}
.snote{text-align:center;font-size:13px;color:var(--dim);line-height:1.6;margin-top:14px;}
.snote a{color:var(--cyan);text-decoration:none;border-bottom:1px solid rgba(0,245,255,.3);}
.snote a:hover{color:#fff;}
.serr{font-size:12px;color:#ff6060;text-align:center;min-height:16px;font-family:'Share Tech Mono',monospace;margin-top:8px;}
.feats{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%;max-width:440px;}
.fi{background:rgba(0,245,255,.03);border:1px solid var(--border);border-radius:10px;padding:12px 14px;display:flex;align-items:center;gap:10px;}
.ficon{font-size:20px;}
.ftxt{font-size:13px;color:var(--text);font-weight:600;line-height:1.3;}
.ftxt span{display:block;font-size:11px;color:var(--dim);font-weight:400;}

/* CHAT */
#cp{gap:0;}
.wbanner{margin:14px 0 6px;background:linear-gradient(135deg,rgba(255,215,0,.05),rgba(0,245,255,.04));border:1px solid rgba(255,215,0,.2);border-radius:14px;padding:16px 20px;display:flex;align-items:center;gap:16px;flex-shrink:0;animation:fadeIn .5s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
.wbi{font-size:30px;animation:float 4s ease-in-out infinite;}
.wbt{flex:1;}
.wblbl{font-family:'Orbitron',monospace;font-size:10px;color:var(--gold);letter-spacing:2.5px;margin-bottom:5px;}
.wbm{font-size:16px;font-weight:600;line-height:1.55;}
.wbm .g{color:var(--gold);font-weight:700;}
.wbm .c{color:var(--cyan);}
.suggs{display:flex;gap:8px;padding:2px 0 10px;overflow-x:auto;scrollbar-width:none;flex-wrap:wrap;flex-shrink:0;}
.suggs::-webkit-scrollbar{display:none;}
.sgbtn{background:rgba(0,245,255,.05);border:1px solid var(--border);border-radius:20px;padding:6px 14px;font-size:13px;color:var(--cyan);font-family:'Rajdhani',sans-serif;font-weight:600;cursor:pointer;white-space:nowrap;transition:all .2s;}
.sgbtn:hover{background:rgba(0,245,255,.12);border-color:var(--cyan);box-shadow:0 0 12px rgba(0,245,255,.2);transform:translateY(-2px);}

.chat-msgs{flex:1;overflow-y:auto;padding:8px 0 12px;display:flex;flex-direction:column;gap:16px;}
.msg{display:flex;gap:10px;animation:msgIn .35s cubic-bezier(.34,1.56,.64,1);}
@keyframes msgIn{from{opacity:0;transform:translateY(14px) scale(.97)}to{opacity:1;transform:none}}
.msg.user{flex-direction:row-reverse;}
.av{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;border:1px solid;margin-top:2px;font-size:15px;}
.av.aav{background:radial-gradient(circle,rgba(255,215,0,.12),transparent);border-color:rgba(255,215,0,.35);box-shadow:0 0 10px rgba(255,215,0,.15);}
.av.uav{background:radial-gradient(circle,rgba(0,245,255,.12),transparent);border-color:rgba(0,245,255,.35);font-family:'Orbitron',monospace;font-size:11px;color:var(--cyan);font-weight:900;}
.bub{max-width:72%;padding:12px 16px;font-size:15px;line-height:1.7;word-break:break-word;}
.bub.ab{background:var(--bg3);border:1px solid rgba(255,215,0,.1);border-left:3px solid var(--gold-dk);border-radius:4px 16px 16px 16px;}
.bub.ub{background:#0a2035;border:1px solid rgba(0,245,255,.1);border-right:3px solid var(--cyan);border-radius:16px 4px 16px 16px;text-align:right;}
.blbl{font-size:9px;letter-spacing:2.5px;font-family:'Share Tech Mono',monospace;margin-bottom:5px;}
.ab .blbl{color:rgba(255,215,0,.5);}
.ub .blbl{color:rgba(0,245,255,.4);}
.tyb{display:flex;gap:5px;align-items:center;padding:4px 0;}
.tyb span{width:7px;height:7px;border-radius:50%;animation:td 1.2s ease-in-out infinite;}
.tyb span:nth-child(1){background:var(--gold);box-shadow:0 0 6px var(--gold);}
.tyb span:nth-child(2){background:var(--cyan);box-shadow:0 0 6px var(--cyan);animation-delay:.22s;}
.tyb span:nth-child(3){background:var(--gold);box-shadow:0 0 6px var(--gold);animation-delay:.44s;}
@keyframes td{0%,80%,100%{transform:scale(.65);opacity:.45}40%{transform:scale(1.2);opacity:1}}

.inp-sec{padding:12px 0 18px;border-top:1px solid var(--border);flex-shrink:0;position:relative;}
.inp-sec::before{content:'';position:absolute;top:-1px;left:15%;right:15%;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);}
.inp-box{display:flex;gap:10px;align-items:flex-end;background:var(--bg3);border:1px solid var(--border);border-radius:16px;padding:10px 10px 10px 18px;transition:border-color .25s,box-shadow .25s;}
.inp-box:focus-within{border-color:rgba(255,215,0,.35);box-shadow:0 0 24px rgba(255,215,0,.07);}
textarea{flex:1;background:transparent;border:none;outline:none;color:var(--text);font-size:15px;font-family:'Rajdhani',sans-serif;font-weight:500;resize:none;max-height:130px;min-height:24px;line-height:1.55;padding:3px 0;}
textarea::placeholder{color:var(--dim);}
.sbtn{width:44px;height:44px;background:linear-gradient(135deg,var(--gold-dk),var(--gold));border:none;border-radius:12px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;box-shadow:0 0 16px rgba(255,215,0,.3);transition:all .2s;}
.sbtn:hover{transform:scale(1.06) rotate(-3deg);box-shadow:0 0 28px rgba(255,215,0,.55);}
.sbtn:active{transform:scale(.94);}
.sbtn svg{width:20px;height:20px;fill:#000;}
.iftr{display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding:0 4px;}
#stxt{font-size:11px;color:var(--dim);font-family:'Share Tech Mono',monospace;}
.abtns{display:flex;gap:8px;}
.tbtn{background:none;border:1px solid rgba(255,80,80,.18);border-radius:7px;color:rgba(255,80,80,.45);font-size:11px;padding:3px 10px;cursor:pointer;font-family:'Share Tech Mono',monospace;transition:all .2s;}
.tbtn:hover{border-color:rgba(255,80,80,.5);color:rgba(255,80,80,.9);background:rgba(255,80,80,.05);}
.tbtn.sk{border-color:rgba(255,215,0,.18);color:rgba(255,215,0,.45);}
.tbtn.sk:hover{border-color:rgba(255,215,0,.5);color:rgba(255,215,0,.9);background:rgba(255,215,0,.05);}

.site-footer{text-align:center;padding:10px 0 16px;font-size:11px;color:var(--dim);font-family:'Share Tech Mono',monospace;letter-spacing:1px;border-top:1px solid var(--border);flex-shrink:0;}
.site-footer a{color:rgba(255,215,0,.5);text-decoration:none;}
.site-footer a:hover{color:var(--gold);}

.corner{position:fixed;width:48px;height:48px;pointer-events:none;z-index:2;}
.corner.tl{top:10px;left:10px;border-top:2px solid rgba(255,215,0,.22);border-left:2px solid rgba(255,215,0,.22);}
.corner.tr{top:10px;right:10px;border-top:2px solid rgba(0,245,255,.18);border-right:2px solid rgba(0,245,255,.18);}
.corner.bl{bottom:10px;left:10px;border-bottom:2px solid rgba(0,245,255,.18);border-left:2px solid rgba(0,245,255,.18);}
.corner.br{bottom:10px;right:10px;border-bottom:2px solid rgba(255,215,0,.22);border-right:2px solid rgba(255,215,0,.22);}

@media(max-width:600px){.layout{padding:0 12px;}.htitle{font-size:17px;}.bub{max-width:86%;font-size:14px;}.feats{grid-template-columns:1fr;}.scard{padding:22px 18px;}}
</style>
</head>
<body>
<div class="bg-grid"></div><div class="bg-glow"></div><div class="scanlines"></div>
<div class="corner tl"></div><div class="corner tr"></div><div class="corner bl"></div><div class="corner br"></div>

<div class="layout">

<!-- HEADER -->
<header class="hdr">
  <div class="logo">
    <svg viewBox="0 0 56 56" fill="none">
      <path d="M9 40h38v5a2 2 0 01-2 2H11a2 2 0 01-2-2v-5z" fill="url(#base)"/>
      <path d="M9 40L7 19l11.5 12.5L28 9l9.5 22.5L49 19 47 40H9z" fill="url(#body)"/>
      <circle cx="15" cy="43" r="2.8" fill="#ff4466"/>
      <circle cx="28" cy="43" r="2.8" fill="#00ccff"/>
      <circle cx="41" cy="43" r="2.8" fill="#ff4466"/>
      <circle cx="7" cy="19" r="2.8" fill="#FFE55C"/>
      <circle cx="28" cy="9" r="3.2" fill="#FFF0A0"/>
      <circle cx="49" cy="19" r="2.8" fill="#FFE55C"/>
      <defs>
        <linearGradient id="base" x1="9" y1="40" x2="47" y2="47" gradientUnits="userSpaceOnUse"><stop stop-color="#8B6914"/><stop offset=".4" stop-color="#FFD700"/><stop offset="1" stop-color="#8B6914"/></linearGradient>
        <linearGradient id="body" x1="7" y1="9" x2="49" y2="40" gradientUnits="userSpaceOnUse"><stop stop-color="#FFF0A0"/><stop offset=".45" stop-color="#FFD700"/><stop offset="1" stop-color="#B8860B"/></linearGradient>
      </defs>
    </svg>
  </div>
  <div><div class="htitle">AI KING</div><div class="hsub">ADITYA RAJ'S PERSONAL AI</div></div>
  <div class="hright">
    <div class="spill"><div class="sdot"></div><span class="stxt">ONLINE</span></div>
    <div class="mctr" id="mc">0 MESSAGES</div>
  </div>
</header>

<!-- SETUP PAGE -->
<div id="sp" class="page active">
  <div class="sh"><span class="sc-emoji">👑</span><div class="stag">// AWAITING AUTHORIZATION</div></div>
  <div class="scard">
    <div class="sct">// API KEY SETUP</div>
    <div class="scd">AI King ko activate karne ke liye apni Anthropic API key daalo. Key sirf tumhare browser mein safe rehti hai.</div>
    <label class="flbl" for="aki">// ANTHROPIC API KEY</label>
    <div class="iw">
      <input type="password" id="aki" placeholder="sk-ant-api03-..." autocomplete="off" spellcheck="false" onkeydown="if(event.key==='Enter')activate()"/>
      <button class="tv" onclick="toggleVis()">👁</button>
    </div>
    <button class="abtn" onclick="activate()">👑 ACTIVATE AI KING</button>
    <div class="serr" id="se"></div>
    <div class="snote">Free API key: <a href="https://console.anthropic.com/keys" target="_blank" rel="noopener">console.anthropic.com/keys</a><br><small style="color:var(--dim);font-size:11px">Key localStorage mein save hoti hai — server pe nahi jaati</small></div>
  </div>
  <div class="feats">
    <div class="fi"><div class="ficon">🧠</div><div class="ftxt">Smart AI<span>Kisi bhi sawaal ka jawab</span></div></div>
    <div class="fi"><div class="ficon">💬</div><div class="ftxt">Hindi Support<span>Hindi & Hinglish mein</span></div></div>
    <div class="fi"><div class="ficon">🔒</div><div class="ftxt">100% Private<span>Browser mein stored</span></div></div>
    <div class="fi"><div class="ficon">⚡</div><div class="ftxt">Fast AI<span>Claude Haiku powered</span></div></div>
  </div>
</div>

<!-- CHAT PAGE -->
<div id="cp" class="page">
  <div class="wbanner" id="wb">
    <div class="wbi">👑</div>
    <div class="wbt">
      <div class="wblbl">// INITIALIZED · READY</div>
      <div class="wbm">नमस्ते! मैं <span class="g">Aditya Raj</span> का AI हूँ।<br>मैं आपकी <span class="c">क्या मदद कर सकता हूँ?</span></div>
    </div>
  </div>
  <div class="suggs" id="sgs">
    <button class="sgbtn" onclick="usg(this)">🤖 तुम कौन हो?</button>
    <button class="sgbtn" onclick="usg(this)">💡 Python code लिखो</button>
    <button class="sgbtn" onclick="usg(this)">📖 कहानी सुनाओ</button>
    <button class="sgbtn" onclick="usg(this)">🌍 भारत के बारे में</button>
    <button class="sgbtn" onclick="usg(this)">🎯 Career advice</button>
    <button class="sgbtn" onclick="usg(this)">✍️ Essay mein help</button>
  </div>
  <div class="chat-msgs" id="cm"></div>
  <div class="inp-sec">
    <div class="inp-box">
      <textarea id="ci" placeholder="अपना सवाल यहाँ लिखें... (Enter = Send)" rows="1" onkeydown="hk(event)" oninput="ar(this)"></textarea>
      <button class="sbtn" onclick="send()"><svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg></button>
    </div>
    <div class="iftr">
      <span id="stxt">👑 AI King taiyaar hai</span>
      <div class="abtns">
        <button class="tbtn sk" onclick="goSettings()">⚙ KEY</button>
        <button class="tbtn" onclick="clrChat()">🗑 CLEAR</button>
      </div>
    </div>
  </div>
</div>

<footer class="site-footer">Made with ❤️ by <a href="https://github.com/adityarajai" target="_blank">Aditya Raj</a> &nbsp;·&nbsp; Powered by Claude AI</footer>
</div>

<script>
const SYS=`Tum "AI King" ho — Aditya Raj ka personal AI assistant.

Identity:
- Naam: AI King 👑
- Creator: Aditya Raj
- Website: adityarajai.github.io/AI-King
- Style: Smart, helpful, friendly, royal

Rules:
1. Hindi ya Hinglish use karo (jo user use kare)
2. Pichli baatein yaad rakho aur reference karo
3. Coding, GK, writing, math — sab mein expert ho
4. Focused answers do — unnecessary padding nahi
5. Markdown: **bold**, \`code\`, lists — jab relevant ho
6. Identity question → "Main AI King hoon, Aditya Raj ka personal AI! 👑"`;

let hist=[],busy=false,total=0,apiKey='';

// Init
(function(){
  apiKey=localStorage.getItem('aikng_k')||'';
  if(apiKey){showChat();loadHist();}
  document.getElementById('ci')?.focus();
})();

function loadHist(){
  try{
    const s=localStorage.getItem('aikng_h');
    if(s){hist=JSON.parse(s);hist.forEach(m=>addMsg(m.role,m.content,false));if(hist.length)hw();}
  }catch(e){hist=[];}
}
function saveHist(){localStorage.setItem('aikng_h',JSON.stringify(hist.slice(-30)));}

function showChat(){
  document.getElementById('sp').classList.remove('active');
  document.getElementById('cp').classList.add('active');
  setTimeout(()=>document.getElementById('ci')?.focus(),150);
}
function showSetup(){
  document.getElementById('cp').classList.remove('active');
  document.getElementById('sp').classList.add('active');
  document.getElementById('aki').value=apiKey||'';
}
function goSettings(){showSetup();}

function toggleVis(){const i=document.getElementById('aki');i.type=i.type==='password'?'text':'password';}

function activate(){
  const k=document.getElementById('aki').value.trim();
  const e=document.getElementById('se');
  if(!k){e.textContent='⚠️ API key daalo!';return;}
  if(!k.startsWith('sk-ant-')){e.textContent='⚠️ Valid key chahiye (sk-ant-... se start)';return;}
  e.textContent='';apiKey=k;localStorage.setItem('aikng_k',k);showChat();
}

function ar(el){el.style.height='auto';el.style.height=Math.min(el.scrollHeight,130)+'px';}
function hk(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}}
function usg(btn){
  const t=btn.textContent.replace(/^[\s\S]{1,3}/,'').trim();
  document.getElementById('ci').value=t;
  document.getElementById('sgs').style.display='none';
  send();
}
function hw(){document.getElementById('wb').style.display='none';document.getElementById('sgs').style.display='none';}

function fmt(t){
  return t
    .replace(/\*\*(.*?)\*\*/g,'<strong style="color:var(--gold)">$1</strong>')
    .replace(/`([^`\n]+)`/g,'<code style="background:rgba(0,245,255,.1);padding:2px 7px;border-radius:5px;font-family:\'Share Tech Mono\',monospace;color:var(--cyan);font-size:13px">$1</code>')
    .replace(/^- (.+)$/gm,'<div style="display:flex;gap:8px;margin:3px 0"><span style="color:var(--gold-dk)">▸</span><span>$1</span></div>')
    .replace(/\n/g,'<br>');
}

function addMsg(role,txt,anim=true){
  const isAI=role==='assistant';
  const c=document.getElementById('cm');
  const d=document.createElement('div');
  d.className='msg'+(isAI?'':' user');
  if(!anim)d.style.animation='none';
  d.innerHTML=`<div class="av ${isAI?'aav':'uav'}">${isAI?'👑':'U'}</div><div class="bub ${isAI?'ab':'ub'}"><div class="blbl">${isAI?'// AI KING':'// YOU'}</div>${fmt(txt)}</div>`;
  c.appendChild(d);c.scrollTop=c.scrollHeight;
  total++;document.getElementById('mc').textContent=total+' MESSAGES';
}

function showTy(){
  const c=document.getElementById('cm');
  const d=document.createElement('div');
  d.className='msg';d.id='ty';
  d.innerHTML=`<div class="av aav">👑</div><div class="bub ab"><div class="blbl">// AI KING</div><div class="tyb"><span></span><span></span><span></span></div></div>`;
  c.appendChild(d);c.scrollTop=c.scrollHeight;
}
function rmTy(){document.getElementById('ty')?.remove();}
function setSt(t){document.getElementById('stxt').textContent=t;}

async function send(){
  const inp=document.getElementById('ci');
  const txt=inp.value.trim();
  if(!txt||busy)return;
  busy=true;inp.value='';inp.style.height='auto';
  hw();addMsg('user',txt);hist.push({role:'user',content:txt});
  showTy();setSt('⚡ Soch raha hoon...');
  try{
    const res=await fetch('https://api.anthropic.com/v1/messages',{
      method:'POST',
      headers:{'Content-Type':'application/json','x-api-key':apiKey,'anthropic-version':'2023-06-01','anthropic-dangerous-direct-browser-access':'true'},
      body:JSON.stringify({model:'claude-3-5-haiku-20241022',max_tokens:1024,system:SYS,messages:hist})
    });
    if(!res.ok){
      const e=await res.json().catch(()=>({}));
      if(res.status===401)throw new Error('Invalid API key! ⚙ KEY se update karo.');
      if(res.status===429)throw new Error('Rate limit! Thoda ruko.');
      throw new Error(e?.error?.message||'HTTP '+res.status);
    }
    const data=await res.json();
    const reply=data.content?.[0]?.text||'Kuch galat ho gaya, dobara try karo!';
    rmTy();hist.push({role:'assistant',content:reply});addMsg('assistant',reply);setSt('👑 AI King taiyaar hai');saveHist();
  }catch(err){
    rmTy();
    const m='⚠️ '+(err.message||'Connection fail. Internet check karo!');
    addMsg('assistant',m);hist.push({role:'assistant',content:m});setSt('❌ Error');
  }
  busy=false;inp.focus();
}

function clrChat(){
  if(!confirm('Poori chat clear karna chahte ho?'))return;
  document.getElementById('cm').innerHTML='';
  hist=[];total=0;localStorage.removeItem('aikng_h');
  document.getElementById('wb').style.display='flex';
  document.getElementById('sgs').style.display='flex';
  document.getElementById('mc').textContent='0 MESSAGES';
  setSt('👑 AI King taiyaar hai');
}
</script>
</body>
</html>
