<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI King Pro</title>
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#060a0f;
  --surface:#0d1117;
  --surface2:#111820;
  --border:#1e2d3d;
  --accent:#00e5ff;
  --accent2:#7b61ff;
  --text:#e8edf2;
  --text-dim:#8899aa;
  --user-bg:#132233;
  --ai-bg:#0d1a1f;
  --danger:#ff4466;
  --success:#00ffaa;
}

/* ── CRITICAL layout reset ── */
html, body { height: 100%; width: 100%; }

body {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  color: var(--text);
  font-family: 'Noto Sans Devanagari', system-ui;
  /* NO overflow:hidden — it kills scroll */
}

.bg-grid {
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none; /* MUST be none */
  z-index: 0;
}

header {
  flex-shrink: 0;
  padding: 12px 18px;
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(135deg, #0d1117, #0a1520);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 2px 20px rgba(0,229,255,0.08);
  position: relative; z-index: 10;
}
.logo { display: flex; align-items: center; gap: 10px; }
.logo-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: 18px; box-shadow: 0 0 15px rgba(0,229,255,0.3);
}
.logo-text {
  font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 1px;
}
.logo-badge {
  font-size: 10px; background: var(--accent2); color: #fff;
  padding: 2px 6px; border-radius: 6px;
  font-family: 'Rajdhani', sans-serif; font-weight: 600;
}
.header-actions { display: flex; gap: 8px; }
.hbtn {
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text-dim); padding: 7px 12px; border-radius: 10px;
  cursor: pointer; font-size: 13px; transition: all .2s;
  display: flex; align-items: center; gap: 5px;
}
.hbtn:hover { border-color: var(--accent); color: var(--accent); }

#status-bar {
  flex-shrink: 0;
  background: rgba(0,229,255,0.05); border-bottom: 1px solid var(--border);
  padding: 6px 18px; font-size: 11px; color: var(--text-dim);
  display: flex; align-items: center; gap: 6px;
  position: relative; z-index: 10;
}
#status-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--success); box-shadow: 0 0 6px var(--success);
  animation: pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

#camera-container {
  display: none; flex-shrink: 0;
  background: #000; border-bottom: 2px solid var(--accent);
  max-height: 200px; overflow: hidden;
  position: relative; z-index: 10;
}
#camera-container video { width: 100%; max-height: 200px; object-fit: cover; opacity: .85; }
#camera-overlay { position: absolute; inset: 0; border: 2px solid rgba(0,229,255,.3); pointer-events: none; }
#camera-overlay::before, #camera-overlay::after {
  content: ''; position: absolute; width: 20px; height: 20px;
  border-color: var(--accent); border-style: solid;
}
#camera-overlay::before { top:8px; left:8px; border-width: 2px 0 0 2px; }
#camera-overlay::after  { bottom:8px; right:8px; border-width: 0 2px 2px 0; }
.camera-controls { position: absolute; bottom: 8px; right: 8px; display: flex; gap: 6px; z-index: 11; }
.cam-btn {
  background: rgba(0,0,0,.7); border: 1px solid var(--accent); color: var(--accent);
  padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 12px;
}

/* ════ CHAT — THE SCROLL FIX ════
   flex:1 + min-height:0 = takes remaining space
   overflow-y:auto = THIS div scrolls, nothing else
   NO z-index, NO position on this element
*/
#chat {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
#chat::-webkit-scrollbar { width: 5px; }
#chat::-webkit-scrollbar-track { background: transparent; }
#chat::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
#chat::-webkit-scrollbar-thumb:hover { background: var(--accent2); }

.msg {
  padding: 13px 17px; border-radius: 16px;
  max-width: 82%; word-wrap: break-word;
  line-height: 1.6; font-size: 14.5px;
  animation: msgIn .25s ease-out;
  position: relative;
  flex-shrink: 0; /* prevent compression */
}
@keyframes msgIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

.user {
  background: linear-gradient(135deg, var(--user-bg), #1a2f42);
  align-self: flex-end;
  border: 1px solid rgba(0,229,255,.15); border-bottom-right-radius: 4px;
}
.ai {
  background: var(--ai-bg); border: 1px solid var(--border);
  border-left: 3px solid var(--accent); border-bottom-left-radius: 4px;
  align-self: flex-start;
}
.ai.thinking { border-left-color: var(--accent2); }

.dots span {
  display: inline-block; width: 6px; height: 6px;
  background: var(--accent); border-radius: 50%; margin: 0 2px;
  animation: dotBounce .9s infinite;
}
.dots span:nth-child(2){animation-delay:.15s}
.dots span:nth-child(3){animation-delay:.3s}
@keyframes dotBounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}

.typing-cursor::after{content:'▋';color:var(--accent);animation:blink .7s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

.msg img.snap { max-width: 100%; border-radius: 10px; margin-top: 8px; border: 1px solid var(--border); }

.copy-btn {
  position: absolute; top: 8px; right: 8px;
  background: var(--surface2); border: 1px solid var(--border);
  color: var(--text-dim); padding: 3px 8px; border-radius: 6px;
  font-size: 11px; cursor: pointer; opacity: 0; transition: opacity .2s;
}
.msg:hover .copy-btn { opacity: 1; }
.copy-btn:hover { color: var(--accent); border-color: var(--accent); }

#history-panel {
  position: fixed; top: 0; right: -320px;
  width: 300px; height: 100vh;
  background: var(--surface); border-left: 1px solid var(--border);
  z-index: 200; display: flex; flex-direction: column;
  box-shadow: -10px 0 30px rgba(0,0,0,.5);
  transition: right .3s ease;
}
#history-panel.open { right: 0; }
.history-header {
  flex-shrink: 0; padding: 16px; border-bottom: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  font-family: 'Rajdhani',sans-serif; font-size: 16px; font-weight: 700; color: var(--accent);
}
#history-list { flex: 1; overflow-y: auto; padding: 12px; }
.history-item {
  padding: 10px 12px; border-radius: 10px; border: 1px solid var(--border);
  margin-bottom: 8px; cursor: pointer; font-size: 12px; color: var(--text-dim); transition: .2s;
}
.history-item:hover { border-color: var(--accent); color: var(--text); }
.history-item .h-time { font-size: 10px; color: var(--accent2); margin-bottom: 4px; }

.bottom {
  flex-shrink: 0;
  background: linear-gradient(0deg, var(--surface), rgba(13,17,23,.97));
  border-top: 1px solid var(--border); padding: 12px 14px;
  position: relative; z-index: 10;
}

#voice-wave{display:none;height:36px;align-items:center;justify-content:center;gap:3px;margin-bottom:10px;}
#voice-wave.active{display:flex;}
#voice-wave span{display:block;width:3px;background:var(--accent);border-radius:3px;animation:wave 1s ease-in-out infinite;}
#voice-wave span:nth-child(1){height:10px}
#voice-wave span:nth-child(2){height:20px;animation-delay:.1s}
#voice-wave span:nth-child(3){height:30px;animation-delay:.2s}
#voice-wave span:nth-child(4){height:20px;animation-delay:.3s}
#voice-wave span:nth-child(5){height:14px;animation-delay:.4s}
#voice-wave span:nth-child(6){height:26px;animation-delay:.15s}
#voice-wave span:nth-child(7){height:18px;animation-delay:.25s}
#voice-wave span:nth-child(8){height:10px;animation-delay:.35s}
@keyframes wave{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.8)}}

#speak-indicator{display:none;align-items:center;gap:6px;font-size:11px;color:var(--accent2);padding:4px 0;}
#speak-indicator.active{display:flex;}

.input-row{display:flex;gap:8px;align-items:flex-end;}

#input {
  flex: 1; padding: 13px 16px; border-radius: 14px;
  border: 1px solid var(--border); background: var(--surface2);
  color: var(--text); font-size: 14px;
  font-family: 'Noto Sans Devanagari', system-ui;
  resize: none; outline: none;
  transition: border-color .2s, box-shadow .2s;
  min-height: 48px; max-height: 120px;
}
#input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(0,229,255,.08);}

.action-btn {
  border: none; border-radius: 12px;
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all .2s; font-size: 18px; flex-shrink: 0;
}
#send-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#000;box-shadow:0 4px 15px rgba(0,229,255,.2);}
#send-btn:hover{transform:scale(1.05);}
#send-btn:active{transform:scale(.96);}
#mic-btn{background:var(--surface2);border:1px solid var(--border);color:var(--text-dim);}
#mic-btn.recording{background:rgba(255,68,102,.15);border-color:var(--danger);color:var(--danger);animation:micPulse 1s infinite;}
@keyframes micPulse{0%,100%{box-shadow:0 0 0 0 rgba(255,68,102,.3)}50%{box-shadow:0 0 0 8px rgba(255,68,102,0)}}
#cam-btn{background:var(--surface2);border:1px solid var(--border);color:var(--text-dim);}
#cam-btn.active{border-color:var(--accent);color:var(--accent);}

#toast {
  position: fixed; bottom: 90px; left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: var(--surface2); border: 1px solid var(--accent);
  color: var(--text); padding: 8px 18px; border-radius: 20px;
  font-size: 13px; opacity: 0; transition: .3s; z-index: 300; pointer-events: none;
}
#toast.show{opacity:1;transform:translateX(-50%) translateY(0);}
</style>
</head>
<body>

<div class="bg-grid"></div>

<header>
  <div class="logo">
    <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCABQAFADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD45RKnjjoiSrcCcivRhA5p1BiQnGcZqVYvavZfhbb/AA81v4eeI9M8QWVxDr2m2xvrG4tBmSePgOrA/LhCVYnghSTzivPNW0O+0y5EV7ZzWxcbkEybSV9cHp+NaUpRnKUVujmqylBJvZlPw54d1DX9Vt9M0y3a4uriQRxRr1ZicAUeJfDmo+H9WuNK1S3e3u7aRo5Y26qwOCK+gf2b/Dd34T8eaLqmoy6GNQnKmHR7q72XrxyDiRUxhX2ncquQWA4HIpf2j/DV54u8f6zqWmzaH/aMDN5mj213uvRGg5kZMYZyo3MiEsoPI4NR7aHteS+gWn7PnPmZoqjeA4ziul0rQ77U7vyLGzmumUbmWJNxx9B1r0j4l2/w70T4Z+HbHQ7K4m8Q6rD9rvJrsYe3iBZVCgfLh2BIPJKrnjNVVlGElF7vT/hwpTc02uh4TJHUDp2rTnj5OKqSJzxUTgdNOpcnhTirsCDANQQL2rRt06ZropxOSrI1/Aerjw74w0/VZcm2STZdKP4oHBSUf98M36V7XoMUFl4lS61ZrE6sl47TzrZRzbreOSRiwWRjw4RtzqGYb1A2qOfBnh3J6ivXvA8N74l0izSP+1rhprNYLuO0tGlBdP3asGkkjiDbEjzndyASMgV5max9lad7J6N/1/Wx15e1WTg1drY7H4dwaZPrFrq2rQ6bd31lqNzrK6rFdo7ag3DoJCpMiIhAyuwdhwflKfEi30xNSvdU0m30y11HUL+21g6pNeJGdNf77+WWIkZHYkhdhPUct8o9B8JeCdchuYb5tL1pStwJ387UdPgExzlkcKrkoxLFlJ5LEnthPFfgfXJ7q4vhpOsuXnM6rFqWnzCHkFUjDKhVF2phQeCg988Cxcb+05lb10/r+tjV0Hbks7nl2upbX+uT3mlCxk1mS7R7OZrGOAeRK8bAlY2BwgkTDsqt8rL8wbjxT4iaz/wknjLUNViYm1MghtB0xBGAkf5qoP1Jr1PxtBfeFtHvEkTWbQw2jxWkd5ZmNTI/yby8UrxFgruR935iSBkk142kG2MDGK9DK4+1vO90tE/6/rVmOPaopRtZvczJo+pNUZkwa1rheDVCdD6V6VSJy0pj7ccitG2HIrOtzyK6LwzpN9rOpW+n6bbSXN1cOI4oo1yzsegFaUlcxrtJXYsajZ+Faena3JPp9vpM+tajpC2wKI8BZoZFJyN6oQwPPUbhjsKt+IPCmueG9V/snW9Pnsr3ap8mUYbB6U3xD4T1fw/qYsNb06awuyiyeVMuG2t0OPerr4SNdR5umq/r5nNh8c8O5cr30ZcsfD0l380firQbgnvLqvlN+Il2mlvvDsloN0vinQYPeLVRKfyi3Gnaj4R1zR4bJ9SsLm0S+hE1sZBjzYz0ZfUc1sxfCvxtdajBpi6BffbLi3NzFCy7WaIfx4J6dsnvT+rVOW3Mren/AAf0MfrlPnvZ39f+Acfe65Nb6fcaRb63qWrJdAJI05dYI1yCdiuSxPGMnaMdjWXMo21fvNLktLmSGWMpJGxVlI5BHUVUnjYDGKKGEjh07bvV/wBI2rY14lxvsloZNyOTWdOK07pGBJIrMuDzWdRHVRYy3PIzXv37JkNlZeL7zxbqag2Xh6wlvCMZLSbSEUD1+8fwr58tT81el+HPiGvg7wI1t4fvUXXbi6DyhoSRGo4HUYPA9f4vaslK0HbrobTpc80vmeufHjVT4y8EeDfiHJb/AGe/ubY2WpxBCnlzox7Hpn58fhWX+1PfRz/F24liYMg020xz38s1w8XxWn8T+DtY0rxjqKm7YpJZOsBALLyB8oPORjJ7N7Vn/EnxNZeJPE82p6fc/aITaxRbyrL8yggjBAPpWtCo+aK7X/Q5MTh7Rm+9j6vstL0/UNG8IeML60OqQ6B4TheHTYiDJd3SqGVMHsMA+5x16V438J9c1v4g/G241TXPEWraTd38VxI0+nT+U8SJGxWFMggIOmCPfrzXDa18Tp7O/wDCF/oOpSynR7ERXEGWVCSFV0OeuVGMjpgVt23jrwfafEGDxXp+oeRHPBKLuMW7jypXXGcAfxc5xkA57EVEJy5WnvZ2KnQSlFx2bV/0/r/gnWaLp3wu0z4WaT438by65czXd7NaNa2RVmmZCectjaMDJJPJraufhp8OZPGyXialfp4T/wCEd/t+RMZuPL/55jjr39e3vXg/iLxPZX/wx0nw3Fclru01Ce4eLY3yq4bBzjHcV1Nr8SdJ/tGwgaS6u7CTw4NJvmgifdAAeeMZI6jIzjIPNXPEVbt37kQwNKySXY6PxHonwf8AEHwm8TeMvBi+Iba50uS3hWzvigCNI4G7IzuUqfUEEV8633DnFewXl14bsPhB4ksfDEmoyWlxNAZZ7wbfNdXTAQYHAHt1NeNXj5J5rN1HJO7OuFFQasrFSN8c/wAqVfmlJOarIxA5qaN+a5oyudrjYmUESqR0rQ09ykBX1rPV6nSTA9K2g7O5z1E5KxNGOHz3NNQfu3XB5IpN4xnmk8wetXdGdmSqT9oZ8nBFSaNrepeH743+lXHkXGCm7bnKt1HP0FVDLgdarzNuBGaibujSnFpmx4k8ZeIPEMaQanfeZCpDCNFCqSOhPrisWaTNRwrGZVEknlqerbc4/CluVgWPMd15h9PLK/zrByUUdXLdn//Z" style="width:42px;height:42px;border-radius:10px;object-fit:cover;box-shadow:0 0 15px rgba(0,229,255,0.3);">
    <span class="logo-text">AI KING</span>
    <span class="logo-badge">PRO</span>
  </div>
  <div class="header-actions">
    <button class="hbtn" id="history-btn">📋 History</button>
    <button class="hbtn" id="clear-btn">🗑️ Clear</button>
  </div>
</header>

<div id="status-bar">
  <div id="status-dot"></div>
  <span id="status-text">AI King तैयार है</span>
</div>

<div id="camera-container">
  <video id="camera-feed" autoplay playsinline muted></video>
  <div id="camera-overlay"></div>
  <div class="camera-controls">
    <button class="cam-btn" id="capture-btn">📸 Capture</button>
    <button class="cam-btn" id="close-cam-btn">✕ बंद</button>
  </div>
</div>

<div id="chat">
  <div class="msg ai">
    नमस्ते! 🙏 मैं Aditya Raj का AI हूँ, लेकिन मैं आपकी कैसे सहायता कर सकता हूँ?
  </div>
</div>

<div id="history-panel">
  <div class="history-header">
    <span>📋 Chat History</span>
    <button class="hbtn" id="close-history-btn">✕</button>
  </div>
  <div id="history-list"></div>
  <div style="padding:12px;border-top:1px solid var(--border);flex-shrink:0;">
    <button class="hbtn" id="clear-history-btn" style="width:100%;justify-content:center;">🗑️ सब Delete करो</button>
  </div>
</div>

<div class="bottom">
  <div id="voice-wave">
    <span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span><span></span>
  </div>
  <div id="speak-indicator"><span>🔊</span> AI बोल रहा है...</div>
  <div class="input-row">
    <button class="action-btn" id="mic-btn">🎤</button>
    <button class="action-btn" id="cam-btn">📷</button>
    <textarea id="input" placeholder="लिखो या माइक से बोलो..." rows="1"></textarea>
    <button class="action-btn" id="send-btn">➤</button>
  </div>
</div>

<div id="toast"></div>

<script>
document.addEventListener("DOMContentLoaded", function () {

  var chatEl     = document.getElementById("chat");
  var inputEl    = document.getElementById("input");
  var statusText = document.getElementById("status-text");
  var voiceWave  = document.getElementById("voice-wave");
  var speakInd   = document.getElementById("speak-indicator");

  /* ── SCROLL: most reliable method for Chrome ── */
  function scrollToBottom() {
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  /* ── TOAST ── */
  function showToast(msg) {
    var t = document.getElementById("toast");
    t.textContent = msg; t.classList.add("show");
    setTimeout(function(){ t.classList.remove("show"); }, 2500);
  }

  /* ── STATUS ── */
  function setStatus(msg, pulse) {
    statusText.textContent = msg;
    document.getElementById("status-dot").style.background =
      pulse ? "var(--accent)" : "var(--success)";
  }

  /* ── COPY BTN ── */
  function makeCopyBtn(parentEl) {
    var cb = document.createElement("button");
    cb.className = "copy-btn"; cb.textContent = "Copy";
    cb.addEventListener("click", function(e) {
      e.stopPropagation();
      var txt = parentEl.innerText.replace(/Copy$/, "").trim();
      navigator.clipboard.writeText(txt).then(function(){ showToast("✅ Copied!"); });
    });
    return cb;
  }

  /* ── ADD MESSAGE ── */
  function addMsg(text, cls, imgSrc) {
    var d = document.createElement("div");
    d.className = "msg " + cls;
    if (imgSrc) {
      var img = document.createElement("img");
      img.className = "snap"; img.src = imgSrc; d.appendChild(img);
      if (text) {
        var p = document.createElement("p");
        p.style.marginTop = "8px"; p.textContent = text; d.appendChild(p);
      }
    } else {
      d.textContent = text;
    }
    d.appendChild(makeCopyBtn(d));
    chatEl.appendChild(d);
    scrollToBottom();
    return d;
  }

  /* ── TYPING ANIMATION ── */
  async function typeText(el, text) {
    el.classList.add("typing-cursor");
    el.textContent = "";
    for (var i = 0; i < text.length; i++) {
      el.textContent += text[i];
      scrollToBottom();
      await new Promise(function(r){ setTimeout(r, 16); });
    }
    el.classList.remove("typing-cursor");
    el.appendChild(makeCopyBtn(el));
    scrollToBottom();
  }

  /* ── HISTORY ── */
  var chatHistory = [];
  try { chatHistory = JSON.parse(localStorage.getItem("aiking_history") || "[]"); } catch(e){}

  function saveToHistory(u, a) {
    chatHistory.unshift({
      time: new Date().toLocaleString("hi-IN"),
      user: u.substring(0,60) + (u.length>60?"...":""),
      ai:   a.substring(0,80) + (a.length>80?"...":""),
      full_user:u, full_ai:a
    });
    if (chatHistory.length > 50) chatHistory = chatHistory.slice(0,50);
    try { localStorage.setItem("aiking_history", JSON.stringify(chatHistory)); } catch(e){}
  }

  function renderHistory() {
    var list = document.getElementById("history-list");
    list.innerHTML = "";
    if (!chatHistory.length) {
      list.innerHTML = '<div style="color:var(--text-dim);text-align:center;padding:30px;font-size:13px;">कोई history नहीं</div>';
      return;
    }
    chatHistory.forEach(function(h) {
      var d = document.createElement("div");
      d.className = "history-item";
      d.innerHTML = '<div class="h-time">'+h.time+'</div><b>आप:</b> '+h.user+'<br><span style="color:var(--text-dim)">AI: '+h.ai+'</span>';
      d.addEventListener("click", function(){ inputEl.value = h.full_user; toggleHistory(); });
      list.appendChild(d);
    });
  }

  function toggleHistory() {
    var p = document.getElementById("history-panel");
    p.classList.toggle("open");
    if (p.classList.contains("open")) renderHistory();
  }
  function clearHistory() {
    chatHistory = [];
    try { localStorage.removeItem("aiking_history"); } catch(e){}
    renderHistory(); showToast("🗑️ History delete हुई");
  }
  function clearChat() {
    chatEl.querySelectorAll(".msg:not(:first-child)").forEach(function(m){ m.remove(); });
    showToast("✅ Chat साफ़ हुई");
  }

  /* ── VOICE INPUT ── */
  var recognition = null, isRecording = false;

  function toggleMic() {
    if (!("webkitSpeechRecognition" in window) && !("SpeechRecognition" in window) && !("SpeechRecognition" in window)) {
      showToast("❌ यह browser voice support नहीं करता"); return;
    }
    if (isRecording) { recognition.stop(); return; }
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.lang = "hi-IN"; recognition.continuous = false; recognition.interimResults = true;
    recognition.onstart = function() {
      isRecording = true;
      document.getElementById("mic-btn").classList.add("recording");
      voiceWave.classList.add("active"); setStatus("🎤 सुन रहा हूँ...", true);
    };
    recognition.onresult = function(e) {
      inputEl.value = Array.from(e.results).map(function(r){ return r[0].transcript; }).join("");
    };
    recognition.onend = function() {
      isRecording = false;
      document.getElementById("mic-btn").classList.remove("recording");
      voiceWave.classList.remove("active"); setStatus("AI King तैयार है");
      if (inputEl.value.trim()) send();
    };
    recognition.onerror = function(e) {
      isRecording = false;
      document.getElementById("mic-btn").classList.remove("recording");
      voiceWave.classList.remove("active"); showToast("❌ Voice error: "+e.error); setStatus("AI King तैयार है");
    };
    recognition.start();
  }

  /* ── CAMERA ── */
  var cameraStream = null, capturedImage = null;

  function toggleCamera() {
    if (cameraStream) { closeCamera(); return; }
    navigator.mediaDevices.getUserMedia({ video:{ facingMode:"environment" }, audio:false })
      .then(function(stream) {
        cameraStream = stream;
        document.getElementById("camera-feed").srcObject = stream;
        document.getElementById("camera-container").style.display = "block";
        document.getElementById("cam-btn").classList.add("active");
        setStatus("📷 Camera चालू है");
      }).catch(function(){ showToast("❌ Camera access नहीं मिला"); });
  }

  function closeCamera() {
    if (cameraStream) { cameraStream.getTracks().forEach(function(t){ t.stop(); }); cameraStream = null; }
    document.getElementById("camera-container").style.display = "none";
    document.getElementById("cam-btn").classList.remove("active");
    setStatus("AI King तैयार है");
  }

  function capturePhoto() {
    var video = document.getElementById("camera-feed");
    var canvas = document.createElement("canvas");
    canvas.width = video.videoWidth; canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    capturedImage = canvas.toDataURL("image/jpeg", 0.8);
    closeCamera(); showToast("📸 Photo लिया गया! अब message भेजो");

    var prev = document.getElementById("img-preview"); if (prev) prev.remove();
    var preview = document.createElement("div");
    preview.id = "img-preview";
    preview.style.cssText = "display:flex;align-items:center;gap:8px;padding:6px 0;font-size:12px;color:var(--accent)";
    var thumb = document.createElement("img"); thumb.src = capturedImage;
    thumb.style.cssText = "height:40px;border-radius:6px;border:1px solid var(--accent)";
    var lbl = document.createElement("span"); lbl.textContent = "Photo ready";
    var rm = document.createElement("button"); rm.textContent = "✕";
    rm.style.cssText = "background:none;border:none;color:var(--danger);cursor:pointer;font-size:16px";
    rm.addEventListener("click", removeCaptured);
    preview.append(thumb, lbl, rm);
    document.querySelector(".bottom").insertBefore(preview, document.querySelector(".input-row"));
  }

  function removeCaptured() {
    capturedImage = null;
    var p = document.getElementById("img-preview"); if (p) p.remove();
  }

  /* ── TTS ── */
  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    window.speechSynthesis.cancel();
    var utt = new SpeechSynthesisUtterance(text.replace(/[*#`>]/g,"").substring(0,500));
    utt.lang = "hi-IN"; utt.rate = 0.95; utt.pitch = 1;
    utt.onstart = function(){ speakInd.classList.add("active"); };
    utt.onend = utt.onerror = function(){ speakInd.classList.remove("active"); };
    window.speechSynthesis.speak(utt);
  }
  function stopSpeech() {
    window.speechSynthesis.cancel(); speakInd.classList.remove("active"); showToast("🔇 Voice रोका गया");
  }

  /* ── SEND ── */
  async function send() {
    var v = inputEl.value.trim();
    if (!v && !capturedImage) return;
    var userText = v || "📸 यह फोटो देखो";
    if (capturedImage) { addMsg("📸 Photo भेजा", "user", capturedImage); }
    else { addMsg(v, "user"); }
    inputEl.value = ""; inputEl.style.height = "auto";
    var imgCopy = capturedImage; capturedImage = null;
    var prev = document.getElementById("img-preview"); if (prev) prev.remove();

    var loading = document.createElement("div");
    loading.className = "msg ai thinking";
    loading.innerHTML = '<div class="dots"><span></span><span></span><span></span></div>';
    chatEl.appendChild(loading);
    scrollToBottom();
    setStatus("🤔 सोच रहा हूँ...", true);

    try {
      var prompt = v || "इस image में क्या है?";
      if (imgCopy) prompt += " [User sent image - describe in Hindi]";
      var res = await fetch("https://text.pollinations.ai/" + encodeURIComponent(prompt));
      var reply = await res.text();
      loading.innerHTML = "";
      await typeText(loading, reply);
      saveToHistory(userText, reply);
      speak(reply);
      setStatus("✅ जवाब दिया गया");
    } catch(err) {
      loading.textContent = "❌ Server error — दोबारा कोशिश करो";
      setStatus("❌ Error हुई");
      scrollToBottom();
    }
  }

  /* ── EVENT LISTENERS ── */
  document.getElementById("history-btn").addEventListener("click", toggleHistory);
  document.getElementById("clear-btn").addEventListener("click", clearChat);
  document.getElementById("close-history-btn").addEventListener("click", toggleHistory);
  document.getElementById("clear-history-btn").addEventListener("click", clearHistory);
  document.getElementById("capture-btn").addEventListener("click", capturePhoto);
  document.getElementById("close-cam-btn").addEventListener("click", closeCamera);
  document.getElementById("send-btn").addEventListener("click", send);
  document.getElementById("mic-btn").addEventListener("click", toggleMic);
  document.getElementById("cam-btn").addEventListener("click", toggleCamera);
  document.querySelector("header").addEventListener("dblclick", stopSpeech);

  inputEl.addEventListener("input", function(){
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + "px";
  });
  inputEl.addEventListener("keydown", function(e){
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
  });

}); // DOMContentLoaded
</script>
</body>
</html>
