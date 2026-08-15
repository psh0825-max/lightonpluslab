'use strict';
/* ============================================================
   CORE SIEGE — i18n.js
   KO(원문 키) → EN 사전. 기본 언어는 한국어, 미번역 문자열은 KO 폴백.
   ============================================================ */

let LANG = (function () {
  try {
    const s = localStorage.getItem('cs.lang');
    if (s) return s;
    return (navigator.language || 'ko').toLowerCase().startsWith('ko') ? 'ko' : 'en';
  } catch (e) { return 'ko'; }
})();
const EN = () => LANG === 'en';

const I18N_EN = {
  // ---- 터렛 ----
  '펄스 터렛': 'Pulse Turret',
  '빠른 연사 기본 포탑. 초반 방어의 핵심.': 'Rapid-fire basic turret. Backbone of early defense.',
  '테슬라 코일': 'Tesla Coil',
  '최대 4체 체인 번개. 군체 러시 제압에 특화.': 'Chain lightning up to 4 targets. Shreds swarm rushes.',
  '집속 레이저': 'Focus Laser',
  '단일 대상 지속 광선. 같은 대상 조준 시 최대 2.2배 과열 피해.': 'Sustained beam. Ramps to 2.2x heat damage on one target.',
  '미사일 포대': 'Missile Battery',
  '유도 미사일. 착탄 지점 범위 폭발 피해.': 'Homing missiles with splash damage on impact.',
  '레일건': 'Railgun',
  '충전 후 직선 관통 저격. 브루트·보스 특화.': 'Charged piercing shot. Built for brutes and bosses.',
  '빙결장': 'Cryo Field',
  '범위 내 모든 적 감속. 공격 능력 없음.': 'Slows all enemies in range. No attack.',
  '요격 드론': 'Interceptor Drone',
  '코어 주위를 선회하며 자동 요격.': 'Orbits the core, auto-engaging.',
  // ---- 병력 ----
  '해병': 'Marine',
  '원거리 보병. 집결 지점 주변을 방어.': 'Ranged infantry. Defends around the rally point.',
  '전투 매딕': 'Combat Medic',
  '아군 병력을 치유하고 주기적으로 보호막을 부여. 공격 불가.': 'Heals troops and grants periodic shields. Cannot attack.',
  '저격수': 'Sniper',
  '초장거리 관통 저격. 강적 처치 특화.': 'Extreme-range shots. Elite killer.',
  '화염척탄병': 'Pyro Grenadier',
  '소이 유탄 범위 폭격. 군집 소탕 특화.': 'Incendiary grenades. Clears packs.',
  // ---- 능력 ----
  '궤도 폭격': 'Orbital Strike',
  '지정 지역에 3연속 궤도 폭격. 총 1,140 피해.': 'Three orbital blasts on target area. 1,140 total damage.',
  '정지장': 'Stasis Field',
  '전장의 모든 적을 4.5초간 75% 감속.': 'Slows all enemies by 75% for 4.5s.',
  '긴급 수리': 'Emergency Repair',
  '코어 +320 수리, 보호막 50% 충전, 모든 터렛 35% 수리.': 'Core +320, shield +50%, all turrets repaired 35%.',
  '코어 과충전': 'Core Overcharge',
  '25초간 모든 터렛 피해 +30%. 사용할 때마다 가격 +80◆.': 'Turret damage +30% for 25s. Price rises +80◆ per use.',
  // ---- 연구소 ----
  '연구소': 'Laboratory',
  '무기 출력': 'Weapon Output',
  '모든 터렛 피해 +4%': 'All turret damage +4%',
  '코어 장갑': 'Core Armor',
  '코어 최대 체력 +8%': 'Core max HP +8%',
  '보호막 공명': 'Shield Resonance',
  '보호막 +10% · 재생 +1.5/s': 'Shield +10%, regen +1.5/s',
  '채굴 효율': 'Mining Efficiency',
  '시작 자원 +50 · 초당 수입 +0.5': 'Start +50◆, income +0.5/s',
  '전리품 회수': 'Salvage Ops',
  '처치 보상 +3% (복리형)': 'Kill bounty +3% (compounding)',
  '강습 보병': 'Assault Infantry',
  '병력 피해·체력 +6%': 'Troop damage & HP +6%',
  // ---- 맵 ----
  '중앙 플랫폼': 'Central Platform',
  '표준 전장': 'Standard battlefield',
  '마그마 균열 지대': 'Magma Rift',
  '주기적 용암 분출 — 적·터렛 모두 피해': 'Periodic eruptions damage enemies and turrets',
  '침식 전초기지': 'Infested Outpost',
  '군체 체력 +10% · 처치 보상 +12%': 'Swarm HP +10%, bounty +12%',
  '극저온 구역': 'Cryo Sector',
  '적 이속 -10% · 터렛 연사 -8%': 'Enemy speed -10%, turret rate -8%',
  '공허 균열': 'Void Fissure',
  '점멸 개체 강화 · 코어 파편 +25%': 'Blinkers empowered, core shards +25%',
  '무작위': 'Random',
  '해금된 구역 중 랜덤 출격': 'Random unlocked sector',
  // ---- 일일 모디파이어 ----
  '신속 군체': 'Swift Swarm',
  '적 이속 +12%': 'Enemy speed +12%',
  '강인 갑각': 'Hardened Chitin',
  '적 체력 +15%': 'Enemy HP +15%',
  '취약 코어': 'Fragile Core',
  '코어 체력 -15%': 'Core HP -15%',
  '짧은 준비': 'Short Prep',
  '준비 시간 -4초': 'Prep time -4s',
  '풍부한 전리품': 'Rich Salvage',
  '처치 보상 +25%': 'Bounty +25%',
  // ---- 스토리 ----
  '수신: 함대 사령부': 'INCOMING: Fleet Command',
  '철수선 도착까지 코어를 사수하라': 'Hold the core until evac arrives',
  '지각 균열에서 첫 생체 반응 감지': 'First bio-signs detected in the crust fissure',
  '군체 정찰대가 접근한다': 'Swarm scouts inbound',
  '놈들이 학습하고 있다 — 신규 병기 인가 승인': 'They are learning — new weapons authorized',
  '산성 개체 출현 — 원거리 공격 주의': 'Acid spitters sighted — watch for ranged fire',
  '중장갑 개체 다수 감지': 'Multiple heavy-armor signatures',
  '군체의 공세가 거세진다': 'The swarm presses harder',
  '공간 왜곡 반응 — 점멸 개체 확인': 'Warp distortions — blinkers confirmed',
  '산란체 확인 — 격파 시 유충이 쏟아진다': 'Carriers confirmed — they burst into larvae',
  '장거리 통신 두절 — 이제 우리뿐이다': 'Long-range comms lost — we are alone now',
  '재생 개체 출현 — 최우선 제거 권장': 'Menders sighted — priority targets',
  '코어 출력 상승 — 공명이 놈들을 부른다': 'Core output rising — the resonance calls them',
  '방어선 너머는 이미 놈들의 땅이다': 'Beyond the line is already theirs',
  '철수선이 항로에 진입했다 — 조금만 더': 'Evac ship on approach — hold on',
  '파괴자 알파': 'Destroyer Alpha',
  '심연의 베헤모스': 'Abyssal Behemoth',
  '공명 포식자': 'Resonance Predator',
  '군체의 어머니': 'Mother of the Swarm',
  '전설로 기록될 방어전이었다': 'A defense that will become legend',
  '함대는 당신의 이름을 기억할 것이다': 'The fleet will remember your name',
  '코어는 침묵했지만, 기록은 남았다': 'The core fell silent, but the record remains',
  '바스티온-7의 마지막 신호가 끊겼다': "Bastion-7's final signal has been lost",
  // ---- 배너/HUD ----
  '방어 준비': 'PREPARE DEFENSE',
  '보스 격파': 'BOSS DESTROYED',
  '작전 재개': 'OPERATION RESUMED',
  '거대 개체가 방어선에 진입한다': 'A colossal entity breaches the line',
  '터렛 출력 +30% — 25초': 'Turret output +30% — 25s',
  '일시정지': 'PAUSED',
  '돌진!': 'CHARGE!',
  '산란!': 'SPAWNING!',
  '수정 실드!': 'CRYSTAL SHIELD!',
  // ---- 힌트 ----
  '드래그로 조준하고 손을 떼면 폭격합니다': 'Drag to aim, release to strike',
  '폭격 지점을 클릭하세요 · 우클릭 취소': 'Click target point · Right-click to cancel',
  '드래그로 집결 지점을 잡고 손을 떼세요': 'Drag to set rally point, then release',
  '집결 지점을 클릭하세요 · 우클릭 취소': 'Click rally point · Right-click to cancel',
  '드래그로 위치를 잡고 손을 떼면 배치됩니다': 'Drag to position, release to build',
  '좌클릭 배치 · 우클릭 취소 (자금이 되는 한 연속 배치)': 'Left-click to build · Right-click to cancel (repeats while affordable)',
  '하단 카드를 필드로 드래그해 터렛을 배치하세요': 'Drag a card onto the field to build a turret',
  '하단 카드 클릭 또는 1~6 키로 터렛을 선택해 배치하세요': 'Click a card or press 1-6 to select and build',
  '[웨이브 시작] 버튼으로 첫 웨이브를 개시하세요': 'Press [Start Wave] to begin the first wave',
  'Space 또는 [웨이브 시작]으로 첫 웨이브를 개시하세요': 'Press Space or [Start Wave] to begin',
  // ---- 코치마크 ----
  '카드를 필드로 드래그해 터렛을 배치하세요': 'Drag a card onto the field to build a turret',
  '준비되면 [웨이브 시작] — 남은 시간만큼 보너스 ◆': 'Ready? [Start Wave] — leftover time pays bonus ◆',
  '위기엔 특수 능력! 궤도 폭격은 드래그로 조준': 'In a pinch, use abilities! Drag to aim Orbital Strike',
  // ---- 설정 ----
  '설정': 'SETTINGS',
  '음악': 'Music',
  '효과음': 'SFX',
  '진동 (모바일)': 'Vibration (mobile)',
  '화질': 'Quality',
  '켜짐': 'On',
  '꺼짐': 'Off',
  '자동': 'Auto',
  '절전': 'Low',
  '닫기': 'Close',
  '계속하기': 'Resume',
  '재시작': 'Restart',
  '포기·정산': 'Give Up',
  '재도전': 'RETRY',
};

const T = s => (LANG === 'en' && I18N_EN[s]) || s;

function setLang(l) {
  LANG = l;
  try { localStorage.setItem('cs.lang', l); } catch (e) {}
}

/* 정적 HTML 텍스트 EN 적용 (KO가 기본 마크업) */
function applyStaticI18n() {
  if (!EN()) return;
  const set = (id, html) => { const el = document.getElementById(id); if (el) el.innerHTML = html; };
  set('btnStart', 'START DEFENSE');
  set('btnLab', '🔬 Laboratory <span class="c">— permanent upgrades</span>');
  set('btnSet', '⚙ Settings');
  set('btnRetry', 'RETRY');
  set('btnLabOver', '🔬 Grow stronger in the Lab');
  set('btnLabClose', 'Close');
  set('btnSetClose', 'Close');
  set('btnResume', 'Resume');
  set('btnRestartP', 'Restart');
  set('btnSetP', 'Settings');
  set('btnGiveUp', 'Give Up');
  set('newBest', '— NEW RECORD —');
  // 시작 화면 태그라인/스토리
  const tag = document.querySelector('#startScreen .tag');
  if (tag) tag.textContent = 'Bastion-7 Defense Operation';
  const stq = document.getElementById('lore');
  if (stq) stq.innerHTML = "Frontier outpost <b>Bastion-7</b> — the swarm beneath the crust has woken to the core's resonance.<br>Until the evac ship arrives, the core must hold.";
  // 난이도
  const dbs = document.querySelectorAll('#diffRow button');
  if (dbs[0]) dbs[0].textContent = 'NORMAL';
  if (dbs[1]) dbs[1].textContent = 'HARD';
  const bc = document.getElementById('btnCancel');
  if (bc) bc.textContent = '✕ Cancel';
  // 게임오버 라벨
  const lbls = document.querySelectorAll('#ovStats .lbl');
  const enL = ['Wave Reached', 'Kills', 'Survival Time', 'Final Score', 'Core Shards'];
  lbls.forEach((el, i) => { if (enL[i]) el.textContent = enL[i]; });
  set('ovTag', 'The defense line has collapsed');
  // 일시정지
  const pv = document.querySelector('#pauseVeil h1');
  if (pv) pv.textContent = 'PAUSED';
  const pvTag = document.querySelector('#pauseVeil .tag');
  if (pvTag) pvTag.innerHTML = 'Press <kbd>P</kbd> to resume';
  // 설정 라벨
  document.querySelectorAll('#setRows .setRow > span').forEach(el => { el.textContent = T(el.textContent); });
  const sh = document.querySelector('#setScreen h1');
  if (sh) sh.textContent = 'SETTINGS';
  const lh = document.querySelector('#labScreen h1');
  if (lh) lh.textContent = 'LABORATORY';
  const lt = document.querySelector('#labScreen .tag');
  if (lt) lt.innerHTML = 'Core shards — <b id="labShards" class="c">0</b>';
  // 조작 안내 (데스크톱/터치)
  const howto = document.getElementById('howto');
  if (howto) howto.innerHTML =
    '<div><kbd>1</kbd>~<kbd>7</kbd> Select turret / drone</div><div class="k">Left-click build · Right-click cancel</div>' +
    '<div><kbd>Q</kbd><kbd>W</kbd><kbd>E</kbd><kbd>T</kbd> Abilities</div><div class="k">Orbital · Stasis · Repair · Overcharge</div>' +
    '<div><kbd>Space</kbd> Call wave early</div><div class="k">Leftover time pays bonus ◆</div>' +
    '<div><kbd>U</kbd> Upgrade · <kbd>X</kbd> Sell</div><div class="k">Click a turret first</div>' +
    '<div><kbd>P</kbd> Pause · <kbd>M</kbd> Mute</div><div class="k">Boss every 5 waves</div>';
  const howtoT = document.getElementById('howtoTouch');
  if (howtoT) howtoT.innerHTML =
    '<div>Drag cards to the field</div><div class="k">Preview above finger · release to build</div>' +
    '<div>Tap a turret</div><div class="k">Upgrade / sell panel</div>' +
    '<div>Round buttons below</div><div class="k">Orbital (drag aim) · Stasis · Repair</div>' +
    '<div>[Call Now] button</div><div class="k">Leftover time pays bonus ◆</div>' +
    '<div>Every 5 waves</div><div class="k">Boss appears</div>';
}
