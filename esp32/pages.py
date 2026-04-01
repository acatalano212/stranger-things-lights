"""HTML pages served as strings to save flash space."""

ADMIN_PASSWORD = "utgst"

LOGIN_PAGE = """\
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin Login</title>
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAD2UExURWBUPq+VY66UYyYlJKuSYq6UY56IXK6UYyspJq6UY2BVPyUlIywqJquSYq+VZK6UY66UYyMiIiEhIUlCNLCWZJiDWa2TY0pDNHNkRyMiIkQ9MSspJoFvTqyTYiUkI7CWZE1FNiMiIq2UY4VzUCIiISIiIUM9MSIiISEhIVVLOSIiIZN+VoVzULCWZJqEWicmJK+VZD45LzYyK6uSYkU+MiwqJq+VY2VZQWpdQyIiIrCWZJ6IXEhBM0Q9MXdoSa+VZDIvKbCWZCEhISEhISEhISIiIiEhIa6VY39uTbCWZFJJODMwKqaOX6mQYZmDWa+VZE1FNv////D4X5kAAABRdFJOUwAXVhQdp7pie0eGPXLBk3YzaSuF26UoDJRMfICXvWPofUM4m1Rbgxw2kSVDoS4kbKNnSrpUbbuRi42JsESTjLMzbZrC4tK9fpr2fnuztaiDK4WS40YAAAABYktHRFGUaXwqAAAAB3RJTUUH6QsWExspCtmXZwAAAaNJREFUOMu1kV17mkAUhCeurKiAFTULdpcIQiCbVhqLpzaiien3d///r+lN1JBQr9pzd555n9mzM8C/nZNGgx3TmwbnxskRoMVN02gfeYB3upbt9J79DWjwvjsY8pF9Wq8Lw/N9zx4/l0490FYmC0Znk3BgR7UGzjQWpm3LOJk6ogaI1HmaXagWt/S5fVkDyBcBYsdL1UDH0nhq8VKZM+SvruA5cWrx+ROgZ/TBOq81itFChJIeWzRVJ0P2hgChLwUbG8XjlI0FkHhLAOFbhvB6VW2N8WUIMaYSgFjHYLm6qgBzbgnozY2eA8hCIJMVC0GyBEKPxIYBEIDI6aHFLfUZsHC2uFu7zWzhCmSS0gNA1wnALBXBfff+w8c4cIGcJntd00QD7oUSQBonac+JAffTjd6n7AUA/Omu5jbPBcTiM93vqd2KuhECKg6pnbK539pd0V1NorPhbKwOljLZfvlq0e3uD7kmJ9zQ/qhSWS6V377fA+kP6c+y3Ogdgv0pg27jl9plVSi57ozoQXTlypDOsNzvBZGSlYJ/L2mrK20J/K/5A4f8Lde257yeAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI1LTExLTIyVDE5OjI3OjM5KzAwOjAwHTGUngAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNS0xMS0yMlQxOToyNzozOSswMDowMGxsLCIAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjUtMTEtMjJUMTk6Mjc6MzkrMDA6MDA7eQ39AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAABJRU5ErkJggg==">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#d4c5a0;font-family:monospace;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.c{background:#111;border:1px solid #222;border-radius:8px;padding:40px 30px;max-width:340px;width:100%;text-align:center}
h1{font-size:1.3rem;color:#c0392b;letter-spacing:3px;margin-bottom:24px}
input{width:100%;padding:12px;background:#1a1a1a;border:1px solid #333;border-radius:4px;color:#d4c5a0;font-family:monospace;font-size:1rem;text-align:center;letter-spacing:4px;outline:none;margin-bottom:16px}
input:focus{border-color:#c0392b;box-shadow:0 0 12px rgba(192,57,43,.3)}
button{width:100%;padding:12px;background:linear-gradient(180deg,#8b1a1a,#5a1010);border:1px solid #c0392b;border-radius:4px;color:#d4c5a0;font-family:monospace;font-size:.95rem;letter-spacing:2px;cursor:pointer}
.e{color:#e74c3c;font-size:.85rem;margin-bottom:12px}
a{display:block;margin-top:20px;color:#555;text-decoration:none;font-size:.8rem}
</style></head><body>
<div class="c"><h1>Admin</h1>
{error}
<form method="POST"><input type="password" name="password" placeholder="Password" autofocus>
<button type="submit">Enter</button></form>
<a href="/">Back</a></div></body></html>"""

INDEX_PAGE = """\
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Upside Down</title>
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAD2UExURWBUPq+VY66UYyYlJKuSYq6UY56IXK6UYyspJq6UY2BVPyUlIywqJquSYq+VZK6UY66UYyMiIiEhIUlCNLCWZJiDWa2TY0pDNHNkRyMiIkQ9MSspJoFvTqyTYiUkI7CWZE1FNiMiIq2UY4VzUCIiISIiIUM9MSIiISEhIVVLOSIiIZN+VoVzULCWZJqEWicmJK+VZD45LzYyK6uSYkU+MiwqJq+VY2VZQWpdQyIiIrCWZJ6IXEhBM0Q9MXdoSa+VZDIvKbCWZCEhISEhISEhISIiIiEhIa6VY39uTbCWZFJJODMwKqaOX6mQYZmDWa+VZE1FNv////D4X5kAAABRdFJOUwAXVhQdp7pie0eGPXLBk3YzaSuF26UoDJRMfICXvWPofUM4m1Rbgxw2kSVDoS4kbKNnSrpUbbuRi42JsESTjLMzbZrC4tK9fpr2fnuztaiDK4WS40YAAAABYktHRFGUaXwqAAAAB3RJTUUH6QsWExspCtmXZwAAAaNJREFUOMu1kV17mkAUhCeurKiAFTULdpcIQiCbVhqLpzaiien3d///r+lN1JBQr9pzd555n9mzM8C/nZNGgx3TmwbnxskRoMVN02gfeYB3upbt9J79DWjwvjsY8pF9Wq8Lw/N9zx4/l0490FYmC0Znk3BgR7UGzjQWpm3LOJk6ogaI1HmaXagWt/S5fVkDyBcBYsdL1UDH0nhq8VKZM+SvruA5cWrx+ROgZ/TBOq81itFChJIeWzRVJ0P2hgChLwUbG8XjlI0FkHhLAOFbhvB6VW2N8WUIMaYSgFjHYLm6qgBzbgnozY2eA8hCIJMVC0GyBEKPxIYBEIDI6aHFLfUZsHC2uFu7zWzhCmSS0gNA1wnALBXBfff+w8c4cIGcJntd00QD7oUSQBonac+JAffTjd6n7AUA/Omu5jbPBcTiM93vqd2KuhECKg6pnbK539pd0V1NorPhbKwOljLZfvlq0e3uD7kmJ9zQ/qhSWS6V377fA+kP6c+y3Ogdgv0pg27jl9plVSi57ozoQXTlypDOsNzvBZGSlYJ/L2mrK20J/K/5A4f8Lde257yeAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI1LTExLTIyVDE5OjI3OjM5KzAwOjAwHTGUngAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNS0xMS0yMlQxOToyNzozOSswMDowMGxsLCIAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjUtMTEtMjJUMTk6Mjc6MzkrMDA6MDA7eQ39AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAABJRU5ErkJggg==">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#d4c5a0;font-family:monospace;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}
.c{max-width:400px;width:100%;text-align:center}
h1{font-size:1.6rem;color:#c0392b;letter-spacing:5px;margin-bottom:8px;text-shadow:0 0 15px rgba(192,57,43,.4)}
.logo{margin-bottom:20px}
.logo .main{font-family:Georgia,serif;font-weight:bold;font-size:2.2rem;letter-spacing:.12em;color:#e2e5e8;text-shadow:0 1px 0 rgba(255,255,255,.2),0 2px 4px rgba(0,0,0,.5)}
.logo .rule{width:180px;height:3px;margin:6px auto;background:#b29a6b}
.logo .the{font-family:Georgia,serif;font-size:.7rem;letter-spacing:.25em;color:#2a2825}
.logo .gl-a{display:inline-flex;align-items:center;gap:0}
.logo .gl-a img{height:2rem;margin:0 -2px;vertical-align:middle}
.sub{font-size:.8rem;color:#666;letter-spacing:2px;margin-bottom:30px}
input{width:100%;padding:14px;background:#111;border:1px solid #333;border-radius:4px;color:#d4c5a0;font-family:monospace;font-size:1.1rem;text-align:center;text-transform:uppercase;letter-spacing:3px;outline:none;margin-bottom:16px}
input:focus{border-color:#c0392b;box-shadow:0 0 12px rgba(192,57,43,.3)}
button{width:100%;padding:14px;background:linear-gradient(180deg,#8b1a1a,#5a1010);border:1px solid #c0392b;border-radius:4px;color:#d4c5a0;font-family:monospace;font-size:1rem;letter-spacing:2px;cursor:pointer}
button:hover{box-shadow:0 0 15px rgba(192,57,43,.3)}
button:disabled{opacity:.5}
.st{margin-top:20px;padding:10px;border-radius:4px;font-size:.8rem;min-height:40px;display:flex;align-items:center;justify-content:center}
.st.ok{background:rgba(39,174,96,.1);color:#27ae60}
.st.err{background:rgba(192,57,43,.1);color:#e74c3c}
.st.idle{background:rgba(255,255,255,.03);color:#555}
.ft{margin-top:30px;font-size:.65rem;color:#333;letter-spacing:2px}
</style></head><body>
<div class="c">

<h1>THE UPSIDE DOWN</h1>
<p class="sub">Send a message through the lights</p>
<input type="text" id="m" placeholder="TYPE HERE..." maxlength="50" autocomplete="off" spellcheck="false">
<button id="b" onclick="send()">Send to the Upside Down</button>
<div class="st idle" id="s">Waiting for your message...</div>
<p class="ft">The lights are always watching</p>
</div>
<script>
const m=document.getElementById('m'),b=document.getElementById('b'),s=document.getElementById('s');
m.addEventListener('input',function(){this.value=this.value.replace(/[^a-zA-Z ]/g,'').toUpperCase()});
m.addEventListener('keydown',function(e){if(e.key==='Enter')send()});
async function send(){
const t=m.value.trim();if(!t){s.textContent='Type a message first!';s.className='st err';return}
b.disabled=true;s.textContent='Sending...';s.className='st idle';
try{const r=await fetch('/api/message',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
const d=await r.json();if(d.success){s.textContent='"'+t+'" is being spelled out...';s.className='st ok';m.value='';
setTimeout(()=>{s.textContent='Waiting for your message...';s.className='st idle';b.disabled=false},10000)}
else{s.textContent=d.error||'Error';s.className='st err';b.disabled=false}}
catch(e){s.textContent='Connection failed';s.className='st err';b.disabled=false}}
</script></body></html>"""

ADMIN_PAGE = """\
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin</title>
<link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAD2UExURWBUPq+VY66UYyYlJKuSYq6UY56IXK6UYyspJq6UY2BVPyUlIywqJquSYq+VZK6UY66UYyMiIiEhIUlCNLCWZJiDWa2TY0pDNHNkRyMiIkQ9MSspJoFvTqyTYiUkI7CWZE1FNiMiIq2UY4VzUCIiISIiIUM9MSIiISEhIVVLOSIiIZN+VoVzULCWZJqEWicmJK+VZD45LzYyK6uSYkU+MiwqJq+VY2VZQWpdQyIiIrCWZJ6IXEhBM0Q9MXdoSa+VZDIvKbCWZCEhISEhISEhISIiIiEhIa6VY39uTbCWZFJJODMwKqaOX6mQYZmDWa+VZE1FNv////D4X5kAAABRdFJOUwAXVhQdp7pie0eGPXLBk3YzaSuF26UoDJRMfICXvWPofUM4m1Rbgxw2kSVDoS4kbKNnSrpUbbuRi42JsESTjLMzbZrC4tK9fpr2fnuztaiDK4WS40YAAAABYktHRFGUaXwqAAAAB3RJTUUH6QsWExspCtmXZwAAAaNJREFUOMu1kV17mkAUhCeurKiAFTULdpcIQiCbVhqLpzaiien3d///r+lN1JBQr9pzd555n9mzM8C/nZNGgx3TmwbnxskRoMVN02gfeYB3upbt9J79DWjwvjsY8pF9Wq8Lw/N9zx4/l0490FYmC0Znk3BgR7UGzjQWpm3LOJk6ogaI1HmaXagWt/S5fVkDyBcBYsdL1UDH0nhq8VKZM+SvruA5cWrx+ROgZ/TBOq81itFChJIeWzRVJ0P2hgChLwUbG8XjlI0FkHhLAOFbhvB6VW2N8WUIMaYSgFjHYLm6qgBzbgnozY2eA8hCIJMVC0GyBEKPxIYBEIDI6aHFLfUZsHC2uFu7zWzhCmSS0gNA1wnALBXBfff+w8c4cIGcJntd00QD7oUSQBonac+JAffTjd6n7AUA/Omu5jbPBcTiM93vqd2KuhECKg6pnbK539pd0V1NorPhbKwOljLZfvlq0e3uD7kmJ9zQ/qhSWS6V377fA+kP6c+y3Ogdgv0pg27jl9plVSi57ozoQXTlypDOsNzvBZGSlYJ/L2mrK20J/K/5A4f8Lde257yeAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI1LTExLTIyVDE5OjI3OjM5KzAwOjAwHTGUngAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNS0xMS0yMlQxOToyNzozOSswMDowMGxsLCIAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjUtMTEtMjJUMTk6Mjc6MzkrMDA6MDA7eQ39AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAABJRU5ErkJggg==">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#d4c5a0;font-family:monospace;min-height:100vh;padding:20px}
.c{max-width:700px;margin:0 auto}
h1{font-size:1.3rem;color:#c0392b;letter-spacing:3px;text-align:center;margin-bottom:6px}
.nav{text-align:center;margin-bottom:20px}.nav a{color:#666;text-decoration:none;font-size:.8rem}
.sec{background:#111;border:1px solid #222;border-radius:6px;padding:16px;margin-bottom:16px}
.sec h2{font-size:.9rem;color:#c0392b;letter-spacing:2px;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #222}
input[type=text],input[type=number]{background:#1a1a1a;border:1px solid #333;border-radius:3px;color:#d4c5a0;font-family:monospace;font-size:.85rem;padding:8px;outline:none;text-transform:uppercase}
input:focus{border-color:#c0392b}
.mr{display:flex;gap:10px;align-items:center}.mr input{flex:1}
.ir{display:flex;gap:10px;align-items:center;margin-top:10px}.ir label{font-size:.8rem;color:#888;white-space:nowrap}.ir input{width:90px}.ir .u{font-size:.75rem;color:#555}
.lg{display:grid;grid-template-columns:repeat(auto-fill,minmax(105px,1fr));gap:6px;margin-top:10px}
.lc{display:flex;align-items:center;gap:4px;background:#0d0d0d;border:1px solid #1a1a1a;border-radius:3px;padding:5px 6px}
.lc .l{font-size:1.1rem;color:#c0392b;width:20px;text-align:center}
.lc input{width:42px;text-align:center;padding:4px}
.lc button{background:none;border:1px solid #333;color:#888;border-radius:3px;padding:2px 5px;cursor:pointer;font-size:.6rem}
.lc button:hover{border-color:#ffaa00;color:#ffaa00}
.btn{padding:10px 18px;border:1px solid #c0392b;border-radius:4px;color:#d4c5a0;font-family:monospace;font-size:.85rem;cursor:pointer;letter-spacing:1px}
.bp{background:linear-gradient(180deg,#8b1a1a,#5a1010)}.bp:hover{box-shadow:0 0 12px rgba(192,57,43,.3)}
.bs{background:#1a1a1a;border-color:#444}.bs:hover{border-color:#ffaa00;color:#ffaa00}
.acts{display:flex;gap:10px;justify-content:flex-end;margin-top:14px}
.tr{display:flex;gap:8px;align-items:center;margin-top:12px;padding-top:12px;border-top:1px solid #1a1a1a}
.tr label{font-size:.8rem;color:#888;white-space:nowrap}.tr input{width:60px}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(60px);padding:10px 20px;border-radius:6px;font-size:.8rem;opacity:0;transition:all .3s;z-index:100}
.toast.show{transform:translateX(-50%) translateY(0);opacity:1}
.toast.ok{background:rgba(39,174,96,.9);color:#fff}.toast.err{background:rgba(192,57,43,.9);color:#fff}
.help{font-size:.65rem;color:#555;margin-top:6px;line-height:1.4}
</style></head><body>
<div class="c">
<h1>Admin Panel</h1>
<div class="nav"><a href="/">Back to messages</a> | <a href="/admin/logout">Logout</a></div>
<div class="sec"><h2>Default Message</h2>
<div class="mr"><input type="text" id="dm" placeholder="RUN WILL RUN" maxlength="50"></div>
<div class="ir"><label>Play every</label><input type="number" id="mi" min="10" max="3600" step="10"><span class="u">sec</span></div>
</div>
<div class="sec"><h2>Letter to LED Mapping</h2>
<p class="help">Set LED index (0-49) for each letter. Use the bulb button to flash that LED.</p>
<div class="lg" id="g"></div>
<div class="tr"><label>Test LED #</label><input type="number" id="ti" min="0" max="99" value="0">
<button class="btn bs" onclick="testLed()">Flash</button></div>
</div>
<div class="acts">
<button class="btn bs" onclick="loadCfg()">Reload</button>
<button class="btn bp" id="sv" onclick="saveCfg()">Save</button>
</div>
<div class="sec" style="margin-top:16px"><h2>System</h2>
<p class="help">Pull latest code from GitHub and reboot. Device will be offline briefly.</p>
<div class="acts" style="margin-top:10px"><button class="btn bs" id="ota" onclick="otaUpdate()">Update from GitHub</button></div>
</div></div>
<div class="toast" id="t"></div>
<script>
const L='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
function toast(m,ok){const t=document.getElementById('t');t.textContent=m;t.className='toast '+(ok?'ok':'err')+' show';setTimeout(()=>t.classList.remove('show'),2500)}
function buildGrid(map){const g=document.getElementById('g');g.innerHTML='';
for(const c of L){const d=document.createElement('div');d.className='lc';
d.innerHTML='<span class="l">'+c+'</span><input type="number" min="0" max="99" value="'+(map[c]||0)+'" id="m-'+c+'"><button onclick="testLed('+((map[c]||0))+')">💡</button>';
g.appendChild(d)}}
async function loadCfg(){try{const r=await fetch('/api/admin/config');const d=await r.json();
document.getElementById('dm').value=d.default_message||'';document.getElementById('mi').value=d.message_interval||60;
buildGrid(d.letter_map||{});toast('Loaded',true)}catch(e){toast('Load failed',false)}}
async function saveCfg(){const map={};for(const c of L)map[c]=parseInt(document.getElementById('m-'+c).value)||0;
const data={letter_map:map,default_message:document.getElementById('dm').value.toUpperCase().trim(),message_interval:parseInt(document.getElementById('mi').value)||60};
try{const r=await fetch('/api/admin/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
const d=await r.json();toast(d.success?'Saved!':'Error',d.success)}catch(e){toast('Save failed',false)}}
async function testLed(i){if(i===undefined)i=parseInt(document.getElementById('ti').value);
try{await fetch('/api/admin/test-led',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({led_index:i})});
toast('Flashing LED #'+i,true)}catch(e){toast('Error',false)}}
async function otaUpdate(){if(!confirm('Pull latest code from GitHub and reboot?'))return;
const b=document.getElementById('ota');b.disabled=true;b.textContent='Updating...';toast('Downloading from GitHub...',true);
try{const r=await fetch('/api/admin/ota-update',{method:'POST'});const d=await r.json();
if(d.success){toast('Updated! Rebooting...',true);setTimeout(()=>location.reload(),5000)}
else{toast('Errors: '+d.errors.join(', '),false);b.disabled=false;b.textContent='Update from GitHub'}}
catch(e){toast('Update failed',false);b.disabled=false;b.textContent='Update from GitHub'}}
loadCfg();
</script></body></html>"""
