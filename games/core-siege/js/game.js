'use strict';
/* ============================================================
   CORE SIEGE — game.js
   상태 · 웨이브 디렉터 · 경제 · 입력 · UI · 메인 루프
   ============================================================ */

const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const Q = new URLSearchParams(location.search);
const DEBUG = Q.has('debug');

const $ = id => document.getElementById(id);
const els = {
  minerals: $('minerals'), waveLabel: $('waveLabel'), waveState: $('waveState'),
  btnCall: $('btnCall'), score: $('score'), best: $('best'),
  btnMute: $('btnMute'), btnPause: $('btnPause'),
  bossBar: $('bossBar'), bossName: $('bossName'), bossFill: $('bossFill'),
  banners: $('banners'), hint: $('hint'),
  shieldFill: $('shieldFill'), hpFill: $('hpFill'), hpText: $('hpText'),
  hpBar: document.querySelector('#coreStatus .bar.hp'),
  cards: $('cards'), abilities: $('abilities'),
  turretPanel: $('turretPanel'), tpName: $('tpName'), tpStats: $('tpStats'),
  tpHp: document.querySelector('#tpHp i'), btnUp: $('btnUp'), btnSell: $('btnSell'),
  tooltip: $('tooltip'), resPill: $('resPill'),
  dock: $('dock'), btnCancel: $('btnCancel'),
  startScreen: $('startScreen'), btnStart: $('btnStart'),
  overScreen: $('overScreen'), btnRetry: $('btnRetry'),
  bossSplash: $('bossSplash'), bossSplashImg: $('bossSplashImg'), bossSplashName: $('bossSplashName'),
  ovWave: $('ovWave'), ovKills: $('ovKills'), ovTime: $('ovTime'), ovScore: $('ovScore'),
  ovTag: $('ovTag'),
  newBest: $('newBest'), pauseVeil: $('pauseVeil'),
  wavePreview: $('wavePreview'), combo: $('combo'), ovRank: $('ovRank'),
  btnResume: $('btnResume'), btnRestartP: $('btnRestartP'), diffRow: $('diffRow'),
  mapRow: $('mapRow'),
  labScreen: $('labScreen'), labRows: $('labRows'), labShards: $('labShards'),
  btnLab: $('btnLab'), btnLabClose: $('btnLabClose'), btnLabOver: $('btnLabOver'),
  ovShards: $('ovShards'),
};

/* ---------- 연구소 UI ---------- */
function renderLab() {
  const lab = labState();
  const shards = shardCount();
  els.labShards.textContent = fmt(shards);
  els.labRows.innerHTML = '';
  for (const d of LAB_DEFS) {
    const lv = lab[d.id] || 0;
    const row = document.createElement('div');
    row.className = 'labRow';
    const pips = Array.from({ length: d.max }, (_, i) =>
      `<i class="${i < lv ? 'on' : ''}"></i>`).join('');
    const maxed = lv >= d.max;
    const cost = maxed ? 0 : d.cost[lv];
    row.innerHTML = `
      <div class="labInfo">
        <b>${T(d.name)}</b>
        <span>${T(d.desc)}</span>
        <div class="pips">${pips}</div>
      </div>
      <button class="labBuy" ${maxed || shards < cost ? 'disabled' : ''}>
        ${maxed ? 'MAX' : cost + (EN() ? ' shards' : ' 파편')}
      </button>`;
    row.querySelector('.labBuy').addEventListener('click', () => {
      const cur = labState();
      const clv = cur[d.id] || 0;
      if (clv >= d.max || shardCount() < d.cost[clv]) { Sfx.error(); return; }
      store('cs.shards', shardCount() - d.cost[clv]);
      cur[d.id] = clv + 1;
      store('cs.lab', JSON.stringify(cur));
      Sfx.upgrade();
      renderLab();
    });
    els.labRows.appendChild(row);
  }
}
function openLab() { renderLab(); els.labScreen.classList.remove('hidden'); Sfx.click(); }
function closeLab() { els.labScreen.classList.add('hidden'); Sfx.click(); }

/* ---------- 밸런스 튜닝 포인트 ---------- */
const ECON = {
  startMinerals: 320, passive: 4,
  buildTimeFirst: 22, buildTime: 13, // 첫 준비만 여유 — 터치 드래그 배치 학습 시간

  callBonusPerSec: 5, droneCost: 150,
};
const POOL = [
  { type: 'rusher', cost: 6, min: 1, w: 10 },
  { type: 'spitter', cost: 13, min: 6, w: 6 }, // 원거리 터렛 저격 — W4 진입 시 신규 사망 벽이라 W6으로 이동
  { type: 'brute', cost: 34, min: 7, w: 5 },
  { type: 'swarm', cost: 3, min: 6, w: 6, pack: 5 },
  { type: 'blinker', cost: 18, min: 8, w: 5 },
  { type: 'carrier', cost: 30, min: 9, w: 3 },
  { type: 'mender', cost: 30, min: 12, w: 3 },
];
const ABILITIES = [
  { id: 'orbital', key: 'Q', name: '궤도 폭격', cd: 26, target: true, desc: '지정 지역에 3연속 궤도 폭격. 총 1,140 피해.' },
  { id: 'stasis', key: 'W', name: '정지장', cd: 34, desc: '전장의 모든 적을 4.5초간 75% 감속.' },
  { id: 'repair', key: 'E', name: '긴급 수리', cd: 48, desc: '코어 +320 수리, 보호막 50% 충전, 모든 터렛 35% 수리.' },
  { id: 'over', key: 'T', name: '코어 과충전', cd: 40, desc: '25초간 모든 터렛 피해 +30%. 사용할 때마다 가격 +80◆.' }, // 후반 자원 싱크
];
// 병기 해금 스케줄 (w = 사용 가능해지는 웨이브)
const CARD_DEFS = [
  { type: 'pulse', w: 1 },
  { type: 'tesla', w: 1 },
  { type: 'cryo', w: 3 },
  { type: 'laser', w: 4 },
  { type: 'missile', w: 6 },
  { type: 'rail', w: 8 },
];
const TROOP_CARDS = [
  { type: 'marine', w: 2 },
  { type: 'medic', w: 6 },
  { type: 'sniper', w: 9 },
  { type: 'pyro', w: 12 },
];
const DRONE_UNLOCK = 5;
const DIFFS = {
  normal: { label: '보통', hp: 1, budget: 1, score: 1 },
  hard: { label: '어려움', hp: 1.22, budget: 1.15, score: 1.5 },
};
const ELITE_START = 6, ELITE_CHANCE = 0.1;
const cardUnlocked = w => G.wave + 1 >= w;

/* ---------- 스토리 ---------- */
const STORY = {
  intro: ['수신: 함대 사령부', '철수선 도착까지 코어를 사수하라'],
  waves: {
    1: '지각 균열에서 첫 생체 반응 감지',
    2: '군체 정찰대가 접근한다',
    3: '놈들이 학습하고 있다 — 신규 병기 인가 승인',
    4: '산성 개체 출현 — 원거리 공격 주의',
    6: '중장갑 개체 다수 감지',
    7: '군체의 공세가 거세진다',
    8: '공간 왜곡 반응 — 점멸 개체 확인',
    9: '산란체 확인 — 격파 시 유충이 쏟아진다',
    11: '장거리 통신 두절 — 이제 우리뿐이다',
    12: '재생 개체 출현 — 최우선 제거 권장',
    13: '코어 출력 상승 — 공명이 놈들을 부른다',
    17: '방어선 너머는 이미 놈들의 땅이다',
    22: '철수선이 항로에 진입했다 — 조금만 더',
  },
  boss: { 5: '파괴자 알파', 10: '심연의 베헤모스', 15: '공명 포식자', 20: '군체의 어머니' },
  over: {
    S: '전설로 기록될 방어전이었다',
    A: '함대는 당신의 이름을 기억할 것이다',
    B: '코어는 침묵했지만, 기록은 남았다',
    C: '바스티온-7의 마지막 신호가 끊겼다',
    D: '바스티온-7의 마지막 신호가 끊겼다',
  },
};
const bossNameFor = n => T(STORY.boss[n] || '') || ((EN() ? 'Behemoth Prime-' : '베헤모스 프라임-') + Math.max(1, n / 5 - 4));
const bossAssetFor = n => ['boss', 'boss2', 'boss3', 'boss4'][(n / 5 - 1) % 4];

/* ---------- 작전 구역 (맵 선택 + 도달 웨이브 언락 + 기믹) ---------- */
const MAPS = [
  { id: 'bastion', name: '중앙 플랫폼', img: 'arena', tint: null, unlock: 1, gdesc: '표준 전장' },
  { id: 'rift', name: '마그마 균열 지대', img: 'arena2', tint: 'rgba(255,110,30,0.05)', unlock: 8, gdesc: '주기적 용암 분출 — 적·터렛 모두 피해' },
  { id: 'infest', name: '침식 전초기지', img: 'arena3', tint: 'rgba(150,40,60,0.055)', unlock: 12, gdesc: '군체 체력 +10% · 처치 보상 +12%' },
  { id: 'cryo', name: '극저온 구역', img: 'arena4', tint: 'rgba(120,200,255,0.05)', unlock: 16, gdesc: '적 이속 -10% · 터렛 연사 -8%' },
  { id: 'void', name: '공허 균열', img: 'arena5', tint: 'rgba(140,80,220,0.05)', unlock: 20, gdesc: '점멸 개체 강화 · 코어 파편 +25%' },
];
const mapMaxWave = () => +(store('cs.mapMax') || 1);
const mapUnlocked = m => m.unlock <= mapMaxWave();

/* ---------- 연구소 (영구 업그레이드, 코어 파편으로 구매) ---------- */
const LAB_DEFS = [
  { id: 'dmg', name: '무기 출력', desc: '모든 터렛 피해 +4%', max: 5, cost: [10, 25, 45, 75, 110] },
  { id: 'hull', name: '코어 장갑', desc: '코어 최대 체력 +8%', max: 5, cost: [12, 28, 50, 80, 115] },
  { id: 'shield', name: '보호막 공명', desc: '보호막 +10% · 재생 +1.5/s', max: 5, cost: [12, 28, 50, 80, 115] },
  { id: 'eco', name: '채굴 효율', desc: '시작 자원 +50 · 초당 수입 +0.5', max: 5, cost: [18, 40, 70, 105, 150] },
  { id: 'salvage', name: '전리품 회수', desc: '처치 보상 +3% (복리형)', max: 5, cost: [25, 55, 95, 140, 190] },
  { id: 'troop', name: '강습 보병', desc: '병력 피해·체력 +6%', max: 5, cost: [15, 35, 60, 95, 135] },
];
function labState() {
  try { return JSON.parse(store('cs.lab') || '{}'); } catch (e) { return {}; }
}
function shardCount() { return +(store('cs.shards') || 0); }

let cardEls = [], abEls = [];
let bgCanvas = null, vigCanvas = null;
let dpr = 1;

/* ---------- 터치 입력 상태 ---------- */
const TOUCH_OFF = 64;            // 손가락 위 고스트 오프셋(px)
let dragST = null;               // {mode:'place'|'orbital'|'card', id, wasSel}
let tapST = null;                // {x, y, id}

function setAim(e) {
  const off = e.pointerType === 'touch' ? TOUCH_OFF : 0;
  const z = G.vs * (G.zoom || 1);
  G.mx = (e.clientX - G.vw / 2 - (G.camx || 0)) / z;
  G.my = (e.clientY - off - G.vh / 2 - (G.camy || 0)) / z;
}
const dockTop = () => els.dock.getBoundingClientRect().top;

/* ---------- 상태 초기화 ---------- */
function resetState() {
  Object.assign(G, {
    state: 'MENU', paused: false, time: 0, playT: 0,
    wave: 0, minerals: DEBUG ? 99999 : ECON.startMinerals,
    score: 0, kills: 0,
    enemies: [], turrets: [], drones: [], projs: [], parts: [],
    effects: [], floaters: [], crystals: [], timers: [],
    core: {
      isCore: true, x: 0, y: 0, r: 40, dead: false,
      hp: 1200, maxhp: 1200, sh: 400, maxsh: 400,
      lastHit: 99, shFlashT: 0, shFlashA: 0, hitFlash: 0,
    },
    coreGone: false,
    shake: 0, stasisT: 0, slowmoT: 0, timeScale: 1,
    cam: { punch: 0 }, lights: [], camx: 0, camy: 0, zoom: 1, shx: 0, shy: 0,
    waveT: 0, buildT: ECON.buildTimeFirst, events: [],
    curMults: { hp: 1, spd: 1, bounty: 1 },
    boss: null, sel: null, placing: null, ghost: null, armed: null,
    cool: { orbital: 0, stasis: 0, repair: 0, over: 0 },
    overT: 0, overCost: 300,
    daily: null, dailyRush: false,
    pillPop: false, crystalTarget: { x: 0, y: 0 },
    best: +(store('cs.best') || 0),
    stats: { built: 0 },
    mx: 0, my: 0,
    troops: [], rally: { x: 0, y: -100 },
    combo: 0, comboT: 0, hitstop: 0, waveKills: 0,
    nextPlan: null, ambient: [], ambT: 1,
    announced: { pulse: true, tesla: true },
    hintOverride: null,
    diffId: store('cs.diff') || 'normal',
    scoreMul: 1,
  });
  G.scoreMul = DIFFS[G.diffId].score;
  // 연구소 영구 업그레이드 적용
  const lab = labState();
  const lv = id => lab[id] || 0;
  G.core.maxhp = Math.round(1200 * (1 + 0.08 * lv('hull')));
  G.core.hp = G.core.maxhp;
  G.core.maxsh = Math.round(400 * (1 + 0.10 * lv('shield')));
  G.core.sh = G.core.maxsh;
  G.labShRegen = 1.5 * lv('shield');
  G.labDmg = 1 + 0.04 * lv('dmg');
  G.labBounty = 1 + 0.03 * lv('salvage');
  G.labIncome = 0.5 * lv('eco');
  G.labTroop = 1 + 0.06 * lv('troop');
  if (!DEBUG) G.minerals = ECON.startMinerals + 50 * lv('eco');
}

/* ---------- 배경 사전 렌더: 금속 플랫폼 + 크립 스폰 지대 ---------- */
function shade(hex, v) {
  const n = parseInt(hex.slice(1), 16);
  const f = 1 + v;
  const r = clamp(Math.round(((n >> 16) & 255) * f), 0, 255);
  const gg = clamp(Math.round(((n >> 8) & 255) * f), 0, 255);
  const b = clamp(Math.round((n & 255) * f), 0, 255);
  return `rgb(${r},${gg},${b})`;
}

function edgeDist(cx, cy, w, h, a) {
  const c = Math.abs(Math.cos(a)), s = Math.abs(Math.sin(a));
  return Math.min(c > 1e-4 ? (w / 2) / c : 1e9, s > 1e-4 ? (h / 2) / s : 1e9);
}

function buildBackground() {
  const w = G.vw, h = G.vh;
  bgCanvas = document.createElement('canvas');
  bgCanvas.width = w; bgCanvas.height = h;
  const g = bgCanvas.getContext('2d');
  const platR = buildMax() + 74; // 논리 반경

  // --- 우주 ---
  g.fillStyle = '#02040a';
  g.fillRect(0, 0, w, h);
  for (let i = 0; i < 5; i++) {
    const x = rand(w), y = rand(h), r = rand(160, 380);
    const gr = g.createRadialGradient(x, y, 0, x, y, r);
    const hue = pick(['rgba(28,60,100,', 'rgba(52,34,92,', 'rgba(18,74,92,']);
    gr.addColorStop(0, hue + '0.08)');
    gr.addColorStop(1, hue + '0)');
    g.fillStyle = gr;
    g.fillRect(x - r, y - r, r * 2, r * 2);
  }
  for (let i = 0; i < 200; i++) {
    g.globalAlpha = rand(0.1, 0.65);
    g.fillStyle = Math.random() < 0.12 ? '#9beeff' : '#c8d2e0';
    g.fillRect(rand(w), rand(h), rand(0.4, 1.4), rand(0.4, 1.4));
  }
  g.globalAlpha = 1;

  // --- 논리 좌표계 진입 (뷰 스케일) ---
  g.save();
  g.translate(w / 2, h / 2);
  g.scale(G.vs, G.vs);
  const cx = 0, cy = 0;

  // --- 플랫폼 외곽 림 (아래쪽 그림자 → 입체감) ---
  g.fillStyle = 'rgba(0,0,0,0.55)';
  g.beginPath(); g.arc(cx, cy + 7, platR + 12, 0, TAU); g.fill();
  g.fillStyle = '#1a232f';
  g.beginPath(); g.arc(cx, cy, platR + 10, 0, TAU); g.fill();
  g.fillStyle = '#080d14';
  g.beginPath(); g.arc(cx, cy, platR + 3, 0, TAU); g.fill();

  // --- 플랫폼 판 (클리핑) ---
  g.save();
  g.beginPath(); g.arc(cx, cy, platR, 0, TAU); g.clip();
  const mapImg = G.map && ASSET_IMG[G.map.img];
  if (mapImg) {
    // AI 생성 전장 바닥 (맵별 이미지 + 회전 변주)
    g.save();
    g.rotate(G.mapRot || 0);
    g.drawImage(mapImg, -platR, -platR, platR * 2, platR * 2);
    g.restore();
    g.fillStyle = 'rgba(5,10,18,0.34)'; // 게임 팔레트에 맞춰 톤 다운
    g.fillRect(cx - platR, cy - platR, platR * 2, platR * 2);
    if (G.map.tint) {
      g.fillStyle = G.map.tint;
      g.fillRect(cx - platR, cy - platR, platR * 2, platR * 2);
    }
  } else {
  g.fillStyle = '#0a121c'; // 이음새 색
  g.fillRect(cx - platR, cy - platR, platR * 2, platR * 2);

  const tile = 54;
  const x0 = Math.floor((cx - platR) / tile) * tile;
  const y0 = Math.floor((cy - platR) / tile) * tile;
  for (let px = x0; px < cx + platR; px += tile) {
    for (let py = y0; py < cy + platR; py += tile) {
      const mergeR = Math.random() < 0.14; // 큰 판처럼 보이게 우측 이음새 생략
      const tw = mergeR ? tile * 2 - 3 : tile - 3;
      const base = shade('#242f3d', rand(-0.07, 0.07));
      g.fillStyle = base;
      g.fillRect(px + 1.5, py + 1.5, tw, tile - 3);
      // 베벨 (좌상 밝게, 우하 어둡게)
      g.fillStyle = 'rgba(210,230,255,0.05)';
      g.fillRect(px + 1.5, py + 1.5, tw, 1.6);
      g.fillRect(px + 1.5, py + 1.5, 1.6, tile - 3);
      g.fillStyle = 'rgba(0,0,0,0.32)';
      g.fillRect(px + 1.5, py + tile - 3.1, tw, 1.6);
      g.fillRect(px + tw - 0.1, py + 1.5, 1.6, tile - 3);
      // 리벳
      g.fillStyle = 'rgba(8,14,22,0.9)';
      for (const [rx, ry] of [[7, 7], [tw - 5, 7], [7, tile - 10], [tw - 5, tile - 10]]) {
        g.beginPath(); g.arc(px + rx, py + ry, 1.6, 0, TAU); g.fill();
      }
      // 디테일 변형 판
      const dv = Math.random();
      if (dv < 0.05) { // 환기 슬릿
        g.fillStyle = 'rgba(5,9,15,0.85)';
        for (let s = 0; s < 4; s++) g.fillRect(px + 14, py + 16 + s * 7, tile - 30, 3);
      } else if (dv < 0.085) { // 원형 해치
        g.strokeStyle = 'rgba(10,16,25,0.9)'; g.lineWidth = 2.5;
        g.beginPath(); g.arc(px + tile / 2, py + tile / 2, 13, 0, TAU); g.stroke();
        g.strokeStyle = 'rgba(190,215,240,0.07)'; g.lineWidth = 1;
        g.beginPath(); g.arc(px + tile / 2, py + tile / 2, 13, Math.PI, Math.PI * 1.6); g.stroke();
      } else if (dv < 0.115) { // 해저드 스트라이프
        g.save();
        g.globalAlpha = 0.16;
        g.fillStyle = '#c9a23f';
        for (let s = 0; s < 3; s++) g.fillRect(px + 8 + s * 14, py + tile - 14, 8, 6);
        g.restore();
      } else if (dv < 0.16) { // 녹/얼룩
        g.globalAlpha = 0.12;
        g.fillStyle = pick(['#5c3a22', '#324150', '#1e2a1e']);
        g.beginPath();
        g.arc(px + rand(10, tile - 10), py + rand(10, tile - 10), rand(6, 16), 0, TAU);
        g.fill();
        g.globalAlpha = 1;
      } else if (dv < 0.18) { // 발광 도관
        g.strokeStyle = 'rgba(76,224,255,0.13)'; g.lineWidth = 2;
        g.beginPath();
        g.moveTo(px + 6, py + tile / 2);
        g.lineTo(px + tw - 4, py + tile / 2);
        g.stroke();
      }
      if (mergeR) py += 0; // (가독용 no-op)
    }
  }

  // 긁힘 자국
  g.strokeStyle = 'rgba(0,0,0,0.22)';
  g.lineWidth = 1;
  for (let i = 0; i < 46; i++) {
    const sx = cx + rand(-platR, platR), sy = cy + rand(-platR, platR);
    const a = rand(TAU), l = rand(6, 30);
    g.beginPath();
    g.moveTo(sx, sy);
    g.lineTo(sx + Math.cos(a) * l, sy + Math.sin(a) * l);
    g.stroke();
  }

  // 잔해 두들
  for (let i = 0; i < 6; i++) {
    const a = rand(TAU), d = rand(platR * 0.45, platR * 0.9);
    const dx = cx + Math.cos(a) * d, dy = cy + Math.sin(a) * d;
    g.globalAlpha = 0.35;
    g.fillStyle = '#05080d';
    g.beginPath(); g.ellipse(dx, dy + 2, 16, 8, 0, 0, TAU); g.fill();
    g.globalAlpha = 1;
    for (let k = 0; k < 5; k++) {
      g.fillStyle = shade('#3a4a5c', rand(-0.25, 0.15));
      g.save();
      g.translate(dx + rand(-12, 12), dy + rand(-6, 6));
      g.rotate(rand(TAU));
      g.fillRect(-4, -2.5, rand(5, 9), rand(3, 5));
      g.restore();
    }
  }

  // 중앙 플라자 (코어 받침)
  g.fillStyle = 'rgba(6,11,18,0.55)';
  g.beginPath(); g.arc(cx, cy, 104, 0, TAU); g.fill();
  g.strokeStyle = 'rgba(70,95,120,0.5)'; g.lineWidth = 2;
  g.beginPath(); g.arc(cx, cy, 104, 0, TAU); g.stroke();
  g.strokeStyle = 'rgba(70,95,120,0.3)'; g.lineWidth = 1.4;
  g.beginPath(); g.arc(cx, cy, 84, 0, TAU); g.stroke();
  g.fillStyle = 'rgba(150,190,220,0.35)';
  for (let i = 0; i < 8; i++) {
    const a = i / 8 * TAU + Math.PI / 8;
    g.beginPath(); g.arc(cx + Math.cos(a) * 94, cy + Math.sin(a) * 94, 2.2, 0, TAU); g.fill();
  }
  } // 프로시저럴 바닥 끝
  const cg = g.createRadialGradient(cx, cy, 0, cx, cy, 150);
  cg.addColorStop(0, 'rgba(76,224,255,0.10)');
  cg.addColorStop(1, 'rgba(76,224,255,0)');
  g.fillStyle = cg;
  g.beginPath(); g.arc(cx, cy, 150, 0, TAU); g.fill();

  // 건설 한계 링 (해저드 대시)
  g.setLineDash([9, 13]);
  g.strokeStyle = 'rgba(201,162,63,0.20)'; g.lineWidth = 3;
  g.beginPath(); g.arc(cx, cy, buildMax(), 0, TAU); g.stroke();
  g.setLineDash([]);
  g.strokeStyle = 'rgba(76,224,255,0.05)'; g.lineWidth = 1.5;
  g.beginPath(); g.arc(cx, cy, buildMax() + 6, 0, TAU); g.stroke();
  g.restore();

  // --- 크립 (화면 가장자리 스폰 지대의 유기물 침식) ---
  for (let a = 0; a < TAU; a += 0.07) {
    const ed = edgeDist(0, 0, G.lw, G.lh, a);
    const n = randInt(1, 3);
    for (let k = 0; k < n; k++) {
      const d = ed - rand(-30, 85);
      if (d < platR - 14) continue;
      const bx = cx + Math.cos(a) * d, by = cy + Math.sin(a) * d;
      const r = rand(26, 72);
      const gr = g.createRadialGradient(bx, by, 0, bx, by, r);
      gr.addColorStop(0, 'rgba(46,14,20,0.5)');
      gr.addColorStop(0.6, 'rgba(34,9,14,0.32)');
      gr.addColorStop(1, 'rgba(30,8,12,0)');
      g.fillStyle = gr;
      g.beginPath(); g.arc(bx, by, r, 0, TAU); g.fill();
    }
  }
  // 크립 농포/정맥 점
  for (let i = 0; i < 90; i++) {
    const a = rand(TAU);
    const ed = edgeDist(0, 0, G.lw, G.lh, a);
    const d = ed - rand(-15, 55);
    if (d < platR - 6) continue;
    const bx = cx + Math.cos(a) * d, by = cy + Math.sin(a) * d;
    g.fillStyle = Math.random() < 0.3 ? 'rgba(150,52,64,0.5)' : 'rgba(80,26,34,0.6)';
    g.beginPath(); g.arc(bx, by, rand(1.2, 3.4), 0, TAU); g.fill();
  }

  g.restore(); // --- 논리 좌표계 끝 ---

  // --- 비네트 ---
  vigCanvas = document.createElement('canvas');
  vigCanvas.width = w; vigCanvas.height = h;
  const v = vigCanvas.getContext('2d');
  const vg = v.createRadialGradient(w / 2, h / 2, Math.min(w, h) * 0.3, w / 2, h / 2, Math.hypot(w, h) / 2);
  vg.addColorStop(0, 'rgba(1,3,8,0)');
  vg.addColorStop(1, 'rgba(1,3,8,0.66)');
  v.fillStyle = vg;
  v.fillRect(0, 0, w, h);
}

const buildMax = () => Math.min(G.lw, G.lh) / 2 - 46;

function resize() {
  dpr = Math.min(2, window.devicePixelRatio || 1);
  G.vw = window.innerWidth;
  G.vh = window.innerHeight;
  // 논리 월드 720 기준 뷰 스케일 — 폰에서도 데스크톱과 동일한 밸런스/기하
  G.vs = clamp(Math.min(G.vw, G.vh) / 720, 0.55, 1);
  G.lw = G.vw / G.vs;
  G.lh = G.vh / G.vs;
  canvas.width = G.vw * dpr;
  canvas.height = G.vh * dpr;
  canvas.style.width = G.vw + 'px';
  canvas.style.height = G.vh + 'px';
  buildBackground();
  const d = document.createElement('canvas');
  d.width = G.vw; d.height = G.vh;
  G.decal = d;
  G.dctx = d.getContext('2d');
  const lt = document.createElement('canvas');
  lt.width = G.vw; lt.height = G.vh;
  G.light = lt;
  G.lctx = lt.getContext('2d');
  G.partCap = G.vw * G.vh < 500000 ? 450 : 750;
  seedEmbers();
}

/* ---------- 카드 / 능력 UI ---------- */
function turretIcon(type) {
  const c = document.createElement('canvas');
  c.width = c.height = 44;
  const g = c.getContext('2d');
  const fake = {
    type, def: TURRETS[type], lvl: 1, x: 0, y: 0, rot: -Math.PI / 2,
    cd: 999, chargeT: 0, charging: false, fireT: 0, flashT: 0, recoilT: 0,
    buildT: 0, beamOn: false, hp: 1, maxhp: 1, target: null,
  };
  g.translate(22, 24);
  g.scale(1.05, 1.05);
  drawTurret(g, fake, true);
  return c;
}

function troopIcon(type) {
  const c = document.createElement('canvas');
  c.width = c.height = 44;
  const g = c.getContext('2d');
  g.translate(22, 22);
  g.rotate(-Math.PI / 2);
  if (ASSET_IMG[type]) {
    const sp = enemySprite(type);
    const s = 34;
    g.drawImage(sp, -s / 2, -s / 2, s, s);
    return c;
  }
  const def = TROOPS[type];
  g.fillStyle = '#33465a';
  g.beginPath(); g.arc(0, 0, 11, 0, TAU); g.fill();
  g.strokeStyle = '#0a121c'; g.lineWidth = 1.4; g.stroke();
  g.fillStyle = def.color;
  g.fillRect(3, -2, 13, 4);
  g.beginPath(); g.arc(0, 0, 5, 0, TAU); g.fill();
  return c;
}

function droneIcon() {
  const c = document.createElement('canvas');
  c.width = c.height = 44;
  const g = c.getContext('2d');
  g.translate(22, 22);
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, 12, '#4ce0ff', 0.5);
  g.globalCompositeOperation = 'source-over';
  g.rotate(-Math.PI / 2);
  const dsp = assetSprite('drone', 36);
  if (dsp) {
    g.drawImage(dsp, -18, -18, 36, 36);
    return c;
  }
  g.fillStyle = '#123246';
  g.beginPath();
  g.moveTo(12, 0); g.lineTo(-8, 8); g.lineTo(-4, 0); g.lineTo(-8, -8);
  g.closePath(); g.fill();
  g.strokeStyle = '#4ce0ff'; g.lineWidth = 1.6; g.stroke();
  return c;
}

// 에셋 로드 시 카드 아이콘 재렌더
let _avSeen = 0;
function refreshCardIcons() {
  for (const cd of cardEls) {
    const cv = cd.kind === 'drone' ? droneIcon()
      : cd.kind === 'troop' ? troopIcon(cd.type)
      : turretIcon(cd.type);
    cd.el.replaceChild(cv, cd.el.children[1]);
  }
}

function abilityIcon(id) {
  const c = document.createElement('canvas');
  c.width = c.height = 40;
  const g = c.getContext('2d');
  g.translate(20, 20);
  g.strokeStyle = '#7ce8ff';
  g.fillStyle = '#7ce8ff';
  g.lineWidth = 2;
  if (id === 'orbital') {
    g.beginPath(); g.arc(0, 0, 11, 0, TAU); g.stroke();
    g.beginPath(); g.arc(0, 0, 2.5, 0, TAU); g.fill();
    for (let i = 0; i < 4; i++) {
      const a = i / 4 * TAU;
      g.beginPath();
      g.moveTo(Math.cos(a) * 7, Math.sin(a) * 7);
      g.lineTo(Math.cos(a) * 15, Math.sin(a) * 15);
      g.stroke();
    }
  } else if (id === 'stasis') {
    poly(g, 6, 12); g.stroke();
    for (let i = 0; i < 6; i++) {
      const a = i / 6 * TAU;
      g.beginPath();
      g.moveTo(0, 0);
      g.lineTo(Math.cos(a) * 8, Math.sin(a) * 8);
      g.stroke();
    }
  } else if (id === 'over') {
    // 번개 볼트 (과충전)
    g.fillStyle = '#ffd9a0';
    g.strokeStyle = '#ffd9a0';
    g.beginPath();
    g.moveTo(3, -13); g.lineTo(-6, 2); g.lineTo(-1, 2);
    g.lineTo(-3, 13); g.lineTo(6, -2); g.lineTo(1, -2);
    g.closePath(); g.fill();
  } else {
    g.lineWidth = 5;
    g.beginPath();
    g.moveTo(-9, 0); g.lineTo(9, 0);
    g.moveTo(0, -9); g.lineTo(0, 9);
    g.stroke();
  }
  return c;
}

function tooltipShow(el, html) {
  if (G.touch) return;
  els.tooltip.innerHTML = html;
  els.tooltip.classList.remove('hidden');
  const r = el.getBoundingClientRect();
  const tw = els.tooltip.offsetWidth;
  els.tooltip.style.left = clamp(r.left + r.width / 2 - tw / 2, 8, G.vw - tw - 8) + 'px';
  els.tooltip.style.top = (r.top - els.tooltip.offsetHeight - 10) + 'px';
}
function tooltipHide() { els.tooltip.classList.add('hidden'); }

function baseStatHtml(type) {
  const fake = makeTurret(type, 0, 0);
  return statText(fake).replace(/\n/g, '<br>');
}

function buildCards() {
  cardEls = [];
  CARD_DEFS.forEach((cd, i) => {
    const type = cd.type;
    const def = TURRETS[type];
    const el = document.createElement('div');
    el.className = 'card';
    el.innerHTML = `<span class="hk">${i + 1}</span><div class="nm">${T(def.name)}</div><div class="cost">${def.cost}◆</div><div class="lock">W${cd.w}</div>`;
    el.insertBefore(turretIcon(type), el.children[1]);
    el.addEventListener('pointerdown', e => {
      Sound.resume();
      if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
      if (!cardUnlocked(cd.w)) {
        Sfx.error();
        G.hintOverride = { txt: EN() ? `${T(def.name)} — unlocks at wave ${cd.w}` : `${def.name} — 웨이브 ${cd.w}에 해금됩니다`, t: 1.6 };
        return;
      }
      if (e.pointerType === 'touch') {
        // 터치: 카드에서 필드로 드래그해 배치 (탭이면 선택 유지, 재탭이면 해제)
        G.touch = true;
        const wasSel = G.placing === type;
        setPlacing(type);
        dragST = { mode: 'card', id: e.pointerId, wasSel };
        Sfx.click();
      } else {
        selectCard(i);
      }
    });
    el.addEventListener('mouseenter', () =>
      tooltipShow(el, `<b>${T(def.name)}</b> <span class="c">${def.cost}◆</span><br>${T(def.desc)}<br><span class="c">${baseStatHtml(type)}</span>`));
    el.addEventListener('mouseleave', tooltipHide);
    els.cards.appendChild(el);
    cardEls.push({ el, type, kind: 'turret', w: cd.w, lockEl: el.querySelector('.lock') });
  });
  // 드론 카드
  const el = document.createElement('div');
  el.className = 'card';
  el.innerHTML = `<span class="hk">7</span><div class="nm">${T('요격 드론')}</div><div class="cost">${ECON.droneCost}◆</div><div class="lock">W${DRONE_UNLOCK}</div>`;
  el.insertBefore(droneIcon(), el.children[1]);
  el.addEventListener('click', () => { Sound.resume(); buyDrone(); });
  el.addEventListener('mouseenter', () =>
    tooltipShow(el, `<b>${T('요격 드론')}</b> <span class="c">${ECON.droneCost}◆</span><br>${T('코어 주위를 선회하며 자동 요격.')}`));
  el.addEventListener('mouseleave', tooltipHide);
  els.cards.appendChild(el);
  cardEls.push({ el, kind: 'drone', w: DRONE_UNLOCK, lockEl: el.querySelector('.lock') });
  // 병력 카드
  TROOP_CARDS.forEach((tc, j) => {
    const def = TROOPS[tc.type];
    const tel = document.createElement('div');
    tel.className = 'card';
    tel.innerHTML = `<span class="hk">${8 + j}</span><div class="nm">${T(def.name)}</div><div class="cost">${def.cost}◆</div><div class="lock">W${tc.w}</div>`;
    tel.insertBefore(troopIcon(tc.type), tel.children[1]);
    tel.addEventListener('click', () => { Sound.resume(); buyTroop(tc.type, tc.w); });
    tel.addEventListener('mouseenter', () =>
      tooltipShow(tel, EN()
        ? `<b>${T(def.name)}</b> <span class="c">${def.cost}◆ · supply ${def.supply}</span><br>${T(def.desc)}<br><span class="c">HP ${def.hp} · DMG ${def.dmg}${def.range ? ' · range ' + def.range : ' · melee'}</span>`
        : `<b>${def.name}</b> <span class="c">${def.cost}◆ · 보급 ${def.supply}</span><br>${def.desc}<br><span class="c">체력 ${def.hp} · 피해 ${def.dmg}${def.range ? ' · 사거리 ' + def.range : ' · 근접'}</span>`));
    tel.addEventListener('mouseleave', tooltipHide);
    els.cards.appendChild(tel);
    cardEls.push({ el: tel, kind: 'troop', type: tc.type, w: tc.w, lockEl: tel.querySelector('.lock') });
  });
}

function buyTroop(type, w) {
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
  if (!cardUnlocked(w)) {
    Sfx.error();
    G.hintOverride = { txt: EN() ? `${T(TROOPS[type].name)} — unlocks at wave ${w}` : `${TROOPS[type].name} — 웨이브 ${w}에 해금됩니다`, t: 1.6 };
    return;
  }
  const def = TROOPS[type];
  if (G.minerals < def.cost) { Sfx.error(); return; }
  G.minerals -= def.cost;
  G.troops.push(makeTroop(type));
  addRing(G.rally.x, G.rally.y, 8, 34, '#4ce0ff', 2, 0.4);
  Sfx.place();
}

function setRally(x, y) {
  const d = Math.hypot(x, y);
  const max = buildMax() + 20;
  if (d > max) { x *= max / d; y *= max / d; }
  G.rally = { x, y };
  addRing(x, y, 6, 40, '#9beeff', 2, 0.5);
  Sfx.click();
}

function armRally() {
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
  if (G.troops.length === 0) {
    Sfx.error();
    G.hintOverride = { txt: EN() ? 'No troops — recruit marines first' : '병력이 없습니다 — 해병을 먼저 고용하세요', t: 1.8 };
    return;
  }
  G.armed = G.armed === 'rally' ? null : 'rally';
  G.placing = null; G.ghost = null;
  Sfx.click();
}

function buildAbilities() {
  abEls = [];
  ABILITIES.forEach(ab => {
    const el = document.createElement('div');
    el.className = 'ab';
    el.appendChild(abilityIcon(ab.id));
    const hk = document.createElement('span');
    hk.className = 'hk';
    hk.textContent = ab.key;
    el.appendChild(hk);
    el.addEventListener('click', () => { Sound.resume(); armAbility(ab.id); });
    el.addEventListener('mouseenter', () =>
      tooltipShow(el, `<b>${T(ab.name)}</b> <span class="c">${EN() ? 'Cooldown' : '쿨다운'} ${ab.cd}s${ab.id === 'over' ? ' · ' + (G.overCost || 300) + '◆' : ''}</span><br>${T(ab.desc)}`));
    el.addEventListener('mouseleave', tooltipHide);
    els.abilities.appendChild(el);
    abEls.push({ el, ab });
  });
  // 집결 명령 버튼 (쿨다운 없음)
  const rb = document.createElement('div');
  rb.className = 'ab ready';
  const rc = document.createElement('canvas');
  rc.width = rc.height = 40;
  const rg = rc.getContext('2d');
  rg.strokeStyle = '#7ce8ff'; rg.fillStyle = '#7ce8ff'; rg.lineWidth = 2.4;
  rg.beginPath(); rg.moveTo(15, 32); rg.lineTo(15, 7); rg.stroke();
  rg.beginPath(); rg.moveTo(15, 7); rg.lineTo(30, 12); rg.lineTo(15, 17); rg.closePath(); rg.fill();
  rb.appendChild(rc);
  const rhk = document.createElement('span');
  rhk.className = 'hk';
  rhk.textContent = 'R';
  rb.appendChild(rhk);
  rb.addEventListener('click', () => { Sound.resume(); armRally(); });
  rb.addEventListener('mouseenter', () =>
    tooltipShow(rb, '<b>집결 명령</b> <span class="c">쿨다운 없음</span><br>병력 전체를 지정 지점으로 이동시켜 그 주변을 방어합니다.'));
  rb.addEventListener('mouseleave', tooltipHide);
  els.abilities.appendChild(rb);
  els.btnRally = rb;
}

/* ---------- 카드 선택 · 배치 · 드론 ---------- */
function setPlacing(type) {
  G.placing = type;
  G.ghost = makeTurret(type, 0, 0);
  G.ghost.buildT = 0;
  G.armed = null;
  G.sel = null;
}

function selectCard(i) {
  const c = cardEls[i];
  if (!c) return;
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
  if (!cardUnlocked(c.w)) {
    Sfx.error();
    const name = c.kind === 'drone' ? '요격 드론' : c.kind === 'troop' ? TROOPS[c.type].name : TURRETS[c.type].name;
    G.hintOverride = { txt: `${name} — 웨이브 ${c.w}에 해금됩니다`, t: 1.6 };
    return;
  }
  if (c.kind === 'drone') { buyDrone(); return; }
  if (c.kind === 'troop') { buyTroop(c.type, c.w); return; }
  if (G.placing === c.type) { cancelModes(); return; }
  setPlacing(c.type);
  Sfx.click();
}

function buyDrone() {
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
  if (!cardUnlocked(DRONE_UNLOCK)) { Sfx.error(); return; }
  if (G.minerals < ECON.droneCost) { Sfx.error(); return; }
  G.minerals -= ECON.droneCost;
  G.drones.push(makeDrone(G.drones.length));
  addRing(0, 0, 40, 110, '#4ce0ff', 2, 0.5);
  Sfx.place();
}

function cancelModes() {
  G.placing = null;
  G.ghost = null;
  G.armed = null;
}

function canPlaceAt(x, y) {
  const dc = Math.hypot(x, y);
  if (dc < G.core.r + 30 || dc > buildMax()) return false;
  for (const t of G.turrets) {
    if (dist2(x, y, t.x, t.y) < 32 * 32) return false;
  }
  return true;
}

function tryPlace() {
  const def = TURRETS[G.placing];
  if (G.minerals < def.cost) { Sfx.error(); return; }
  if (!canPlaceAt(G.mx, G.my)) { Sfx.error(); return; }
  G.minerals -= def.cost;
  G.turrets.push(makeTurret(G.placing, G.mx, G.my));
  G.stats.built++;
  addRing(G.mx, G.my, 6, 34, '#4ce0ff', 2, 0.4);
  Sfx.place();
  cancelModes(); // 배치 1회 후 자동 해제 — 잔류 배치 모드 오터치 방지
}

function trySelectAt(wx, wy) {
  const r = G.touch ? 34 : 24;
  let best = null, bd = r * r;
  for (const t of G.turrets) {
    const d = dist2(wx, wy, t.x, t.y);
    if (d < bd) { bd = d; best = t; }
  }
  if (best) { G.sel = best; Sfx.click(); }
  else G.sel = null;
}

function statText(t) {
  const d = t.def, dm = turretDmg(t), rg = Math.round(turretRange(t));
  if (EN()) {
    switch (t.type) {
      case 'pulse': return `DMG ${Math.round(dm)} · ${(d.rof * LVL.rof[t.lvl - 1]).toFixed(1)}/s\nRange ${rg}`;
      case 'tesla': return `DMG ${Math.round(dm)} · chains ${d.chain + t.lvl - 1}\nRange ${rg}`;
      case 'laser': return `DPS ${Math.round(dm)} (x2.2 on heat)\nRange ${rg}`;
      case 'missile': return `DMG ${Math.round(dm)} · blast ${d.splash + t.lvl * 5}\nRange ${rg}`;
      case 'rail': return `DMG ${Math.round(dm)} · piercing\nRange ${rg}`;
      case 'cryo': return `Slow ${Math.round((d.slow + 0.12 * (t.lvl - 1)) * 100)}%\nRadius ${rg}`;
    }
    return '';
  }
  switch (t.type) {
    case 'pulse': return `피해 ${Math.round(dm)} · 연사 ${(d.rof * LVL.rof[t.lvl - 1]).toFixed(1)}/s\n사거리 ${rg}`;
    case 'tesla': return `피해 ${Math.round(dm)} · 체인 ${d.chain + t.lvl - 1}체\n사거리 ${rg}`;
    case 'laser': return `초당 피해 ${Math.round(dm)} (과열 시 ×2.2)\n사거리 ${rg}`;
    case 'missile': return `피해 ${Math.round(dm)} · 폭발 반경 ${d.splash + t.lvl * 5}\n사거리 ${rg}`;
    case 'rail': return `피해 ${Math.round(dm)} · 직선 관통\n사거리 ${rg}`;
    case 'cryo': return `감속 ${Math.round((d.slow + 0.12 * (t.lvl - 1)) * 100)}%\n범위 ${rg}`;
  }
  return '';
}

function upgradeSel() {
  const t = G.sel;
  if (!t || t.lvl >= 3) return;
  const cost = upgradeCost(t);
  if (G.minerals < cost) { Sfx.error(); return; }
  G.minerals -= cost;
  t.invested += cost;
  t.lvl++;
  const nm = t.def.hp * LVL.hp[t.lvl - 1];
  t.hp += nm - t.maxhp;
  t.maxhp = nm;
  t.buildT = 0.3;
  addRing(t.x, t.y, 8, 40, '#4ce0ff', 2.5, 0.5);
  Sfx.upgrade();
}

function sellSel() {
  const t = G.sel;
  if (!t) return;
  G.minerals += sellValue(t);
  const i = G.turrets.indexOf(t);
  if (i >= 0) G.turrets.splice(i, 1);
  G.sel = null;
  addRing(t.x, t.y, 20, 4, '#4ce0ff', 2, 0.35);
  Sfx.sell();
}

/* ---------- 특수 능력 ---------- */
function armAbility(id) {
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
  if (G.cool[id] > 0) { Sfx.error(); return; }
  const ab = ABILITIES.find(a => a.id === id);
  if (ab.target) {
    G.armed = G.armed === id ? null : id;
    G.placing = null; G.ghost = null;
    Sfx.click();
  } else if (id === 'stasis') castStasis();
  else if (id === 'repair') castRepair();
  else if (id === 'over') castOver();
}

function castOver() {
  if (G.minerals < G.overCost) {
    Sfx.error();
    G.hintOverride = { txt: EN() ? `Core Overcharge — ${G.overCost}◆ needed` : `코어 과충전 — ${G.overCost}◆ 필요`, t: 1.6 };
    return;
  }
  G.minerals -= G.overCost;
  G.overCost += 80; // 반복 사용 시 가격 상승 (자원 싱크)
  G.cool.over = 40;
  G.overT = 25;
  addRing(0, 0, 40, 300, '#ffd9a0', 3, 0.9);
  addFlash(0, 0, 120, '#ffd9a0');
  Sfx.railCharge();
  Sfx.upgrade();
  showBanner('코어 과충전', '', '터렛 출력 +30% — 25초');
}

function castOrbital(x, y) {
  G.cool.orbital = 26;
  Sfx.orbitalIn();
  addRing(x, y, 95, 60, '#eaf7ff', 2, 0.7);
  for (let i = 0; i < 3; i++) {
    G.timers.push({
      t: 0.7 + i * 0.17, fn: () => {
        const bx = x + rand(-24, 24), by = y + rand(-24, 24);
        boom(bx, by, 58, '#eaf7ff', 1.6);
        splashDamage(bx, by, 95, 380);
        scorch(bx, by, 44);
      }
    });
  }
}

function castStasis() {
  G.cool.stasis = 34;
  G.stasisT = 4.5;
  addRing(0, 0, 40, Math.max(G.vw, G.vh) * 0.7, '#9beeff', 3, 1.1);
  Sfx.stasis();
}

function castRepair() {
  G.cool.repair = 48;
  const c = G.core;
  c.hp = Math.min(c.maxhp, c.hp + 320);
  c.sh = Math.min(c.maxsh, c.sh + c.maxsh * 0.5);
  for (const t of G.turrets) t.hp = Math.min(t.maxhp, t.hp + (t.maxhp - t.hp) * 0.35);
  for (let i = 0; i < 22; i++) {
    const a = rand(TAU), r = rand(10, 60);
    addPart({
      x: Math.cos(a) * r, y: Math.sin(a) * r, vx: 0, vy: -rand(30, 70),
      dur: rand(0.5, 1), size: 2.2, color: '#9beeff', add: true, shape: 'dot',
    });
  }
  addRing(0, 0, 30, 90, '#9beeff', 3, 0.6);
  Sfx.repair();
}

/* ---------- 웨이브 디렉터 ---------- */
function weightedPick(arr) {
  let sum = 0;
  for (const p of arr) sum += p.w;
  let r = rand(sum);
  for (const p of arr) { r -= p.w; if (r <= 0) return p; }
  return arr[arr.length - 1];
}

function planWaveData(n) {
  const k = n - 1;
  const D = DIFFS[G.diffId];
  const mults = {
    hp: (1 + 0.14 * k + 0.011 * k * k) * D.hp,
    spd: Math.min(1.55, 1 + n * 0.014),
    bounty: (1 + n * 0.038) * (D.hp > 1 ? 1.12 : 1) * (n <= 4 ? 1.2 : 1), // 초반 보상 가산 — 4번째 터렛 도달 가속
  };
  // 맵 기믹 보정
  const M = G.map;
  if (M && M.id === 'infest') { mults.hp *= 1.10; mults.bounty *= 1.12; }
  if (M && M.id === 'cryo') { mults.spd *= 0.90; }
  // W1 -25% ~ W15 ±0 ~ W20+ +4%: 초반 완만·후반 유지 (시드 봇 12런 검증 — 조기 W4 사망 0)
  let budget = (40 + n * 26 + n * n * 2.6) * D.budget;
  const dur = 20 + Math.min(20, n);
  const events = [];
  const isBoss = n % 5 === 0;
  if (isBoss) {
    events.push({ t: 3, type: 'boss', ang: rand(TAU) });
    budget *= 0.45;
  }
  const avail = POOL.filter(p => n >= p.min);
  const surges = clamp(2 + Math.floor(n / 3), 2, 6);
  for (let i = 0; i < surges; i++) {
    let sb = budget / surges;
    const ang = rand(TAU), spread = rand(0.5, 2.0);
    const t0 = 2 + (i + rand(0.2, 0.6)) / surges * (dur - 4);
    events.push({ t: Math.max(0.3, t0 - 1.5), warn: true, ang, spread });
    let guard = 0;
    while (sb > 0 && guard++ < 300) {
      const p = weightedPick(avail);
      const cnt = p.pack || 1;
      for (let c = 0; c < cnt; c++) {
        events.push({ t: t0 + rand(0, 2.4), type: p.type, ang: ang + rand(-spread / 2, spread / 2) });
      }
      sb -= p.cost * cnt;
    }
  }
  events.sort((a, b) => a.t - b.t);
  return { events, mults, isBoss };
}

// 다음 웨이브를 미리 계획하고 구성 미리보기를 렌더 (실제 웨이브와 동일한 계획 사용)
function preparePreview() {
  const n = G.wave + 1;
  G.nextPlan = { n, plan: planWaveData(n) };
  const counts = new Map();
  let boss = false;
  for (const ev of G.nextPlan.plan.events) {
    if (ev.warn) continue;
    if (ev.type === 'boss') { boss = true; continue; }
    counts.set(ev.type, (counts.get(ev.type) || 0) + 1);
  }
  els.wavePreview.innerHTML = '';
  if (boss) {
    const b = document.createElement('span');
    b.className = 'pvBoss';
    b.textContent = '★ 베헤모스';
    els.wavePreview.appendChild(b);
  }
  for (const [ty, cnt] of counts) {
    const item = document.createElement('span');
    item.className = 'pvItem';
    const cv = document.createElement('canvas');
    cv.width = cv.height = 22;
    const g = cv.getContext('2d');
    g.translate(11, 11);
    g.rotate(-Math.PI / 2);
    const sp = enemySprite(ty);
    const s = ty === 'brute' ? 20 : 24;
    g.drawImage(sp, -s / 2, -s / 2, s, s);
    item.appendChild(cv);
    const num = document.createElement('i');
    num.textContent = '×' + cnt;
    item.appendChild(num);
    els.wavePreview.appendChild(item);
  }
}

function announceUnlocks() {
  for (const cd of cardEls) {
    const key = cd.kind === 'drone' ? 'drone' : cd.type;
    if (G.announced[key] || !cardUnlocked(cd.w)) continue;
    G.announced[key] = true;
    const name = T(cd.kind === 'drone' ? '요격 드론' : cd.kind === 'troop' ? TROOPS[cd.type].name : TURRETS[cd.type].name);
    G.timers.push({
      t: 2.0, fn: () => {
        showBanner(EN() ? 'NEW WEAPON AUTHORIZED' : '신규 병기 인가', '', name + (EN() ? ' available' : ' 사용 가능'));
        Sfx.unlock();
        cd.el.classList.remove('flash');
        void cd.el.offsetWidth;
        cd.el.classList.add('flash');
      }
    });
    break; // 한 번에 하나씩
  }
}

function spawnRadius(ang) {
  const c = Math.abs(Math.cos(ang)), s = Math.abs(Math.sin(ang));
  const rx = c > 1e-4 ? (G.lw / 2 + 60) / c : 1e9;
  const ry = s > 1e-4 ? (G.lh / 2 + 60) / s : 1e9;
  return Math.min(rx, ry);
}

function spawnEvent(ev) {
  const R = spawnRadius(ev.ang);
  const x = Math.cos(ev.ang) * R, y = Math.sin(ev.ang) * R;
  const elite = ev.type !== 'boss' && ev.type !== 'swarm' &&
    G.wave >= ELITE_START && Math.random() < ELITE_CHANCE;
  const e = makeEnemy(ev.type, x, y, G.curMults, elite);
  // 크립 분출 (솟아나는 연출)
  for (let i = 0; i < 5; i++) {
    const a = rand(TAU), s = rand(30, 100);
    addPart({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
      dur: rand(0.3, 0.55), size: rand(1.5, 3), color: '#4a1a22',
      shape: 'chunk', grav: 180, drag: 1.5,
    });
  }
  if (ev.type === 'boss') {
    G.slowmoT = Math.max(G.slowmoT, 0.7);
    Sfx.bossSting();
    const bossIdx = G.wave / 5;
    // 첫 보스는 "이겨내는 경험"으로 설계 (약 66% 체력)
    e.hp = e.maxhp = e.maxhp * (bossIdx === 1 ? 0.66 : (1 + (bossIdx - 1) * 0.45));
    e.spriteKey = bossAssetFor(G.wave); // 네임드 보스 전용 스프라이트
    // 네임드별 고유 기믹 (프라임 로테이션도 스프라이트 따라감)
    e.mech = { boss: 'charge', boss2: 'submerge', boss3: 'shield', boss4: 'spawn' }[e.spriteKey] || 'charge';
    e.mechT = 6;
    e.mechPhase = 'idle';
    if (e.mech === 'shield') e.shieldStages = [0.75, 0.5, 0.25];
    if (e.mech === 'submerge' || e.mech === 'spawn') e.summonT = undefined; // 소환 대신 고유 기믹
    G.boss = e;
    const bn = bossNameFor(G.wave);
    els.bossName.textContent = bn + ' — WAVE ' + G.wave;
    showBanner('⚠ ' + bn, 'danger', '거대 개체가 방어선에 진입한다');
    showBossSplash(e.spriteKey, bn);
    Sfx.bossRoar();
    addShake(6);
    addPunch(0.9);
    vib(80);
  }
  G.enemies.push(e);
}

function callWave() {
  if (G.state !== 'BUILD') return;
  const bonus = G.wave > 0 ? Math.round(G.buildT * ECON.callBonusPerSec) : 0;
  if (bonus > 0) {
    G.minerals += bonus;
    addFloater(0, -70, '+' + bonus + '◆', '#4ce0ff');
  }
  G.wave++;
  // 최고 도달 웨이브 갱신 → 작전 구역 해금
  if (G.wave > mapMaxWave()) {
    store('cs.mapMax', G.wave);
    const nm = MAPS.find(m => m.unlock === G.wave);
    if (nm) {
      G.timers.push({
        t: 2.2, fn: () => {
          showBanner(EN() ? 'NEW SECTOR UNLOCKED' : '신규 작전 구역 해금', '', T(nm.name) + ' — ' + T(nm.gdesc));
          Sfx.unlock();
        }
      });
    }
  }
  const plan = (G.nextPlan && G.nextPlan.n === G.wave) ? G.nextPlan.plan : planWaveData(G.wave);
  G.nextPlan = null;
  G.events = plan.events;
  G.curMults = plan.mults;
  // 일일 작전 모디파이어 (적 스탯/보상)
  if (G.daily) {
    for (const m of G.daily.mods) {
      if (m.id === 'swift') G.curMults.spd *= 1.12;
      else if (m.id === 'tough') G.curMults.hp *= 1.15;
      else if (m.id === 'rich') G.curMults.bounty *= 1.25;
    }
  }
  G.waveT = 0;
  G.waveKills = 0;
  G.enraged = false;
  G.state = 'WAVE';
  const sub = plan.isBoss
    ? (EN() ? `Colossal entity '${bossNameFor(G.wave)}' approaching` : `거대 개체 '${bossNameFor(G.wave)}' 접근`)
    : (STORY.waves[G.wave] || '');
  showBanner('WAVE ' + G.wave, plan.isBoss ? 'danger' : '', sub);
  addRing(0, 0, 44, 200, '#4ce0ff', 2.5, 0.8);
  Sfx.waveHorn();
}

function clearWave() {
  const bonus = Math.round(60 + G.wave * 22);
  G.minerals += bonus;
  G.score += Math.round((250 + G.wave * 30) * G.scoreMul);
  G.slowmoT = Math.max(G.slowmoT, 0.3);
  Sfx.fanfare();
  showBanner(EN() ? 'WAVE ' + G.wave + ' DEFENDED' : '웨이브 ' + G.wave + ' 방어 성공', '',
    EN() ? `Kills ${G.waveKills} · Bonus +${bonus}◆` : `처치 ${G.waveKills} · 보너스 +${bonus}◆`);
  G.state = 'BUILD';
  G.buildT = ECON.buildTime - (G.dailyRush ? 4 : 0);
  // 전장 흔적(사체·혈흔·그을음) 서서히 풍화
  if (G.dctx) {
    G.dctx.globalCompositeOperation = 'destination-out';
    G.dctx.fillStyle = 'rgba(0,0,0,0.16)';
    G.dctx.fillRect(0, 0, G.vw, G.vh);
    G.dctx.globalCompositeOperation = 'source-over';
  }
  preparePreview();
  announceUnlocks();
  saveBest();
  saveRun();
}

function saveBest() {
  if (G.score > G.best) {
    G.best = Math.round(G.score);
    store('cs.best', G.best);
  }
}

/* ---------- 러닝 저장 / 이어하기 (BUILD 진입 시 스냅샷) ---------- */
/* ---------- 첫 판 코치마크 (3스텝: 배치 → 소환 → 능력) ---------- */
const COACH_TXT = [
  '',
  '카드를 필드로 드래그해 터렛을 배치하세요',
  '준비되면 [웨이브 시작] — 남은 시간만큼 보너스 ◆',
  '위기엔 특수 능력! 궤도 폭격은 드래그로 조준',
];
function coachShow(step) {
  G.tutStep = step;
  const c = document.getElementById('coach');
  if (!c) return;
  document.getElementById('coachTxt').textContent = T(COACH_TXT[step]);
  const tgt = step === 2 ? els.btnCall : step === 3 ? els.abilities : els.cards;
  const r = tgt.getBoundingClientRect();
  const below = step === 2; // 상단바 버튼은 아래쪽에 표시
  document.getElementById('coachArrow').style.display = below ? 'none' : '';
  document.getElementById('coachArrowUp').style.display = below ? '' : 'none';
  if (below) {
    c.style.top = (r.bottom + 8) + 'px';
    c.style.bottom = 'auto';
  } else {
    c.style.top = 'auto';
    c.style.bottom = (innerHeight - r.top + 8) + 'px';
  }
  c.style.left = clamp(r.left + r.width / 2, 100, innerWidth - 100) + 'px';
  c.classList.remove('hidden');
}
function coachDone() {
  G.tutStep = 0;
  const c = document.getElementById('coach');
  if (c) c.classList.add('hidden');
  store('cs.tut', '1');
}
function coachTick() {
  if (!G.tutStep) return;
  if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') { coachDone(); return; }
  if (G.tutStep === 1 && G.stats.built > 0) coachShow(2);
  else if (G.tutStep === 2 && G.state === 'WAVE') { coachShow(3); G._tut3T = G.time + 7; }
  else if (G.tutStep === 3 && G.time > G._tut3T) coachDone();
}

/* ---------- 설정 (볼륨·진동·화질) ---------- */
function bindSettings() {
  const $id = x => document.getElementById(x);
  const scr = $id('setScreen');
  if (!scr) return;
  const vm = $id('volMus'), vs = $id('volSfx'), tv = $id('tglVib'), tq = $id('tglQ');
  const vm0 = store('cs.volM'), vs0 = store('cs.volS');
  vm.value = vm0 === null ? 100 : +vm0;
  vs.value = vs0 === null ? 100 : +vs0;
  const syncTgl = () => {
    tv.textContent = G.vibOn ? '켜짐' : '꺼짐';
    tq.textContent = G.qMode === 'low' ? '절전' : '자동';
  };
  syncTgl();
  vm.addEventListener('input', () => { Sound.resume(); Sound.setVol('mus', vm.value / 100); });
  vs.addEventListener('input', () => { Sound.resume(); Sound.setVol('sfx', vs.value / 100); Sfx.click(); });
  tv.addEventListener('click', () => { G.vibOn = !G.vibOn; store('cs.vib', G.vibOn ? '1' : '0'); if (G.vibOn) vib(30); syncTgl(); });
  tq.addEventListener('click', () => {
    G.qMode = G.qMode === 'low' ? 'auto' : 'low';
    store('cs.q', G.qMode);
    if (G.qMode === 'low') { G.quality = 0.45; seedEmbers(); }
    syncTgl();
  });
  // 언어 전환 (전체 재렌더를 위해 리로드)
  const tl = $id('tglLang');
  if (tl) {
    tl.textContent = EN() ? 'English' : '한국어';
    tl.addEventListener('click', () => {
      setLang(EN() ? 'ko' : 'en');
      location.reload();
    });
  }
  const open = () => { scr.classList.remove('hidden'); Sfx.click(); };
  $id('btnSet') && $id('btnSet').addEventListener('click', open);
  $id('btnSetP') && $id('btnSetP').addEventListener('click', open);
  $id('btnSetClose').addEventListener('click', () => { scr.classList.add('hidden'); Sfx.click(); });
  // 포기하고 정산 (일시정지 메뉴)
  const gu = $id('btnGiveUp');
  if (gu) gu.addEventListener('click', () => {
    togglePause(false);
    if (G.state === 'WAVE' || G.state === 'BUILD') startGameOver();
  });
}

/* ---------- 일일 작전 (날짜 시드 도전) ---------- */
function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
const DAILY_MODS = [
  { id: 'swift', name: '신속 군체', desc: '적 이속 +12%' },
  { id: 'tough', name: '강인 갑각', desc: '적 체력 +15%' },
  { id: 'fragile', name: '취약 코어', desc: '코어 체력 -15%' },
  { id: 'rush', name: '짧은 준비', desc: '준비 시간 -4초' },
  { id: 'rich', name: '풍부한 전리품', desc: '처치 보상 +25%' },
];
function dailyInfo() {
  const d = new Date();
  const key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
  const rng = mulberry32(key);
  const map = MAPS[Math.floor(rng() * MAPS.length)];
  const i1 = Math.floor(rng() * DAILY_MODS.length);
  let i2 = Math.floor(rng() * (DAILY_MODS.length - 1));
  if (i2 >= i1) i2++;
  return { key, map, mods: [DAILY_MODS[i1], DAILY_MODS[i2]] };
}
let _dailyReq = null;
function startDaily() { _dailyReq = dailyInfo(); startGame(); }
function syncDailyBtn() {
  const el = document.getElementById('btnDaily');
  if (!el) return;
  const info = dailyInfo();
  const best = +(store('cs.daily_' + info.key) || 0);
  el.innerHTML = `📅 ${EN() ? 'DAILY OP' : '일일 작전'} — ${T(info.mods[0].name)} · ${T(info.mods[1].name)}` +
    (best > 0 ? ` <span class="c">(${EN() ? 'best' : '기록'} ${fmt(best)})</span>` : '');
}

function saveRun() {
  try {
    store('cs.run', JSON.stringify({
      v: 1, wave: G.wave, minerals: Math.round(G.minerals), score: Math.round(G.score),
      kills: G.kills, playT: Math.round(G.playT), diff: G.diffId,
      map: G.map.id, rot: G.mapRot,
      core: { hp: Math.round(G.core.hp), sh: Math.round(G.core.sh) },
      cool: { ...G.cool }, built: G.stats.built, overCost: G.overCost,
      turrets: G.turrets.map(t => ({ t: t.type, x: Math.round(t.x), y: Math.round(t.y), l: t.lvl, hp: Math.round(t.hp), inv: t.invested || 0 })),
      troops: G.troops.map(u => ({ t: u.type, hp: Math.round(u.hp) })),
      drones: G.drones.length,
    }));
  } catch (e) { /* 저장 실패는 무시 (프라이빗 모드 등) */ }
}
function loadRun() {
  try {
    const r = JSON.parse(store('cs.run') || 'null');
    return r && r.v === 1 && MAPS.some(m => m.id === r.map) ? r : null;
  } catch (e) { return null; }
}
function clearRun() { try { localStorage.removeItem('cs.run'); } catch (e) {} }
function syncResumeBtn() {
  const el = document.getElementById('btnResumeRun');
  if (!el) return;
  const r = loadRun();
  el.classList.toggle('hidden', !r);
  if (r) {
    const m = MAPS.find(x => x.id === r.map);
    el.textContent = `${EN() ? 'CONTINUE' : '이어하기'} — WAVE ${r.wave + 1} · ${m ? T(m.name) : ''}`;
  }
}

/* ---------- 게임 흐름 ---------- */
function startGame(resume) {
  const snap = resume ? loadRun() : null;
  if (!snap) clearRun(); // 새 런 시작 → 이전 저장 폐기
  resetState();
  if (G.dctx) G.dctx.clearRect(0, 0, G.vw, G.vh);
  const wq = parseInt(Q.get('wave') || '0', 10);
  if (wq > 1) {
    G.wave = wq - 1;
    for (const cd of cardEls) {
      if (cardUnlocked(cd.w)) G.announced[cd.kind === 'drone' ? 'drone' : cd.type] = true;
    }
  }
  G.state = 'BUILD';
  G.buildT = ECON.buildTimeFirst;
  // 작전 구역(맵) — 선택값 우선, '무작위'면 해금된 것 중 랜덤 + 회전 변주
  const avail = MAPS.filter(m => (ASSET_IMG[m.img] || m.id === 'bastion') && mapUnlocked(m));
  const selId = store('cs.map') || 'random';
  G.map = selId === 'random'
    ? (avail.length ? pick(avail) : MAPS[0])
    : (avail.find(m => m.id === selId) || avail[0] || MAPS[0]);
  G.mapRot = rand(TAU);
  if (snap) { // 이어하기: 맵/회전 고정
    G.map = MAPS.find(m => m.id === snap.map) || MAPS[0];
    G.mapRot = snap.rot || 0;
  }
  // 일일 작전: 시드 맵 + 모디파이어 (이어하기 제외, 난이도 보통 고정)
  G.daily = null;
  if (_dailyReq) {
    G.daily = _dailyReq;
    _dailyReq = null;
    clearRun();
    G.map = G.daily.map;
    G.mapRot = mulberry32(G.daily.key + 7)() * TAU;
    G.diffId = 'normal';
    G.scoreMul = 1;
    for (const m of G.daily.mods) {
      if (m.id === 'fragile') { G.core.maxhp = Math.round(G.core.maxhp * 0.85); G.core.hp = G.core.maxhp; }
      else if (m.id === 'rush') G.dailyRush = true;
    }
    if (G.dailyRush) G.buildT = Math.max(6, G.buildT - 4);
  }
  G.gimT = 9; // 맵 기믹 타이머 (마그마 분출 등)
  G.mapCdMul = G.map.id === 'cryo' ? 1.087 : 1; // 극저온: 터렛 연사 -8%
  if (G.map.gdesc && G.map.id !== 'bastion') {
    G.hintOverride = { txt: (EN() ? 'Gimmick — ' : '기믹 — ') + T(G.map.gdesc), t: 6 };
  }
  G._arenaBg = false;
  buildBackground();
  G._arenaBg = !!ASSET_IMG[G.map.img];
  seedEmbers();
  els.startScreen.classList.add('hidden');
  els.overScreen.classList.add('hidden');
  els.pauseVeil.classList.add('hidden');
  const tvEl = document.getElementById('titleVid');
  if (tvEl) tvEl.pause();
  const ovEl = document.getElementById('overVid');
  if (ovEl) ovEl.pause();
  if (els.bossSplash) { els.bossSplash.classList.remove('show'); els.bossSplash.classList.add('hidden'); }
  clearInterval(G._cntIv);
  // 이어하기: 스냅샷 복원 (자원·터렛·병력·드론·쿨다운)
  if (snap) {
    G.wave = snap.wave;
    G.minerals = snap.minerals;
    G.score = snap.score;
    G.kills = snap.kills;
    G.playT = snap.playT;
    G.diffId = DIFFS[snap.diff] ? snap.diff : G.diffId;
    G.scoreMul = DIFFS[G.diffId].score;
    G.core.hp = clamp(snap.core.hp, 1, G.core.maxhp);
    G.core.sh = clamp(snap.core.sh, 0, G.core.maxsh);
    Object.assign(G.cool, snap.cool || {});
    G.stats.built = snap.built || 0;
    G.overCost = snap.overCost || 300;
    for (const s of snap.turrets || []) {
      if (!TURRETS[s.t]) continue;
      const t = makeTurret(s.t, s.x, s.y);
      t.lvl = clamp(s.l || 1, 1, 3);
      t.maxhp = t.def.hp * LVL.hp[t.lvl - 1];
      t.hp = clamp(s.hp, 1, t.maxhp);
      t.invested = s.inv || 0;
      t.buildT = 0;
      G.turrets.push(t);
    }
    for (const s of snap.troops || []) {
      if (!TROOPS[s.t]) continue;
      const u = makeTroop(s.t);
      u.hp = clamp(s.hp, 1, u.maxhp);
      G.troops.push(u);
    }
    for (let i = 0; i < (snap.drones || 0); i++) G.drones.push(makeDrone(i));
    for (const cd of cardEls) {
      if (cardUnlocked(cd.w)) G.announced[cd.kind === 'drone' ? 'drone' : cd.type] = true;
    }
    G.buildT = ECON.buildTime;
    syncDiffUI();
  }
  preparePreview();
  // 첫 실행 온보딩 (일반 새 게임에서만)
  if (!store('cs.tut') && !snap && !G.daily) {
    G.timers.push({ t: 1.4, fn: () => coachShow(1) });
  }
  const secLbl = (EN() ? 'Sector — ' : '작전 구역 — ') + T(G.map.name);
  if (snap) {
    showBanner('작전 재개', '', `WAVE ${G.wave + 1} — ${T(G.map.name)}`);
  } else if (G.wave === 0) {
    showBanner(STORY.intro[0], '', STORY.intro[1]);
    G.timers.push({ t: 2.8, fn: () => showBanner('방어 준비', '', secLbl) });
  } else {
    showBanner('방어 준비', '', secLbl);
  }
  Sound.resume();
}

/* ---------- 메뉴 배경의 배회 괴수 (타이틀 분위기) ---------- */
function spawnAmbient() {
  const need = Math.min(180, Math.min(G.lw, G.lh) * 0.24); // 중앙(타이틀) 회피 거리
  for (let tries = 0; tries < 10; tries++) {
    const a0 = rand(TAU);
    const a1 = a0 + Math.PI + rand(-1.7, 1.7);
    const x0 = Math.cos(a0) * (spawnRadius(a0) + 30);
    const y0 = Math.sin(a0) * (spawnRadius(a0) + 30);
    const x1 = Math.cos(a1) * (spawnRadius(a1) + 30);
    const y1 = Math.sin(a1) * (spawnRadius(a1) + 30);
    const dx = x1 - x0, dy = y1 - y0;
    const lane = Math.abs(x0 * dy - y0 * dx) / Math.hypot(dx, dy);
    if (lane < need) continue;
    const e = makeEnemy(pick(['rusher', 'rusher', 'spitter', 'brute']), x0, y0, { hp: 1, spd: 1, bounty: 1 });
    e.face = Math.atan2(dy, dx);
    e.spawnT = 0;
    e.life = 45;
    G.ambient.push(e);
    return;
  }
}

function startGameOver() {
  if (G.state === 'DYING' || G.state === 'OVER') return;
  G.state = 'DYING';
  G.slowmoT = 1.3;
  cancelModes();
  G.sel = null;
  for (let i = 0; i < 9; i++) {
    G.timers.push({
      t: i * 0.16, fn: () => {
        boom(rand(-34, 34), rand(-34, 34), rand(20, 38), pick(['#4ce0ff', '#ff9a3d', '#eaf7ff']), 1.2);
      }
    });
  }
  G.timers.push({
    t: 1.5, fn: () => {
      G.coreGone = true;
      boom(0, 0, 130, '#ffffff', 2);
      addRing(0, 0, 20, 420, '#4ce0ff', 6, 1.3);
      addShake(22);
      for (const e of G.enemies) {
        e.dead = true; // 잔존 참조(레이저 타겟 등)가 유령을 계속 공격하지 않도록
        sparkBurst(e.x, e.y, e.def.color, 4, 120);
      }
      G.enemies.length = 0;
      G.boss = null;
    }
  });
  G.timers.push({ t: 2.6, fn: showGameOver });
}

function showGameOver() {
  G.state = 'OVER';
  saveBest();
  clearRun(); // 런 종료 → 이어하기 소멸
  // 코어 파편 지급 (영구 통화 — 죽어도 성장, 공허 균열 +25%)
  // 기본 +3: 초반 사망도 연구소 진입까지 2~3판이면 닿게 (첫 업그레이드 10파편)
  const earned = Math.round((3 + G.wave * 2 + Math.floor(G.wave / 5) * 5) * (G.map && G.map.id === 'void' ? 1.25 : 1));
  store('cs.shards', shardCount() + earned);
  els.ovShards.textContent = '+' + earned;
  els.ovWave.textContent = G.wave;
  els.ovKills.textContent = fmt(G.kills);
  const m = Math.floor(G.playT / 60), s = Math.floor(G.playT % 60);
  els.ovTime.textContent = m + ':' + String(s).padStart(2, '0');
  // 랭크
  const rank = G.wave >= 20 ? 'S' : G.wave >= 14 ? 'A' : G.wave >= 9 ? 'B' : G.wave >= 5 ? 'C' : 'D';
  // 일일 작전 기록 갱신
  if (G.daily) {
    const dk = 'cs.daily_' + G.daily.key;
    const prev = +(store(dk) || 0);
    if (Math.round(G.score) > prev) store(dk, Math.round(G.score));
    syncDailyBtn();
  }
  const ovT = document.getElementById('ovTitle');
  if (ovT) {
    const win = rank === 'S' || rank === 'A';
    ovT.textContent = win ? 'MISSION COMPLETE' : 'CORE DESTROYED';
    ovT.style.color = win ? '#d9f6ff' : '';
    ovT.style.textShadow = win ? '0 0 34px rgba(76,224,255,.55), 0 0 90px rgba(76,224,255,.3)' : '';
  }
  els.ovRank.textContent = rank;
  els.ovRank.className = 'rank-' + rank;
  els.ovTag.textContent = (G.daily ? (EN() ? '📅 DAILY OP — ' : '📅 일일 작전 — ') : '') + T(STORY.over[rank]);
  // 점수 카운트업
  const target = Math.round(G.score);
  const t0 = performance.now();
  clearInterval(G._cntIv);
  els.ovScore.textContent = '0';
  G._cntIv = setInterval(() => {
    const k = Math.min(1, (performance.now() - t0) / 900);
    const ease = 1 - (1 - k) * (1 - k);
    els.ovScore.textContent = fmt(target * ease);
    if (k >= 1) clearInterval(G._cntIv);
  }, 33);
  els.newBest.classList.toggle('hidden', target < G.best || G.best === 0 || target !== G.best);
  // 결과 시네마틱 (S/A=철수 성공 / 그 외=함락) — 파일 없으면 정적 배경 유지
  const ovv = document.getElementById('overVid');
  if (ovv) {
    const src = (rank === 'S' || rank === 'A') ? 'assets/win.mp4' : 'assets/over.mp4';
    ovv.style.display = '';
    if (ovv.getAttribute('src') !== src) ovv.src = src;
    ovv.play().catch(() => {});
  }
  els.overScreen.classList.remove('hidden');
  renderMapRow(); // 이번 런에서 해금된 구역 반영
}

/* ---------- 보스 등장 스플래시 (제미나이 아트, 없으면 배너만) ---------- */
const BOSS_ART = {};
for (const k of ['boss', 'boss2', 'boss3', 'boss4']) {
  const im = new Image();
  im.src = 'assets/' + k + '_art.webp';
  BOSS_ART[k] = im;
}
let _bsT1 = null, _bsT2 = null;
function showBossSplash(key, name) {
  const im = BOSS_ART[key];
  if (!im || !im.complete || !im.naturalWidth || !els.bossSplash) return;
  els.bossSplashImg.src = im.src;
  els.bossSplashName.textContent = name;
  els.bossSplash.classList.remove('hidden');
  requestAnimationFrame(() => els.bossSplash.classList.add('show'));
  clearTimeout(_bsT1); clearTimeout(_bsT2);
  _bsT1 = setTimeout(() => {
    els.bossSplash.classList.remove('show');
    _bsT2 = setTimeout(() => els.bossSplash.classList.add('hidden'), 380);
  }, 2500);
}

function showBanner(main, cls = '', sub = '') {
  els.banners.innerHTML =
    `<div class="banner ${cls}">${T(main)}</div>` +
    (sub ? `<div class="banner sub">${T(sub)}</div>` : '');
}

function togglePause(force) {
  if (G.state === 'MENU' || G.state === 'OVER') return;
  G.paused = force !== undefined ? force : !G.paused;
  els.pauseVeil.classList.toggle('hidden', !G.paused);
}

/* ---------- 입력 ---------- */
function bindInput() {
  window.addEventListener('pointermove', e => {
    if (dragST && e.pointerId !== dragST.id) return;
    setAim(e);
  });

  canvas.addEventListener('pointerdown', e => {
    Sound.resume();
    if (e.button === 2) { cancelModes(); G.sel = null; return; }
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    if (G.state === 'MENU' || G.state === 'OVER' || G.state === 'DYING') return;
    setAim(e);

    if (e.pointerType === 'touch') {
      // 터치: 누르는 동안 조준(고스트가 손가락 위에 뜸), 떼면 실행
      G.touch = true;
      if (G.placing) { dragST = { mode: 'place', id: e.pointerId }; return; }
      if (G.armed === 'orbital') { dragST = { mode: 'orbital', id: e.pointerId }; return; }
      if (G.armed === 'rally') { dragST = { mode: 'rally', id: e.pointerId }; return; }
      tapST = { x: e.clientX, y: e.clientY, id: e.pointerId };
      return;
    }
    // 마우스: 즉시 실행
    if (G.armed === 'orbital') { castOrbital(G.mx, G.my); G.armed = null; return; }
    if (G.armed === 'rally') { setRally(G.mx, G.my); G.armed = null; return; }
    if (G.placing) { tryPlace(); return; }
    trySelectAt(e.clientX - G.vw / 2, e.clientY - G.vh / 2);
  });

  window.addEventListener('pointerup', e => {
    if (dragST && e.pointerId === dragST.id) {
      const d = dragST;
      dragST = null;
      if (G.state !== 'BUILD' && G.state !== 'WAVE') return;
      setAim(e);
      if (d.mode === 'place' && G.placing) { tryPlace(); return; }
      if (d.mode === 'orbital' && G.armed === 'orbital') {
        castOrbital(G.mx, G.my);
        G.armed = null;
        return;
      }
      if (d.mode === 'rally' && G.armed === 'rally') {
        setRally(G.mx, G.my);
        G.armed = null;
        return;
      }
      if (d.mode === 'card' && G.placing) {
        // 필드까지 끌고 나왔으면 배치, 카드 위에서 뗐으면 선택 유지/해제(재탭)
        if (e.clientY < dockTop() - 8) tryPlace();
        else if (d.wasSel) cancelModes();
      }
      return;
    }
    if (tapST && e.pointerId === tapST.id) {
      const t = tapST;
      tapST = null;
      if (Math.hypot(e.clientX - t.x, e.clientY - t.y) < 12) {
        trySelectAt(t.x - G.vw / 2, t.y - G.vh / 2);
      }
    }
  });
  window.addEventListener('pointercancel', () => { dragST = null; tapST = null; });

  canvas.addEventListener('contextmenu', e => e.preventDefault());
  document.addEventListener('gesturestart', e => e.preventDefault());

  window.addEventListener('keydown', e => {
    if (e.repeat) return;
    Sound.resume();
    const k = e.key.toLowerCase();
    if (k === ' ') {
      e.preventDefault();
      if (G.state === 'BUILD') callWave();
      return;
    }
    if (k >= '1' && k <= '9') { selectCard(+k - 1); return; }
    if (k === 'r') { armRally(); return; }
    if (k === 'q') armAbility('orbital');
    else if (k === 'w') armAbility('stasis');
    else if (k === 'e') armAbility('repair');
    else if (k === 't') armAbility('over');
    else if (k === 'p') togglePause();
    else if (k === 'm') toggleMute();
    else if (k === 'u') upgradeSel();
    else if (k === 'x') sellSel();
    else if (k === 'escape') { cancelModes(); G.sel = null; }
  });

  els.btnStart.addEventListener('click', () => { Sound.resume(); startGame(); });
  const brr = document.getElementById('btnResumeRun');
  if (brr) brr.addEventListener('click', () => { Sound.resume(); startGame(true); });
  const bdl = document.getElementById('btnDaily');
  if (bdl) bdl.addEventListener('click', () => { Sound.resume(); startDaily(); });
  els.btnRetry.addEventListener('click', () => { Sound.resume(); startGame(); });
  els.btnCall.addEventListener('click', () => { Sound.resume(); callWave(); });
  els.btnPause.addEventListener('click', () => togglePause());
  els.btnMute.addEventListener('click', () => { Sound.resume(); toggleMute(); });
  els.btnUp.addEventListener('click', upgradeSel);
  els.btnSell.addEventListener('click', sellSel);
  els.btnCancel.addEventListener('click', () => { cancelModes(); Sfx.click(); });
  els.btnResume.addEventListener('click', () => togglePause(false));
  els.btnRestartP.addEventListener('click', () => { Sound.resume(); startGame(); });
  els.btnLab.addEventListener('click', () => { Sound.resume(); openLab(); });
  els.btnLabOver.addEventListener('click', () => { Sound.resume(); openLab(); });
  els.btnLabClose.addEventListener('click', closeLab);
  // 난이도 선택
  els.diffRow.querySelectorAll('button').forEach(b => {
    b.addEventListener('click', () => {
      Sound.resume();
      G.diffId = b.dataset.diff;
      G.scoreMul = DIFFS[G.diffId].score;
      store('cs.diff', G.diffId);
      syncDiffUI();
      Sfx.click();
    });
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden && (G.state === 'WAVE' || G.state === 'BUILD') && !G.paused) togglePause(true);
  });
  window.addEventListener('resize', resize);
}

function toggleMute() {
  Sound.setMuted(!Sound.muted);
  els.btnMute.textContent = Sound.muted ? '🔇' : '🔊';
}

function syncDiffUI() {
  els.diffRow.querySelectorAll('button').forEach(b =>
    b.classList.toggle('sel', b.dataset.diff === G.diffId));
}

/* ---------- 작전 구역 선택 UI ---------- */
function mapThumb(m) {
  const c = document.createElement('canvas');
  c.width = 112; c.height = 60;
  const g = c.getContext('2d');
  const im = ASSET_IMG[m.img];
  if (im) {
    // 중앙 크롭
    g.drawImage(im, 0, im.height * 0.2, im.width, im.height * 0.6, 0, 0, 112, 60);
    g.fillStyle = 'rgba(5,10,18,0.25)';
    g.fillRect(0, 0, 112, 60);
  } else {
    g.fillStyle = '#1c2836';
    g.fillRect(0, 0, 112, 60);
    g.strokeStyle = 'rgba(76,224,255,0.3)';
    g.strokeRect(3, 3, 106, 54);
  }
  return c;
}

function renderMapRow() {
  els.mapRow.innerHTML = '';
  const selId = store('cs.map') || 'random';
  const entries = [{ id: 'random', name: '무작위', gdesc: '해금된 구역 중 랜덤 출격', unlock: 1 }, ...MAPS];
  for (const m of entries) {
    const locked = m.id !== 'random' && !mapUnlocked(m);
    const el = document.createElement('div');
    el.className = 'mapCard' + (locked ? ' locked' : '') + (selId === m.id ? ' sel' : '');
    if (m.id === 'random') {
      const c = document.createElement('canvas');
      c.width = 112; c.height = 60;
      const g = c.getContext('2d');
      g.fillStyle = '#141e2a'; g.fillRect(0, 0, 112, 60);
      g.font = '26px Bahnschrift'; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillStyle = '#4ce0ff'; g.fillText('?', 56, 32);
      el.appendChild(c);
    } else {
      el.appendChild(mapThumb(m));
    }
    const nm = document.createElement('div');
    nm.className = 'mn';
    nm.textContent = T(m.name);
    el.appendChild(nm);
    const gd = document.createElement('div');
    gd.className = 'mg';
    gd.textContent = locked ? (EN() ? 'Unlocks at wave ' + m.unlock : '웨이브 ' + m.unlock + ' 도달 시 해금') : T(m.gdesc);
    el.appendChild(gd);
    el.addEventListener('click', () => {
      Sound.resume();
      if (locked) { Sfx.error(); return; }
      store('cs.map', m.id);
      renderMapRow();
      Sfx.click();
    });
    els.mapRow.appendChild(el);
  }
}

/* ---------- 메인 업데이트 ---------- */
function update(dt) {
  G.time += dt;

  // 타이머
  for (let i = 0; i < G.timers.length; i++) {
    const t = G.timers[i];
    t.t -= dt;
    if (t.t <= 0) {
      t.fn();
      G.timers[i] = G.timers[G.timers.length - 1];
      G.timers.pop(); i--;
    }
  }

  for (const id in G.cool) G.cool[id] = Math.max(0, G.cool[id] - dt);
  G.stasisT = Math.max(0, G.stasisT - dt);

  const c = G.core;
  c.lastHit += dt;
  c.shFlashT = Math.max(0, c.shFlashT - dt);
  c.hitFlash = Math.max(0, c.hitFlash - dt * 1.6);
  if (c.hp > 0 && c.lastHit > 5 && c.sh < c.maxsh) {
    c.sh = Math.min(c.maxsh, c.sh + (16 + (G.labShRegen || 0)) * dt);
  }

  if (G.state === 'BUILD' || G.state === 'WAVE') {
    G.minerals += (ECON.passive + (G.labIncome || 0)) * dt;
    G.playT += dt;
  }

  if (G.state === 'BUILD') {
    G.buildT -= dt;
    if (G.buildT <= 0) callWave();
  } else if (G.state === 'WAVE') {
    G.waveT += dt;
    while (G.events.length) {
      const ev = G.events[0];
      if (ev.t > G.waveT) break;
      if (!ev.warn && G.enemies.length > 140) { ev.t = G.waveT + 1; break; }
      G.events.shift();
      if (ev.warn) {
        G.effects.push({ kind: 'warn', ang: ev.ang, spread: Math.max(0.5, ev.spread), t: 0, dur: 1.7, layer: 'ui' });
      } else {
        spawnEvent(ev);
      }
    }
    // 마그마 균열 지대: 주기적 용암 분출 (적·터렛 공용 피해 — 배치 리스크)
    if (G.map && G.map.id === 'rift') {
      G.gimT -= dt;
      if (G.gimT <= 0) {
        G.gimT = 12 + rand(6);
        const spots = 2 + Math.min(3, Math.floor(G.wave / 8));
        for (let k = 0; k < spots; k++) {
          const a = rand(TAU), d = rand(60, buildMax() * 0.95);
          const gx = Math.cos(a) * d, gy = Math.sin(a) * d;
          addRing(gx, gy, 72, 60, '#ff9a3d', 3, 1.2); // 경고 링
          G.timers.push({
            t: 1.2, fn: () => {
              boom(gx, gy, 60, '#ff7a3d', 1.3);
              splashDamage(gx, gy, 70, 90);
              for (const t of G.turrets) {
                if (dist2(gx, gy, t.x, t.y) < 70 * 70) damageStructure(t, 70);
              }
              for (const u of G.troops) {
                if (dist2(gx, gy, u.x, u.y) < 70 * 70) damageStructure(u, 70);
              }
              scorch(gx, gy, 38);
            }
          });
        }
        Sound.tone({ type: 'sawtooth', f: 70, f2: 40, dur: 0.6, v: 0.12, lp: 300 });
      }
    }
    // 교착 방지: 웨이브가 150초를 넘기면 잔존 군체가 격노
    if (!G.enraged && G.waveT > 150 && G.enemies.length > 0) {
      G.enraged = true;
      for (const e of G.enemies) { e.spd *= 1.5; e.dmg *= 1.5; }
      showBanner('군체가 격노한다', 'danger', '적 이동 속도·공격력 대폭 상승');
      Sfx.bossRoar();
    }
    if (G.events.length === 0 && G.enemies.length === 0) clearWave();
  } else if (G.state === 'MENU') {
    if (Math.random() < dt * 3) {
      addPart({
        x: rand(-G.lw / 2, G.lw / 2), y: rand(-G.lh / 2, G.lh / 2),
        vx: rand(-8, 8), vy: rand(-8, 8), dur: rand(1.5, 3),
        size: 1.2, color: '#4ce0ff', add: true, shape: 'snow', drag: 0,
      });
    }
    // 배회 괴수
    G.ambT -= dt;
    if (G.ambT <= 0 && G.ambient.length < 5) {
      G.ambT = rand(2.5, 5);
      spawnAmbient();
    }
    for (let i = 0; i < G.ambient.length; i++) {
      const a = G.ambient[i];
      a.ph += dt * a.spd * 0.045;
      a.x += Math.cos(a.face) * a.spd * 0.5 * dt;
      a.y += Math.sin(a.face) * a.spd * 0.5 * dt;
      a.life -= dt;
      if (a.life <= 0 || Math.hypot(a.x, a.y) > Math.hypot(G.lw, G.lh) / 2 + 130) {
        G.ambient.splice(i, 1); i--;
      }
    }
  }

  // 콤보 유지 시간
  if (G.comboT > 0) {
    G.comboT -= dt;
    if (G.comboT <= 0) {
      if (G.combo >= 8) {
        const b = G.combo * 3;
        G.minerals += b;
        addFloater(0, -74, `콤보 ×${G.combo}  +${b}◆`, '#4ce0ff');
      }
      G.combo = 0;
    }
  }
  if (G.hintOverride) {
    G.hintOverride.t -= dt;
    if (G.hintOverride.t <= 0) G.hintOverride = null;
  }

  // 엔티티 업데이트
  const es = G.enemies;
  for (let i = 0; i < es.length; i++) {
    updateEnemy(es[i], dt);
    if (es[i].dead) { es[i] = es[es.length - 1]; es.pop(); i--; }
  }

  Grid.clear();
  for (let i = 0; i < es.length; i++) Grid.insert(es[i]);
  separateEnemies();

  const ts = G.turrets;
  for (let i = 0; i < ts.length; i++) {
    updateTurret(ts[i], dt);
    if (ts[i].dead) { ts.splice(i, 1); i--; }
  }
  const ds = G.drones;
  for (let i = 0; i < ds.length; i++) {
    updateDrone(ds[i], dt);
    if (ds[i].dead) { ds.splice(i, 1); i--; }
  }
  const tp = G.troops;
  for (let i = 0; i < tp.length; i++) {
    updateTroop(tp[i], dt);
    if (tp[i].dead) { tp.splice(i, 1); i--; }
  }
  const ps = G.projs;
  for (let i = 0; i < ps.length; i++) {
    updateProjectile(ps[i], dt);
    if (ps[i].dead) { ps[i] = ps[ps.length - 1]; ps.pop(); i--; }
  }
  const cs = G.crystals;
  for (let i = 0; i < cs.length; i++) {
    updateCrystal(cs[i], dt);
    if (cs[i].dead) { cs[i] = cs[cs.length - 1]; cs.pop(); i--; }
  }

  updateParticles(dt);
  updateEffects(dt);
  updateFloaters(dt);
  updateEmbers(dt);

  G.shake = Math.max(0, G.shake - 40 * dt - G.shake * 4 * dt);
  if (G.cam) G.cam.punch = Math.max(0, G.cam.punch - (G.cam.punch * 5 + 0.5) * dt);
  if (G.overT > 0) G.overT -= dt;
}

/* ---------- 렌더 ---------- */
function draw() {
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.drawImage(bgCanvas, 0, 0);
  ctx.drawImage(G.decal, 0, 0);

  // 카메라: 셰이크 + 저속 드리프트 + 이벤트 줌 펀치
  const shx = rand(-1, 1) * G.shake, shy = rand(-1, 1) * G.shake;
  const camx = Math.sin(G.time * 0.21) * 2.4 + Math.sin(G.time * 0.53) * 1.2;
  const camy = Math.cos(G.time * 0.17) * 2.2 + Math.sin(G.time * 0.43) * 1.1;
  const zoom = 1 + (G.cam ? G.cam.punch * 0.05 : 0) + Math.sin(G.time * 0.6) * 0.003;
  G.camx = camx; G.camy = camy; G.zoom = zoom; G.shx = shx; G.shy = shy;
  const worldXf = g => {
    g.translate(G.vw / 2 + shx + camx, G.vh / 2 + shy + camy);
    g.scale(G.vs * zoom, G.vs * zoom);
  };
  ctx.save();
  worldXf(ctx);

  drawEffects(ctx, 'under');
  for (const t of G.turrets) if (t.type === 'cryo') drawCryoAura(ctx, t);

  // 배치 모드 오버레이
  if (G.placing && G.ghost) {
    ctx.globalAlpha = 0.25;
    ctx.strokeStyle = '#4ce0ff';
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(0, 0, buildMax(), 0, TAU); ctx.stroke();
    ctx.globalAlpha = 1;
    const ok = canPlaceAt(G.mx, G.my) && G.minerals >= TURRETS[G.placing].cost;
    const rg = turretRange(G.ghost);
    ctx.globalAlpha = 0.07;
    ctx.fillStyle = ok ? '#4ce0ff' : '#ff4d5e';
    ctx.beginPath(); ctx.arc(G.mx, G.my, rg, 0, TAU); ctx.fill();
    ctx.globalAlpha = 0.4;
    ctx.strokeStyle = ok ? '#4ce0ff' : '#ff4d5e';
    ctx.beginPath(); ctx.arc(G.mx, G.my, rg, 0, TAU); ctx.stroke();
    ctx.globalAlpha = ok ? 0.65 : 0.3;
    G.ghost.x = G.mx; G.ghost.y = G.my;
    drawTurret(ctx, G.ghost, true);
    ctx.globalAlpha = 1;
  }
  if (G.sel) {
    const rg = turretRange(G.sel);
    ctx.globalAlpha = 0.3;
    ctx.strokeStyle = '#4ce0ff';
    ctx.setLineDash([5, 7]);
    ctx.beginPath(); ctx.arc(G.sel.x, G.sel.y, rg, 0, TAU); ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
  }
  if (G.armed === 'orbital') {
    ctx.globalAlpha = 0.5;
    ctx.strokeStyle = '#eaf7ff';
    ctx.setLineDash([6, 8]);
    ctx.lineDashOffset = -G.time * 20;
    ctx.beginPath(); ctx.arc(G.mx, G.my, 95, 0, TAU); ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
  }

  if (G.state === 'MENU') for (const a of G.ambient) drawEnemy(ctx, a);
  if (!G.coreGone) drawCore(ctx);
  // 집결 깃발 (병력 보유 또는 지정 중일 때)
  if ((G.troops.length > 0 || G.armed === 'rally') && (G.state === 'BUILD' || G.state === 'WAVE')) {
    const rx = G.rally.x, ry = G.rally.y;
    ctx.globalAlpha = 0.18;
    ctx.strokeStyle = '#4ce0ff';
    ctx.setLineDash([4, 8]);
    ctx.beginPath(); ctx.arc(rx, ry, 210, 0, TAU); ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 0.9;
    ctx.strokeStyle = '#9beeff';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(rx, ry + 6); ctx.lineTo(rx, ry - 14); ctx.stroke();
    ctx.fillStyle = '#4ce0ff';
    ctx.beginPath();
    ctx.moveTo(rx, ry - 14); ctx.lineTo(rx + 11, ry - 10); ctx.lineTo(rx, ry - 6);
    ctx.closePath(); ctx.fill();
    ctx.globalAlpha = 1;
  }
  if (G.armed === 'rally') {
    ctx.globalAlpha = 0.4;
    ctx.strokeStyle = '#9beeff';
    ctx.setLineDash([6, 8]);
    ctx.lineDashOffset = -G.time * 20;
    ctx.beginPath(); ctx.arc(G.mx, G.my, 24, 0, TAU); ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 1;
  }
  for (const t of G.turrets) drawTurret(ctx, t);
  for (const u of G.troops) drawTroop(ctx, u);
  for (const d of G.drones) drawDrone(ctx, d);
  let bossRef = null;
  for (const e of G.enemies) {
    if (e.boss) { bossRef = e; continue; }
    drawEnemy(ctx, e);
  }
  if (bossRef) drawEnemy(ctx, bossRef);
  for (const p of G.projs) drawProjectile(ctx, p);
  drawCrystals(ctx);
  drawEffects(ctx, 'over');
  drawParticles(ctx);
  ctx.restore();

  // 어둠 + 라이트 펀칭 + 블룸 (월드 위, UI 아래)
  drawLighting(ctx);

  // 라이팅 위 월드 패스: 발광 앰비언트 · HP 바 · 플로터 · 커서
  ctx.save();
  worldXf(ctx);
  drawEmbers(ctx);
  drawEffects(ctx, 'ui');
  // 적 HP 바
  for (const e of G.enemies) {
    if (e.boss || e.hp >= e.maxhp) continue;
    const w = e.r * 2 + 8, k = e.hp / e.maxhp;
    ctx.fillStyle = 'rgba(4,10,18,0.75)';
    ctx.fillRect(e.x - w / 2, e.y - e.r - 8, w, 3);
    ctx.fillStyle = k > 0.45 ? '#7dd87d' : '#ff4d5e';
    ctx.fillRect(e.x - w / 2, e.y - e.r - 8, w * k, 3);
  }
  drawFloaters(ctx);

  // 커스텀 커서 (터치는 배치/조준 중일 때만 표시, 화면 크기 불변)
  if ((G.state === 'BUILD' || G.state === 'WAVE') && (!G.touch || G.placing || G.armed)) {
    const ok = !G.placing || (canPlaceAt(G.mx, G.my) && G.minerals >= TURRETS[G.placing].cost);
    const iv = 1 / G.vs;
    ctx.strokeStyle = ok ? '#4ce0ff' : '#ff4d5e';
    ctx.lineWidth = 1.4 * iv;
    ctx.globalAlpha = 0.9;
    ctx.beginPath(); ctx.arc(G.mx, G.my, 6 * iv, 0, TAU); ctx.stroke();
    ctx.beginPath();
    for (const [dx, dy] of [[10, 0], [-10, 0], [0, 10], [0, -10]]) {
      ctx.moveTo(G.mx + dx * 0.5 * iv, G.my + dy * 0.5 * iv);
      ctx.lineTo(G.mx + dx * iv, G.my + dy * iv);
    }
    ctx.stroke();
    ctx.globalAlpha = 1;
  }

  ctx.restore();

  // 스크린 스페이스 오버레이
  ctx.drawImage(vigCanvas, 0, 0);
  if (G.stasisT > 0) {
    ctx.fillStyle = `rgba(120,200,255,${0.05 + Math.sin(G.time * 5) * 0.015})`;
    ctx.fillRect(0, 0, G.vw, G.vh);
  }
  if (G.core.hitFlash > 0) {
    ctx.fillStyle = `rgba(255,50,70,${G.core.hitFlash * 0.22})`;
    ctx.fillRect(0, 0, G.vw, G.vh);
  }
  if (G.core.hp > 0 && G.core.hp / G.core.maxhp < 0.35) {
    ctx.fillStyle = `rgba(255,40,60,${0.04 + 0.035 * Math.sin(G.time * 6)})`;
    ctx.fillRect(0, 0, G.vw, G.vh);
  }
}

/* ---------- HUD 동기화 ---------- */
let _lastMin = -1, _lastScore = -1;
function syncHud() {
  const min = Math.floor(G.minerals);
  if (min !== _lastMin) { _lastMin = min; els.minerals.textContent = fmt(min); }
  if (G.pillPop) {
    G.pillPop = false;
    els.resPill.classList.remove('pop');
    void els.resPill.offsetWidth;
    els.resPill.classList.add('pop');
  }
  const sc = Math.round(G.score);
  if (sc !== _lastScore) { _lastScore = sc; els.score.textContent = fmt(sc); }
  els.best.textContent = fmt(G.best);

  if (G.state === 'BUILD') {
    els.waveLabel.textContent = 'WAVE ' + (G.wave + 1);
    els.waveState.innerHTML = (EN() ? 'Prep ' : '방어 준비 ') + `<b>${Math.ceil(G.buildT)}</b>s`;
    els.btnCall.classList.remove('hidden');
    const bonus = G.wave > 0 ? Math.round(G.buildT * ECON.callBonusPerSec) : 0;
    els.btnCall.innerHTML = bonus > 0
      ? `${EN() ? 'Call Now' : '즉시 소환'} <span class="bonus">+${bonus}◆</span>`
      : `${EN() ? 'Start Wave' : '웨이브 시작'} <span class="bonus">(Space)</span>`;
  } else if (G.state === 'WAVE') {
    els.waveLabel.textContent = 'WAVE ' + G.wave;
    els.waveState.innerHTML = (EN() ? 'Enemies ' : '적 잔여 ') + `<b>${G.enemies.length + G.events.filter(e => !e.warn).length}</b>`;
    els.btnCall.classList.add('hidden');
  } else {
    els.btnCall.classList.add('hidden');
  }

  const c = G.core;
  els.shieldFill.style.width = (c.sh / c.maxsh * 100) + '%';
  els.hpFill.style.width = (Math.max(0, c.hp) / c.maxhp * 100) + '%';
  els.hpText.textContent = Math.max(0, Math.ceil(c.hp)) + ' / ' + c.maxhp;
  els.hpBar.classList.toggle('low', c.hp / c.maxhp < 0.35);

  if (G.boss && !G.boss.dead) {
    els.bossBar.classList.remove('hidden');
    els.bossFill.style.width = (Math.max(0, G.boss.hp) / G.boss.maxhp * 100) + '%';
  } else {
    els.bossBar.classList.add('hidden');
  }

  for (const { el, ab } of abEls) {
    const k = G.cool[ab.id] / ab.cd;
    el.style.setProperty('--cd', k.toFixed(3));
    el.classList.toggle('ready', k <= 0);
    el.classList.toggle('armed', G.armed === ab.id || (ab.id === 'over' && G.overT > 0));
  }
  if (els.btnRally) els.btnRally.classList.toggle('armed', G.armed === 'rally');
  for (const cd of cardEls) {
    const locked = !cardUnlocked(cd.w);
    cd.el.classList.toggle('locked', locked);
    if (cd.kind === 'drone') {
      cd.el.classList.toggle('dis', !locked && G.minerals < ECON.droneCost);
      cd.el.querySelector('.nm').textContent = `${T('요격 드론')} ×${G.drones.length}`;
    } else if (cd.kind === 'troop') {
      const def = TROOPS[cd.type];
      cd.el.classList.toggle('dis', !locked && G.minerals < def.cost);
      const n = G.troops.reduce((s, u) => s + (u.type === cd.type ? 1 : 0), 0);
      cd.el.querySelector('.nm').textContent = `${T(def.name)} ×${n}`;
    } else {
      cd.el.classList.toggle('dis', !locked && G.minerals < TURRETS[cd.type].cost);
      cd.el.classList.toggle('sel', G.placing === cd.type);
    }
  }

  // 다음 웨이브 미리보기 (준비 시간에만)
  els.wavePreview.classList.toggle('hidden', G.state !== 'BUILD' || !G.nextPlan);

  // 콤보 표시
  if (G.combo >= 5) {
    els.combo.classList.remove('hidden');
    const txt = '×' + G.combo;
    if (els.combo.textContent !== txt) {
      els.combo.textContent = txt;
      els.combo.classList.remove('pop');
      void els.combo.offsetWidth;
      els.combo.classList.add('pop');
    }
  } else {
    els.combo.classList.add('hidden');
  }

  if (G.sel) {
    const t = G.sel;
    els.turretPanel.classList.remove('hidden');
    els.tpName.innerHTML = `${t.def.name}<em>Lv.${t.lvl}</em>`;
    els.tpStats.textContent = statText(t);
    els.tpHp.style.width = (t.hp / t.maxhp * 100) + '%';
    if (t.lvl < 3) {
      const cost = upgradeCost(t);
      els.btnUp.textContent = `${EN() ? 'Upgrade' : '강화'} ${cost}◆ (U)`;
      els.btnUp.disabled = G.minerals < cost;
    } else {
      els.btnUp.textContent = EN() ? 'MAX LEVEL' : '최대 레벨';
      els.btnUp.disabled = true;
    }
    els.btnSell.textContent = `${EN() ? 'Sell' : '매각'} +${sellValue(t)}◆ (X)`;
  } else {
    els.turretPanel.classList.add('hidden');
  }

  // 힌트 (터치/마우스 문구 분기)
  let hint = '';
  if (G.hintOverride) {
    hint = G.hintOverride.txt;
  } else if (G.armed === 'orbital') {
    hint = T(G.touch ? '드래그로 조준하고 손을 떼면 폭격합니다' : '폭격 지점을 클릭하세요 · 우클릭 취소');
  } else if (G.armed === 'rally') {
    hint = T(G.touch ? '드래그로 집결 지점을 잡고 손을 떼세요' : '집결 지점을 클릭하세요 · 우클릭 취소');
  } else if (G.placing) {
    hint = T(G.touch ? '드래그로 위치를 잡고 손을 떼면 배치됩니다' : '좌클릭 배치 · 우클릭 취소 (자금이 되는 한 연속 배치)');
  } else if (G.state === 'BUILD' && G.turrets.length === 0) {
    hint = T(G.touch ? '하단 카드를 필드로 드래그해 터렛을 배치하세요' : '하단 카드 클릭 또는 1~6 키로 터렛을 선택해 배치하세요');
  } else if (G.state === 'BUILD' && G.wave === 0) {
    hint = T(G.touch ? '[웨이브 시작] 버튼으로 첫 웨이브를 개시하세요' : 'Space 또는 [웨이브 시작]으로 첫 웨이브를 개시하세요');
  }
  els.hint.textContent = hint;
  els.hint.style.opacity = hint ? 1 : 0;
  els.btnCancel.classList.toggle('hidden', !(G.touch && (G.placing || G.armed)));

  // 크리스탈 목표점 (자원 표시 위치, 월드 좌표로 변환)
  const r = els.resPill.getBoundingClientRect();
  G.crystalTarget.x = (r.left + r.width / 2 - G.vw / 2) / G.vs;
  G.crystalTarget.y = (r.top + r.height / 2 - G.vh / 2) / G.vs;

  // 음악 강도
  if (G.state === 'WAVE') Music.intensity = G.boss ? 1.6 : 1;
  else if (G.state === 'BUILD') Music.intensity = 0.35;
  else if (G.state === 'MENU') Music.intensity = 0.5;
  else Music.intensity = 0.15;
}

/* ---------- 메인 루프 ---------- */
let _last = performance.now(), _fps = 60;
function frame(now) {
  requestAnimationFrame(frame);
  let rdt = Math.min(0.033, (now - _last) / 1000);
  _last = now;
  _fps = lerp(_fps, 1 / Math.max(rdt, 1e-4), 0.05);
  window.__fps = Math.round(_fps);
  // 오토 품질: 프레임 저하 시 라이트/앰비언트 밀도 자동 감축 (설정 '절전'이면 고정)
  if (!G._qT || now - G._qT > 2000) {
    G._qT = now;
    const q = G.qMode === 'low' ? 0.45 : _fps < 42 ? 0.45 : _fps < 52 ? 0.7 : 1;
    if (q !== (G.quality || 1)) { G.quality = q; seedEmbers(); }
    // 모바일 메모리 회수로 캔버스 컨텍스트가 유실되면 스프라이트·배경이 전부 백지가 됨
    // (오프스크린 캔버스 다수라 부분 복구 불가) → 1회 리로드로 복구, 진행은 cs.run에서 재개
    if (!G._ctxReload
        && ((ctx.isContextLost && ctx.isContextLost())
          || (G.lctx && G.lctx.isContextLost && G.lctx.isContextLost()))) {
      G._ctxReload = true;
      location.reload();
    }
  }

  if (G.slowmoT > 0) {
    G.slowmoT -= rdt;
    G.timeScale = lerp(G.timeScale, 0.3, Math.min(1, rdt * 10));
  } else {
    G.timeScale = lerp(G.timeScale, 1, Math.min(1, rdt * 6));
  }
  if (G.hitstop > 0) G.hitstop -= rdt; // 명중 순간 정지
  const dt = G.paused ? 0 : rdt * G.timeScale * (G.hitstop > 0 ? 0.08 : 1);
  if ((G.assetsVer || 0) !== _avSeen) {
    _avSeen = G.assetsVer || 0;
    refreshCardIcons();
    renderMapRow(); // 썸네일 갱신
    const mi = (G.map && G.map.img) || 'arena';
    if (ASSET_IMG[mi] && !G._arenaBg) { G._arenaBg = true; buildBackground(); }
  }
  update(dt);
  draw();
  syncHud();
  coachTick();
}

/* ---------- 부트 ---------- */
resetState();
G.touch = matchMedia('(pointer: coarse)').matches;
applyStaticI18n(); // EN 모드면 정적 마크업 교체 (카드/HUD는 렌더 시점에 T() 적용)
loadAssets(); // AI 생성 이미지 에셋 (없으면 프로시저럴 폴백)
resize();
buildCards();
buildAbilities();
bindInput();
syncDiffUI();
renderMapRow();
// 타이틀 시네마틱 영상 로드 (실패 시 제거 → 키아트 폴백)
const _tv = document.getElementById('titleVid');
if (_tv) {
  _tv.addEventListener('error', () => _tv.remove(), { once: true });
  _tv.src = 'assets/title.mp4';
}
const _ov = document.getElementById('overVid');
if (_ov) _ov.addEventListener('error', () => { _ov.style.display = 'none'; });
els.best.textContent = fmt(G.best);
els.btnMute.textContent = Sound.muted ? '🔇' : '🔊';
syncResumeBtn();
syncDailyBtn();
G.vibOn = (store('cs.vib') === null ? G.touch : store('cs.vib') === '1');
G.qMode = store('cs.q') || 'auto';
bindSettings();
// PWA 서비스 워커 (http/https에서만 — file:// 더블클릭 실행은 그대로 동작)
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
  navigator.serviceWorker.register('sw.js').catch(() => {});
}
window.G = G;
requestAnimationFrame(frame);
