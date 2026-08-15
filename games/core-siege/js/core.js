'use strict';
/* ============================================================
   CORE SIEGE — core.js
   수학 유틸 · 글로우 스프라이트 캐시 · 공간 그리드 · 사운드/음악 엔진
   ============================================================ */

const TAU = Math.PI * 2;
const rand = (a = 1, b) => b === undefined ? Math.random() * a : a + Math.random() * (b - a);
const randInt = (a, b) => Math.floor(rand(a, b + 1));
const pick = arr => arr[(Math.random() * arr.length) | 0];
const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
const lerp = (a, b, t) => a + (b - a) * t;
const dist2 = (ax, ay, bx, by) => { const dx = bx - ax, dy = by - ay; return dx * dx + dy * dy; };
const dist = (ax, ay, bx, by) => Math.hypot(bx - ax, by - ay);
const angleTo = (ax, ay, bx, by) => Math.atan2(by - ay, bx - ax);
const fmt = n => Math.round(n).toLocaleString('en-US');

function lerpAngle(a, b, t) {
  let d = (b - a) % TAU;
  if (d > Math.PI) d -= TAU;
  if (d < -Math.PI) d += TAU;
  return a + d * t;
}

function store(k, v) {
  try {
    if (v === undefined) return localStorage.getItem(k);
    localStorage.setItem(k, v);
  } catch (e) { return null; }
}

// 전역 게임 상태 컨테이너 — game.js 에서 채운다 (모든 파일이 공유)
const G = {};

/* ---------- 글로우 스프라이트 (shadowBlur 대체, 성능용 사전 렌더) ---------- */
const _glowCache = new Map();
function glowSprite(color) {
  let c = _glowCache.get(color);
  if (c) return c;
  c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,0.9)');
  gr.addColorStop(0.22, color);
  gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gr;
  g.fillRect(0, 0, 64, 64);
  _glowCache.set(color, c);
  return c;
}
// 호출측에서 globalCompositeOperation='lighter' 설정
function drawGlow(ctx, x, y, r, color, alpha = 1) {
  ctx.globalAlpha = alpha;
  ctx.drawImage(glowSprite(color), x - r, y - r, r * 2, r * 2);
  ctx.globalAlpha = 1;
}

function poly(g, n, r, rot = 0) {
  g.beginPath();
  for (let i = 0; i < n; i++) {
    const a = rot + i / n * TAU;
    const x = Math.cos(a) * r, y = Math.sin(a) * r;
    i ? g.lineTo(x, y) : g.moveTo(x, y);
  }
  g.closePath();
}

/* ---------- 공간 그리드 (적 분리 · 투사체 충돌 질의) ---------- */
const Grid = {
  cell: 80,
  map: new Map(),
  clear() { this.map.clear(); },
  insert(e) {
    const k = Math.floor(e.x / this.cell) + ',' + Math.floor(e.y / this.cell);
    const arr = this.map.get(k);
    if (arr) arr.push(e); else this.map.set(k, [e]);
  },
  query(x, y, r, out) {
    out.length = 0;
    const c = this.cell;
    const x0 = Math.floor((x - r) / c), x1 = Math.floor((x + r) / c);
    const y0 = Math.floor((y - r) / c), y1 = Math.floor((y + r) / c);
    for (let gx = x0; gx <= x1; gx++) {
      for (let gy = y0; gy <= y1; gy++) {
        const arr = this.map.get(gx + ',' + gy);
        if (arr) for (let i = 0; i < arr.length; i++) out.push(arr[i]);
      }
    }
    return out;
  }
};

/* ============================================================
   사운드 엔진 — 전부 WebAudio 합성 (외부 에셋 0)
   ============================================================ */
// 진동 (모바일 햅틱 — 설정에서 토글)
function vib(ms) {
  if (!G.vibOn || !navigator.vibrate) return;
  try { navigator.vibrate(ms); } catch (e) {}
}

const Sound = {
  ctx: null, master: null, sfxBus: null, musBus: null,
  muted: store('cs.muted') === '1',
  _noiseBuf: null, _musBase: 0.30, _sfxBase: 0.55,

  setVol(kind, v) { // v: 0..1
    if (kind === 'mus') {
      this._musBase = 0.30 * v;
      if (this.musBus) this.musBus.gain.value = this._musBase;
      store('cs.volM', Math.round(v * 100));
    } else {
      this._sfxBase = 0.55 * v;
      if (this.sfxBus) this.sfxBus.gain.value = this._sfxBase;
      store('cs.volS', Math.round(v * 100));
    }
  },

  ensure() {
    if (this.ctx) return true;
    try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch (e) { return false; }
    const c = this.ctx;
    this.master = c.createGain();
    this.master.gain.value = this.muted ? 0 : 1;
    const comp = c.createDynamicsCompressor();
    comp.threshold.value = -18;
    comp.ratio.value = 8;
    this.master.connect(comp);
    comp.connect(c.destination);
    const vs0 = store('cs.volS'), vm0 = store('cs.volM');
    this._sfxBase = 0.55 * ((vs0 === null ? 100 : +vs0) / 100);
    this._musBase = 0.30 * ((vm0 === null ? 100 : +vm0) / 100);
    this.sfxBus = c.createGain(); this.sfxBus.gain.value = this._sfxBase; this.sfxBus.connect(this.master);
    this.musBus = c.createGain(); this.musBus.gain.value = this._musBase; this.musBus.connect(this.master);
    // 1초짜리 화이트노이즈 버퍼 (재사용)
    const buf = c.createBuffer(1, c.sampleRate, c.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    this._noiseBuf = buf;
    // 컨볼버 리버브 (합성 IR — 공간감. sfx 22% / music 10% 센드)
    try {
      const ir = c.createBuffer(2, c.sampleRate * 1.4, c.sampleRate);
      for (let ch = 0; ch < 2; ch++) {
        const cd = ir.getChannelData(ch);
        for (let i = 0; i < cd.length; i++) cd[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / cd.length, 2.4);
      }
      const verb = c.createConvolver();
      verb.buffer = ir;
      verb.connect(this.master);
      const sSend = c.createGain(); sSend.gain.value = 0.22;
      this.sfxBus.connect(sSend); sSend.connect(verb);
      const mSend = c.createGain(); mSend.gain.value = 0.10;
      this.musBus.connect(mSend); mSend.connect(verb);
    } catch (e) { /* 리버브 실패해도 드라이 사운드는 유지 */ }
    Music.start(c, this.musBus);
    return true;
  },

  resume() {
    if (this.ensure() && this.ctx.state === 'suspended') this.ctx.resume();
  },

  setMuted(m) {
    this.muted = m;
    store('cs.muted', m ? '1' : '0');
    if (this.master) this.master.gain.value = m ? 0 : 1;
  },

  // 사이드체인 덕킹 — 큰 임팩트 순간 음악을 눌러 타격감 강조
  duck(amount = 0.5, rel = 0.5) {
    if (!this.ctx || this.muted || !this.musBus) return;
    const g = this.musBus.gain, t = this.ctx.currentTime;
    g.cancelScheduledValues(t);
    g.setValueAtTime(Math.min(g.value, this._musBase * (1 - amount)), t);
    g.setTargetAtTime(this._musBase, t + 0.05, rel * 0.4);
  },

  // 단일 오실레이터 톤. o:{type,f,f2,dur,v,a,lp,at,bus}
  tone(o) {
    if (!this.ctx || this.muted) return;
    const c = this.ctx, t = c.currentTime + (o.at || 0);
    const dur = o.dur || 0.2;
    const osc = c.createOscillator();
    osc.type = o.type || 'sine';
    osc.frequency.setValueAtTime(Math.max(1, o.f || 440), t);
    if (o.f2) osc.frequency.exponentialRampToValueAtTime(Math.max(1, o.f2), t + dur);
    const g = c.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(o.v || 0.15, t + (o.a || 0.006));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g);
    let node = g;
    if (o.lp) {
      const f = c.createBiquadFilter();
      f.type = 'lowpass'; f.frequency.value = o.lp;
      node.connect(f); node = f;
    }
    node.connect(o.bus || this.sfxBus);
    osc.start(t);
    osc.stop(t + dur + 0.08);
  },

  // 노이즈 샷. o:{dur,v,ft,f,f2,at,q}
  noise(o) {
    if (!this.ctx || this.muted) return;
    const c = this.ctx, t = c.currentTime + (o.at || 0);
    const dur = o.dur || 0.25;
    const src = c.createBufferSource();
    src.buffer = this._noiseBuf;
    src.loop = true;
    const f = c.createBiquadFilter();
    f.type = o.ft || 'lowpass';
    f.frequency.setValueAtTime(o.f || 1000, t);
    if (o.f2) f.frequency.exponentialRampToValueAtTime(Math.max(20, o.f2), t + dur);
    if (o.q) f.Q.value = o.q;
    const g = c.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(o.v || 0.2, t + 0.008);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(f); f.connect(g); g.connect(this.sfxBus);
    src.start(t);
    src.stop(t + dur + 0.05);
  }
};

/* ---------- 효과음 라이브러리 ---------- */
const Sfx = {
  _laserT: 0, _crysT: 0,
  shoot(kind) {
    switch (kind) {
      case 'pulse':
        Sound.noise({ ft: 'highpass', f: 6000, dur: 0.018, v: 0.05 }); // 발사 클릭
        Sound.tone({ type: 'square', f: 740 + rand(-60, 60), f2: 190, dur: 0.07, v: 0.07 });
        break;
      case 'tesla':
        Sound.noise({ ft: 'bandpass', f: 2600, f2: 900, dur: 0.13, v: 0.16, q: 2 });
        Sound.tone({ type: 'sawtooth', f: 190, f2: 55, dur: 0.11, v: 0.1 });
        break;
      case 'missile': Sound.noise({ f: 950, f2: 260, dur: 0.32, v: 0.13 }); break;
      case 'rail':
        Sound.noise({ ft: 'highpass', f: 4500, dur: 0.03, v: 0.2 }); // 크랙
        Sound.tone({ type: 'square', f: 1500, f2: 90, dur: 0.2, v: 0.22 });
        Sound.noise({ ft: 'highpass', f: 700, dur: 0.2, v: 0.16 });
        Sound.duck(0.3, 0.35);
        break;
      case 'drone': Sound.tone({ type: 'square', f: 1150 + rand(-90, 90), f2: 560, dur: 0.05, v: 0.035 }); break;
      case 'spit': Sound.tone({ type: 'triangle', f: 320, f2: 130, dur: 0.12, v: 0.05 }); break;
    }
  },
  laserTick() {
    if (G.time - this._laserT < 0.1) return;
    this._laserT = G.time;
    Sound.tone({ type: 'sawtooth', f: 1250 + rand(-100, 100), f2: 880, dur: 0.07, v: 0.03, lp: 2400 });
  },
  railCharge() { Sound.tone({ type: 'sawtooth', f: 70, f2: 900, dur: 0.85, v: 0.05, lp: 1400 }); },
  explode(size) { // size 0..2 — 클릭 트랜지언트 + 노이즈 스윕 + 서브 드롭 + 금속 링
    const v = 0.18 + size * 0.1;
    Sound.noise({ ft: 'highpass', f: 5200, dur: 0.03, v: 0.14 + size * 0.05 }); // 클릭
    Sound.noise({ f: 1300 + size * 600, f2: 90, dur: 0.4 + size * 0.25, v });
    Sound.tone({ type: 'sine', f: 100 - size * 18, f2: 28, dur: 0.35 + size * 0.2, v: 0.24 + size * 0.1 });
    Sound.noise({ ft: 'bandpass', f: 3400, f2: 2100, dur: 0.3, v: 0.05 + size * 0.03, q: 9, at: 0.02 }); // 금속 잔향
    Sound.duck(0.35 + size * 0.2, 0.5 + size * 0.2);
  },
  enemyDie() {
    Sound.noise({ ft: 'bandpass', f: 620 + rand(-140, 140), f2: 140, dur: 0.14, v: 0.09, q: 1.4 });
    Sound.tone({ type: 'sine', f: 95 + rand(-15, 15), f2: 42, dur: 0.12, v: 0.06 }); // 육중한 착지 썸프
  },
  place() {
    Sound.tone({ type: 'triangle', f: 210, f2: 430, dur: 0.12, v: 0.14 });
    Sound.noise({ f: 500, f2: 150, dur: 0.1, v: 0.1 });
  },
  upgrade() {
    Sound.tone({ type: 'triangle', f: 420, f2: 640, dur: 0.1, v: 0.12 });
    Sound.tone({ type: 'triangle', f: 640, f2: 940, dur: 0.14, v: 0.12, at: 0.09 });
  },
  sell() { Sound.tone({ type: 'triangle', f: 520, f2: 210, dur: 0.18, v: 0.11 }); },
  error() {
    Sound.tone({ type: 'square', f: 150, dur: 0.07, v: 0.08 });
    Sound.tone({ type: 'square', f: 118, dur: 0.1, v: 0.08, at: 0.08 });
  },
  click() { Sound.tone({ type: 'triangle', f: 700, f2: 500, dur: 0.04, v: 0.05 }); },
  coreHit() {
    Sound.tone({ type: 'sawtooth', f: 230, f2: 65, dur: 0.26, v: 0.2 });
    Sound.noise({ f: 800, f2: 120, dur: 0.22, v: 0.14 });
    Sound.duck(0.45, 0.6);
  },
  shieldHit() { Sound.tone({ type: 'sine', f: 1350, f2: 680, dur: 0.11, v: 0.09 }); },
  crystal(pitch = 1) {
    if (G.time - this._crysT < 0.06) return;
    this._crysT = G.time;
    Sound.tone({ type: 'sine', f: (1560 + rand(-120, 260)) * pitch, dur: 0.07, v: 0.035 });
  },
  unlock() {
    [523, 784, 1046, 1568].forEach((f, i) =>
      Sound.tone({ type: 'triangle', f, dur: 0.18, v: 0.09, at: i * 0.09 }));
  },
  fanfare() {
    [392, 523, 659, 784].forEach((f, i) =>
      Sound.tone({ type: 'square', f, dur: 0.2, v: 0.055, at: i * 0.1, lp: 2200 }));
    Sound.tone({ type: 'triangle', f: 1046, dur: 0.5, v: 0.07, at: 0.4 });
  },
  bossSting() {
    Sound.tone({ type: 'sawtooth', f: 49, f2: 34, dur: 1.3, v: 0.3, lp: 240, a: 0.03 });
    Sound.tone({ type: 'sine', f: 2600, f2: 500, dur: 0.9, v: 0.05, at: 0.06 });
  },
  waveHorn() {
    Sound.tone({ type: 'sawtooth', f: 97, dur: 1.1, v: 0.11, lp: 700, a: 0.05 });
    Sound.tone({ type: 'sawtooth', f: 146, dur: 1.1, v: 0.08, lp: 700, a: 0.05 });
  },
  bossRoar() {
    Sound.tone({ type: 'sawtooth', f: 58, f2: 36, dur: 1.6, v: 0.3, lp: 320, a: 0.08 });
    Sound.noise({ f: 420, f2: 70, dur: 1.4, v: 0.16 });
    Sound.duck(0.6, 1.2);
  },
  orbitalIn() { Sound.tone({ type: 'sine', f: 2100, f2: 260, dur: 0.72, v: 0.1 }); },
  stasis() {
    Sound.tone({ type: 'sine', f: 420, f2: 78, dur: 1.3, v: 0.14 });
    Sound.tone({ type: 'sine', f: 840, f2: 156, dur: 1.3, v: 0.07 });
  },
  repair() {
    [440, 554, 659, 880].forEach((f, i) =>
      Sound.tone({ type: 'triangle', f, dur: 0.14, v: 0.09, at: i * 0.07 }));
  },
  turretDown() {
    Sound.tone({ type: 'sawtooth', f: 320, f2: 60, dur: 0.3, v: 0.14 });
    Sound.noise({ f: 900, f2: 100, dur: 0.3, v: 0.12 });
  }
};

/* ============================================================
   음악 — D 마이너 펜타토닉 프로시저럴 루프
   intensity: 0 대기 / 1 웨이브 / 1.6 보스
   ============================================================ */
const Music = {
  c: null, out: null, step: 0, nextT: 0, bpm: 104,
  intensity: 0, _cur: 0,
  bass: [73.42, 73.42, 87.31, 65.41],       // D2 D2 F2 C2
  penta: [293.66, 349.23, 392.0, 440.0, 523.25], // D4 F4 G4 A4 C5

  start(c, out) {
    this.c = c; this.out = out;
    this.nextT = c.currentTime + 0.15;
    setInterval(() => this.tick(), 60);
  },
  note(f, t, dur, type, v, lp) {
    const c = this.c;
    const o = c.createOscillator();
    o.type = type; o.frequency.value = f;
    const g = c.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(v, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    const fl = c.createBiquadFilter();
    fl.type = 'lowpass'; fl.frequency.value = lp;
    o.connect(g); g.connect(fl); fl.connect(this.out);
    o.start(t); o.stop(t + dur + 0.05);
  },
  tick() {
    if (!this.c || Sound.muted) { if (this.c) this._skipAhead(); return; }
    const c = this.c;
    this._cur += (this.intensity - this._cur) * 0.06;
    while (this.nextT < c.currentTime + 0.18) {
      this.schedule(this.step, this.nextT);
      this.nextT += 60 / this.bpm / 2; // 8분음표
      this.step = (this.step + 1) % 64;
    }
  },
  _skipAhead() {
    const c = this.c;
    while (this.nextT < c.currentTime + 0.18) {
      this.nextT += 60 / this.bpm / 2;
      this.step = (this.step + 1) % 64;
    }
  },
  // 맵별 변주: [피치 배율, 햇 밀도 배율, 패드 밝기(lp) 배율]
  mapMood() {
    const id = (G.map && G.map.id) || 'bastion';
    return {
      bastion: [1, 1, 1], rift: [0.891, 1.35, 0.8], infest: [0.943, 0.85, 0.7],
      cryo: [1.122, 0.6, 1.4], void: [0.841, 1.1, 0.55],
    }[id] || [1, 1, 1];
  },
  schedule(s, t) {
    const it = this._cur;
    const [tp, hatK, brK] = this.mapMood();
    // 저음 드론 (항상)
    if (s % 8 === 0) {
      const f = this.bass[(s / 8 | 0) % 4] * tp;
      this.note(f, t, 0.9, 'sawtooth', 0.10 + it * 0.02, (260 + it * 140) * brK);
      this.note(f * 1.006, t, 0.9, 'sawtooth', 0.06, 220 * brK);
    }
    // 패드 스웰 (16스텝마다)
    if (s % 32 === 8) {
      this.note(146.83 * tp, t, 3.2, 'sawtooth', 0.03 + it * 0.012, 480 * brK);
      this.note(220.0 * tp, t, 3.2, 'sawtooth', 0.025 + it * 0.012, 480 * brK);
    }
    if (it < 0.4) return;
    // 하이햇 틱
    if (s % 2 === 1 && Math.random() < hatK) {
      const src = this.c.createBufferSource();
      src.buffer = Sound._noiseBuf; src.loop = true;
      const f = this.c.createBiquadFilter();
      f.type = 'highpass'; f.frequency.value = 6800;
      const g = this.c.createGain();
      g.gain.setValueAtTime(0.014 + it * 0.008, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.05);
      src.connect(f); f.connect(g); g.connect(this.out);
      src.start(t); src.stop(t + 0.08);
    }
    // 아르페지오
    if ((s % 4 === 0 || (it > 1.2 && s % 4 === 2)) && Math.random() < 0.75) {
      const f = this.penta[(s * 5 + ((s / 16 | 0) * 3)) % 5] * tp;
      this.note(f * (it > 1.2 && s % 16 === 0 ? 2 : 1), t, 0.22, 'triangle', 0.045 + it * 0.015, 2600 * brK);
    }
    // 보스: 킥
    if (it > 1.2 && s % 4 === 0) {
      const o = this.c.createOscillator();
      o.type = 'sine';
      o.frequency.setValueAtTime(130, t);
      o.frequency.exponentialRampToValueAtTime(38, t + 0.12);
      const g = this.c.createGain();
      g.gain.setValueAtTime(0.16, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
      o.connect(g); g.connect(this.out);
      o.start(t); o.stop(t + 0.2);
    }
  }
};
