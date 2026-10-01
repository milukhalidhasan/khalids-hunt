# Builds the treasure-hunt game from the 3D model page.
# Reads artifact-3d.html, reuses its house-building code, and adds the game on top.
# Writes source/artifact-game.html (for publishing) and ../index.html (opens in any browser).
import os

HERE = os.path.dirname(os.path.abspath(__file__))
model = open(os.path.join(HERE, "artifact-3d.html"), encoding="utf-8").read()
start = model.index('(function () {\n  "use strict";')
end = model.index("  /* ---------------- labels ---------------- */")
MODEL_JS = model[start:end]

HEAD = r'''<title>Khalid's Treasure Hunt</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+Da+2:wght@500;600;700;800&family=Hind+Siliguri:wght@500;600&display=swap">
<style>
:root{--ink:#2a1e16;--cream:#fff6e6;--brick:#a5432a;--gold:#e3a33a;--soft:#f3e2c4;--muted:#7a5a44;
  --f:"Baloo Da 2","Hind Siliguri","Segoe UI",Arial,sans-serif}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{height:100%}
body{margin:0;background:#dce9ee;color:var(--ink);font:500 16px/1.4 var(--f);overflow:hidden}
#game{position:relative;height:100%;overflow:hidden;-webkit-user-select:none;user-select:none}
#stage{position:absolute;inset:0;touch-action:none;background:#dce9ee}
#stage canvas{display:block;width:100%;height:100%;outline:none}
#loading{position:absolute;inset:0;display:grid;place-items:center;font-size:1.1rem}
.hud{position:absolute;inset:0;pointer-events:none;padding-block:12px;padding-inline:16px}
.hud-top{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:start}
.pill{pointer-events:auto;background:var(--cream);border:2.5px solid var(--ink);border-radius:14px;padding:5px 14px 6px;box-shadow:0 3px 0 var(--ink);font-variant-numeric:tabular-nums;min-width:88px}
.lbl{display:block;font-size:.74rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);line-height:1.1}
.pill b{display:block;font-size:1.55rem;line-height:1.05;font-weight:800}
.meta{text-align:right}
.task{justify-self:center;display:flex;align-items:center;gap:12px;background:var(--cream);border:2.5px solid var(--ink);border-radius:18px;padding:6px 18px 6px 8px;box-shadow:0 4px 0 var(--ink);max-width:560px;min-width:0}
.task img{width:66px;height:66px;border-radius:12px;background:var(--soft);flex:none;border:2px solid var(--ink)}
.task .lbl{color:var(--brick)}
.task b{display:block;font-size:1.5rem;line-height:1.1;font-weight:800;overflow-wrap:anywhere}
.task small{display:block;font-size:.95rem;color:#6b4a36;min-height:1.3em}
.btns{position:absolute;right:16px;top:104px;display:grid;gap:9px;pointer-events:auto}
.rbtn{width:52px;height:52px;border-radius:50%;border:2.5px solid var(--ink);background:var(--cream);box-shadow:0 3px 0 var(--ink);display:grid;place-items:center;cursor:pointer;color:var(--ink);font:800 .9rem/1 var(--f);padding:0}
.rbtn svg{width:24px;height:24px}
.rbtn.hint{background:var(--gold)}
.rbtn:active{transform:translateY(2px);box-shadow:0 1px 0 var(--ink)}
#toast{position:absolute;left:50%;top:124px;transform:translateX(-50%);background:var(--ink);color:var(--cream);padding:8px 18px;border-radius:12px;font-size:1.08rem;font-weight:600;max-width:min(90vw,540px);text-align:center;opacity:0;transition:opacity .25s}
#toast.on{opacity:1}
.keys{position:absolute;left:16px;right:16px;bottom:14px;font-size:.9rem;font-weight:600;color:#23332f;text-shadow:0 1px 0 rgba(255,255,255,.85)}
#joy{position:absolute;left:22px;bottom:26px;width:136px;height:136px;border-radius:50%;background:rgba(255,246,230,.55);border:2.5px solid rgba(42,30,22,.6);pointer-events:auto;touch-action:none}
#knob{position:absolute;left:50%;top:50%;width:58px;height:58px;margin:-29px 0 0 -29px;border-radius:50%;background:var(--brick);border:2.5px solid var(--ink)}
.pop{position:absolute;left:0;top:0;font:800 2rem/1 var(--f);color:var(--gold);-webkit-text-stroke:2px var(--ink);pointer-events:none;animation:pop 1.2s ease-out forwards}
@keyframes pop{0%{opacity:0;transform:translate(-50%,-30%) scale(.6)}15%{opacity:1;transform:translate(-50%,-60%) scale(1.12)}100%{opacity:0;transform:translate(-50%,-240%) scale(1)}}
@media (prefers-reduced-motion:reduce){.pop{animation-duration:.01s}}
.overlay{position:absolute;inset:0;display:grid;place-items:center;padding:16px;background:rgba(42,30,22,.32);pointer-events:auto}
.card{background:var(--cream);border:3px solid var(--ink);border-radius:22px;box-shadow:0 6px 0 var(--ink);padding:22px 24px 20px;max-width:540px;width:100%;max-height:100%;overflow:auto;text-align:center}
.card h1{margin:0;font:800 clamp(1.9rem,6vw,2.8rem)/1.08 var(--f);color:var(--brick);text-wrap:balance}
.card p{margin:10px 0 0;font-size:1.04rem;line-height:1.45}
.card .ctl{font-size:.93rem;color:#6b4a36}
.big{margin-top:16px;font:800 1.3rem/1 var(--f);padding:14px 30px;border-radius:16px;border:3px solid var(--ink);background:var(--gold);color:var(--ink);box-shadow:0 4px 0 var(--ink);cursor:pointer}
.big:active{transform:translateY(3px);box-shadow:0 1px 0 var(--ink)}
.row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:14px}
.chip{border:2px solid var(--ink);border-radius:999px;padding:5px 16px;background:#fff;font:700 .98rem var(--f);cursor:pointer;color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--cream)}
.stars{font-size:2.6rem;letter-spacing:.18em;color:var(--gold);-webkit-text-stroke:1.5px var(--ink);margin-top:4px;line-height:1.2}
.stars .off{color:#e8dcc8}
.found-list{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:12px}
.found-list figure{margin:0;display:grid;justify-items:center;gap:2px;font-size:.8rem;font-weight:700;color:#6b4a36;width:62px}
.found-list img{width:46px;height:46px;border-radius:10px;background:var(--soft);border:2px solid var(--ink)}
.credit{margin-top:16px;font-size:.82rem;color:var(--muted)}
button:focus-visible{outline:3px solid var(--brick);outline-offset:3px}
.rbtn,.big,.chip,#joy{touch-action:manipulation}
.bubble{position:absolute;left:0;top:0;transform:translate(-50%,-100%);background:#fff;color:var(--ink);border:2.5px solid var(--ink);border-radius:16px;padding:3px 14px 5px;font:800 1.25rem/1.2 var(--f);box-shadow:0 3px 0 var(--ink);white-space:nowrap;pointer-events:none}
.bubble::after{content:"";position:absolute;left:50%;bottom:-11px;margin-left:-9px;border-style:solid;border-width:10px 9px 0;border-color:var(--ink) transparent transparent}
.bubble.show{animation:bub .35s ease-out}
@keyframes bub{0%{transform:translate(-50%,-100%) scale(.4)}70%{transform:translate(-50%,-100%) scale(1.12)}100%{transform:translate(-50%,-100%) scale(1)}}
@media (prefers-reduced-motion:reduce){.bubble.show{animation:none}}
@media (max-width:720px) and (orientation:portrait){
  .hud-top{grid-template-columns:1fr 1fr}
  .task{grid-column:1/-1;grid-row:1;justify-self:stretch}
  .pill b{font-size:1.2rem}.task b{font-size:1.15rem}.task img{width:48px;height:48px}
  .btns{top:auto;bottom:28px;right:18px;grid-template-columns:repeat(2,52px)}
  .keys{display:none}
  #toast{top:168px}
}
/* phones held sideways */
@media (max-height:520px) and (orientation:landscape){
  .hud{padding-block:8px;padding-inline:max(12px,env(safe-area-inset-left)) max(12px,env(safe-area-inset-right))}
  .pill{padding:3px 10px 4px;min-width:70px;border-radius:12px}
  .pill b{font-size:1.15rem}
  .lbl{font-size:.66rem}
  .task{padding:4px 12px 4px 6px;gap:8px;border-radius:14px}
  .task img{width:44px;height:44px;border-radius:9px}
  .task b{font-size:1.1rem}
  .task small{font-size:.8rem;min-height:0}
  .btns{top:auto;bottom:16px;right:max(16px,env(safe-area-inset-right));grid-template-columns:repeat(2,50px);gap:8px}
  .rbtn{width:50px;height:50px}
  #toast{top:72px;font-size:.95rem}
  #joy{left:max(24px,env(safe-area-inset-left));bottom:18px;width:150px;height:150px}
  #knob{width:62px;height:62px;margin:-31px 0 0 -31px}
  .keys{display:none}
  .card{padding:14px 18px;border-radius:18px}
  .card h1{font-size:1.7rem}
  .card p{font-size:.92rem;margin-top:6px}
  .big{margin-top:10px;padding:10px 24px;font-size:1.1rem}
  .row{margin-top:8px}
  .stars{font-size:2rem}
  .bubble{font-size:1.05rem}
}
</style>
'''

BODY = r'''<div id="game">
  <div id="stage" aria-label="Game view"><div id="loading">Loading the house…</div></div>

  <div class="hud" id="hud" hidden>
    <div class="hud-top">
      <div class="pill"><span class="lbl" id="l-score">Score</span><b id="h-score">0</b></div>
      <div class="task" role="status" aria-live="polite"><img id="task-img" alt=""><div><span class="lbl" id="l-find">Find</span><b id="task-name"></b><small id="task-hint"></small></div></div>
      <div class="pill meta"><span class="lbl" id="l-item">Item</span><b id="h-count">1 / 8</b><span class="lbl" id="h-time">0:00</span></div>
    </div>
    <div class="btns">
      <button type="button" class="rbtn hint" id="b-hint" aria-label="Hint"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg></button>
      <button type="button" class="rbtn" id="b-sound" aria-label="Sound on"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path id="snd-on" d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/><path id="snd-off" d="M17 9l5 6M22 9l-5 6" style="display:none"/></svg></button>
      <button type="button" class="rbtn" id="b-lang" aria-label="Language">বাং</button>
      <button type="button" class="rbtn" id="b-pause" aria-label="Pause"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg></button>
      <button type="button" class="rbtn" id="b-full" aria-label="Full screen" hidden><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>
    </div>
    <div class="bubble" id="bubble" hidden></div>
    <div id="toast" role="status" aria-live="polite"></div>
    <div id="joy" hidden><div id="knob"></div></div>
    <div class="keys" id="keys"></div>
  </div>

  <div class="overlay" id="menu">
    <div class="card">
      <h1 id="m-title">Khalid's Treasure Hunt</h1>
      <p id="m-story"></p>
      <p class="ctl" id="m-score"></p>
      <p class="ctl" id="m-ctl"></p>
      <div class="row"><button type="button" class="chip" id="m-en" aria-pressed="true">English</button><button type="button" class="chip" id="m-bn" aria-pressed="false">বাংলা</button></div>
      <button type="button" class="big" id="m-start">Start the hunt</button>
      <p class="ctl" id="m-best"></p>
      <p class="credit" id="m-credit"></p>
    </div>
  </div>

  <div class="overlay" id="pause" hidden>
    <div class="card">
      <h1 id="p-title">Paused</h1>
      <button type="button" class="big" id="p-resume">Resume</button>
      <div class="row"><button type="button" class="chip" id="p-restart">Start over</button></div>
    </div>
  </div>

  <div class="overlay" id="done" hidden>
    <div class="card">
      <h1 id="d-title"></h1>
      <div class="stars" id="d-stars" aria-hidden="true"></div>
      <p id="d-score"></p>
      <p class="ctl" id="d-text"></p>
      <div class="found-list" id="d-list"></div>
      <button type="button" class="big" id="d-again"></button>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/BufferGeometryUtils.js"></script>
<script>
if (!window.THREE) document.getElementById("loading").textContent = "Could not load the 3D engine. Check the internet and reload. · ৩ডি ইঞ্জিন লোড হয়নি। ইন্টারনেট দেখে আবার খুলুন।";
</script>
<script>
'''

GAME_JS = r'''
  /* =====================================================================
     KHALID'S TREASURE HUNT
     Everything above builds the house (same code as the 3D model page).
     ===================================================================== */
  function timeLabel() {}
  function cutLabel() {}
  var $ = function (id) { return document.getElementById(id); };
  var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
  var inApp = !!window.RafiApp;   // true inside the Android app
  controls.enabled = false;
  var maxPR = Math.min(window.devicePixelRatio || 1, touch ? 1.25 : 1.5), curPR = maxPR;
  renderer.setPixelRatio(curPR);
  if (touch) {
    // phones: lighter shadows and half the grass
    renderer.shadowMap.type = THREE.PCFShadowMap;
    sun.shadow.mapSize.set(1024, 1024);
    scene.traverse(function (o) { if (o.isInstancedMesh) o.count = Math.floor(o.count * 0.5); });
  }
  camera.fov = 52; camera.near = 0.2; camera.updateProjectionMatrix();
  doorPivots.forEach(function (pv) { pv.rotation.y = pv.userData.openA; });
  updateSun(16);
  clipArr.length = 0;
  cutPlane.constant = 4.6;

  /* ---------- text in both languages ---------- */
  var U = {
    en: {
      title: "Khalid's Treasure Hunt",
      story: "Khalid and his dog Bhulu have just moved into the new brick house, and Khalid's favourite things are scattered all over the rooms, the verandah and the yard. Help him find each one. The faster you find it, the more points you get. Pick the wrong thing and Bhulu barks!",
      score: "Each find is worth 100–200 points, plus up to 135 for speed. A hint shows where to look but costs 40.",
      keys: "Walk: W A S D or arrow keys · Shift: walk slowly · Turn: Q / E or drag · Click a thing to pick it up · Hint: H · Pause: Esc",
      touch: "Joystick to walk (push further to run) · drag to turn · tap a thing to pick it up · bulb for a hint",
      rotate: "Turn your phone sideways for a bigger view.",
      start: "Start the hunt", best: "Best score: {b}", credit: "House designed by Md. Khalid Hasan Milu",
      lScore: "Score", lFind: "Find", lItem: "Item",
      found: "Found the {i}! +{p}", speedy: " Speedy!", closer: "Walk closer to pick it up!", woof: "Woof! Woof!",
      look: "Look in: {p}", hintToast: "Look in: {p} (−40)", sparkle: "Look for the sparkle!",
      paused: "Paused", resume: "Resume", restart: "Start over",
      doneTitle: "All found!", doneText: "Khalid found all {n} things in {t}.", doneScore: "Score {s} · Best {b}", newBest: "New best score!", again: "Play again",
      pts: "pts", langBtn: "বাং", full: "Full screen"
    },
    bn: {
      title: "খালিদের গুপ্তধন খোঁজা",
      story: "খালিদ আর ওর কুকুর ভুলু নতুন ইটের বাড়িতে উঠেছে, আর খালিদের প্রিয় জিনিসগুলো ঘরে, বারান্দায় আর উঠানে ছড়িয়ে আছে। একটা একটা করে খুঁজে দাও। যত তাড়াতাড়ি পাবে, তত বেশি পয়েন্ট। ভুল জিনিস ধরলে ভুলু ঘেউ ঘেউ করবে!",
      score: "প্রতিটি জিনিসে ১০০–২০০ পয়েন্ট, আর দ্রুততার জন্য ১৩৫ পর্যন্ত বোনাস। সাহায্য নিলে জায়গা দেখাবে, তবে ৪০ পয়েন্ট কাটবে।",
      keys: "হাঁটো: W A S D বা তীর চিহ্ন · Shift: আস্তে হাঁটো · ঘোরাও: Q / E বা টেনে · জিনিসে ক্লিক করে তোলো · সাহায্য: H · বিরতি: Esc",
      touch: "জয়স্টিকে হাঁটো (বেশি ঠেললে দৌড়) · টেনে ঘোরাও · জিনিস ছুঁয়ে তোলো · সাহায্যের জন্য বাতি",
      rotate: "বড় করে দেখতে ফোনটা আড়াআড়ি ধরো।",
      start: "খোঁজা শুরু করো", best: "সেরা স্কোর: {b}", credit: "বাড়ির নকশা: মোঃ খালিদ হাসান মিলু",
      lScore: "স্কোর", lFind: "খুঁজে বের করো", lItem: "জিনিস",
      found: "{i} পাওয়া গেছে! +{p}", speedy: " দারুণ দ্রুত!", closer: "আরও কাছে গিয়ে তোলো!", woof: "ঘেউ ঘেউ!",
      look: "খুঁজে দেখো: {p}", hintToast: "খুঁজে দেখো: {p} (−৪০)", sparkle: "ঝিলিক দেখে খোঁজো!",
      paused: "বিরতি", resume: "আবার চালাও", restart: "নতুন করে শুরু",
      doneTitle: "সব পাওয়া গেছে!", doneText: "খালিদ {t}-এ সব {n}টি জিনিস খুঁজে পেয়েছে।", doneScore: "স্কোর {s} · সেরা {b}", newBest: "নতুন সেরা স্কোর!", again: "আবার খেলো",
      pts: "পয়েন্ট", langBtn: "EN", full: "পুরো পর্দা"
    }
  };
  function u(k, vars) {
    var s = U[lang][k];
    if (vars) Object.keys(vars).forEach(function (v) { s = s.split("{" + v + "}").join(vars[v]); });
    return s;
  }
  function num(n) { return lang === "bn" ? bnNum(n) : String(n); }
  function fmtTime(sec) { var m = Math.floor(sec / 60), s = Math.floor(sec % 60); return num(m + ":" + (s < 10 ? "0" : "") + s); }

  /* ---------- where Khalid can walk (plan inches) ---------- */
  function floorAt(x, z) {
    if (x >= 0 && x <= 455 && z >= 0 && z <= 426) return 0;
    if (x >= 0 && x <= 455 && z > 426 && z <= 474) return -2;
    if (x >= 191.5 && x <= 263.5 && z > 474 && z <= 514) return -2 - (z - 474) / 40 * 28;
    return -30;
  }
  var RECTS = [];
  WALLS.forEach(function (w) {
    var x1 = w[0], z1 = w[1], x2 = w[2], z2 = w[3], horiz = (x2 - x1) >= (z2 - z1);
    var gaps = OPEN.filter(function (o) {
      return o.sill === 0 && (horiz ? (o.o === "h" && o.w1 >= z1 - 0.5 && o.w2 <= z2 + 0.5 && o.s >= x1 - 0.5 && o.e <= x2 + 0.5)
                                    : (o.o === "v" && o.w1 >= x1 - 0.5 && o.w2 <= x2 + 0.5 && o.s >= z1 - 0.5 && o.e <= z2 + 0.5));
    }).sort(function (a, b) { return a.s - b.s; });
    var cur = horiz ? x1 : z1, end = horiz ? x2 : z2;
    gaps.forEach(function (o) { if (o.s > cur) RECTS.push(horiz ? [cur, z1, o.s, z2] : [x1, cur, x2, o.s]); cur = o.e; });
    if (end > cur) RECTS.push(horiz ? [cur, z1, end, z2] : [x1, cur, x2, end]);
  });
  [
    [70, 30, 154, 102], [136, 12, 154, 30], [136, 102, 154, 120], [10, 120, 32, 162], [80, 160, 116, 178],
    [301, 30, 385, 102], [301, 12, 319, 30], [301, 102, 319, 120], [423, 120, 445, 162], [339, 160, 375, 178],
    [70, 312, 154, 372], [136, 294, 154, 312], [136, 372, 154, 390], [92, 398, 134, 416], [20, 392, 56, 416], [29, 374, 47, 390],
    [301, 312, 385, 372], [301, 294, 319, 312], [301, 372, 319, 390], [397, 248, 439, 270], [399, 392, 435, 416], [408, 374, 426, 390],
    [159, 10, 243, 34], [219, 34, 243, 90], [161, 100, 189, 128], [159, 50, 175, 96],
    [271, 16, 296, 32], [10, 220, 35, 236], [420, 220, 445, 236], [280, 110, 296, 130], [252, 45, 262, 55], [45, 191, 55, 201], [400, 191, 410, 201],
    [197.5, 225, 257.5, 261], [205, 207, 223, 223], [232, 207, 250, 223], [205, 263, 223, 279], [232, 263, 250, 279], [179, 234, 195, 252], [259.5, 234, 275.5, 252],
    [159, 330, 191, 408], [270, 334, 296, 360], [270, 366, 296, 392], [209, 350, 245, 372], [161, 312, 173, 324], [162, 288, 174, 300],
    [24, 427, 90, 446], [375, 434, 391, 450], [402, 439, 418, 455],
    [10, 466.5, 151, 471.5], [161, 466.5, 183.5, 471.5], [271.5, 466.5, 294, 471.5], [304, 466.5, 445, 471.5],
    [183.5, 465, 191.5, 473], [263.5, 465, 271.5, 473], [-3, 461, 13, 477], [148, 461, 164, 477], [291, 461, 307, 477], [442, 461, 458, 477],
    [10, 476, 162, 500], [293, 476, 445, 500], [167.5, 477.5, 184.5, 494.5], [270.5, 477.5, 287.5, 494.5], [167.5, 495.5, 184.5, 512.5], [270.5, 495.5, 287.5, 512.5]
  ].forEach(function (r) { RECTS.push(r); });
  function px(v) { return v * 12 + OX; }
  function pz(v) { return v * 12 + OZ; }
  var CIRCLES = [
    [px(-12), pz(-40), 8], [px(24), pz(-38), 8], [px(46), pz(-8), 8], [px(-52), pz(8), 8],
    [px(46), pz(34), 14], [px(-44), pz(-30), 12], [px(16), pz(-31), 6], [px(19.5), pz(-34), 6], [px(13), pz(-35), 6],
    [px(-58), pz(-44), 36], [px(-30), pz(-38), 50], [px(6), pz(-30), 6], [-30, 492, 20], [485, 492, 20]
  ];
  [-30, -18, -6, 6, 18].forEach(function (z) { CIRCLES.push([px(56), pz(z), 4]); });
  var POND = [px(-42), pz(36), 15 * 12, 10 * 12], PR = 9;
  function collide(p) {
    for (var it = 0; it < 3; it++) {
      RECTS.forEach(function (r) {
        var cx = Math.max(r[0], Math.min(p.x, r[2])), cz = Math.max(r[1], Math.min(p.z, r[3])), dx = p.x - cx, dz = p.z - cz, d2 = dx * dx + dz * dz;
        if (d2 >= PR * PR) return;
        if (d2 > 1e-6) { var d = Math.sqrt(d2), k = (PR - d) / d; p.x += dx * k; p.z += dz * k; return; }
        var l = p.x - r[0], rr = r[2] - p.x, t = p.z - r[1], b = r[3] - p.z, m = Math.min(l, rr, t, b);
        if (m === l) p.x = r[0] - PR; else if (m === rr) p.x = r[2] + PR; else if (m === t) p.z = r[1] - PR; else p.z = r[3] + PR;
      });
      CIRCLES.forEach(function (c) {
        var dx = p.x - c[0], dz = p.z - c[1], d = Math.sqrt(dx * dx + dz * dz), m = c[2] + PR;
        if (d < m && d > 1e-6) { p.x = c[0] + dx / d * m; p.z = c[1] + dz / d * m; }
      });
      var ex = (p.x - POND[0]) / (POND[2] + PR), ez = (p.z - POND[1]) / (POND[3] + PR), e = Math.sqrt(ex * ex + ez * ez);
      if (e < 1 && e > 1e-6) { p.x = POND[0] + ex / e * (POND[2] + PR); p.z = POND[1] + ez / e * (POND[3] + PR); }
      var wx = (p.x - OX) / 12, wz = (p.z - OZ) / 12, wd = Math.sqrt(wx * wx + wz * wz);
      if (wd > 60) { p.x = OX + wx / wd * 720; p.z = OZ + wz / wd * 720; }
    }
  }
  // which room a point is in ("yard" outside); 3" of slack so doorways count
  function roomAt(x, z) {
    for (var i = 0; i < ROOMS.length; i++) {
      var rs = ROOMS[i].r;
      for (var j = 0; j < rs.length; j++) { var r = rs[j]; if (x >= r[0] - 3 && x <= r[2] + 3 && z >= r[1] - 3 && z <= r[3] + 3) return ROOMS[i].k; }
    }
    return "yard";
  }
  // true when a straight line between two points misses every wall and piece of furniture
  function clearLine(ax, az, bx, bz) {
    var dx = bx - ax, dz = bz - az;
    for (var i = 0; i < RECTS.length; i++) {
      var r = RECTS[i], t0 = 0, t1 = 1, p = [-dx, dx, -dz, dz], q = [ax - r[0], r[2] - ax, az - r[1], r[3] - az], hit = true;
      for (var k = 0; k < 4 && hit; k++) {
        if (p[k] === 0) { if (q[k] < 0) hit = false; }
        else { var t = q[k] / p[k]; if (p[k] < 0) { if (t > t1) hit = false; else if (t > t0) t0 = t; } else { if (t < t0) hit = false; else if (t < t1) t1 = t; } }
      }
      if (hit) return false;
    }
    return true;
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function mix(a, b, w) { return a + (b - a) * w; }
  function turnTo(o, target, k) {
    var d = target - o.face;
    while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
    o.face += d * Math.min(1, k);
  }

  /* ---------- the hidden things ---------- */
  function im(hex, o) {
    var m = new THREE.MeshStandardMaterial(Object.assign({ color: hex, roughness: 0.6 }, o || {}));
    m.color.convertSRGBToLinear();
    return m;
  }
  var IMT = {
    red: im(0xd9362b), redD: im(0xd9362b, { side: THREE.DoubleSide }), yellow: im(0xf2c230), yellowD: im(0xf2c230, { side: THREE.DoubleSide }),
    blue: im(0x2e62b8), green: im(0x3c9a4a), white: im(0xf7f5ee), black: im(0x1e1e1e, { roughness: 0.4 }),
    gold: im(0xe0b040, { metalness: 0.85, roughness: 0.3 }), bamboo: im(0xc9ad62), paper: im(0xfbfaf4, { roughness: 0.9 }),
    clay: im(0xb65a2e, { roughness: 0.9 }), cane: im(0xc9a15e, { roughness: 0.9, side: THREE.DoubleSide }), orange: im(0xf0a02a), leaf: im(0x3f8a3a),
    brown: im(0x6b4a2e), lens: im(0xbfe0f2, { transparent: true, opacity: 0.6, side: THREE.DoubleSide }), lightBlue: im(0xbfe0f2),
    glassWarm: im(0xffe7a8, { emissive: 0xffb84a, emissiveIntensity: 0.9, transparent: true, opacity: 0.88 }),
    marble: [0xe0413a, 0x2f7fd0, 0x3fae5a, 0xf2c230].map(function (c) { return im(c, { roughness: 0.1, metalness: 0.1 }); }),
    face: im(0xfbf7ee), egg: im(0xf3e6cf), ring: im(0xffd25a, { emissive: 0xffc23a, emissiveIntensity: 1 }),
    steel: im(0xcfd4da, { metalness: 0.55, roughness: 0.3 }), willow: im(0xe3c48a, { roughness: 0.7 }),
    teddy: im(0xa8743f, { roughness: 1 }), teddyL: im(0xe8c89a, { roughness: 1 }), pink: im(0xf08cb4, { roughness: 0.5 }),
    bubble: im(0xe6f6ff, { transparent: true, opacity: 0.45, roughness: 0.05 }), plastic: im(0x7fc4ec, { transparent: true, opacity: 0.78, roughness: 0.15 }),
    woodRed: im(0x8a3a22, { roughness: 0.6 }), drumSkin: im(0xeadcc0, { roughness: 0.9 }), gourd: im(0xb8742e, { roughness: 0.6 }),
    blueD: im(0x2e62b8, { side: THREE.DoubleSide }), greenD: im(0x3c9a4a, { side: THREE.DoubleSide }),
    pad: im(0x3f8f3a, { side: THREE.DoubleSide, roughness: 0.7 }), petal: im(0xfdf6f0, { roughness: 0.6 }), petalPink: im(0xf2a7c3, { roughness: 0.6 }),
    parrot: im(0x3fbf3f, { roughness: 0.6 }), parrotD: im(0x2c8f3a, { roughness: 0.6 }), teal: im(0x23a3a0),
    woodY: im(0x9a6a3a, { roughness: 0.8 }), leather: im(0x7a4a2a), coco: im(0x5f9a2e, { roughness: 0.7 }), coco2: im(0x86b03e, { roughness: 0.7 }),
    thread: im(0xf0508a, { roughness: 0.8 })
  };
  function mm(geo, mat, parent, x, y, z) { var m = new THREE.Mesh(geo, mat); m.position.set(x || 0, y || 0, z || 0); m.castShadow = true; m.receiveShadow = true; parent.add(m); return m; }
  function V2(a) { return a.map(function (q) { return new THREE.Vector2(q[0], q[1]); }); }
  function mkKite() {
    var g = new THREE.Group(), k = new THREE.Group(), a = new THREE.Shape(), b = new THREE.Shape();
    a.moveTo(0, 1.1); a.lineTo(-0.75, 0.3); a.lineTo(0, -0.8); a.lineTo(0, 1.1);
    b.moveTo(0, 1.1); b.lineTo(0, -0.8); b.lineTo(0.75, 0.3); b.lineTo(0, 1.1);
    mm(new THREE.ShapeGeometry(a), IMT.redD, k); mm(new THREE.ShapeGeometry(b), IMT.yellowD, k);
    mm(new THREE.BoxGeometry(0.03, 1.9, 0.03), IMT.bamboo, k, 0, 0.15, 0.02); mm(new THREE.BoxGeometry(1.5, 0.03, 0.03), IMT.bamboo, k, 0, 0.3, 0.02);
    for (var i = 0; i < 4; i++) mm(new THREE.BoxGeometry(0.18, 0.09, 0.02), i % 2 ? IMT.yellowD : IMT.redD, k, Math.sin(i * 1.3) * 0.12, -0.95 - i * 0.26, 0);
    k.position.y = 1.9; k.rotation.x = -0.2; g.add(k); return g;
  }
  function mkTop() {
    var g = new THREE.Group(), s = new THREE.Group();
    mm(new THREE.LatheGeometry(V2([[0, 0], [0.05, 0.02], [0.32, 0.32], [0.36, 0.42], [0.28, 0.52], [0.07, 0.56], [0.05, 0.72], [0, 0.74]]), 20), IMT.red, s);
    mm(new THREE.TorusGeometry(0.345, 0.03, 8, 24), IMT.yellow, s, 0, 0.4, 0).rotation.x = Math.PI / 2;
    mm(new THREE.TorusGeometry(0.2, 0.025, 8, 24), IMT.green, s, 0, 0.53, 0).rotation.x = Math.PI / 2;
    g.add(s); g.userData.spin = s; g.userData.spinRate = 9; return g;
  }
  function mkBook() {
    var g = new THREE.Group();
    mm(new THREE.BoxGeometry(0.95, 0.14, 0.7), IMT.blue, g, 0, 0.07, 0);
    mm(new THREE.BoxGeometry(0.9, 0.1, 0.64), IMT.white, g, 0.03, 0.08, 0);
    mm(new THREE.BoxGeometry(0.2, 0.145, 0.7), IMT.yellow, g, -0.3, 0.075, 0);
    mm(new THREE.BoxGeometry(0.85, 0.12, 0.62), IMT.red, g, 0.05, 0.2, 0.02).rotation.y = 0.35;
    g.rotation.y = 0.4; return g;
  }
  function mkBag() {
    var g = new THREE.Group();
    mm(new THREE.BoxGeometry(0.85, 1.05, 0.42), IMT.blue, g, 0, 0.53, 0);
    mm(new THREE.BoxGeometry(0.6, 0.42, 0.14), IMT.yellow, g, 0, 0.35, 0.26);
    mm(new THREE.TorusGeometry(0.16, 0.035, 8, 20, Math.PI), IMT.black, g, 0, 1.05, 0);
    mm(new THREE.BoxGeometry(0.1, 0.9, 0.05), IMT.black, g, -0.25, 0.55, -0.24); mm(new THREE.BoxGeometry(0.1, 0.9, 0.05), IMT.black, g, 0.25, 0.55, -0.24);
    return g;
  }
  function mkLantern() {
    var g = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.3, 0.34, 0.14, 20), IMT.red, g, 0, 0.07, 0);
    mm(new THREE.SphereGeometry(0.24, 20, 14), IMT.glassWarm, g, 0, 0.42, 0).scale.y = 1.25;
    mm(new THREE.CylinderGeometry(0.06, 0.3, 0.18, 20), IMT.red, g, 0, 0.78, 0);
    mm(new THREE.TorusGeometry(0.26, 0.02, 6, 24, Math.PI), IMT.black, g, 0, 0.86, 0);
    [-0.29, 0.29].forEach(function (x) { mm(new THREE.BoxGeometry(0.03, 0.62, 0.03), IMT.black, g, x, 0.46, 0); });
    return g;
  }
  function mkDuck() {
    var g = new THREE.Group();
    mm(new THREE.SphereGeometry(0.34, 20, 14), IMT.yellow, g, 0, 0.3, 0).scale.set(1, 0.85, 1.3);
    mm(new THREE.SphereGeometry(0.22, 20, 14), IMT.yellow, g, 0, 0.66, 0.26);
    mm(new THREE.ConeGeometry(0.08, 0.2, 12), IMT.orange, g, 0, 0.64, 0.52).rotation.x = Math.PI / 2;
    [-0.09, 0.09].forEach(function (x) { mm(new THREE.SphereGeometry(0.035, 8, 6), IMT.black, g, x, 0.73, 0.44); });
    g.rotation.y = -0.7; return g;
  }
  function mkKey() {
    var g = new THREE.Group(), k = new THREE.Group();
    mm(new THREE.TorusGeometry(0.2, 0.06, 10, 24), IMT.gold, k, -0.45, 0, 0);
    mm(new THREE.BoxGeometry(0.75, 0.08, 0.08), IMT.gold, k, 0.1, 0, 0);
    mm(new THREE.BoxGeometry(0.08, 0.2, 0.08), IMT.gold, k, 0.38, -0.12, 0); mm(new THREE.BoxGeometry(0.08, 0.14, 0.08), IMT.gold, k, 0.24, -0.09, 0);
    k.position.y = 0.45; k.rotation.z = 0.2; g.add(k); g.userData.spin = k; g.userData.spinRate = 1.2; return g;
  }
  function mkWatch() {
    var g = new THREE.Group(), w = new THREE.Group();
    mm(new THREE.TorusGeometry(0.22, 0.06, 10, 28), IMT.brown, w);
    mm(new THREE.CylinderGeometry(0.15, 0.15, 0.06, 24), IMT.gold, w, 0, 0.26, 0).rotation.x = Math.PI / 2;
    mm(new THREE.CylinderGeometry(0.12, 0.12, 0.065, 24), IMT.face, w, 0, 0.26, 0.005).rotation.x = Math.PI / 2;
    w.position.y = 0.32; g.add(w); g.userData.spin = w; g.userData.spinRate = 1.2; return g;
  }
  function mkMarbles() {
    var g = new THREE.Group();
    [[0, 0], [0.3, 0.1], [-0.2, 0.25], [0.12, -0.28]].forEach(function (q, i) { mm(new THREE.SphereGeometry(0.13, 16, 12), IMT.marble[i], g, q[0], 0.13, q[1]); });
    return g;
  }
  function mkCar() {
    var g = new THREE.Group();
    mm(new THREE.BoxGeometry(1.0, 0.26, 0.5), IMT.red, g, 0, 0.26, 0);
    mm(new THREE.BoxGeometry(0.55, 0.24, 0.46), IMT.lightBlue, g, -0.05, 0.5, 0);
    [[-0.32, 0.26], [0.32, 0.26], [-0.32, -0.26], [0.32, -0.26]].forEach(function (q) { mm(new THREE.CylinderGeometry(0.13, 0.13, 0.08, 16), IMT.black, g, q[0], 0.13, q[1]).rotation.x = Math.PI / 2; });
    g.rotation.y = -0.6; return g;
  }
  function mkGlasses() {
    var g = new THREE.Group();
    [-0.19, 0.19].forEach(function (x) { mm(new THREE.TorusGeometry(0.14, 0.025, 8, 24), IMT.black, g, x, 0.15, 0); mm(new THREE.CircleGeometry(0.13, 20), IMT.lens, g, x, 0.15, 0.001); });
    mm(new THREE.BoxGeometry(0.1, 0.03, 0.03), IMT.black, g, 0, 0.2, 0);
    [-0.33, 0.33].forEach(function (x) { mm(new THREE.BoxGeometry(0.03, 0.03, 0.5), IMT.black, g, x, 0.17, -0.25); });
    g.rotation.y = 0.5; return g;
  }
  function mkBall() {
    var g = new THREE.Group(), b = new THREE.Group();
    mm(new THREE.SphereGeometry(0.24, 20, 14), IMT.red, b);
    mm(new THREE.TorusGeometry(0.242, 0.014, 6, 32), IMT.white, b);
    b.position.y = 0.24; g.add(b); g.userData.spin = b; g.userData.spinRate = 1.5; return g;
  }
  function mkFootball() {
    var g = new THREE.Group(), b = new THREE.Group();
    var ico = new THREE.IcosahedronGeometry(0.45, 1);
    mm(ico, IMT.white, b);
    b.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(0.455, 0)), new THREE.LineBasicMaterial({ color: 0x1e1e1e })));
    b.position.y = 0.45; g.add(b); g.userData.spin = b; g.userData.spinRate = 0.8; return g;
  }
  function mkFlute() {
    var g = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.055, 0.055, 1.5, 12), IMT.bamboo, g, 0, 0.06, 0).rotation.z = Math.PI / 2;
    for (var i = 0; i < 6; i++) mm(new THREE.CylinderGeometry(0.018, 0.018, 0.02, 8), IMT.black, g, -0.3 + i * 0.12, 0.115, 0);
    [-0.6, 0.62].forEach(function (x) { mm(new THREE.CylinderGeometry(0.062, 0.062, 0.05, 12), IMT.red, g, x, 0.06, 0).rotation.z = Math.PI / 2; });
    g.rotation.y = 0.3; return g;
  }
  function mkBoat() {
    var g = new THREE.Group(), hull = new THREE.Shape(), sail = new THREE.Shape();
    hull.moveTo(-0.7, 0.28); hull.lineTo(0.7, 0.28); hull.lineTo(0.42, 0); hull.lineTo(-0.42, 0); hull.lineTo(-0.7, 0.28);
    var hg = new THREE.ExtrudeGeometry(hull, { depth: 0.36, bevelEnabled: false }); hg.translate(0, 0, -0.18); mm(hg, IMT.paper, g);
    sail.moveTo(-0.32, 0.28); sail.lineTo(0.32, 0.28); sail.lineTo(0, 0.78); sail.lineTo(-0.32, 0.28);
    var sg2 = new THREE.ExtrudeGeometry(sail, { depth: 0.03, bevelEnabled: false }); sg2.translate(0, 0, -0.015); mm(sg2, IMT.paper, g);
    g.rotation.y = 0.8; return g;
  }
  function mkPot() {
    var g = new THREE.Group();
    mm(new THREE.LatheGeometry(V2([[0, 0], [0.22, 0], [0.42, 0.22], [0.48, 0.45], [0.4, 0.7], [0.2, 0.84], [0.15, 0.95], [0.21, 1.02], [0.19, 1.06], [0.12, 1.0], [0, 1.0]]), 24), IMT.clay, g);
    mm(new THREE.TorusGeometry(0.47, 0.02, 6, 32), IMT.yellow, g, 0, 0.45, 0).rotation.x = Math.PI / 2;
    return g;
  }
  function mkEggs() {
    var g = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.5, 0.34, 0.32, 20, 1, true), IMT.cane, g, 0, 0.16, 0);
    mm(new THREE.CircleGeometry(0.34, 20), IMT.cane, g, 0, 0.01, 0).rotation.x = -Math.PI / 2;
    mm(new THREE.TorusGeometry(0.5, 0.03, 6, 28), IMT.brown, g, 0, 0.32, 0).rotation.x = Math.PI / 2;
    [[0, 0], [0.18, 0.1], [-0.16, 0.12], [0.06, -0.2], [-0.12, -0.14]].forEach(function (q) { mm(new THREE.SphereGeometry(0.11, 12, 10), IMT.egg, g, q[0], 0.28, q[1]).scale.y = 1.3; });
    return g;
  }
  function mkMango() {
    var g = new THREE.Group();
    mm(new THREE.SphereGeometry(0.25, 20, 14), IMT.orange, g, 0, 0.3, 0).scale.set(1, 1.25, 0.9);
    mm(new THREE.CylinderGeometry(0.02, 0.02, 0.1, 6), IMT.brown, g, 0, 0.64, 0);
    mm(new THREE.SphereGeometry(0.12, 12, 8), IMT.leaf, g, 0.1, 0.66, 0).scale.set(1.6, 0.25, 0.7);
    return g;
  }
  function SPH(r) { return new THREE.SphereGeometry(r, 16, 12); }
  // a round stick from point a to point b
  function stickM(a, b, r, mat, parent) {
    var p = new THREE.Vector3(a[0], a[1], a[2]), d = new THREE.Vector3(b[0], b[1], b[2]).sub(p), L = d.length();
    var m = mm(new THREE.CylinderGeometry(r, r, L, 6), mat, parent);
    m.position.copy(p).addScaledVector(d, 0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
    return m;
  }
  function mkHandFan() {
    var g = new THREE.Group(), f = new THREE.Group();
    for (var i = 0; i < 8; i++) mm(new THREE.CircleGeometry(0.5, 6, i * Math.PI / 4, Math.PI / 4), i % 2 ? IMT.redD : IMT.yellowD, f);
    mm(new THREE.TorusGeometry(0.5, 0.035, 6, 32), IMT.green, f);
    mm(new THREE.CircleGeometry(0.13, 16), IMT.greenD, f, 0, 0, 0.003);
    mm(new THREE.CylinderGeometry(0.035, 0.035, 0.6, 8), IMT.bamboo, f, 0, -0.8, 0);
    f.rotation.x = -Math.PI / 2 - 0.1; f.position.y = 0.08; g.add(f); g.rotation.y = 2.4; return g;
  }
  function mkTeddy() {
    var g = new THREE.Group(), fur = IMT.teddy, lt = IMT.teddyL;
    mm(SPH(0.34), fur, g, 0, 0.36, 0).scale.set(1, 1.1, 0.9);
    mm(SPH(0.2), lt, g, 0, 0.36, 0.2).scale.set(1, 1.1, 0.5);
    mm(SPH(0.27), fur, g, 0, 0.86, 0.02);
    mm(SPH(0.11), lt, g, 0, 0.8, 0.23).scale.set(1.1, 0.85, 0.8);
    mm(SPH(0.04), IMT.black, g, 0, 0.84, 0.31);
    [-1, 1].forEach(function (s) {
      mm(SPH(0.1), fur, g, s * 0.19, 1.08, 0);
      mm(SPH(0.055), lt, g, s * 0.19, 1.08, 0.05);
      mm(SPH(0.12), fur, g, s * 0.33, 0.45, 0.08).scale.set(0.8, 1.5, 0.8);
      mm(SPH(0.13), fur, g, s * 0.18, 0.1, 0.25).scale.set(0.9, 0.8, 1.5);
      mm(SPH(0.03), IMT.black, g, s * 0.09, 0.93, 0.27);
      mm(new THREE.ConeGeometry(0.07, 0.15, 8), IMT.red, g, s * 0.08, 0.64, 0.26).rotation.z = s * Math.PI / 2;
    });
    g.rotation.y = -0.5; return g;
  }
  function mkBank() {
    var g = new THREE.Group();
    mm(new THREE.LatheGeometry(V2([[0, 0], [0.18, 0], [0.34, 0.12], [0.42, 0.32], [0.38, 0.52], [0.22, 0.66], [0.08, 0.72], [0, 0.73]]), 24), IMT.clay, g);
    mm(new THREE.TorusGeometry(0.418, 0.022, 6, 32), IMT.yellow, g, 0, 0.32, 0).rotation.x = Math.PI / 2;
    mm(new THREE.TorusGeometry(0.372, 0.02, 6, 32), IMT.green, g, 0, 0.52, 0).rotation.x = Math.PI / 2;
    for (var i = 0; i < 8; i++) { var a = i / 8 * Math.PI * 2; mm(SPH(0.035), IMT.white, g, Math.cos(a) * 0.405, 0.42, Math.sin(a) * 0.405); }
    mm(new THREE.BoxGeometry(0.18, 0.03, 0.04), IMT.black, g, 0, 0.72, 0);
    return g;
  }
  function mkPencilBox() {
    var g = new THREE.Group();
    mm(new THREE.BoxGeometry(0.8, 0.12, 0.28), IMT.blue, g, 0, 0.06, 0);
    mm(new THREE.BoxGeometry(0.82, 0.03, 0.3), IMT.red, g, 0, 0.135, 0);
    mm(new THREE.BoxGeometry(0.3, 0.005, 0.16), IMT.yellow, g, 0.15, 0.152, 0);
    [[0.26, IMT.yellow, 0], [0.34, IMT.green, 0.12]].forEach(function (q) {
      var p = new THREE.Group(); p.position.set(q[2], 0.03, q[0]); p.rotation.y = 0.1; g.add(p);
      mm(new THREE.CylinderGeometry(0.03, 0.03, 0.62, 6), q[1], p).rotation.z = Math.PI / 2;
      mm(new THREE.ConeGeometry(0.03, 0.08, 6), IMT.willow, p, 0.35, 0, 0).rotation.z = -Math.PI / 2;
      mm(new THREE.CylinderGeometry(0.031, 0.031, 0.06, 6), IMT.pink, p, -0.33, 0, 0).rotation.z = Math.PI / 2;
    });
    g.rotation.y = -0.3; return g;
  }
  function mkAlarm() {
    var g = new THREE.Group(), c = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.28, 0.28, 0.16, 24), IMT.red, c).rotation.x = Math.PI / 2;
    mm(new THREE.CylinderGeometry(0.23, 0.23, 0.02, 24), IMT.face, c, 0, 0, 0.08).rotation.x = Math.PI / 2;
    mm(new THREE.BoxGeometry(0.025, 0.16, 0.01), IMT.black, c, 0, 0.07, 0.095);
    mm(new THREE.BoxGeometry(0.12, 0.022, 0.01), IMT.black, c, 0.055, 0, 0.095);
    [-1, 1].forEach(function (s) {
      mm(new THREE.SphereGeometry(0.13, 16, 8, 0, Math.PI * 2, 0, Math.PI / 2), IMT.gold, c, s * 0.16, 0.25, 0).rotation.z = -s * 0.5;
      mm(new THREE.CylinderGeometry(0.03, 0.045, 0.12, 8), IMT.black, c, s * 0.17, -0.3, 0).rotation.z = s * 0.35;
    });
    mm(new THREE.BoxGeometry(0.03, 0.1, 0.03), IMT.black, c, 0, 0.33, 0);
    c.position.y = 0.36; g.add(c); g.rotation.y = 0.5; return g;
  }
  function mkBat() {
    var g = new THREE.Group(), b = new THREE.Group();
    mm(new THREE.BoxGeometry(0.36, 0.07, 1.4), IMT.willow, b, 0, 0.035, 0);
    mm(new THREE.CylinderGeometry(0.05, 0.05, 0.55, 10), IMT.black, b, 0, 0.05, 0.97).rotation.x = Math.PI / 2;
    mm(SPH(0.06), IMT.black, b, 0, 0.05, 1.26);
    mm(new THREE.BoxGeometry(0.28, 0.004, 0.26), IMT.red, b, 0, 0.072, 0.4);
    mm(new THREE.BoxGeometry(0.28, 0.004, 0.08), IMT.blue, b, 0, 0.072, 0.18);
    b.position.z = -0.3; g.add(b); g.rotation.y = 0.9; return g;
  }
  function mkTiffin() {
    var g = new THREE.Group();
    for (var i = 0; i < 3; i++) {
      mm(new THREE.CylinderGeometry(0.26, 0.25, 0.2, 20), IMT.steel, g, 0, 0.1 + i * 0.21, 0);
      mm(new THREE.TorusGeometry(0.262, 0.014, 6, 24), IMT.steel, g, 0, 0.205 + i * 0.21, 0).rotation.x = Math.PI / 2;
    }
    mm(new THREE.SphereGeometry(0.26, 20, 8, 0, Math.PI * 2, 0, Math.PI / 2), IMT.steel, g, 0, 0.62, 0).scale.y = 0.3;
    [-1, 1].forEach(function (s) { mm(new THREE.BoxGeometry(0.03, 0.66, 0.06), IMT.steel, g, s * 0.285, 0.36, 0); mm(new THREE.BoxGeometry(0.05, 0.08, 0.08), IMT.red, g, s * 0.29, 0.52, 0); });
    mm(new THREE.TorusGeometry(0.28, 0.022, 8, 20, Math.PI), IMT.steel, g, 0, 0.66, 0);
    return g;
  }
  function mkBrush() {
    var g = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.13, 0.11, 0.3, 16), IMT.green, g, 0, 0.15, 0);
    var b = new THREE.Group(); b.position.set(0.03, 0.08, 0); b.rotation.z = -0.25; g.add(b);
    mm(new THREE.BoxGeometry(0.045, 0.6, 0.03), IMT.blue, b, 0, 0.3, 0);
    mm(new THREE.BoxGeometry(0.05, 0.12, 0.06), IMT.white, b, 0, 0.55, 0.035);
    var p = new THREE.Group(); p.position.set(-0.05, 0.08, 0.02); p.rotation.z = 0.35; g.add(p);
    mm(new THREE.CylinderGeometry(0.06, 0.06, 0.42, 12), IMT.white, p, 0, 0.21, 0).scale.z = 0.6;
    mm(new THREE.CylinderGeometry(0.061, 0.061, 0.1, 12), IMT.red, p, 0, 0.28, 0).scale.z = 0.6;
    mm(new THREE.CylinderGeometry(0.03, 0.03, 0.06, 8), IMT.red, p, 0, 0.45, 0);
    return g;
  }
  function mkSoap() {
    var g = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.34, 0.28, 0.06, 20), IMT.lightBlue, g, 0, 0.03, 0).scale.z = 0.7;
    mm(SPH(0.2), IMT.pink, g, 0, 0.1, 0).scale.set(1.2, 0.4, 0.75);
    [[0.15, 0.24, 0.05, 0.06], [-0.1, 0.3, -0.05, 0.05], [0.02, 0.42, 0.02, 0.07], [0.2, 0.46, -0.06, 0.04], [-0.16, 0.52, 0.04, 0.045]].forEach(function (q) {
      mm(SPH(q[3]), IMT.bubble, g, q[0], q[1], q[2]).castShadow = false;
    });
    return g;
  }
  function mkBottle() {
    var g = new THREE.Group();
    mm(new THREE.LatheGeometry(V2([[0, 0], [0.15, 0], [0.165, 0.02], [0.165, 0.6], [0.12, 0.72], [0.07, 0.78], [0.07, 0.82], [0, 0.82]]), 20), IMT.plastic, g);
    mm(new THREE.CylinderGeometry(0.08, 0.08, 0.09, 14), IMT.white, g, 0, 0.86, 0);
    mm(new THREE.CylinderGeometry(0.172, 0.172, 0.2, 20, 1, true), IMT.redD, g, 0, 0.32, 0);
    return g;
  }
  function mkDhol() {
    var g = new THREE.Group(), d = new THREE.Group();
    function rad(y) { return 0.3 + 0.1 * (1 - 4 * y * y); }
    var prof = [];
    for (var i = 0; i <= 8; i++) { var y = -0.5 + i / 8; prof.push([rad(y), y]); }
    mm(new THREE.LatheGeometry(V2(prof), 24), IMT.woodRed, d);
    [-1, 1].forEach(function (s) {
      mm(new THREE.CylinderGeometry(0.305, 0.305, 0.03, 24), IMT.drumSkin, d, 0, s * 0.5, 0);
      mm(new THREE.TorusGeometry(0.305, 0.025, 6, 24), IMT.brown, d, 0, s * 0.5, 0).rotation.x = Math.PI / 2;
    });
    // zig-zag lacing that hugs the barrel
    var pts = [];
    function lace(a0, a1, up) {
      for (var j = 0; j < 4; j++) {
        var t0 = j / 4, t1 = (j + 1) / 4, ya = up ? -0.5 + t0 : 0.5 - t0, yb = up ? -0.5 + t1 : 0.5 - t1;
        var aa = a0 + (a1 - a0) * t0, ab = a0 + (a1 - a0) * t1, ra = rad(ya) + 0.012, rb = rad(yb) + 0.012;
        pts.push(new THREE.Vector3(Math.cos(aa) * ra, ya, Math.sin(aa) * ra), new THREE.Vector3(Math.cos(ab) * rb, yb, Math.sin(ab) * rb));
      }
    }
    for (var k = 0; k < 10; k++) { var a = k / 10 * Math.PI * 2, st = Math.PI / 10; lace(a, a + st, true); lace(a + st, a + 2 * st, false); }
    d.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xf2c230 })));
    d.rotation.z = Math.PI / 2; d.position.y = 0.4; g.add(d); g.rotation.y = 0.3; return g;
  }
  function mkEktara() {
    var g = new THREE.Group(), e = new THREE.Group();
    mm(SPH(0.24), IMT.gourd, e).scale.set(1, 0.85, 1);
    mm(new THREE.TorusGeometry(0.235, 0.02, 6, 24), IMT.red, e).rotation.x = Math.PI / 2;
    [-1, 1].forEach(function (s) { stickM([s * 0.18, 0.1, 0], [s * 0.05, 1.3, 0], 0.025, IMT.bamboo, e); });
    mm(new THREE.CylinderGeometry(0.025, 0.025, 0.26, 8), IMT.brown, e, 0, 1.22, 0).rotation.z = Math.PI / 2;
    stickM([0, 0.2, 0], [0, 1.22, 0], 0.006, IMT.white, e);
    mm(SPH(0.05), IMT.red, e, 0, 1.33, 0);
    e.rotation.x = -Math.PI / 2 + 0.08; e.position.y = 0.24; g.add(e); g.rotation.y = 0.15; return g;
  }
  function mkUmbrella() {
    var g = new THREE.Group(), u = new THREE.Group();
    for (var i = 0; i < 8; i++) mm(new THREE.ConeGeometry(1.0, 0.42, 2, 1, true, i * Math.PI / 4, Math.PI / 4), i % 2 ? IMT.blueD : IMT.redD, u);
    for (var k = 0; k < 8; k++) { var a = k * Math.PI / 4; mm(SPH(0.03), IMT.black, u, Math.sin(a), -0.21, Math.cos(a)); }
    mm(SPH(0.04), IMT.black, u, 0, 0.24, 0);
    mm(new THREE.CylinderGeometry(0.022, 0.022, 1.86, 8), IMT.black, u, 0, -0.72, 0);
    mm(new THREE.TorusGeometry(0.1, 0.03, 8, 16, Math.PI), IMT.brown, u, 0.1, -1.65, 0).rotation.z = Math.PI;
    u.rotation.z = 0.96; u.position.y = 0.95; g.add(u); return g;
  }
  function mkParrot() {
    var g = new THREE.Group(), p = new THREE.Group();
    mm(new THREE.CylinderGeometry(0.46, 0.5, 0.1, 20), IMT.woodRed, g, 0, 0.05, 0);
    for (var i = 0; i < 16; i++) { var a = i / 16 * Math.PI * 2; mm(new THREE.CylinderGeometry(0.012, 0.012, 1.0, 5), IMT.gold, g, Math.cos(a) * 0.44, 0.6, Math.sin(a) * 0.44); }
    [0.12, 1.1].forEach(function (y) { mm(new THREE.TorusGeometry(0.44, 0.02, 6, 28), IMT.gold, g, 0, y, 0).rotation.x = Math.PI / 2; });
    [0, Math.PI / 2].forEach(function (a) { var d = mm(new THREE.TorusGeometry(0.44, 0.015, 6, 20, Math.PI), IMT.gold, g, 0, 1.1, 0); d.rotation.y = a; d.scale.y = 0.6; });
    mm(new THREE.TorusGeometry(0.06, 0.015, 6, 12), IMT.gold, g, 0, 1.42, 0);
    mm(new THREE.CylinderGeometry(0.02, 0.02, 0.8, 6), IMT.brown, g, 0, 0.5, 0).rotation.z = Math.PI / 2;
    p.position.set(0, 0.52, 0); g.add(p);
    mm(SPH(0.15), IMT.parrot, p, 0, 0.17, 0).scale.set(0.9, 1.3, 0.95);
    [-1, 1].forEach(function (s) { mm(SPH(0.1), IMT.parrotD, p, s * 0.1, 0.16, -0.02).scale.set(0.45, 1.3, 1); mm(SPH(0.018), IMT.black, p, s * 0.07, 0.44, 0.08); });
    mm(SPH(0.11), IMT.parrot, p, 0, 0.4, 0.03);
    mm(new THREE.ConeGeometry(0.045, 0.12, 8), IMT.red, p, 0, 0.37, 0.14).rotation.x = Math.PI / 2 + 0.7;
    mm(new THREE.TorusGeometry(0.09, 0.012, 6, 16), IMT.black, p, 0, 0.32, 0.01).rotation.x = Math.PI / 2 - 0.3;
    mm(new THREE.BoxGeometry(0.07, 0.34, 0.025), IMT.teal, p, 0, -0.05, -0.12).rotation.x = 0.45;
    g.userData.wiggle = p; return g;
  }
  function mkSling() {
    var g = new THREE.Group(), s = new THREE.Group();
    stickM([0, 0, 0], [0, 0.62, 0], 0.05, IMT.woodY, s);
    stickM([0, 0.6, 0], [-0.23, 1.02, 0], 0.045, IMT.woodY, s); stickM([0, 0.6, 0], [0.23, 1.02, 0], 0.045, IMT.woodY, s);
    stickM([-0.23, 1.0, 0], [-0.05, 1.42, 0], 0.016, IMT.red, s); stickM([0.23, 1.0, 0], [0.05, 1.42, 0], 0.016, IMT.red, s);
    mm(new THREE.BoxGeometry(0.16, 0.1, 0.04), IMT.leather, s, 0, 1.45, 0);
    s.rotation.x = -Math.PI / 2; s.position.y = 0.06; g.add(s); g.rotation.y = 0.7; return g;
  }
  function mkCoconut() {
    var g = new THREE.Group();
    mm(SPH(0.34), IMT.coco, g, 0, 0.36, 0).scale.set(1, 1.12, 1);
    mm(new THREE.CylinderGeometry(0.1, 0.13, 0.06, 12), IMT.coco2, g, 0, 0.74, 0);
    stickM([0.02, 0.74, 0], [0.16, 1.1, 0.02], 0.02, IMT.white, g);
    mm(SPH(0.3), IMT.coco2, g, 0.52, 0.3, 0.12).scale.set(1.12, 1, 1);
    mm(SPH(0.05), IMT.brown, g, 0.84, 0.32, 0.14);
    return g;
  }
  function mkLily() {
    var g = new THREE.Group(), f = new THREE.Group();
    mm(new THREE.CircleGeometry(0.55, 24, 0.3, Math.PI * 2 - 0.6), IMT.pad, g, 0, 0.03, 0).rotation.x = -Math.PI / 2;
    f.position.set(0.1, 0.05, 0.04); g.add(f);
    for (var i = 0; i < 10; i++) { var p = new THREE.Group(); p.rotation.y = i / 10 * Math.PI * 2; f.add(p); var m = mm(SPH(0.1), i % 2 ? IMT.petal : IMT.petalPink, p, 0, 0.08, 0.17); m.scale.set(0.55, 0.25, 1.5); m.rotation.x = -0.55; }
    for (var j = 0; j < 7; j++) { var q = new THREE.Group(); q.rotation.y = j / 7 * Math.PI * 2 + 0.3; f.add(q); var n = mm(SPH(0.08), IMT.petalPink, q, 0, 0.16, 0.09); n.scale.set(0.5, 0.25, 1.4); n.rotation.x = -1.0; }
    mm(SPH(0.06), IMT.yellow, f, 0, 0.17, 0);
    return g;
  }
  function mkNatai() {
    var g = new THREE.Group(), n = new THREE.Group();
    [-1, 1].forEach(function (s) { mm(new THREE.CylinderGeometry(0.3, 0.3, 0.04, 6), IMT.bamboo, n, 0, s * 0.3, 0); });
    for (var i = 0; i < 6; i++) { var a = i / 6 * Math.PI * 2; mm(new THREE.CylinderGeometry(0.022, 0.022, 0.64, 5), IMT.brown, n, Math.cos(a) * 0.26, 0, Math.sin(a) * 0.26); }
    mm(new THREE.CylinderGeometry(0.2, 0.2, 0.52, 18), IMT.thread, n);
    mm(new THREE.CylinderGeometry(0.035, 0.035, 1.5, 8), IMT.brown, n);
    n.rotation.z = Math.PI / 2; n.position.y = 0.3; g.add(n); g.rotation.y = 0.5; return g;
  }
  // at: [plan x, plan z, height above that floor, inches]; room = a room key, or place = [en, bn] for the yard
  var ITEMS = [
    { k: "kite", en: "red kite", bn: "লাল ঘুড়ি", room: "bed3", at: [40, 305, 0], pts: 100, make: mkKite, s: 1 },
    { k: "top", en: "spinning top", bn: "লাটিম", room: "bed1", at: [52, 132, 0], pts: 100, make: mkTop, s: 1.2 },
    { k: "book", en: "storybook", bn: "গল্পের বই", room: "bed2", at: [403, 130, 0], pts: 100, make: mkBook, s: 1 },
    { k: "bag", en: "school bag", bn: "স্কুলব্যাগ", room: "bed4", at: [360, 392, 0], pts: 100, make: mkBag, s: 1 },
    { k: "lantern", en: "hurricane lantern", bn: "হারিকেন", room: "kitchen", at: [200, 72, 0], pts: 120, make: mkLantern, s: 1.1 },
    { k: "duck", en: "rubber duck", bn: "রাবারের হাঁস", room: "bathC", at: [284, 62, 0], pts: 150, make: mkDuck, s: 1 },
    { k: "key", en: "golden key", bn: "সোনার চাবি", room: "bathL", at: [70, 224, 0], pts: 150, make: mkKey, s: 1.2 },
    { k: "watch", en: "grandpa's watch", bn: "দাদুর হাতঘড়ি", room: "bathR", at: [394, 226, 0], pts: 150, make: mkWatch, s: 1.3 },
    { k: "marbles", en: "marbles", bn: "মার্বেল", room: "dining", at: [128, 214, 0], pts: 120, make: mkMarbles, s: 1.5 },
    { k: "car", en: "toy car", bn: "খেলনা গাড়ি", room: "dining", at: [326, 214, 0], pts: 120, make: mkCar, s: 1 },
    { k: "glasses", en: "grandpa's glasses", bn: "দাদুর চশমা", room: "drawing", at: [227, 361, 16], pts: 120, make: mkGlasses, s: 1.4 },
    { k: "ball", en: "cricket ball", bn: "ক্রিকেট বল", room: "drawing", at: [262, 322, 0], pts: 100, make: mkBall, s: 1.4 },
    { k: "football", en: "football", bn: "ফুটবল", room: "verandah", at: [132, 447, 0], pts: 100, make: mkFootball, s: 1 },
    { k: "flute", en: "bamboo flute", bn: "বাঁশের বাঁশি", room: "verandah", at: [60, 438, 15.5], pts: 120, make: mkFlute, s: 1 },
    { k: "boat", en: "paper boat", bn: "কাগজের নৌকা", place: ["by the pond", "পুকুর পাড়ে"], at: [-78, 669, 0], pts: 200, make: mkBoat, s: 1.1 },
    { k: "pot", en: "clay water pot", bn: "মাটির কলসি", place: ["by the tubewell", "টিউবওয়েলের পাশে"], at: [345, -118, 0], pts: 200, make: mkPot, s: 1.1 },
    { k: "eggs", en: "basket of eggs", bn: "ডিমের ঝুড়ি", place: ["by the haystack", "খড়ের গাদার পাশে"], at: [-72, -200, 0], pts: 200, make: mkEggs, s: 1.1 },
    { k: "mango", en: "ripe mango", bn: "পাকা আম", place: ["under the mango tree", "আম গাছের নিচে"], at: [735, 615, 0], pts: 200, make: mkMango, s: 1.4 },
    { k: "fan", en: "hand fan", bn: "হাতপাখা", room: "bed1", at: [80, 92, 23.4], pts: 110, make: mkHandFan, s: 1.1 },
    { k: "teddy", en: "teddy bear", bn: "টেডি বিয়ার", room: "bed2", at: [372, 88, 23.4], pts: 100, make: mkTeddy, s: 1 },
    { k: "bank", en: "clay money bank", bn: "মাটির ব্যাংক", room: "bed2", at: [425, 42, 0], pts: 120, make: mkBank, s: 1.1 },
    { k: "pencil", en: "pencil box", bn: "পেন্সিল বক্স", room: "bed3", at: [46, 404, 30], pts: 120, make: mkPencilBox, s: 1.2 },
    { k: "alarm", en: "alarm clock", bn: "এলার্ম ঘড়ি", room: "bed4", at: [310, 381, 22], pts: 110, make: mkAlarm, s: 1.2 },
    { k: "bat", en: "cricket bat", bn: "ক্রিকেট ব্যাট", room: "bed4", at: [425, 322, 0], pts: 100, make: mkBat, s: 1 },
    { k: "tiffin", en: "tiffin carrier", bn: "টিফিন ক্যারিয়ার", room: "kitchen", at: [214, 22, 33.5], pts: 120, make: mkTiffin, s: 1.1 },
    { k: "brush", en: "toothbrush", bn: "টুথব্রাশ", room: "bathC", at: [258, 24, 0], pts: 150, make: mkBrush, s: 1.3 },
    { k: "soap", en: "bar of soap", bn: "সাবান", room: "bathR", at: [432, 196, 0], pts: 150, make: mkSoap, s: 1.3 },
    { k: "bottle", en: "water bottle", bn: "পানির বোতল", room: "dining", at: [252, 232, 30], pts: 110, make: mkBottle, s: 1.1 },
    { k: "dhol", en: "dhol drum", bn: "ঢোল", room: "drawing", at: [280, 404, 0], pts: 110, make: mkDhol, s: 1.1 },
    { k: "ektara", en: "ektara", bn: "একতারা", room: "drawing", at: [180, 369, 16], pts: 120, make: mkEktara, s: 1 },
    { k: "umbrella", en: "umbrella", bn: "ছাতা", room: "verandah", at: [300, 440, 0], pts: 100, make: mkUmbrella, s: 1 },
    { k: "parrot", en: "parrot in a cage", bn: "খাঁচার টিয়া পাখি", room: "verandah", at: [438, 437, 0], pts: 120, make: mkParrot, s: 1 },
    { k: "sling", en: "slingshot", bn: "গুলতি", place: ["under the jackfruit tree", "কাঁঠাল গাছের নিচে"], at: [-252.5, -75, 0], pts: 200, make: mkSling, s: 1.3 },
    { k: "coconut", en: "green coconuts", bn: "ডাব", place: ["under a coconut palm", "নারকেল গাছের নিচে"], at: [743.5, 177, 0], pts: 200, make: mkCoconut, s: 1.2 },
    { k: "lily", en: "water lily", bn: "শাপলা ফুল", place: ["on the pond bank, house side", "পুকুরের বাড়ির দিকের পাড়ে"], at: [-276.5, 525, 0], pts: 200, make: mkLily, s: 1.4 },
    { k: "natai", en: "kite reel (natai)", bn: "নাটাই", place: ["on the north side of the house", "বাড়ির উত্তর পাশে"], at: [-60, 201, 0], pts: 200, make: mkNatai, s: 1.2 }
  ];
  function itemName(it) { return lang === "bn" ? it.bn : it.en; }
  function placeName(it) { return it.place ? it.place[lang === "bn" ? 1 : 0] : (lang === "bn" ? ROOM[it.room].bn : ROOM[it.room].en); }

  // pictures of every item for the task banner
  var thumbs = {};
  (function () {
    var tr;
    try { tr = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); } catch (e) { return; }
    tr.setSize(128, 128, false); tr.setPixelRatio(1); tr.outputEncoding = THREE.sRGBEncoding;
    var ts = new THREE.Scene(), tc = new THREE.PerspectiveCamera(32, 1, 0.05, 60);
    ts.add(new THREE.HemisphereLight(0xffffff, 0x8a6a4a, 1.0));
    var dl = new THREE.DirectionalLight(0xffffff, 0.9); dl.position.set(2, 4, 3); ts.add(dl);
    ITEMS.forEach(function (it) {
      var g = it.make(); ts.add(g);
      var box = new THREE.Box3().setFromObject(g), c = box.getCenter(new THREE.Vector3()), sz = box.getSize(new THREE.Vector3()).length();
      tc.position.set(c.x + sz * 0.95, c.y + sz * 0.75, c.z + sz * 1.35); tc.lookAt(c);
      tr.render(ts, tc); thumbs[it.k] = tr.domElement.toDataURL("image/png"); ts.remove(g);
    });
    tr.dispose(); if (tr.forceContextLoss) tr.forceContextLoss();
  })();

  // place every item in the house and yard, each with a slightly bigger invisible ball that catches taps
  var ringGeo = new THREE.TorusGeometry(0.85, 0.05, 8, 40), hitMat = new THREE.MeshBasicMaterial({ visible: false });
  ITEMS.forEach(function (it, i) {
    it.obj = it.make(); it.obj.scale.setScalar(it.s);
    it.baseY = floorAt(it.at[0], it.at[1]) + it.at[2];
    it.obj.position.set(X(it.at[0]), Y(it.baseY), Z(it.at[1]));
    it.phase = i * 0.7;
    it.ring = new THREE.Mesh(ringGeo, IMT.ring); it.ring.rotation.x = Math.PI / 2; it.ring.visible = false;
    it.ring.position.set(X(it.at[0]), Y(it.baseY) + 0.04, Z(it.at[1]));
    scene.add(it.obj); scene.add(it.ring);
    it.obj.updateMatrixWorld(true);
    var bb = new THREE.Box3().setFromObject(it.obj), rr = Math.max(0.9, bb.getSize(new THREE.Vector3()).length() * 0.55);
    it.hit = new THREE.Mesh(new THREE.SphereGeometry(rr, 10, 8), hitMat); bb.getCenter(it.hit.position); it.hit.userData.pick = it;
    scene.add(it.hit);
  });

  /* ---------- Khalid ---------- */
  function tube(r1, r2, h, mat, parent, top) {   // a limb hanging down from its joint
    var geo = new THREE.CylinderGeometry(r1, r2, h, 12); geo.translate(0, -h / 2 + (top || 0), 0);
    var m = new THREE.Mesh(geo, mat); m.castShadow = true; parent.add(m); return m;
  }
  function mkBoy() {
    var C = {
      skin: im(0xc68a5a, { roughness: 0.65 }), skinD: im(0xad7048, { roughness: 0.65 }),
      shirt: im(0xd9412f, { roughness: 0.85 }), stripe: im(0xf2c230, { roughness: 0.85 }), shorts: im(0x2f4f86, { roughness: 0.9 }),
      belt: im(0x5a3a22), hair: im(0x1b1411, { roughness: 0.55 }), sandal: im(0x2f7fd0, { roughness: 0.7 }), sole: im(0x3a2a20),
      white: im(0xffffff, { roughness: 0.25 }), iris: im(0x3a2412, { roughness: 0.2 }), pupil: im(0x0d0806, { roughness: 0.2 }),
      lip: im(0x9a4232), mouth: im(0x5a1a14), blush: im(0xe0786a, { transparent: true, opacity: 0.35, depthWrite: false })
    };
    var g = new THREE.Group(), hips = new THREE.Group(); g.add(hips); hips.position.y = 1.55;
    mm(new THREE.CylinderGeometry(0.35, 0.37, 0.4, 16), C.shorts, hips, 0, 0.02, 0).scale.z = 0.85;
    mm(new THREE.CylinderGeometry(0.356, 0.356, 0.07, 16), C.belt, hips, 0, 0.2, 0).scale.z = 0.86;
    function leg(sx) {
      var hip = new THREE.Group(); hip.position.set(sx * 0.17, -0.05, 0); hips.add(hip);
      tube(0.19, 0.175, 0.34, C.shorts, hip, 0.1);
      tube(0.14, 0.125, 0.72, C.skin, hip);
      var knee = new THREE.Group(); knee.position.y = -0.72; hip.add(knee);
      mm(new THREE.SphereGeometry(0.127, 12, 8), C.skin, knee);
      tube(0.125, 0.095, 0.66, C.skin, knee);
      var ankle = new THREE.Group(); ankle.position.y = -0.66; knee.add(ankle);
      mm(new THREE.BoxGeometry(0.19, 0.09, 0.3), C.skin, ankle, 0, -0.04, 0.06);
      mm(new THREE.BoxGeometry(0.23, 0.04, 0.38), C.sole, ankle, 0, -0.1, 0.06);
      mm(new THREE.BoxGeometry(0.21, 0.035, 0.07), C.sandal, ankle, 0, -0.005, 0.12);
      return { hip: hip, knee: knee, ankle: ankle };
    }
    var L = leg(1), R = leg(-1);   // Khalid faces +z, so his left side is +x
    var torso = new THREE.Group(); torso.position.y = 0.18; hips.add(torso);
    mm(new THREE.LatheGeometry(V2([[0, 0], [0.37, 0], [0.4, 0.22], [0.39, 0.55], [0.37, 0.8], [0.3, 0.98], [0.14, 1.06], [0, 1.07]]), 20), C.shirt, torso).scale.z = 0.78;
    [[0.36, 0.404], [0.56, 0.396]].forEach(function (q) { mm(new THREE.CylinderGeometry(q[1], q[1] + 0.002, 0.09, 20, 1, true), C.stripe, torso, 0, q[0], 0).scale.z = 0.79; });
    mm(new THREE.TorusGeometry(0.15, 0.035, 8, 20), C.stripe, torso, 0, 1.03, 0).rotation.x = Math.PI / 2;
    mm(new THREE.BoxGeometry(0.13, 0.14, 0.02), C.stripe, torso, 0.17, 0.74, 0.265);
    mm(new THREE.CylinderGeometry(0.11, 0.12, 0.22, 12), C.skin, torso, 0, 1.13, 0);
    function arm(sx) {
      var sh = new THREE.Group(); sh.position.set(sx * 0.41, 0.9, 0); torso.add(sh);
      mm(new THREE.SphereGeometry(0.15, 12, 10), C.shirt, sh);
      tube(0.15, 0.13, 0.3, C.shirt, sh, 0.02);
      tube(0.1, 0.092, 0.46, C.skin, sh);
      var el = new THREE.Group(); el.position.y = -0.46; sh.add(el);
      mm(new THREE.SphereGeometry(0.092, 10, 8), C.skin, el);
      tube(0.09, 0.078, 0.4, C.skin, el);
      mm(new THREE.SphereGeometry(0.105, 12, 10), C.skin, el, 0, -0.47, 0.01).scale.set(0.78, 1.05, 0.95);
      mm(new THREE.SphereGeometry(0.04, 8, 6), C.skin, el, -sx * 0.06, -0.43, 0.05);
      return { sh: sh, el: el, sx: sx };
    }
    var AL = arm(1), AR = arm(-1);
    // head
    var head = new THREE.Group(); head.position.y = 1.52; torso.add(head);
    mm(new THREE.SphereGeometry(0.44, 24, 18), C.skin, head).scale.set(1, 1.03, 0.96);
    [-1, 1].forEach(function (s) { mm(new THREE.SphereGeometry(0.1, 10, 8), C.skin, head, s * 0.43, -0.02, -0.02).scale.set(0.45, 1, 0.75); });
    mm(new THREE.SphereGeometry(0.465, 24, 14, 0, Math.PI * 2, 0, Math.PI * 0.56), C.hair, head, 0, 0.03, -0.035).rotation.x = -0.8;
    for (var i = -2; i <= 2; i++) mm(new THREE.SphereGeometry(0.095, 10, 8), C.hair, head, i * 0.1, 0.31 - Math.abs(i) * 0.025, 0.32 - Math.abs(i) * 0.035).scale.set(1.25, 0.7, 0.8);
    [[0.05, -0.05, -0.4, -0.2], [-0.07, 0.02, 0.35, -0.35]].forEach(function (q) { var c = mm(new THREE.ConeGeometry(0.07, 0.2, 8), C.hair, head, q[0], 0.46, q[1]); c.rotation.z = q[2]; c.rotation.x = q[3]; });
    var eyes = [], brows = [];
    [-1, 1].forEach(function (s) {
      var e = new THREE.Group(); e.position.set(s * 0.155, 0.04, 0.37); head.add(e);
      mm(new THREE.SphereGeometry(0.085, 14, 10), C.white, e).scale.set(1, 1.2, 0.55);
      mm(new THREE.SphereGeometry(0.055, 12, 8), C.iris, e, 0, -0.005, 0.035).scale.set(1, 1.1, 0.5);
      mm(new THREE.SphereGeometry(0.03, 8, 6), C.pupil, e, 0, -0.005, 0.055).scale.set(1, 1.1, 0.5);
      mm(new THREE.SphereGeometry(0.014, 6, 4), C.white, e, -0.018, 0.025, 0.066);
      eyes.push(e);
      var b = mm(new THREE.BoxGeometry(0.13, 0.028, 0.03), C.hair, head, s * 0.155, 0.17, 0.385); b.rotation.z = -s * 0.12; brows.push(b);
      mm(new THREE.SphereGeometry(0.07, 10, 8), C.blush, head, s * 0.26, -0.1, 0.33).scale.set(1, 0.6, 0.35);
    });
    mm(new THREE.SphereGeometry(0.05, 10, 8), C.skinD, head, 0, -0.07, 0.425).scale.set(1, 0.8, 0.8);
    var smile = mm(new THREE.TorusGeometry(0.075, 0.016, 6, 16, Math.PI), C.lip, head, 0, -0.17, 0.39); smile.rotation.z = Math.PI;
    var mouthO = mm(new THREE.SphereGeometry(0.07, 12, 8), C.mouth, head, 0, -0.19, 0.375); mouthO.scale.set(1.1, 0.8, 0.45); mouthO.visible = false;
    g.traverse(function (o) { if (o.isMesh && o.material === C.blush) o.castShadow = false; });
    scene.add(g);
    return { g: g, hips: hips, torso: torso, head: head, L: L, R: R, AL: AL, AR: AR, eyes: eyes, brows: brows, smile: smile, mouthO: mouthO };
  }

  /* ---------- Bhulu, Khalid's dog ---------- */
  function mkDog() {
    var fur = im(0xc98d4f, { roughness: 0.95 }), furD = im(0x94602f, { roughness: 0.95 }), cream = im(0xf3e3c3, { roughness: 0.95 }),
      dark = im(0x2a1d15, { roughness: 0.4 }), pink = im(0xe58a8f, { roughness: 0.5 }), red = im(0xc0392b, { roughness: 0.6 }), white = im(0xffffff, { roughness: 0.3 });
    var g = new THREE.Group(), root = new THREE.Group(), spine = new THREE.Group();
    g.add(root); root.add(spine); spine.position.set(0, 1.24, -0.5);   // the spine pivots at the hips so the dog can sit
    mm(SPH(0.5), fur, spine, 0, 0.02, 0.5).scale.set(0.72, 0.74, 1.35);
    mm(SPH(0.34), cream, spine, 0, -0.08, 0.92).scale.set(0.85, 0.95, 0.75);
    mm(SPH(0.3), cream, spine, 0, -0.2, 0.45).scale.set(0.8, 0.5, 1.4);
    function dleg(x, z, front) {
      var up = new THREE.Group(); up.position.set(x, -0.1, z); spine.add(up);
      mm(SPH(0.16), fur, up, 0, -0.06, 0).scale.set(0.8, 1.3, 1.1);
      tube(0.1, 0.085, 0.55, fur, up);
      var lo = new THREE.Group(); lo.position.y = -0.55; up.add(lo);
      mm(SPH(0.085), fur, lo);
      tube(0.075, 0.065, 0.52, front ? cream : fur, lo);
      mm(SPH(0.09), cream, lo, 0, -0.54, 0.05).scale.set(1, 0.6, 1.4);
      return { up: up, lo: lo };
    }
    var FL = dleg(0.2, 0.9, true), FR = dleg(-0.2, 0.9, true), BL = dleg(0.22, 0.12, false), BR = dleg(-0.22, 0.12, false);
    var neck = new THREE.Group(); neck.position.set(0, 0.18, 1.08); spine.add(neck);
    mm(new THREE.CylinderGeometry(0.19, 0.25, 0.5, 12), fur, neck, 0, 0.16, 0.04).rotation.x = 0.5;
    mm(new THREE.TorusGeometry(0.21, 0.045, 8, 20), red, neck, 0, 0.1, 0.02).rotation.x = Math.PI / 2 - 0.5;
    mm(SPH(0.055), IMT.gold, neck, 0, -0.03, 0.24);
    var head = new THREE.Group(); head.position.set(0, 0.45, 0.2); neck.add(head);
    mm(SPH(0.3), fur, head).scale.set(1, 0.92, 1.05);
    mm(SPH(0.2), cream, head, 0, -0.1, 0.17).scale.set(0.95, 0.75, 1);
    mm(new THREE.CylinderGeometry(0.1, 0.13, 0.3, 12), fur, head, 0, -0.05, 0.37).rotation.x = Math.PI / 2;
    mm(SPH(0.055), dark, head, 0, -0.02, 0.53).scale.set(1.2, 0.9, 0.8);
    var jaw = new THREE.Group(); jaw.position.set(0, -0.13, 0.22); head.add(jaw);
    mm(new THREE.BoxGeometry(0.15, 0.05, 0.3), cream, jaw, 0, -0.02, 0.13);
    var tongue = mm(new THREE.BoxGeometry(0.09, 0.02, 0.2), pink, jaw, 0, -0.02, 0.3); tongue.rotation.x = 0.6;
    [-1, 1].forEach(function (s) {
      mm(SPH(0.045), dark, head, s * 0.12, 0.07, 0.26);
      mm(SPH(0.014), white, head, s * 0.12 - 0.012, 0.09, 0.3);
      mm(SPH(0.035), cream, head, s * 0.1, 0.15, 0.25).scale.set(1.2, 0.6, 0.6);
    });
    var ears = [];
    [-1, 1].forEach(function (s) {
      var ear = new THREE.Group(); ear.position.set(s * 0.17, 0.2, -0.03); ear.rotation.z = -s * 0.32; head.add(ear);
      mm(new THREE.ConeGeometry(0.1, 0.28, 8), furD, ear, 0, 0.12, 0).scale.z = 0.45;
      ears.push(ear);
    });
    var tail = new THREE.Group(); tail.position.set(0, 0.22, -0.06); spine.add(tail);
    mm(new THREE.TorusGeometry(0.2, 0.055, 8, 16, Math.PI * 1.25), fur, tail, 0, 0.2, 0).rotation.set(0, Math.PI / 2, -Math.PI / 2);
    mm(SPH(0.06), cream, tail, 0, 0.34, 0.14);
    scene.add(g);
    return { g: g, root: root, spine: spine, FL: FL, FR: FR, BL: BL, BR: BR, neck: neck, head: head, jaw: jaw, tongue: tongue, ears: ears, tail: tail };
  }

  var boy = mkBoy(), dog = mkDog();
  var dogHit = new THREE.Mesh(new THREE.SphereGeometry(1.0, 10, 8), hitMat); dogHit.position.set(0, 1.2, 0.3); dogHit.userData.pick = "dog"; dog.g.add(dogHit);
  var arrow = new THREE.Group();
  (function () { var cg = new THREE.ConeGeometry(0.28, 0.75, 16); cg.rotateX(Math.PI / 2); var m = new THREE.Mesh(cg, IMT.ring); arrow.add(m); arrow.visible = false; scene.add(arrow); })();
  var START = { x: 227.5, z: 600 };
  var P = { x: START.x, z: START.z, y: -30, face: Math.PI, faceGoal: null };
  // Khalid's animation state (speed in ft/s)
  var BA = { spd: 0, ph: 0, lastC: 1, blink: 2, look: 0, lookGoal: 0, lookT: 1, cheer: -1, shrug: -1, roll: 0, prevFace: Math.PI };
  // Bhulu's state (plan inches, like Khalid)
  var DG = { x: 0, z: 0, y: -30, face: Math.PI, spd: 0, ph: 0, sit: 1, still: 2, bark: -1, barkAt: null, happy: -1, look: 0 };
  var trail = [];   // Khalid's footsteps; Bhulu walks along them, so he goes through the same doors
  var tmpW = new THREE.Vector3();

  /* ---------- sound (made in the browser, no files) ---------- */
  var AC = null, muted = false, noiseBuf = null;
  function audio() {
    if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { AC = null; } }
    if (AC && AC.state === "suspended") AC.resume();
  }
  function tone(f, t, d, type, v) {
    var o = AC.createOscillator(), g = AC.createGain();
    o.type = type; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(v, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(g); g.connect(AC.destination); o.start(t); o.stop(t + d + 0.05);
  }
  function noise() {
    if (!noiseBuf) {
      noiseBuf = AC.createBuffer(1, Math.floor(AC.sampleRate * 0.3), AC.sampleRate);
      var d = noiseBuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    var s = AC.createBufferSource(); s.buffer = noiseBuf; return s;
  }
  // one "woof": a falling growl through a mouth-like filter, plus a breathy burst at the start
  function woof(t, p) {
    var o = AC.createOscillator(), bp = AC.createBiquadFilter(), g = AC.createGain();
    o.type = "sawtooth";
    o.frequency.setValueAtTime(300 * p, t); o.frequency.linearRampToValueAtTime(560 * p, t + 0.035); o.frequency.exponentialRampToValueAtTime(190 * p, t + 0.17);
    bp.type = "bandpass"; bp.Q.value = 1.6; bp.frequency.setValueAtTime(1300, t); bp.frequency.exponentialRampToValueAtTime(520, t + 0.17);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.55, t + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.2);
    o.connect(bp); bp.connect(g); g.connect(AC.destination); o.start(t); o.stop(t + 0.22);
    var n = noise(), nb = AC.createBiquadFilter(), ng = AC.createGain();
    nb.type = "bandpass"; nb.frequency.value = 1700; nb.Q.value = 0.9;
    ng.gain.setValueAtTime(0.0001, t); ng.gain.exponentialRampToValueAtTime(0.3, t + 0.01); ng.gain.exponentialRampToValueAtTime(0.0001, t + 0.1);
    n.connect(nb); nb.connect(ng); ng.connect(AC.destination); n.start(t); n.stop(t + 0.12);
  }
  function sfx(kind) {
    if (muted || !AC) return;
    var t = AC.currentTime;
    if (kind === "found") [523, 659, 784, 1047].forEach(function (f, i) { tone(f, t + i * 0.08, 0.18, "triangle", 0.2); });
    else if (kind === "bark") { woof(t, 1); woof(t + 0.3, 1.06); }
    else if (kind === "step") {
      var n = noise(), lp = AC.createBiquadFilter(), g = AC.createGain();
      lp.type = "lowpass"; lp.frequency.value = 650;
      g.gain.setValueAtTime(0.06, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.06);
      n.connect(lp); lp.connect(g); g.connect(AC.destination); n.start(t); n.stop(t + 0.07);
    }
    else if (kind === "hint") [880, 1175].forEach(function (f, i) { tone(f, t + i * 0.12, 0.25, "sine", 0.15); });
    else if (kind === "done") [523, 659, 784, 1047, 1319, 1568].forEach(function (f, i) { tone(f, t + i * 0.11, 0.3, "triangle", 0.2); });
  }

  /* ---------- game state ---------- */
  var game = { state: "menu", score: 0, list: [], idx: 0, t: 0, total: 0, hint: false, sparkle: false, lastSec: -1, found: [] };
  var cam = { yaw: 0, dist: 17, h: 9, look: new THREE.Vector3(0, 0, 0), orbit: 0 };
  function readBest() { try { return parseInt(localStorage.getItem("rafi-hunt-best") || "0", 10) || 0; } catch (e) { return 0; } }
  function saveBest(v) { try { localStorage.setItem("rafi-hunt-best", String(v)); } catch (e) {} }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  // 10 things a round: 3 in the yard, 2 in the baths, 5 in the other rooms and the verandah
  function pickRound() {
    var yardI = shuffle(ITEMS.filter(function (i) { return i.place; })).slice(0, 3);
    var bath = shuffle(ITEMS.filter(function (i) { return i.room && i.room.indexOf("bath") === 0; })).slice(0, 2);
    var rest = shuffle(ITEMS.filter(function (i) { return !i.place && !(i.room && i.room.indexOf("bath") === 0); })).slice(0, 5);
    return shuffle(yardI.concat(bath, rest));
  }
  var toastTimer = null;
  function toast(text, ms) {
    var el = $("toast"); el.textContent = text; el.classList.add("on");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { el.classList.remove("on"); }, ms || 2200);
  }
  function setTask() {
    var it = game.list[game.idx];
    if (!it) return;
    $("task-img").src = thumbs[it.k] || ""; $("task-img").alt = itemName(it);
    $("task-name").textContent = itemName(it);
    $("task-hint").textContent = game.hint ? u("look", { p: placeName(it) }) : "";
    $("h-count").textContent = num(game.idx + 1) + " / " + num(game.list.length);
  }
  function hudScore() { $("h-score").textContent = num(game.score); }
  function placeDog() {
    trail.length = 0; DG.x = P.x + 30; DG.z = P.z + 10; DG.y = floorAt(DG.x, DG.z); DG.face = P.face;
    DG.spd = 0; DG.sit = 1; DG.still = 2; DG.bark = -1; DG.happy = -1;
  }
  function isFull() { return !!(document.fullscreenElement || document.webkitFullscreenElement); }
  function goFull() {
    var el = document.documentElement;
    try {
      var pr = el.requestFullscreen ? el.requestFullscreen({ navigationUI: "hide" }) : (el.webkitRequestFullscreen ? el.webkitRequestFullscreen() : null);
      if (pr && pr.then) pr.then(function () { try { screen.orientation.lock("landscape").catch(function () {}); } catch (e) {} }).catch(function () {});
    } catch (e) {}
  }
  function startGame() {
    audio();
    if (touch && !inApp && !isFull()) goFull();
    game.list = pickRound(); game.idx = 0; game.score = 0; game.t = 0; game.total = 0; game.hint = false; game.sparkle = false; game.lastSec = -1; game.found = [];
    ITEMS.forEach(function (it) { it.gone = false; it.near = false; it.anim = -1; it.obj.visible = true; it.obj.scale.setScalar(it.s); it.obj.position.y = Y(it.baseY); it.ring.visible = false; });
    P.x = START.x; P.z = START.z; P.y = -30; P.face = Math.PI; P.faceGoal = null; cam.yaw = 0;
    BA.cheer = -1; BA.shrug = -1; BA.spd = 0;
    placeDog();
    $("menu").hidden = true; $("done").hidden = true; $("pause").hidden = true; $("hud").hidden = false; $("bubble").hidden = true; bubbleT = 0;
    game.state = "play";
    hudScore(); setTask();
    toast(lang === "bn" ? "খুঁজে বের করো: " + itemName(game.list[0]) : "Find the " + itemName(game.list[0]) + "!", 2600);
  }
  function useHint() {
    if (game.state !== "play" || game.hint) return;
    var it = game.list[game.idx];
    game.hint = true; game.score = Math.max(0, game.score - 40); hudScore();
    it.ring.visible = true; arrow.visible = true;
    $("task-hint").textContent = u("look", { p: placeName(it) });
    toast(u("hintToast", { p: placeName(it) })); sfx("hint");
  }
  function popText(text, obj) {
    var v = obj.position.clone(); v.y += 1.6; v.project(camera);
    var el = document.createElement("div"); el.className = "pop"; el.textContent = text;
    el.style.left = ((v.x * 0.5 + 0.5) * stage.clientWidth) + "px"; el.style.top = ((-v.y * 0.5 + 0.5) * stage.clientHeight) + "px";
    $("hud").appendChild(el); setTimeout(function () { el.remove(); }, 1300);
  }
  var sparks = [], sparkGeo = new THREE.SphereGeometry(0.07, 6, 4);
  function burst(pos) {
    for (var i = 0; i < 18; i++) {
      var m = new THREE.Mesh(sparkGeo, IMT.ring); m.position.copy(pos); m.position.y += 0.6;
      var a = Math.random() * Math.PI * 2, s = 3 + Math.random() * 4;
      m.userData.v = new THREE.Vector3(Math.cos(a) * s, 5 + Math.random() * 4, Math.sin(a) * s); m.userData.life = 0.9;
      scene.add(m); sparks.push(m);
    }
  }
  // little dust clouds when Khalid runs on the ground outside
  var puffs = [], puffI = 0, puffGeo = new THREE.SphereGeometry(0.22, 8, 6);
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].forEach(function () {
    var pmat = new THREE.MeshLambertMaterial({ color: 0xcdb892, transparent: true, opacity: 0, depthWrite: false }); pmat.color.convertSRGBToLinear();
    var pm = new THREE.Mesh(puffGeo, pmat); pm.visible = false; pm.userData.life = 0; scene.add(pm); puffs.push(pm);
  });
  function puff(pos) { var m = puffs[puffI++ % puffs.length]; m.position.copy(pos); m.position.y += 0.12; m.userData.life = 0.6; m.visible = true; }
  function updateFx(dt) {
    for (var i = sparks.length - 1; i >= 0; i--) {
      var sp = sparks[i]; sp.userData.life -= dt;
      sp.userData.v.y -= 18 * dt; sp.position.addScaledVector(sp.userData.v, dt); sp.scale.setScalar(Math.max(0.01, sp.userData.life / 0.9));
      if (sp.userData.life <= 0) { scene.remove(sp); sparks.splice(i, 1); }
    }
    puffs.forEach(function (m) {
      if (!m.visible) return;
      m.userData.life -= dt;
      if (m.userData.life <= 0) { m.visible = false; return; }
      var k = 1 - m.userData.life / 0.6;
      m.scale.setScalar(0.5 + k * 1.3); m.material.opacity = 0.5 * (1 - k); m.position.y += dt * 0.5;
    });
  }
  function found(it) {
    var bonus = Math.max(0, Math.round((45 - game.t) * 3)), pts = it.pts + bonus;
    game.score += pts; hudScore();
    game.found.push({ it: it, t: game.t });
    it.gone = true; it.anim = 0; it.ring.visible = false; arrow.visible = false;
    popText("+" + num(pts), it.obj); burst(it.obj.position); sfx("found");
    toast(u("found", { i: itemName(it), p: num(pts) }) + (bonus >= 60 ? u("speedy") : ""));
    BA.cheer = 0; BA.shrug = -1; DG.happy = 0;
    P.faceGoal = Math.atan2(it.at[0] - P.x, it.at[1] - P.z);
    game.idx++; game.t = 0; game.hint = false; game.sparkle = false;
    var next = game.list[game.idx];
    if (next) next.near = false;
    if (game.idx >= game.list.length) { setTimeout(finish, 1100); game.state = "ending"; }
    else setTask();
  }
  // the wrong thing: Bhulu turns to it and barks, and Khalid shrugs
  var bubbleT = 0;
  function wrongPick(it) {
    if (DG.bark >= 0 && DG.bark < 0.55) return;
    DG.bark = 0; DG.barkAt = { x: it.at[0], z: it.at[1] };
    BA.shrug = 0; sfx("bark"); showBubble();
  }
  function showBubble() {
    var b = $("bubble"); b.textContent = u("woof"); b.hidden = false;
    b.classList.remove("show"); void b.offsetWidth; b.classList.add("show");
    bubbleT = 1.4; updateBubble(0);
  }
  function updateBubble(dt) {
    if (bubbleT <= 0) return;
    var b = $("bubble");
    bubbleT -= dt;
    if (bubbleT <= 0) { b.hidden = true; return; }
    dog.head.getWorldPosition(tmpW); tmpW.y += 0.75; tmpW.project(camera);
    b.style.visibility = tmpW.z > 1 ? "hidden" : "";
    b.style.left = ((tmpW.x * 0.5 + 0.5) * stage.clientWidth) + "px"; b.style.top = ((-tmpW.y * 0.5 + 0.5) * stage.clientHeight) + "px";
  }
  function finish() {
    game.state = "done"; sfx("done");
    var max = game.list.reduce(function (s, it) { return s + it.pts + 135; }, 0), ratio = game.score / max;
    var stars = ratio >= 0.72 ? 3 : ratio >= 0.45 ? 2 : 1, best = readBest(), isBest = game.score > best;
    if (isBest) { best = game.score; saveBest(best); }
    game.stars = stars; game.isBest = isBest;
    BA.cheer = 0; DG.happy = 0;
    renderDone(); $("done").hidden = false; $("hud").hidden = true;
  }
  function renderDone() {
    $("d-title").textContent = game.isBest ? u("newBest") : u("doneTitle");
    $("d-stars").innerHTML = [0, 1, 2].map(function (i) { return '<span class="' + (i < game.stars ? "" : "off") + '">★</span>'; }).join("");
    $("d-score").textContent = u("doneScore", { s: num(game.score), b: num(readBest()) });
    $("d-text").textContent = u("doneText", { n: num(game.list.length), t: fmtTime(game.total) });
    $("d-list").innerHTML = game.found.map(function (f) { return '<figure><img src="' + (thumbs[f.it.k] || "") + '" alt="' + itemName(f.it) + '"><figcaption>' + fmtTime(f.t) + "</figcaption></figure>"; }).join("");
    $("d-again").textContent = u("again");
  }
  function pause() {
    if (game.state !== "play") return;
    game.state = "pause"; $("pause").hidden = false;
  }
  function resume() { if (game.state !== "pause") return; game.state = "play"; $("pause").hidden = true; }
  function showMenu() {
    game.state = "menu";
    ["done", "pause", "hud"].forEach(function (id) { $(id).hidden = true; });
    $("menu").hidden = false;
    P.x = START.x; P.z = START.z; P.y = -30; P.face = Math.PI; placeDog(); setLang(lang);
  }
  // hooks for the Android app: the back button and leaving the app
  window.rafiBack = function () {
    if (game.state === "play") { pause(); return true; }
    if (game.state === "pause") { resume(); return true; }
    if (game.state === "done") { showMenu(); return true; }
    return false;
  };
  window.rafiPause = function () { pause(); if (AC && AC.state === "running") AC.suspend(); };
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) window.rafiPause();
    else if (AC && AC.state === "suspended" && !muted) AC.resume();
  });

  /* ---------- language ---------- */
  function setLang(l) {
    lang = l;
    document.documentElement.lang = l;
    $("m-en").setAttribute("aria-pressed", l === "en"); $("m-bn").setAttribute("aria-pressed", l === "bn");
    $("m-title").textContent = u("title"); $("m-story").textContent = u("story"); $("m-score").textContent = u("score");
    $("m-ctl").textContent = (touch ? u("touch") : u("keys")) + (touch && !inApp && window.innerHeight > window.innerWidth ? " " + u("rotate") : "");
    $("m-start").textContent = u("start");
    var b = readBest(); $("m-best").textContent = b ? u("best", { b: num(b) }) : "";
    $("m-credit").textContent = u("credit");
    $("l-score").textContent = u("lScore"); $("l-find").textContent = u("lFind"); $("l-item").textContent = u("lItem");
    $("keys").textContent = touch ? "" : u("keys"); $("b-lang").textContent = u("langBtn");
    $("b-full").setAttribute("aria-label", u("full"));
    $("p-title").textContent = u("paused"); $("p-resume").textContent = u("resume"); $("p-restart").textContent = u("restart");
    if (bubbleT > 0) $("bubble").textContent = u("woof");
    if (game.list.length) { setTask(); hudScore(); }
    if (game.state === "done") renderDone();
    try { localStorage.setItem("rafi-hunt-lang", l); } catch (e) {}
  }

  /* ---------- controls ---------- */
  var keys = {}, joy = { x: 0, y: 0, id: null }, drag = null;
  window.addEventListener("keydown", function (e) {
    if (game.state === "pause" && (e.code === "Escape" || e.code === "KeyP")) { resume(); return; }
    if (game.state !== "play") return;
    keys[e.code] = true;
    if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Space"].indexOf(e.code) >= 0) e.preventDefault();
    if (e.code === "KeyH") useHint();
    if (e.code === "KeyM") toggleSound();
    if (e.code === "Escape" || e.code === "KeyP") pause();
  });
  window.addEventListener("keyup", function (e) { keys[e.code] = false; });
  window.addEventListener("blur", function () { keys = {}; pause(); });
  var canvasEl = renderer.domElement, ray = new THREE.Raycaster(), ndc = new THREE.Vector2(), hoverT = 0;
  function pickAt(cx, cy) {
    var rc = canvasEl.getBoundingClientRect();
    ndc.set((cx - rc.left) / rc.width * 2 - 1, -((cy - rc.top) / rc.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    var list = [dogHit];
    ITEMS.forEach(function (it) { if (!it.gone) list.push(it.hit); });
    var hs = ray.intersectObjects(list, false);
    return hs.length ? hs[0].object.userData.pick : null;
  }
  // a tap or click on a thing: pick it up if it is the one and Khalid is close, or Bhulu barks
  function tapAt(cx, cy) {
    if (game.state !== "play") return;
    audio();
    var p = pickAt(cx, cy);
    if (!p) return;
    if (p === "dog") { DG.happy = 0; return; }
    if (p !== game.list[game.idx]) { wrongPick(p); return; }
    var dx = p.at[0] - P.x, dz = p.at[1] - P.z, d = Math.sqrt(dx * dx + dz * dz);
    if (d <= 120 && Math.abs(p.baseY - P.y) <= 48 && (d <= 48 || roomAt(P.x, P.z) === roomAt(p.at[0], p.at[1]))) found(p);
    else toast(u("closer"));
  }
  canvasEl.addEventListener("pointerdown", function (e) { drag = { id: e.pointerId, x: e.clientX, sx: e.clientX, sy: e.clientY, t: performance.now() }; });
  canvasEl.addEventListener("pointermove", function (e) {
    if (drag && drag.id === e.pointerId) { cam.yaw -= (e.clientX - drag.x) * 0.006; drag.x = e.clientX; return; }
    if (e.pointerType === "mouse" && game.state === "play") {
      var n = performance.now(); if (n - hoverT < 90) return; hoverT = n;
      canvasEl.style.cursor = pickAt(e.clientX, e.clientY) ? "pointer" : "";
    }
  });
  canvasEl.addEventListener("pointerup", function (e) {
    if (!drag || drag.id !== e.pointerId) return;
    if (Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy) < 12 && performance.now() - drag.t < 500) tapAt(e.clientX, e.clientY);
    drag = null;
  });
  ["pointercancel", "pointerleave"].forEach(function (ev) { canvasEl.addEventListener(ev, function (e) { if (drag && drag.id === e.pointerId) drag = null; }); });
  canvasEl.addEventListener("contextmenu", function (e) { e.preventDefault(); });
  var joyEl = $("joy"), knob = $("knob");
  function moveJoy(e) {
    var r = joyEl.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), m = r.width / 2 - 22, d = Math.sqrt(dx * dx + dy * dy);
    if (d > m) { dx *= m / d; dy *= m / d; }
    knob.style.transform = "translate(" + dx + "px," + dy + "px)"; joy.x = dx / m; joy.y = dy / m;
  }
  joyEl.addEventListener("pointerdown", function (e) { joy.id = e.pointerId; joyEl.setPointerCapture(e.pointerId); moveJoy(e); e.stopPropagation(); });
  joyEl.addEventListener("pointermove", function (e) { if (joy.id === e.pointerId) moveJoy(e); });
  ["pointerup", "pointercancel"].forEach(function (ev) { joyEl.addEventListener(ev, function (e) { if (joy.id === e.pointerId) { joy.id = null; joy.x = joy.y = 0; knob.style.transform = ""; } }); });
  if (touch) joyEl.hidden = false;
  function toggleSound() {
    muted = !muted;
    $("snd-on").style.display = muted ? "none" : ""; $("snd-off").style.display = muted ? "" : "none";
    $("b-sound").setAttribute("aria-label", muted ? "Sound off" : "Sound on");
  }
  $("b-hint").addEventListener("click", useHint);
  $("b-sound").addEventListener("click", function () { audio(); toggleSound(); });
  $("b-lang").addEventListener("click", function () { setLang(lang === "en" ? "bn" : "en"); });
  $("b-pause").addEventListener("click", pause);
  if (touch && !inApp && (document.fullscreenEnabled || document.webkitFullscreenEnabled)) $("b-full").hidden = false;
  $("b-full").addEventListener("click", function () {
    if (!isFull()) { goFull(); return; }
    var ex = document.exitFullscreen || document.webkitExitFullscreen; if (ex) ex.call(document);
  });
  $("p-resume").addEventListener("click", resume);
  $("p-restart").addEventListener("click", startGame);
  $("m-start").addEventListener("click", startGame);
  $("d-again").addEventListener("click", startGame);
  $("m-en").addEventListener("click", function () { setLang("en"); });
  $("m-bn").addEventListener("click", function () { setLang("bn"); });

  function resize() {
    var w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
  }
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener("resize", resize);
  resize();

  /* ---------- Khalid's moves ---------- */
  function animBoy(dt, now) {
    var t = now / 1000, b = boy, sp = BA.spd;
    var mv = clamp(sp / 1.2, 0, 1), run = clamp((sp - 3.2) / 3.4, 0, 1), idle = 1 - mv;
    BA.ph += dt * (3 + sp * 1.05);
    var s = Math.sin(BA.ph), c = Math.cos(BA.ph);
    // a foot lands each time the stride reaches its front-most point
    if (mv > 0.4 && (c >= 0) !== (BA.lastC >= 0) && game.state === "play") {
      sfx("step");
      if (run > 0.3 && P.y < -20) { (c < 0 ? b.L : b.R).ankle.getWorldPosition(tmpW); puff(tmpW); }
    }
    BA.lastC = c;
    // walk or run: legs swing, knees bend on the way forward, arms swing the other way
    var A = (0.42 + 0.4 * run) * mv, kneeA = 0.55 + 0.85 * run;
    var thL = -A * s, thR = A * s;
    var kL = (0.08 + kneeA * Math.max(0, c)) * mv, kR = (0.08 + kneeA * Math.max(0, -c)) * mv;
    var AA = (0.32 + 0.55 * run) * mv, sway = Math.sin(t * 1.3) * 0.04 * idle;
    var shL = AA * s + sway, shR = -AA * s + sway, elb = -0.1 - (0.15 + 1.05 * run) * mv, out = 0.09 + 0.05 * run;
    var bob = (0.03 + 0.09 * run) * mv * (Math.abs(c) - 0.5);
    var lean = (0.04 + 0.2 * run) * mv, twist = s * (0.1 + 0.08 * run) * mv;
    var breathe = Math.sin(t * 2.3) * idle;
    // standing still: look around now and then, and blink
    BA.lookT -= dt;
    if (BA.lookT < 0) { BA.lookT = 1.4 + Math.random() * 2.6; BA.lookGoal = (Math.random() - 0.5) * 1.1; }
    BA.look += (BA.lookGoal * idle - BA.look) * Math.min(1, dt * 3.5);
    BA.blink -= dt; if (BA.blink < -0.13) BA.blink = 1.8 + Math.random() * 3.2;
    var eyeY = BA.blink < 0 ? 0.12 : 1;
    // cheer after a find: a little crouch, a jump with both arms up, and a landing
    var ch = 0, jump = 0, squat = 0, tuck = 0;
    if (BA.cheer >= 0) {
      var k = BA.cheer += dt;
      if (k > 1.25) BA.cheer = -1;
      else {
        ch = k < 0.08 ? k / 0.08 : k > 1.05 ? (1.25 - k) / 0.2 : 1;
        var jk = (k - 0.14) / 0.46; if (jk > 0 && jk < 1) { jump = Math.sin(jk * Math.PI) * 1.15; tuck = Math.sin(jk * Math.PI); }
        if (k < 0.14) squat = Math.sin(k / 0.14 * Math.PI / 2); else if (k > 0.6 && k < 0.9) squat = Math.sin((k - 0.6) / 0.3 * Math.PI) * 0.8;
        eyeY = 0.55;
      }
    }
    // shrug and head shake when Bhulu barks
    var sh = 0, shake = 0;
    if (BA.shrug >= 0) {
      var q = BA.shrug += dt;
      if (q > 0.9) BA.shrug = -1;
      else { sh = q < 0.12 ? q / 0.12 : q > 0.7 ? (0.9 - q) / 0.2 : 1; shake = Math.sin(q * 26) * 0.28 * (1 - q / 0.9); }
    }
    b.hips.position.y = 1.55 + bob - 0.2 * squat + jump;
    b.hips.position.x = Math.sin(t * 0.9) * 0.025 * idle;
    b.hips.rotation.y = -twist * 0.5;
    b.hips.rotation.z = Math.sin(t * 0.9) * 0.03 * idle;
    b.torso.rotation.x = mix(lean, -0.12, ch) + 0.1 * squat;
    b.torso.rotation.y = twist;
    b.torso.scale.set(1 + breathe * 0.01, 1 + breathe * 0.014, 1 + breathe * 0.01);
    var legT = -0.55 * squat - 0.7 * tuck, legK = 1.0 * squat + 1.3 * tuck;
    b.L.hip.rotation.x = mix(thL, legT, ch); b.R.hip.rotation.x = mix(thR, legT * 0.85, ch);
    b.L.knee.rotation.x = mix(kL, legK, ch); b.R.knee.rotation.x = mix(kR, legK * 0.9, ch);
    [b.L, b.R].forEach(function (lg) { lg.ankle.rotation.x = -(lg.hip.rotation.x + lg.knee.rotation.x) * 0.6 * (1 - tuck * 0.5); });
    [[b.AL, shL], [b.AR, shR]].forEach(function (a) {
      var arm = a[0], sx = arm.sx;
      arm.sh.rotation.x = mix(mix(a[1], -0.5, sh), -2.85, ch);
      arm.sh.rotation.z = sx * mix(mix(out, 0.45, sh), 0.4, ch);
      arm.el.rotation.x = mix(mix(elb, -1.2, sh), -0.15, ch);
      arm.el.rotation.z = sx * 0.6 * sh * (1 - ch);
    });
    b.head.rotation.x = -lean * 0.6 - 0.22 * ch + 0.05 * sh;
    b.head.rotation.y = BA.look + shake;
    b.head.rotation.z = 0.12 * sh + Math.sin(t * 0.7) * 0.03 * idle;
    b.eyes.forEach(function (e) { e.scale.y = eyeY; });
    b.brows.forEach(function (w) { w.position.y = 0.17 + 0.045 * Math.max(ch, sh); });
    b.smile.visible = ch < 0.3; b.mouthO.visible = ch >= 0.3;
    // lean into turns while running
    var df = P.face - BA.prevFace; while (df > Math.PI) df -= 2 * Math.PI; while (df < -Math.PI) df += 2 * Math.PI;
    BA.prevFace = P.face;
    var rollGoal = dt > 0 ? clamp(-df / dt * 0.05 * mv, -0.16, 0.16) : 0;
    BA.roll += (rollGoal - BA.roll) * Math.min(1, dt * 6);
    b.g.position.set(X(P.x), Y(P.y), Z(P.z)); b.g.rotation.set(0, P.face, BA.roll);
  }

  /* ---------- Bhulu's moves ---------- */
  function dogFollow(dt) {
    var lt = trail[trail.length - 1];
    if (!lt || (P.x - lt.x) * (P.x - lt.x) + (P.z - lt.z) * (P.z - lt.z) > 36) trail.push({ x: P.x, z: P.z });
    var sx = P.x - DG.x, sz = P.z - DG.z;
    if (sx * sx + sz * sz < 44 * 44 && clearLine(DG.x, DG.z, P.x, P.z)) trail.length = 0;   // close, with nothing in between
    if (trail.length > 700) { var jump = trail[trail.length - 60]; DG.x = jump.x; DG.z = jump.z; trail.splice(0, trail.length - 60); }
    var len = 0, ax = DG.x, az = DG.z;
    for (var i = 0; i < trail.length; i++) { var q = trail[i]; len += Math.sqrt((q.x - ax) * (q.x - ax) + (q.z - az) * (q.z - az)); ax = q.x; az = q.z; }
    len += Math.sqrt((P.x - ax) * (P.x - ax) + (P.z - az) * (P.z - az));
    var want = len - 36, goal = want > 0 ? Math.min(170, 30 + want * 2.4) : 0;
    DG.spd += (goal - DG.spd) * Math.min(1, dt * (goal > DG.spd ? 5 : 8));
    var step = DG.spd * dt, hx = 0, hz = 0;
    for (var guard = 0; step > 0.0001 && guard < 50; guard++) {
      var tq = trail.length ? trail[0] : null, tx = tq ? tq.x : P.x, tz = tq ? tq.z : P.z;
      var dx = tx - DG.x, dz = tz - DG.z, d = Math.sqrt(dx * dx + dz * dz);
      if (!tq) { var room = d - 36; if (room <= 0) break; if (step > room) step = room; }
      if (d < 1e-4) { if (tq) { trail.shift(); continue; } break; }
      hx = dx; hz = dz;
      if (tq && d <= step) { DG.x = tx; DG.z = tz; step -= d; trail.shift(); }
      else { var mvd = Math.min(step, d); DG.x += dx / d * mvd; DG.z += dz / d * mvd; step = 0; }
    }
    if (DG.spd > 8 && (hx || hz)) turnTo(DG, Math.atan2(hx, hz), dt * 8);
    DG.y += (floorAt(DG.x, DG.z) - DG.y) * Math.min(1, dt * 10);
  }
  function dogStep(dt, now) {
    if (game.state === "play" || game.state === "ending") dogFollow(dt);
    else DG.spd *= Math.max(0, 1 - dt * 8);
    if (DG.bark >= 0) {
      DG.bark += dt;
      if (DG.barkAt) turnTo(DG, Math.atan2(DG.barkAt.x - DG.x, DG.barkAt.z - DG.z), dt * 10);
      if (DG.bark > 0.8) DG.bark = -1;
    }
    if (DG.happy >= 0) { DG.happy += dt; if (DG.happy > 1.2) DG.happy = -1; }
    animDog(dt, now);
  }
  function animDog(dt, now) {
    var t = now / 1000, d = dog, sp = DG.spd / 12;
    var mv = clamp(sp / 1.5, 0, 1);
    DG.ph += dt * (3 + sp * 1.9);
    var s = Math.sin(DG.ph), c = Math.cos(DG.ph);
    // sit down after standing still for a moment
    DG.still = (mv > 0.08 || DG.bark >= 0 || DG.happy >= 0) ? 0 : DG.still + dt;
    var sitGoal = DG.still > 0.7 ? 1 : 0;
    DG.sit += (sitGoal - DG.sit) * Math.min(1, dt * (sitGoal ? 3.5 : 9));
    var st = DG.sit, th = 0.55 * st, A = 0.6 * mv;
    var bp = 0;   // two barks: the jaw snaps open twice
    if (DG.bark >= 0) { var k = DG.bark; bp = Math.max(0, 1 - Math.abs(k - 0.08) / 0.1) + Math.max(0, 1 - Math.abs(k - 0.38) / 0.1); }
    var hop = DG.happy >= 0 ? Math.abs(Math.sin(DG.happy / 1.2 * Math.PI * 3)) * 0.45 * (1 - DG.happy / 1.2) : 0;
    d.root.position.y = -0.55 * st + Math.abs(c) * 0.07 * mv + hop;
    d.spine.rotation.x = -th - bp * 0.12 - (hop > 0.02 ? 0.15 : 0);
    // trot: front-left moves with back-right, front-right with back-left
    d.FL.up.rotation.x = A * s + th; d.FR.up.rotation.x = -A * s + th;
    d.FL.lo.rotation.x = 0.9 * mv * Math.max(0, -c); d.FR.lo.rotation.x = 0.9 * mv * Math.max(0, c);
    d.BR.up.rotation.x = A * s - 0.45 * st; d.BL.up.rotation.x = -A * s - 0.45 * st;
    d.BR.lo.rotation.x = 0.6 * mv * Math.max(0, -c) + 1.8 * st; d.BL.lo.rotation.x = 0.6 * mv * Math.max(0, c) + 1.8 * st;
    // head: watch Khalid while sitting, look up to bark
    var lookGoal = 0;
    if (st > 0.5 && DG.bark < 0) {
      var ang = Math.atan2(P.x - DG.x, P.z - DG.z) - DG.face;
      while (ang > Math.PI) ang -= 2 * Math.PI; while (ang < -Math.PI) ang += 2 * Math.PI;
      lookGoal = clamp(ang, -0.9, 0.9);
    }
    DG.look += (lookGoal - DG.look) * Math.min(1, dt * 4);
    d.neck.rotation.y = DG.look;
    d.head.rotation.x = 0.45 * st + 0.08 * mv - bp * 0.35 + Math.sin(t * 1.7) * 0.03;
    d.head.rotation.z = st * Math.sin(t * 0.6) * 0.12;
    var pant = st > 0.4 && DG.bark < 0;
    d.jaw.rotation.x = bp * 0.6 + (pant ? 0.16 + Math.sin(t * 13) * 0.05 : 0);
    d.tongue.visible = pant;
    d.ears.forEach(function (e) { e.rotation.x = -0.25 * bp + Math.sin(DG.ph) * 0.05 * mv; });
    var wagSpd = DG.happy >= 0 ? 24 : bp > 0 ? 18 : 10 + 4 * mv, wagAmp = DG.happy >= 0 ? 0.6 : 0.35;
    d.tail.rotation.y = Math.sin(t * wagSpd) * wagAmp;
    d.g.position.set(X(DG.x), Y(DG.y), Z(DG.z)); d.g.rotation.y = DG.face;
  }

  /* ---------- main loop ---------- */
  var last = performance.now(), wasInside = null, tmpV = new THREE.Vector3(), perf = { n: 0, acc: 0 };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function setInside(inside) {
    if (inside === wasInside) return;
    wasInside = inside;
    clipArr.length = 0; if (inside) clipArr.push(cutPlane);
    groups.roof.visible = !inside;
  }
  function updateItems(dt, now) {
    ITEMS.forEach(function (it) {
      if (!it.obj.visible) return;
      if (it.gone) {
        it.anim += dt;
        var k = Math.min(1, it.anim / 0.6);
        it.obj.position.y = Y(it.baseY) + k * 2.2; it.obj.scale.setScalar(it.s * (1 - k * 0.9));
        if (k >= 1) it.obj.visible = false;
        return;
      }
      it.obj.position.y = Y(it.baseY) + (reduce ? 0 : Math.sin(now * 0.003 + it.phase) * 0.06 + 0.04);
      var ud = it.obj.userData;
      if (ud.spin && !reduce) ud.spin.rotation.y += dt * ud.spinRate;
      if (ud.wiggle && !reduce) ud.wiggle.rotation.y = Math.sin(now * 0.0025 + it.phase) * 0.7;
      if (it.ring.visible) { var s = 1 + Math.sin(now * 0.006) * 0.15; it.ring.scale.set(s, s, s); }
    });
  }
  function playStep(dt) {
    game.t += dt; game.total += dt;
    var f = 0, r = 0;
    if (keys.KeyW || keys.ArrowUp) f += 1; if (keys.KeyS || keys.ArrowDown) f -= 1;
    if (keys.KeyD || keys.ArrowRight) r += 1; if (keys.KeyA || keys.ArrowLeft) r -= 1;
    if (keys.KeyQ) cam.yaw += 1.9 * dt; if (keys.KeyE) cam.yaw -= 1.9 * dt;
    f -= joy.y; r += joy.x;
    var mag = Math.sqrt(f * f + r * r); if (mag > 1) { f /= mag; r /= mag; mag = 1; }
    var mx = (-Math.sin(cam.yaw)) * f + Math.cos(cam.yaw) * r, mz = (-Math.cos(cam.yaw)) * f + (-Math.sin(cam.yaw)) * r;
    var speed = (keys.ShiftLeft || keys.ShiftRight ? 42 : 90) * mag, ox = P.x, oz = P.z;
    P.x += mx * speed * dt; P.z += mz * speed * dt;
    collide(P);
    var moved = Math.sqrt((P.x - ox) * (P.x - ox) + (P.z - oz) * (P.z - oz)) / 12 / Math.max(dt, 1e-3);
    BA.spd += (moved - BA.spd) * Math.min(1, dt * 10);
    P.y += (floorAt(P.x, P.z) - P.y) * Math.min(1, dt * 12);
    if (mag > 0.05) { P.faceGoal = null; turnTo(P, Math.atan2(mx, mz), dt * 12); }
    else if (P.faceGoal !== null) turnTo(P, P.faceGoal, dt * 8);

    var target = game.list[game.idx];
    if (target && !game.hint && !game.sparkle && game.t > 40) { game.sparkle = true; target.ring.visible = true; toast(u("sparkle")); }
    if (arrow.visible && target) {
      arrow.position.set(X(P.x), Y(P.y) + 4.8, Z(P.z));
      arrow.rotation.y = Math.atan2(X(target.at[0]) - X(P.x), Z(target.at[1]) - Z(P.z));
    }
    // walking up to a thing: pick it up if it is the one, otherwise Bhulu barks (once per visit)
    ITEMS.forEach(function (it) {
      if (it.gone || game.state !== "play") return;
      var dx = it.at[0] - P.x, dz = it.at[1] - P.z, near = dx * dx + dz * dz <= 28 * 28 && Math.abs(it.baseY - P.y) <= 40;
      if (near && !it.near) { if (it === game.list[game.idx]) found(it); else wrongPick(it); }
      it.near = near;
    });
    var sec = Math.floor(game.total);
    if (sec !== game.lastSec) { game.lastSec = sec; $("h-time").textContent = fmtTime(game.total); }
  }
  function followCam(dt) {
    var inside = P.x >= -2 && P.x <= 457 && P.z >= -2 && P.z <= 474;
    setInside(inside);
    var near = touch ? 0.82 : 1, tDist = (inside ? 12 : 17) * near, tH = (inside ? 16 : 9) * near;   // a bit closer on small phone screens
    cam.dist += (tDist - cam.dist) * Math.min(1, dt * 3); cam.h += (tH - cam.h) * Math.min(1, dt * 3);
    tmpV.set(X(P.x) + Math.sin(cam.yaw) * cam.dist, Y(P.y) + cam.h, Z(P.z) + Math.cos(cam.yaw) * cam.dist);
    camera.position.lerp(tmpV, Math.min(1, dt * 6));
    cam.look.lerp(tmpV.set(X(P.x), Y(P.y) + 2.2, Z(P.z)), Math.min(1, dt * 8));
    camera.lookAt(cam.look);
  }
  function update(now) {
    var raw = (now - last) / 1000, dt = clamp(raw, 0, 0.05); last = now;
    // slow phone? draw fewer pixels
    if (raw > 0 && raw < 0.5 && !document.hidden) {
      perf.acc += raw; perf.n++;
      if (perf.acc > 3) {
        var fps = perf.n / perf.acc; perf.acc = 0; perf.n = 0;
        if (fps < 30 && curPR > 0.75) { curPR = Math.max(0.75, curPR - 0.25); renderer.setPixelRatio(curPR); resize(); }
      }
    }
    skyDome.position.copy(camera.position);
    if (!reduce) fans.forEach(function (f) { f.rotation.y += dt * 5; });
    updateItems(dt, now); updateFx(dt);
    if (game.state === "play") playStep(dt);
    else if (game.state !== "pause") BA.spd *= Math.max(0, 1 - dt * 8);
    if (game.state !== "pause") { animBoy(dt, now); dogStep(dt, now); updateBubble(dt); }
    if (game.state === "menu") {
      setInside(false);
      cam.orbit += dt * (reduce ? 0 : 0.08);
      camera.position.set(Math.sin(cam.orbit) * 58 - 6, 24, Math.cos(cam.orbit) * 58 + 8);
      cam.look.set(0, 2, 2); camera.lookAt(cam.look);
    } else if (game.state !== "pause") followCam(dt);
  }
  function loop(now) {
    requestAnimationFrame(loop);
    update(now);
    renderer.render(scene, camera);
  }

  placeDog();
  var savedLang = "en";
  try { savedLang = localStorage.getItem("rafi-hunt-lang") || "en"; } catch (e) {}
  setLang(savedLang === "bn" ? "bn" : "en");
  requestAnimationFrame(loop);
})();
</script>
'''

fragment = HEAD + BODY + MODEL_JS + GAME_JS
open(os.path.join(HERE, "artifact-game.html"), "w", encoding="utf-8").write(fragment)

def page(body, viewport):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="' + viewport + '">\n'
            + HEAD + '</head>\n<body>\n' + body + MODEL_JS + GAME_JS + '\n</body>\n</html>\n')

open(os.path.join(os.path.dirname(HERE), "index.html"), "w", encoding="utf-8").write(
    page(BODY, "width=device-width, initial-scale=1, viewport-fit=cover"))

# Android app page: same game with three.js built in, so it plays without internet
CDN = "https://cdn.jsdelivr.net/npm/three@0.128.0/"
body_offline = BODY
for url, name in [("build/three.min.js", "three.min.js"), ("examples/js/controls/OrbitControls.js", "OrbitControls.js"),
                  ("examples/js/utils/BufferGeometryUtils.js", "BufferGeometryUtils.js")]:
    tag = '<script src="' + CDN + url + '"></script>'
    assert tag in body_offline, tag
    lib = open(os.path.join(HERE, "lib", name), encoding="utf-8").read()
    assert "</script" not in lib
    body_offline = body_offline.replace(tag, "<script>\n" + lib + "\n</script>")
assets = os.path.join(HERE, "android", "assets")
os.makedirs(assets, exist_ok=True)
open(os.path.join(assets, "index.html"), "w", encoding="utf-8").write(
    page(body_offline, "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"))
print("ok", len(fragment))
