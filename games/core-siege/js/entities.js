'use strict';
/* ============================================================
   CORE SIEGE — entities.js
   적 · 터렛 · 드론 · 투사체 · 파티클 · 이펙트 (전부 프로시저럴)
   ============================================================ */

/* ---------- 레벨 배율 (밸런스 튜닝 포인트) ---------- */
const LVL = {
  dmg:   [1, 1.6, 2.5],
  rof:   [1, 1.15, 1.35],
  range: [1, 1.12, 1.25],
  hp:    [1, 1.5, 2.1],
};
const turretRange = t => t.def.range * LVL.range[t.lvl - 1];
const turretDmg   = t => (t.def.dmg || t.def.dps || 0) * LVL.dmg[t.lvl - 1] * (G.labDmg || 1) * (G.overT > 0 ? 1.3 : 1); // 과충전 +30%
const upgradeCost = t => Math.round(t.def.cost * (t.lvl === 1 ? 1.0 : 1.9));
const sellValue   = t => Math.round(t.invested * 0.6);

/* ---------- 적 정의 ---------- */
const ENEMIES = {
  rusher: {
    name: '러셔', hp: 26, spd: 95, r: 9, dmg: 8, atkRate: 0.75, range: 0,
    bounty: 6, aggro: 110, color: '#ff5347', blood: '#4a1410', draw: drawRusher,
  },
  spitter: {
    name: '스피터', hp: 60, spd: 62, r: 11, dmg: 9, atkRate: 2.0, range: 150,
    bounty: 11, aggro: 175, color: '#a3e635', blood: '#2c3a0c', draw: drawSpitter,
  },
  brute: {
    name: '브루트', hp: 250, spd: 43, r: 17, dmg: 30, atkRate: 1.2, range: 0,
    bounty: 26, aggro: 220, color: '#ff7a45', blood: '#521c12', draw: drawBrute,
  },
  swarm: {
    name: '스웜링', hp: 9, spd: 125, r: 5.5, dmg: 4, atkRate: 0.6, range: 0,
    bounty: 2, aggro: 80, color: '#ff8a3d', blood: '#47160e', draw: drawSwarm,
  },
  blinker: {
    name: '블링커', hp: 64, spd: 72, r: 10, dmg: 13, atkRate: 0.8, range: 0,
    bounty: 15, aggro: 90, color: '#c084fc', blood: '#2a1544', draw: drawBlinker,
  },
  carrier: {
    name: '산란체', hp: 150, spd: 40, r: 14, dmg: 12, atkRate: 1.4, range: 0,
    bounty: 18, aggro: 120, color: '#ffb347', blood: '#5a3a14', draw: drawCarrier,
  },
  mender: {
    name: '재생체', hp: 100, spd: 52, r: 11, dmg: 6, atkRate: 1.5, range: 0,
    bounty: 20, aggro: 90, color: '#ffc654', blood: '#5a4210', draw: drawMender, heal: true,
  },
  egg: { // 군체의 어머니가 낳는 알집 — 부화 전 파괴가 카운터플레이
    name: '알집', hp: 55, spd: 0, r: 8, dmg: 0, atkRate: 9, range: 0,
    bounty: 5, aggro: 0, color: '#ffb347', blood: '#5a3a14', draw: drawEgg,
  },
  boss: {
    name: '베헤모스', hp: 1800, spd: 27, r: 34, dmg: 70, atkRate: 1.6, range: 0,
    bounty: 260, aggro: 170, color: '#ff3355', blood: '#4a0e14', draw: drawBoss,
  },
};

function makeEnemy(type, x, y, m, elite) {
  const d = ENEMIES[type];
  const e = {
    type, def: d, x, y,
    hp: d.hp * m.hp, maxhp: d.hp * m.hp,
    spd: d.spd * m.spd * rand(0.9, 1.1),
    r: d.r, dmg: d.dmg * (1 + (m.hp - 1) * 0.3),
    atkRate: d.atkRate, rangeAtk: d.range || 0,
    bounty: Math.round(d.bounty * m.bounty * (G.labBounty || 1)),
    aggro: d.aggro,
    face: angleTo(x, y, 0, 0), ph: rand(TAU), seed: rand(1000), wob: rand(-1, 1),
    target: null, retargetT: rand(0.4), atkT: rand(0.2, 0.7),
    slowT: 0, slowPct: 0, hitT: 0, dmgAcc: 0, dmgAccT: 0, lunge: 0,
    spawnT: 0.45, dead: false,
  };
  if (type === 'blinker') e.blinkCd = rand(1.2, 2);
  if (type === 'boss') { e.boss = true; e.summonT = 4; }
  if (elite) {
    e.elite = true;
    e.hp = e.maxhp = e.hp * 2.6;
    e.bounty = Math.round(e.bounty * 3);
    e.r = Math.round(d.r * 1.25);
    e.spd *= 0.9;
    e.dmg *= 1.5;
  }
  return e;
}

function applySlow(e, pct, dur) {
  if (pct >= e.slowPct || e.slowT <= 0) e.slowPct = pct;
  e.slowT = Math.max(e.slowT, dur);
}

function pickEnemyTarget(e) {
  let best = null, bd = e.aggro * e.aggro;
  const st = G.turrets, dr = G.drones, tp = G.troops;
  for (let i = 0; i < st.length; i++) {
    const d = dist2(e.x, e.y, st[i].x, st[i].y);
    if (d < bd) { bd = d; best = st[i]; }
  }
  for (let i = 0; i < dr.length; i++) {
    const d = dist2(e.x, e.y, dr[i].x, dr[i].y);
    if (d < bd) { bd = d; best = dr[i]; }
  }
  for (let i = 0; i < tp.length; i++) {
    const d = dist2(e.x, e.y, tp[i].x, tp[i].y);
    if (d < bd) { bd = d; best = tp[i]; }
  }
  return best || G.core;
}

function updateEnemy(e, dt) {
  // 스폰 연출 중 (크립에서 솟아나는 동안 정지)
  if (e.spawnT > 0) {
    e.spawnT -= dt;
    e.ph += dt * 5;
    return;
  }
  // 알집: 부화 카운트다운 (파괴되면 부화 안 함)
  if (e.hatchT !== undefined) {
    e.hatchT -= dt;
    e.ph += dt * 6;
    e.hitT = Math.max(0, e.hitT - dt);
    if (e.hatchT <= 0) {
      e.dead = true; // 보상 없이 소멸 → 유충 부화
      for (let i = 0; i < 3; i++) {
        const s = makeEnemy('swarm', e.x + rand(-8, 8), e.y + rand(-8, 8), G.curMults);
        s.spawnT = 0.3;
        G.enemies.push(s);
      }
      splat(e.x, e.y, '#5a3a14', 10);
      addRing(e.x, e.y, 6, 36, '#ffb347', 2, 0.4);
      Sound.tone({ type: 'triangle', f: 620, f2: 180, dur: 0.18, v: 0.08 });
    }
    return;
  }
  let f = 1;
  if (e.slowT > 0) { e.slowT -= dt; f *= (1 - Math.min(0.85, e.slowPct)); }
  if (G.stasisT > 0) f *= 0.25;
  const edt = dt * f;

  e.ph += edt * e.spd * 0.045;
  e.hitT = Math.max(0, e.hitT - dt);
  e.lunge = Math.max(0, e.lunge - dt * 3.5);

  if (e.dmgAcc > 0) {
    e.dmgAccT -= dt;
    if (e.dmgAccT <= 0) {
      addFloater(e.x, e.y - e.r - 8, Math.max(1, Math.round(e.dmgAcc)), '#eaf7ff');
      e.dmgAcc = 0;
    }
  }

  e.retargetT -= dt;
  if (!e.target || e.target.dead || e.retargetT <= 0) {
    e.target = pickEnemyTarget(e);
    e.retargetT = 0.5 + rand(0.4);
  }
  const tg = e.target;
  const d = dist(e.x, e.y, tg.x, tg.y);
  const stopAt = (tg.r || 40) + e.r + (e.rangeAtk ? e.rangeAtk : -2);

  // 네임드 보스 고유 기믹 — true 반환 시 이동/공격을 기믹이 제어
  if (e.boss && e.mech && updateBossMech(e, dt, edt, tg, d)) return;

  if (e.blinkCd !== undefined) {
    e.blinkCd -= edt;
    if (e.blinkCd <= 0 && d > stopAt + 120) doBlink(e, tg);
  }
  if (e.summonT !== undefined) {
    e.summonT -= dt;
    if (e.summonT <= 0) { bossSummon(e); e.summonT = 5.5; }
  }
  // 재생체: 주변 아군(군체) 치유 파동
  if (e.def.heal) {
    e.healT = (e.healT || rand(0.5)) - edt;
    if (e.healT <= 0) {
      e.healT = 1.2;
      let healed = false;
      for (const o of G.enemies) {
        if (o.dead || o === e || o.hp >= o.maxhp) continue;
        if (dist2(e.x, e.y, o.x, o.y) < 120 * 120) {
          o.hp = Math.min(o.maxhp, o.hp + o.maxhp * 0.04);
          healed = true;
        }
      }
      if (healed) addRing(e.x, e.y, 8, 64, '#ffc654', 1.5, 0.5);
    }
  }

  let desired = angleTo(e.x, e.y, tg.x, tg.y);
  desired += Math.sin(G.time * 1.4 + e.seed) * 0.14 * e.wob;
  e.face = lerpAngle(e.face, desired, Math.min(1, dt * 7));

  if (d > stopAt) {
    e.x += Math.cos(e.face) * e.spd * edt;
    e.y += Math.sin(e.face) * e.spd * edt;
  } else {
    e.atkT -= edt;
    if (e.atkT <= 0) { enemyAttack(e, tg); e.atkT = e.atkRate; }
  }
}

function enemyAttack(e, tg) {
  if (e.rangeAtk > 0) {
    const a = angleTo(e.x, e.y, tg.x, tg.y);
    G.projs.push({
      kind: 'spit', x: e.x + Math.cos(a) * e.r, y: e.y + Math.sin(a) * e.r,
      vx: Math.cos(a) * 180, vy: Math.sin(a) * 180,
      dmg: e.dmg, target: tg, life: 3, r: 4, color: '#a3e635', dead: false,
    });
    Sfx.shoot('spit');
    return;
  }
  e.lunge = 1;
  const a = angleTo(e.x, e.y, tg.x, tg.y);
  sparkBurst(tg.x - Math.cos(a) * (tg.r || 40) * 0.8, tg.y - Math.sin(a) * (tg.r || 40) * 0.8, e.def.color, 4, 90);
  if (tg.isCore) damageCore(e.dmg, angleTo(0, 0, e.x, e.y));
  else damageStructure(tg, e.dmg);
}

function doBlink(e, tg) {
  blinkFx(e.x, e.y);
  const voidMap = G.map && G.map.id === 'void'; // 공허 균열: 점멸 강화
  const a = angleTo(e.x, e.y, tg.x, tg.y);
  const step = Math.min(voidMap ? 145 : 100, dist(e.x, e.y, tg.x, tg.y) - (tg.r || 40) - e.r);
  e.x += Math.cos(a) * step;
  e.y += Math.sin(a) * step;
  blinkFx(e.x, e.y);
  e.blinkCd = (voidMap ? 1.9 : 2.4) + rand(0.8);
  Sound.tone({ type: 'sine', f: 950, f2: 210, dur: 0.14, v: 0.05 });
}
function blinkFx(x, y) {
  for (let i = 0; i < 6; i++) {
    const a = rand(TAU);
    addPart({ x: x + Math.cos(a) * 8, y: y + Math.sin(a) * 8, vx: Math.cos(a) * 60, vy: Math.sin(a) * 60, dur: 0.3, size: 2, color: '#c084fc', add: true, shape: 'dot' });
  }
}

/* ---------- 네임드 보스 고유 기믹 ----------
   charge(파괴자 알파)=예고 후 돌진 충격파 / submerge(심연)=잠수 후 근접 부상 분출
   shield(공명)=체력 구간별 수정 실드(피격 무효) / spawn(군체)=후방 알집 산란 */
function updateBossMech(e, dt, edt, tg, d) {
  e.mechT -= edt;
  const dc = dist(e.x, e.y, 0, 0); // 기믹 트리거는 코어 기준 거리 (타겟이 터렛이어도 발동)
  switch (e.mech) {
    case 'charge': {
      if (e.mechPhase === 'windup') {
        e.mechP -= dt;
        e.face = lerpAngle(e.face, angleTo(e.x, e.y, e.cx, e.cy), Math.min(1, dt * 6));
        if (e.mechP <= 0) {
          e.mechPhase = 'dash';
          e.mechP = 1.15;
          e.chargeHit = new Set();
          Sound.noise({ f: 1400, f2: 200, dur: 0.4, v: 0.2 });
        }
        return true; // 웅크림 (정지)
      }
      if (e.mechPhase === 'dash') {
        e.mechP -= dt;
        const sp = e.spd * 4.4;
        e.x += Math.cos(e.face) * sp * edt;
        e.y += Math.sin(e.face) * sp * edt;
        // 경로상 구조물/병력 충돌 (대상당 1회) — 첫 보스(W5)는 완화
        const fk = G.wave <= 5 ? 0.6 : 1;
        for (const t of [...G.turrets, ...G.troops, ...G.drones]) {
          if (t.dead || e.chargeHit.has(t)) continue;
          if (dist2(e.x, e.y, t.x, t.y) < (e.r + (t.r || 18)) * (e.r + (t.r || 18))) {
            e.chargeHit.add(t);
            damageStructure(t, Math.round(65 * fk));
            sparkBurst(t.x, t.y, '#ff9a3d', 6, 150);
            addShake(4);
          }
        }
        const dcNow = dist(e.x, e.y, 0, 0);
        const out = dcNow > Math.min(G.lw, G.lh) / 2 - 40; // 플랫폼 밖 이탈 방지
        if (dcNow < 45 + e.r) { // 코어 직격
          damageCore(Math.round(45 * fk), angleTo(0, 0, e.x, e.y));
          boom(e.x, e.y, 70, '#ff9a3d', 1.4);
          e.mechPhase = 'idle';
          return true;
        }
        if (e.mechP <= 0 || out) {
          boom(e.x, e.y, 55, '#ff9a3d', 1.0);
          e.mechPhase = 'idle';
        }
        return true;
      }
      if (e.mechT <= 0 && dc > 140) {
        e.mechT = 13 + rand(3);
        e.mechPhase = 'windup';
        e.mechP = 1.0;
        e.cx = tg.x; e.cy = tg.y;
        addRing(e.x, e.y, e.r, e.r + 44, '#ff9a3d', 3, 1.0);
        addFloater(e.x, e.y - e.r - 16, '돌진!', '#ff9a3d');
        Sound.tone({ type: 'sawtooth', f: 60, f2: 180, dur: 0.9, v: 0.14, lp: 600 });
      }
      return false;
    }
    case 'submerge': {
      if (e.mechPhase === 'sub') {
        e.mechP -= dt;
        const a = angleTo(e.x, e.y, 0, 0);
        e.face = a;
        if (dist(e.x, e.y, 0, 0) > 95) {
          e.x += Math.cos(a) * e.spd * 2.8 * edt;
          e.y += Math.sin(a) * e.spd * 2.8 * edt;
        }
        if (!e.mechWarned && e.mechP < 0.85) { // 부상 예고
          e.mechWarned = true;
          addRing(e.x, e.y, 14, 96, '#4d7dff', 3, 0.85);
        }
        if (e.mechP <= 0) { // 부상 분출
          e.mechPhase = 'idle';
          e.untargetable = false;
          boom(e.x, e.y, 75, '#4d7dff', 1.3);
          for (const t of [...G.turrets, ...G.troops, ...G.drones]) {
            if (!t.dead && dist2(e.x, e.y, t.x, t.y) < 100 * 100) damageStructure(t, 55);
          }
          if (dist2(e.x, e.y, 0, 0) < 120 * 120) damageCore(30, angleTo(0, 0, e.x, e.y));
        }
        return true;
      }
      if (e.mechT <= 0 && dc > 170) {
        e.mechT = 11 + rand(2);
        e.mechPhase = 'sub';
        e.mechP = 2.3;
        e.mechWarned = false;
        e.untargetable = true;
        e.target = null;
        addRing(e.x, e.y, e.r, e.r + 50, '#4d7dff', 2.5, 0.6);
        for (let i = 0; i < 10; i++) {
          const a = rand(TAU);
          addPart({ x: e.x + Math.cos(a) * e.r, y: e.y + Math.sin(a) * e.r, vx: Math.cos(a) * 90, vy: Math.sin(a) * 90, dur: 0.5, size: 3, color: '#4d7dff', add: true, shape: 'dot' });
        }
        Sound.noise({ f: 600, f2: 80, dur: 0.6, v: 0.16 });
      }
      return false;
    }
    case 'shield': {
      if (e.shieldT > 0) {
        e.shieldT -= dt;
        if (e.shieldT <= 0 || e.shieldHits <= 0) {
          e.shieldT = 0; e.shieldHits = 0;
          if (e.spdBoosted) { e.spd /= 1.25; e.spdBoosted = false; }
          addRing(e.x, e.y, e.r, e.r + 40, '#c084fc', 2.5, 0.5);
          Sound.tone({ type: 'sine', f: 1400, f2: 300, dur: 0.3, v: 0.1 });
        }
      }
      return false;
    }
    case 'spawn': {
      if (e.mechT <= 0) {
        e.mechT = 8;
        if (G.enemies.length < 110) {
          for (let i = 0; i < 3; i++) {
            const a = e.face + Math.PI + rand(-0.8, 0.8); // 후방 산란
            const egg = makeEnemy('egg', e.x + Math.cos(a) * (e.r + 14), e.y + Math.sin(a) * (e.r + 14), G.curMults);
            egg.hatchT = 3.5;
            egg.spawnT = 0.25;
            G.enemies.push(egg);
          }
          addRing(e.x, e.y, e.r * 0.5, e.r + 34, '#ffb347', 2, 0.55);
          addFloater(e.x, e.y - e.r - 16, '산란!', '#ffb347');
          Sound.tone({ type: 'triangle', f: 280, f2: 80, dur: 0.4, v: 0.12 });
        }
      }
      return false;
    }
  }
  return false;
}

function bossSummon(b) {
  if (G.enemies.length > 120) return;
  for (let i = 0; i < 4; i++) {
    const a = rand(TAU);
    const e = makeEnemy('swarm', b.x + Math.cos(a) * (b.r + 14), b.y + Math.sin(a) * (b.r + 14), G.curMults);
    G.enemies.push(e);
  }
  addRing(b.x, b.y, b.r, b.r + 46, '#ff3355', 2, 0.5);
  Sound.tone({ type: 'sawtooth', f: 120, f2: 60, dur: 0.4, v: 0.1, lp: 500 });
}

/* ---------- 데미지 처리 ---------- */
function damageEnemy(e, dmg) {
  if (e.dead) return;
  // 공명 포식자: 수정 실드 — 피격 횟수 소모로 무효화
  if (e.shieldHits > 0) {
    e.shieldHits--;
    e.hitT = 0.05;
    sparkBurst(e.x + rand(-e.r, e.r) * 0.5, e.y + rand(-e.r, e.r) * 0.5, '#c084fc', 3, 110);
    return;
  }
  e.hp -= dmg;
  e.hitT = 0.09;
  e.dmgAcc += dmg;
  if (e.dmgAccT <= 0) e.dmgAccT = 0.24;
  // 실드 발동 체크 (체력 75/50/25% 최초 진입 시)
  if (e.shieldStages && e.hp > 0) {
    const k = e.hp / e.maxhp;
    if (e.shieldStages.length && k <= e.shieldStages[0]) {
      e.shieldStages.shift();
      e.shieldHits = 14;
      e.shieldT = 6;
      if (!e.spdBoosted) { e.spd *= 1.25; e.spdBoosted = true; }
      addRing(e.x, e.y, e.r, e.r + 52, '#c084fc', 3.5, 0.8);
      addFloater(e.x, e.y - e.r - 16, '수정 실드!', '#c084fc');
      Sound.tone({ type: 'sine', f: 500, f2: 1500, dur: 0.4, v: 0.12 });
    }
  }
  if (e.hp <= 0) killEnemy(e);
}

// 사체 스프라이트 (어둡게 눌린 톤) — 전장에 잔존
const _corpses = new Map();
function corpseSprite(type) {
  let c = _corpses.get(type);
  if (c) return c;
  const sp = enemySprite(type);
  c = document.createElement('canvas');
  c.width = sp.width; c.height = sp.height;
  const g = c.getContext('2d');
  g.drawImage(sp, 0, 0);
  g.globalCompositeOperation = 'source-atop';
  g.fillStyle = 'rgba(10,6,10,0.66)';
  g.fillRect(0, 0, c.width, c.height);
  _corpses.set(type, c);
  return c;
}

function stampCorpse(e) {
  if (!G.dctx || e.boss) return;
  const g = G.dctx;
  const vs = G.vs || 1;
  const sp = corpseSprite(e.type);
  const s = sp.width / SS * (e.elite ? e.r / e.def.r : 1) * vs;
  g.save();
  g.translate(e.x * vs + G.vw / 2, e.y * vs + G.vh / 2);
  g.rotate(e.face + rand(-0.4, 0.4));
  g.globalAlpha = 0.5;
  g.drawImage(sp, -s / 2, -s / 2, s, s);
  g.restore();
}

function killEnemy(e) {
  if (e.dead) return;
  e.dead = true;
  G.kills++;
  G.waveKills++;
  G.combo++;
  G.comboT = 1.3;
  G.score += Math.round(e.bounty * 2 * (G.scoreMul || 1));
  spawnCrystals(e.x, e.y, e.bounty);
  stampCorpse(e);
  splat(e.x, e.y, e.def.blood, e.r);
  sparkBurst(e.x, e.y, e.def.color, Math.min(12, 3 + e.r * 0.7), 120 + e.r * 5);
  // 사체 파편
  const chunks = clamp(Math.round(e.r * 0.5), 2, 8);
  for (let i = 0; i < chunks; i++) {
    const a = rand(TAU), s = rand(60, 160);
    addPart({
      x: e.x, y: e.y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 40,
      dur: rand(0.4, 0.75), size: rand(1.6, 1.6 + e.r * 0.14),
      color: pick([e.def.blood, PAL.zerg.flesh, e.def.color]),
      shape: 'chunk', grav: 300, drag: 1.4,
    });
  }
  for (let i = 0; i < 3; i++) {
    addPart({ x: e.x, y: e.y, vx: rand(-40, 40), vy: rand(-40, 40), dur: rand(0.5, 0.9), size: e.r * 0.5, color: '#141b26', shape: 'smoke' });
  }
  Sfx.enemyDie();
  // 산란체: 격파 시 유충 분열
  if (e.type === 'carrier' && !e.ambient) {
    const n = e.elite ? 8 : 5;
    for (let i = 0; i < n; i++) {
      const a = rand(TAU);
      const s = makeEnemy('swarm', e.x + Math.cos(a) * 10, e.y + Math.sin(a) * 10, G.curMults);
      s.spawnT = 0.25;
      G.enemies.push(s);
    }
    addRing(e.x, e.y, 8, 44, '#ffb347', 2, 0.4);
    Sound.tone({ type: 'triangle', f: 500, f2: 160, dur: 0.2, v: 0.1 });
  }
  // 군체의 어머니: 최후의 산란 폭발
  if (e.boss && e.mech === 'spawn') {
    for (let i = 0; i < 8; i++) {
      const a = rand(TAU);
      const s = makeEnemy('swarm', e.x + Math.cos(a) * 14, e.y + Math.sin(a) * 14, G.curMults);
      s.spawnT = 0.3 + i * 0.05;
      G.enemies.push(s);
    }
    addRing(e.x, e.y, 10, 80, '#ffb347', 3, 0.7);
  }
  if (e.boss) bossDeath(e);
  else if (e.elite) { boom(e.x, e.y, e.r * 1.5, '#ffc654', 0.9); }
  else if (e.r >= 15) { boom(e.x, e.y, e.r * 1.3, '#ff9a5c', 0.6); }
}

// 혈흔 데칼 (사체 잔존 흔적)
function splat(x, y, color, r) {
  if (!G.dctx) return;
  const g = G.dctx;
  const vs = G.vs || 1;
  r *= vs;
  const cx = x * vs + G.vw / 2, cy = y * vs + G.vh / 2;
  g.globalAlpha = 0.42;
  g.fillStyle = color;
  g.beginPath(); g.arc(cx, cy, r * 0.75, 0, TAU); g.fill();
  g.globalAlpha = 0.34;
  for (let i = 0; i < 6; i++) {
    const a = rand(TAU), d = rand(r * 0.4, r * 1.5);
    g.beginPath();
    g.arc(cx + Math.cos(a) * d, cy + Math.sin(a) * d, rand(1.2, r * 0.35), 0, TAU);
    g.fill();
  }
  g.globalAlpha = 1;
}

function bossDeath(e) {
  G.boss = null;
  G.slowmoT = 1.0;
  const bx = e.x, by = e.y;
  for (let i = 0; i < 7; i++) {
    G.timers.push({
      t: i * 0.14, fn: () => {
        boom(bx + rand(-30, 30), by + rand(-30, 30), rand(22, 40), '#ff3355', 1.2);
      }
    });
  }
  G.timers.push({
    t: 1.05, fn: () => {
      boom(bx, by, 90, '#ffffff', 2);
      addRing(bx, by, 10, 260, '#ff8899', 5, 0.9);
      addShake(18);
      showBanner('보스 격파', 'danger', '+' + fmt(e.bounty * 2) + '◆ 획득');
    }
  });
  scorch(bx, by, 60);
}

function damageStructure(t, dmg) {
  if (t.dead) return;
  // 매딕 보호막: 피해 흡수 (병력 전용)
  if (t.shield > 0) {
    const ab = Math.min(t.shield, dmg);
    t.shield -= ab;
    dmg -= ab;
    sparkBurst(t.x, t.y, '#8fffc9', 2, 80);
    if (dmg <= 0) { t.lastHitT = 0; return; }
  }
  t.hp -= dmg;
  t.flashT = 0.12;
  if (t.hp <= 0) {
    t.dead = true;
    boom(t.x, t.y, 26, '#4ce0ff', 1);
    scorch(t.x, t.y, 22);
    Sfx.turretDown();
    if (G.sel === t) G.sel = null;
  }
}

function damageCore(dmg, ang) {
  // 초반 학습 유예 — 누수 소수가 코어를 순삭하는 스파이럴 방지 (W1~3 40%, W4~5 20% 경감)
  if (G.wave <= 3) dmg *= 0.6;
  else if (G.wave <= 5) dmg *= 0.8;
  const c = G.core;
  c.lastHit = 0;
  if (c.sh > 0) {
    c.sh -= dmg;
    c.shFlashT = 0.3;
    c.shFlashA = ang;
    Sfx.shieldHit();
    if (c.sh < 0) { c.hp += c.sh; c.sh = 0; }
  } else {
    c.hp -= dmg;
    c.hitFlash = 0.35;
    Sfx.coreHit();
    addShake(4);
    addPunch(0.3);
    vib(45);
    sparkBurst(Math.cos(ang) * c.r, Math.sin(ang) * c.r, '#ff8866', 6, 150);
  }
  if (c.hp <= 0 && (G.state === 'WAVE' || G.state === 'BUILD')) {
    c.hp = 0;
    startGameOver();
  }
}

/* ---------- 터렛 정의 ---------- */
const TURRETS = {
  pulse: {
    name: '펄스 터렛', cost: 90, hp: 200, range: 175, rof: 3.2, dmg: 11, projSpd: 470,
    color: '#4ce0ff', desc: '빠른 연사 기본 포탑. 초반 방어의 핵심.',
  },
  tesla: {
    name: '테슬라 코일', cost: 220, hp: 200, range: 150, rof: 1.25, dmg: 22, chain: 4,
    color: '#9beeff', desc: '최대 4체 체인 번개. 군체 러시 제압에 특화.',
  },
  laser: {
    name: '집속 레이저', cost: 240, hp: 200, range: 215, dps: 30,
    color: '#7ce8ff', desc: '단일 대상 지속 광선. 같은 대상 조준 시 최대 2.2배 과열 피해.',
  },
  missile: {
    name: '미사일 포대', cost: 300, hp: 220, range: 290, rof: 0.75, dmg: 60, splash: 62,
    color: '#bfe9ff', desc: '유도 미사일. 착탄 지점 범위 폭발 피해.',
  },
  rail: {
    name: '레일건', cost: 420, hp: 260, range: 360, rof: 0.5, dmg: 170, charge: 0.9,
    color: '#eaf7ff', desc: '충전 후 직선 관통 저격. 브루트·보스 특화.',
  },
  cryo: {
    name: '빙결장', cost: 160, hp: 220, range: 135, slow: 0.45,
    color: '#9beeff', desc: '범위 내 모든 적 감속. 공격 능력 없음.',
  },
};

function makeTurret(type, x, y) {
  const def = TURRETS[type];
  return {
    isTurret: true, type, def, x, y, lvl: 1,
    hp: def.hp, maxhp: def.hp, r: 14,
    rot: angleTo(0, 0, x, y), cd: 0, target: null,
    heat: 0, lastTarget: null, chargeT: 0, charging: false, sprkT: 0,
    flashT: 0, fireT: 0, recoilT: 0, buildT: 0.35, beamOn: false,
    invested: def.cost, dead: false,
  };
}

function acquireTarget(t, range) {
  let best = null, bd = range * range;
  const es = G.enemies;
  for (let i = 0; i < es.length; i++) {
    const e = es[i];
    if (e.dead || e.untargetable) continue;
    const d = dist2(t.x, t.y, e.x, e.y);
    if (d < bd) { bd = d; best = e; }
  }
  return best;
}

function updateTurret(t, dt) {
  t.flashT = Math.max(0, t.flashT - dt);
  t.fireT = Math.max(0, t.fireT - dt);
  t.recoilT = Math.max(0, t.recoilT - dt);
  t.buildT = Math.max(0, t.buildT - dt);
  if (t.hp < t.maxhp) t.hp = Math.min(t.maxhp, t.hp + (G.state === 'BUILD' ? 9 : 2.5) * dt);

  const range = turretRange(t);
  t.cd -= dt;

  if (t.type === 'cryo') {
    if (t.cd <= 0) {
      t.cd = 0.25;
      const slow = t.def.slow + 0.12 * (t.lvl - 1);
      const es = G.enemies;
      for (let i = 0; i < es.length; i++) {
        if (!es[i].dead && dist2(t.x, t.y, es[i].x, es[i].y) < range * range) applySlow(es[i], slow, 0.42);
      }
      if (Math.random() < 0.5) {
        const a = rand(TAU), rr = rand(range * 0.3, range * 0.95);
        addPart({ x: t.x + Math.cos(a) * rr, y: t.y + Math.sin(a) * rr, vx: 0, vy: -12, dur: 1.1, size: 1.6, color: '#9beeff', add: true, shape: 'snow' });
      }
    }
    return;
  }

  if (!t.target || t.target.dead || t.target.untargetable || dist2(t.x, t.y, t.target.x, t.target.y) > range * range) {
    t.target = acquireTarget(t, range);
  }
  const tg = t.target;

  if (tg) t.rot = lerpAngle(t.rot, angleTo(t.x, t.y, tg.x, tg.y), Math.min(1, dt * 9));
  else t.rot += dt * 0.35;

  t.beamOn = false;

  switch (t.type) {
    case 'pulse': {
      if (tg && t.cd <= 0 && aimedAt(t, tg, 0.35)) {
        const a = t.rot;
        const spd = t.def.projSpd;
        G.projs.push({
          kind: 'bolt', x: t.x + Math.cos(a) * 16, y: t.y + Math.sin(a) * 16,
          vx: Math.cos(a) * spd, vy: Math.sin(a) * spd,
          dmg: turretDmg(t), r: 3, life: 1.1, color: t.def.color, dead: false,
        });
        t.cd = (G.mapCdMul || 1) / (t.def.rof * LVL.rof[t.lvl - 1]);
        t.fireT = 0.07;
        Sfx.shoot('pulse');
      }
      break;
    }
    case 'tesla': {
      if (tg && t.cd <= 0) {
        teslaChain(t, tg);
        t.cd = (G.mapCdMul || 1) / (t.def.rof * LVL.rof[t.lvl - 1]);
        t.fireT = 0.12;
      }
      break;
    }
    case 'laser': {
      if (tg) {
        if (t.lastTarget !== tg) { t.heat = 0; t.lastTarget = tg; }
        t.heat = Math.min(2.2, t.heat + dt);
        const ramp = 1 + (t.heat / 2.2) * 1.2;
        damageEnemy(tg, turretDmg(t) * ramp * dt);
        t.beamOn = true;
        t.sprkT -= dt;
        if (t.sprkT <= 0) {
          t.sprkT = 0.06;
          sparkBurst(tg.x, tg.y, '#7ce8ff', 2, 90);
        }
        Sfx.laserTick();
      } else {
        t.heat = Math.max(0, t.heat - dt * 2);
      }
      break;
    }
    case 'missile': {
      if (tg && t.cd <= 0) {
        const a = t.rot;
        G.projs.push({
          kind: 'missile', x: t.x + Math.cos(a) * 10, y: t.y + Math.sin(a) * 10,
          vx: Math.cos(a) * 70, vy: Math.sin(a) * 70,
          dmg: turretDmg(t), splash: t.def.splash + t.lvl * 5,
          target: tg, life: 4, spd: 340, turn: 4.2, r: 4,
          color: t.def.color, smokeT: 0, dead: false,
        });
        t.cd = (G.mapCdMul || 1) / (t.def.rof * LVL.rof[t.lvl - 1]);
        t.fireT = 0.15;
        Sfx.shoot('missile');
      }
      break;
    }
    case 'rail': {
      if (t.cd <= 0 && tg) {
        if (!t.charging) { t.charging = true; t.chargeT = 0; Sfx.railCharge(); }
        t.chargeT += dt;
        if (t.chargeT >= t.def.charge) {
          fireRail(t);
          t.charging = false;
          t.chargeT = 0;
          t.cd = (G.mapCdMul || 1) / (t.def.rof * LVL.rof[t.lvl - 1]);
        }
      } else if (!tg) {
        t.charging = false;
        t.chargeT = Math.max(0, t.chargeT - dt * 2);
      }
      break;
    }
  }
}

function aimedAt(t, tg, tol) {
  let d = (angleTo(t.x, t.y, tg.x, tg.y) - t.rot) % TAU;
  if (d > Math.PI) d -= TAU;
  if (d < -Math.PI) d += TAU;
  return Math.abs(d) < tol;
}

function teslaChain(t, first) {
  const dmg0 = turretDmg(t);
  const chain = t.def.chain + (t.lvl - 1);
  const hit = [first];
  let last = { x: t.x, y: t.y };
  let d = dmg0;
  let cur = first;
  for (let i = 0; i < chain; i++) {
    addZap(last.x, last.y, cur.x, cur.y, '#9beeff');
    damageEnemy(cur, d);
    applySlow(cur, 0.9, 0.15);
    hit.push(cur);
    last = cur;
    d *= 0.72;
    let next = null, bd = 110 * 110;
    for (let j = 0; j < G.enemies.length; j++) {
      const e = G.enemies[j];
      if (e.dead || hit.includes(e)) continue;
      const dd = dist2(last.x, last.y, e.x, e.y);
      if (dd < bd) { bd = dd; next = e; }
    }
    if (!next) break;
    cur = next;
  }
  Sfx.shoot('tesla');
}

function fireRail(t) {
  const a = t.rot;
  const range = turretRange(t);
  const dx = Math.cos(a), dy = Math.sin(a);
  const x1 = t.x + dx * 18, y1 = t.y + dy * 18;
  const x2 = t.x + dx * range, y2 = t.y + dy * range;
  const dmg = turretDmg(t);
  const es = G.enemies;
  let hits = 0;
  for (let i = 0; i < es.length; i++) {
    const e = es[i];
    if (e.dead) continue;
    const px = e.x - x1, py = e.y - y1;
    const proj = px * dx + py * dy;
    if (proj < 0 || proj > range) continue;
    const perp = Math.abs(px * dy - py * dx);
    if (perp < 15 + e.r) {
      damageEnemy(e, dmg);
      sparkBurst(e.x, e.y, '#eaf7ff', 5, 160);
      hits++;
    }
  }
  if (hits > 0) G.hitstop = Math.max(G.hitstop || 0, 0.05); // 명중 순간 정지 (타격감)
  G.effects.push({ kind: 'line', x1, y1, x2, y2, color: '#eaf7ff', lw: 3.5, t: 0, dur: 0.28, layer: 'over' });
  addFlash(x1, y1, 26, '#eaf7ff');
  t.recoilT = 0.2;
  t.fireT = 0.15;
  addShake(3.5);
  Sfx.shoot('rail');
}

/* ---------- 기동 병력 (집결 지점 기반 자동 교전) ---------- */
const TROOPS = {
  marine: {
    name: '해병', cost: 80, supply: 1, hp: 95, dmg: 9, rof: 1.7, range: 130,
    spd: 100, r: 8, color: '#4ce0ff', desc: '원거리 보병. 집결 지점 주변을 방어.',
  },
  medic: {
    name: '전투 매딕', cost: 150, supply: 2, hp: 190, dmg: 0, rof: 0, range: 0,
    spd: 92, r: 9, color: '#8fffc9', heal: 16, shieldAmt: 35, shieldCd: 7,
    desc: '아군 병력을 치유하고 주기적으로 보호막을 부여. 공격 불가.',
  },
  sniper: {
    name: '저격수', cost: 160, supply: 1, hp: 70, dmg: 42, rof: 0.55, range: 265,
    spd: 88, r: 7.5, color: '#ffd9a0', desc: '초장거리 관통 저격. 강적 처치 특화.',
  },
  pyro: {
    name: '화염척탄병', cost: 180, supply: 2, hp: 210, dmg: 15, rof: 0.85, range: 150,
    spd: 84, r: 10, color: '#ff9a3d', splash: 52, desc: '소이 유탄 범위 폭격. 군집 소탕 특화.',
  },
};

function makeTroop(type) {
  const def = TROOPS[type];
  const a = rand(TAU);
  const thp = Math.round(def.hp * (G.labTroop || 1));
  return {
    isTroop: true, type, def,
    x: G.rally.x + Math.cos(a) * 20, y: G.rally.y + Math.sin(a) * 20,
    hp: thp, maxhp: thp, r: def.r,
    face: a, cd: 0, target: null, retargetT: 0,
    flashT: 0, lastHitT: 9, slot: rand(TAU), dead: false,
    shield: 0, shieldT: 0, shT: 2, healTgt: null, // 매딕 보호막/치유
  };
}

function troopSupply() {
  let s = 0;
  for (const u of G.troops) s += u.def.supply;
  return s;
}

function updateTroop(u, dt) {
  u.flashT = Math.max(0, u.flashT - dt);
  u.lastHitT += dt;
  u.cd -= dt;
  // 보호막 지속시간 감쇠
  if (u.shieldT > 0) {
    u.shieldT -= dt;
    if (u.shieldT <= 0) u.shield = 0;
  }
  // 전투 이탈 시 자가 재생
  if (u.lastHitT > 3 && u.hp < u.maxhp) u.hp = Math.min(u.maxhp, u.hp + 3 * dt);
  // 전투 매딕: 부상 아군 치유 + 주기적 보호막 (공격 안 함)
  if (u.def.heal) { updateMedic(u, dt); return; }

  // 타겟: 집결 지점 200 이내 또는 자신 130 이내의 적
  u.retargetT -= dt;
  if (!u.target || u.target.dead || u.retargetT <= 0) {
    u.retargetT = 0.4;
    let best = null, bd = Infinity;
    for (const e of G.enemies) {
      if (e.dead || e.spawnT > 0 || e.untargetable) continue;
      const dr = dist2(G.rally.x, G.rally.y, e.x, e.y);
      const ds = dist2(u.x, u.y, e.x, e.y);
      if (dr > 210 * 210 && ds > 130 * 130) continue;
      if (ds < bd) { bd = ds; best = e; }
    }
    u.target = best;
  }

  const tg = u.target;
  let destX, destY;
  if (tg) {
    const gap = u.def.range > 0 ? u.def.range * 0.85 : tg.r + u.r - 1;
    const d = dist(u.x, u.y, tg.x, tg.y);
    u.face = lerpAngle(u.face, angleTo(u.x, u.y, tg.x, tg.y), Math.min(1, dt * 10));
    if (d > gap) {
      destX = tg.x; destY = tg.y;
    } else {
      // 사거리 내 — 사격/타격
      if (u.cd <= 0) {
        u.cd = 1 / u.def.rof;
        const tk = (G.labDmg || 1) * (G.labTroop || 1);
        if (u.def.range > 0) {
          const a = u.face;
          if (u.type === 'pyro') {
            // 소이 유탄 — 착탄/도달 시 범위 폭발
            const d0 = dist(u.x, u.y, tg.x, tg.y);
            G.projs.push({
              kind: 'nade', x: u.x + Math.cos(a) * 8, y: u.y + Math.sin(a) * 8,
              vx: Math.cos(a) * 240, vy: Math.sin(a) * 240,
              dmg: u.def.dmg * tk, splash: u.def.splash,
              life: Math.max(0.22, d0 / 240), r: 3, color: '#ff9a3d', dead: false,
            });
            Sfx.shoot('spit');
          } else {
            const sn = u.type === 'sniper';
            G.projs.push({
              kind: 'bolt', x: u.x + Math.cos(a) * 8, y: u.y + Math.sin(a) * 8,
              vx: Math.cos(a) * (sn ? 840 : 480), vy: Math.sin(a) * (sn ? 840 : 480),
              dmg: u.def.dmg * tk, r: sn ? 2.8 : 2.4, life: sn ? 0.42 : 0.5,
              color: sn ? '#ffd9a0' : '#7ce8ff', dead: false,
            });
            if (sn) Sound.noise({ ft: 'highpass', f: 3800, dur: 0.05, v: 0.12 });
            Sfx.shoot('drone');
          }
          u.flashT = 0.09;
        } else {
          damageEnemy(tg, u.def.dmg * tk);
          sparkBurst(tg.x, tg.y, '#9beeff', 3, 90);
          u.flashT = 0.14;
        }
      }
      destX = u.x; destY = u.y;
    }
  } else {
    // 집결 대형 (링 포메이션)
    destX = G.rally.x + Math.cos(u.slot) * 30;
    destY = G.rally.y + Math.sin(u.slot) * 30;
    if (dist2(u.x, u.y, destX, destY) > 14 * 14) {
      u.face = lerpAngle(u.face, angleTo(u.x, u.y, destX, destY), Math.min(1, dt * 8));
    }
  }
  const dd = dist(u.x, u.y, destX, destY);
  if (dd > 4) {
    const mv = Math.min(dd, u.def.spd * dt);
    const a = angleTo(u.x, u.y, destX, destY);
    u.x += Math.cos(a) * mv;
    u.y += Math.sin(a) * mv;
    u.wob = (u.wob || 0) + mv * 0.15; // 보행 위상
  }
  // 병력끼리 겹침 방지 (소수라 단순 페어)
  for (const o of G.troops) {
    if (o === u || o.dead) continue;
    const rr = u.r + o.r;
    const d2 = dist2(u.x, u.y, o.x, o.y);
    if (d2 < rr * rr && d2 > 0.01) {
      const d = Math.sqrt(d2), push = (rr - d) * 0.4;
      u.x += (u.x - o.x) / d * push;
      u.y += (u.y - o.y) / d * push;
    }
  }
}

function updateMedic(u, dt) {
  // 치유 대상: 가장 심하게 다친 아군 병력 (자신 제외)
  u.retargetT -= dt;
  if (!u.healTgt || u.healTgt.dead || u.healTgt.hp >= u.healTgt.maxhp || u.retargetT <= 0) {
    u.retargetT = 0.5;
    let best = null, worst = 0.999;
    for (const o of G.troops) {
      if (o === u || o.dead) continue;
      const k = o.hp / o.maxhp;
      if (k < worst && dist2(u.x, u.y, o.x, o.y) < 320 * 320) { worst = k; best = o; }
    }
    u.healTgt = best;
  }
  const tg = u.healTgt;
  let destX, destY;
  if (tg) {
    destX = tg.x; destY = tg.y;
    const d = dist(u.x, u.y, tg.x, tg.y);
    u.face = lerpAngle(u.face, angleTo(u.x, u.y, tg.x, tg.y), Math.min(1, dt * 9));
    if (d < 64) { // 치유 빔
      tg.hp = Math.min(tg.maxhp, tg.hp + u.def.heal * (G.labTroop || 1) * dt);
      u.beamTgt = tg;
      destX = u.x; destY = u.y;
      if ((u.healFxT = (u.healFxT || 0) - dt) <= 0) {
        u.healFxT = 0.5;
        addFloater(tg.x, tg.y - tg.r - 10, '+', '#8fffc9');
      }
    } else u.beamTgt = null;
  } else {
    u.beamTgt = null;
    // 대상 없으면 집결 대형 유지
    destX = G.rally.x + Math.cos(u.slot) * 30;
    destY = G.rally.y + Math.sin(u.slot) * 30;
    if (dist2(u.x, u.y, destX, destY) > 14 * 14) {
      u.face = lerpAngle(u.face, angleTo(u.x, u.y, destX, destY), Math.min(1, dt * 8));
    }
  }
  const dd = dist(u.x, u.y, destX, destY);
  if (dd > 4) {
    const mv = Math.min(dd, u.def.spd * dt);
    const a = angleTo(u.x, u.y, destX, destY);
    u.x += Math.cos(a) * mv;
    u.y += Math.sin(a) * mv;
    u.wob = (u.wob || 0) + mv * 0.15;
  }
  // 보호막 펄스: 반경 100 아군 병력에 실드 부여
  u.shT -= dt;
  if (u.shT <= 0) {
    u.shT = u.def.shieldCd;
    let granted = false;
    for (const o of G.troops) {
      if (o.dead || o.def.heal) continue; // 매딕끼리는 제외
      if (dist2(u.x, u.y, o.x, o.y) < 100 * 100) {
        o.shield = Math.max(o.shield, Math.round(u.def.shieldAmt * (G.labTroop || 1)));
        o.shieldT = 6;
        granted = true;
      }
    }
    if (granted) {
      addRing(u.x, u.y, 10, 100, '#8fffc9', 2.5, 0.6);
      Sound.tone({ type: 'sine', f: 700, f2: 1150, dur: 0.18, v: 0.07 });
    }
  }
  // 겹침 방지 (일반 병력과 동일)
  for (const o of G.troops) {
    if (o === u || o.dead) continue;
    const rr = u.r + o.r;
    const d2 = dist2(u.x, u.y, o.x, o.y);
    if (d2 < rr * rr && d2 > 0.01) {
      const d = Math.sqrt(d2), push = (rr - d) * 0.4;
      u.x += (u.x - o.x) / d * push;
      u.y += (u.y - o.y) / d * push;
    }
  }
}

function drawTroop(g, u) {
  // 매딕 치유 빔 (월드 좌표)
  if (u.def.heal && u.beamTgt && !u.beamTgt.dead) {
    g.save();
    g.globalCompositeOperation = 'lighter';
    g.strokeStyle = 'rgba(143,255,201,0.45)';
    g.lineWidth = 3.5;
    g.beginPath(); g.moveTo(u.x, u.y); g.lineTo(u.beamTgt.x, u.beamTgt.y); g.stroke();
    g.strokeStyle = '#eafff3';
    g.lineWidth = 1.2;
    g.beginPath(); g.moveTo(u.x, u.y); g.lineTo(u.beamTgt.x, u.beamTgt.y); g.stroke();
    drawGlow(g, u.beamTgt.x, u.beamTgt.y, 10, '#8fffc9', 0.6);
    g.restore();
  }
  g.save();
  g.translate(u.x, u.y);
  g.fillStyle = 'rgba(2,4,10,0.4)';
  g.beginPath(); g.ellipse(0, u.r * 0.5, u.r * 1.0, u.r * 0.42, 0, 0, TAU); g.fill();
  g.rotate(u.face);
  // 보행 봅 + 피격 스쿼시
  const hk = Math.max(0, 1 - u.lastHitT / 0.18);
  if (u.wob) { g.rotate(Math.sin(u.wob) * 0.055); g.translate(Math.sin(u.wob * 2) * 0.7, 0); }
  if (hk > 0) g.scale(1 - hk * 0.1, 1 + hk * 0.1);
  const sp = ASSET_IMG[u.type] ? enemySprite(u.type) : null;
  if (sp) {
    const s = sp.width / SS;
    g.drawImage(sp, -s / 2, -s / 2, s, s);
  } else if (u.def.heal) {
    // 프로시저럴 폴백: 백색 강화복 + 녹색 십자 (매딕)
    g.fillStyle = '#e8f4ee';
    g.beginPath(); g.arc(0, 0, u.r * 0.9, 0, TAU); g.fill();
    g.strokeStyle = '#0a121c'; g.lineWidth = 1; g.stroke();
    g.fillStyle = '#37d183';
    g.fillRect(-u.r * 0.55, -1.7, u.r * 1.1, 3.4);
    g.fillRect(-1.7, -u.r * 0.55, 3.4, u.r * 1.1);
  } else {
    // 프로시저럴 폴백: 강청색 강화복 병사
    g.fillStyle = '#33465a';
    g.beginPath(); g.arc(0, 0, u.r * 0.85, 0, TAU); g.fill();
    g.strokeStyle = '#0a121c'; g.lineWidth = 1; g.stroke();
    g.fillStyle = u.def.color;
    g.fillRect(u.r * 0.2, -1.4, u.r * 1.1, 2.8); // 총열/방패
    g.beginPath(); g.arc(0, 0, u.r * 0.4, 0, TAU); g.fill();
  }
  if (u.flashT > 0) {
    const k = Math.min(1, u.flashT * 8);
    g.globalCompositeOperation = 'lighter';
    if (u.def.range > 0) {
      // 방향성 머즐 플래시
      drawGlow(g, u.r + 5, 0, 6 * k + 3, '#ffe9c4', k);
      g.globalAlpha = k;
      g.fillStyle = '#fff';
      g.beginPath();
      g.moveTo(u.r + 2, 0);
      g.lineTo(u.r + 11 + k * 4, -1.7);
      g.lineTo(u.r + 11 + k * 4, 1.7);
      g.closePath(); g.fill();
      g.globalAlpha = 1;
    } else {
      // 근접: 전방 블레이드 스윙 아크
      const sw = (1 - k) * 1.5;
      g.strokeStyle = `rgba(155,238,255,${k})`;
      g.lineWidth = 2.4;
      g.beginPath(); g.arc(2, 0, u.r + 6, -1.2 + sw, 0.1 + sw); g.stroke();
      drawGlow(g, u.r + 4, 0, 6, '#9beeff', k * 0.8);
    }
    g.globalCompositeOperation = 'source-over';
  }
  g.restore();
  // 매딕 보호막 버블
  if (u.shield > 0) {
    g.save();
    g.globalCompositeOperation = 'lighter';
    g.globalAlpha = 0.4 + Math.sin(G.time * 6 + u.slot) * 0.12;
    g.strokeStyle = '#8fffc9';
    g.lineWidth = 1.5;
    g.beginPath(); g.arc(u.x, u.y, u.r + 5, 0, TAU); g.stroke();
    drawGlow(g, u.x, u.y, u.r + 8, '#8fffc9', 0.16);
    g.restore();
    g.globalAlpha = 1;
  }
  if (u.hp < u.maxhp) {
    const w = u.r * 2 + 6, k = u.hp / u.maxhp;
    g.fillStyle = 'rgba(4,10,18,0.8)';
    g.fillRect(u.x - w / 2, u.y + u.r + 4, w, 2.8);
    g.fillStyle = k > 0.4 ? '#4ce0ff' : '#ff4d5e';
    g.fillRect(u.x - w / 2, u.y + u.r + 4, w * k, 2.8);
  }
}

/* ---------- 드론 ---------- */
function makeDrone(idx) {
  return {
    isDrone: true, idx, ang: rand(TAU),
    orbit: 96 + (idx % 8) * 13, // 무제한 — 8링 로테이션으로 분산

    x: 0, y: -96, r: 8, hp: 80, maxhp: 80,
    cd: 0, target: null, retargetT: 0, flashT: 0, dead: false,
  };
}

function updateDrone(d, dt) {
  d.ang += dt * (1.15 - d.idx * 0.05);
  d.x = Math.cos(d.ang) * d.orbit;
  d.y = Math.sin(d.ang) * d.orbit;
  d.flashT = Math.max(0, d.flashT - dt);
  if (G.state === 'BUILD' && d.hp < d.maxhp) d.hp = Math.min(d.maxhp, d.hp + 7 * dt);

  d.retargetT -= dt;
  if (!d.target || d.target.dead || d.retargetT <= 0) {
    d.target = acquireTarget(d, 190);
    d.retargetT = 0.4;
  }
  d.cd -= dt;
  if (d.target && d.cd <= 0) {
    const a = angleTo(d.x, d.y, d.target.x, d.target.y);
    G.projs.push({
      kind: 'bolt', x: d.x, y: d.y,
      vx: Math.cos(a) * 520, vy: Math.sin(a) * 520,
      dmg: 7 * (G.labDmg || 1), r: 2.2, life: 0.6, color: '#8ff0ff', dead: false,
    });
    d.cd = 0.4;
    Sfx.shoot('drone');
  }
}

/* ---------- 투사체 ---------- */
const _q = [];
function updateProjectile(p, dt) {
  p.life -= dt;
  if (p.life <= 0) {
    if (p.kind === 'missile') missileBoom(p);
    if (p.kind === 'spit') spitSplat(p);
    if (p.kind === 'nade') nadeBoom(p);
    p.dead = true;
    return;
  }
  if (p.kind === 'missile') {
    if (!p.target || p.target.dead) {
      p.target = acquireTarget(p, 280);
    }
    if (p.target) {
      const want = angleTo(p.x, p.y, p.target.x, p.target.y);
      const cur = Math.atan2(p.vy, p.vx);
      const na = lerpAngle(cur, want, Math.min(1, p.turn * dt));
      const sp = Math.min(p.spd, Math.hypot(p.vx, p.vy) + 500 * dt);
      p.vx = Math.cos(na) * sp;
      p.vy = Math.sin(na) * sp;
    }
    p.smokeT -= dt;
    if (p.smokeT <= 0) {
      p.smokeT = 0.03;
      addPart({ x: p.x, y: p.y, vx: rand(-12, 12), vy: rand(-12, 12), dur: 0.5, size: 2.6, color: '#33465c', shape: 'smoke' });
    }
  }
  if (p.kind === 'spit' && p.target && !p.target.dead) {
    const want = angleTo(p.x, p.y, p.target.x, p.target.y);
    const cur = Math.atan2(p.vy, p.vx);
    const na = lerpAngle(cur, want, Math.min(1, 2.2 * dt));
    const sp = Math.hypot(p.vx, p.vy);
    p.vx = Math.cos(na) * sp;
    p.vy = Math.sin(na) * sp;
  }
  p.x += p.vx * dt;
  p.y += p.vy * dt;

  if (p.kind === 'bolt') {
    Grid.query(p.x, p.y, 40, _q);
    for (let i = 0; i < _q.length; i++) {
      const e = _q[i];
      if (e.dead || e.untargetable) continue;
      if (dist2(p.x, p.y, e.x, e.y) < (e.r + p.r) * (e.r + p.r)) {
        damageEnemy(e, p.dmg);
        sparkBurst(p.x, p.y, p.color, 3, 100);
        p.dead = true;
        return;
      }
    }
  } else if (p.kind === 'missile') {
    Grid.query(p.x, p.y, 40, _q);
    for (let i = 0; i < _q.length; i++) {
      const e = _q[i];
      if (e.dead || e.untargetable) continue;
      if (dist2(p.x, p.y, e.x, e.y) < (e.r + 9) * (e.r + 9)) {
        missileBoom(p);
        p.dead = true;
        return;
      }
    }
  } else if (p.kind === 'nade') {
    Grid.query(p.x, p.y, 40, _q);
    for (let i = 0; i < _q.length; i++) {
      const e = _q[i];
      if (e.dead || e.untargetable) continue;
      if (dist2(p.x, p.y, e.x, e.y) < (e.r + 4) * (e.r + 4)) {
        nadeBoom(p);
        p.dead = true;
        return;
      }
    }
  } else if (p.kind === 'spit') {
    const tg = p.target;
    if (tg && !tg.dead) {
      if (dist2(p.x, p.y, tg.x, tg.y) < (tg.r + 5) * (tg.r + 5)) {
        if (tg.isCore) damageCore(p.dmg, Math.atan2(p.y, p.x));
        else damageStructure(tg, p.dmg);
        spitSplat(p);
        p.dead = true;
      }
    } else if (dist2(p.x, p.y, 0, 0) < 44 * 44) {
      damageCore(p.dmg, Math.atan2(p.y, p.x));
      spitSplat(p);
      p.dead = true;
    }
  }
}

function missileBoom(p) {
  splashDamage(p.x, p.y, p.splash, p.dmg);
  boom(p.x, p.y, p.splash * 0.75, '#bfe9ff', 0.8);
  scorch(p.x, p.y, p.splash * 0.4);
}

function spitSplat(p) {
  for (let i = 0; i < 5; i++) {
    addPart({ x: p.x, y: p.y, vx: rand(-70, 70), vy: rand(-70, 70), dur: 0.35, size: 2, color: '#a3e635', add: true, shape: 'dot' });
  }
}

function splashDamage(x, y, r, dmg) {
  const es = G.enemies;
  for (let i = 0; i < es.length; i++) {
    const e = es[i];
    if (e.dead || e.untargetable) continue;
    const d = dist(x, y, e.x, e.y);
    if (d < r + e.r) {
      const k = 1 - Math.max(0, (d - e.r)) / r * 0.5;
      damageEnemy(e, dmg * k);
    }
  }
}

/* ---------- 파티클 · 이펙트 · 플로터 · 크리스탈 ---------- */
function addPart(p) {
  if (G.parts.length > (G.partCap || 750)) return;
  p.life = 0;
  p.drag = p.drag === undefined ? 2.2 : p.drag;
  p.spin = rand(-6, 6);
  p.rot = rand(TAU);
  G.parts.push(p);
}

function sparkBurst(x, y, color, n, spd) {
  for (let i = 0; i < n; i++) {
    const a = rand(TAU), s = rand(spd * 0.35, spd);
    addPart({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
      dur: rand(0.25, 0.55), size: rand(1.4, 2.6), color, add: true, shape: 'spark',
    });
  }
}

function boom(x, y, r, color, size) {
  addShake(2 + size * 4);
  addPunch(size * 0.3);
  if (size >= 1) vib(18);
  addFlash(x, y, r * 2.2, '#ffe9c4');
  addFlash(x, y, r * 1.3, color);
  addRing(x, y, 4, r * 2, color, 2.5, 0.45);
  sparkBurst(x, y, color, Math.min(16, 5 + r * 0.3), 150 + r * 5);
  // 불티 (중력 낙하)
  if (size >= 0.7) {
    for (let i = 0; i < 4 + size * 3; i++) {
      const a = rand(TAU), s = rand(60, 200);
      addPart({
        x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s - 60,
        dur: rand(0.5, 1), size: rand(1.4, 2.4), color: pick(['#ffb347', '#ff7a3d']),
        shape: 'dot', add: true, grav: 240, drag: 1,
      });
    }
  }
  for (let i = 0; i < 5; i++) {
    addPart({
      x: x + rand(-6, 6), y: y + rand(-6, 6), vx: rand(-30, 30), vy: rand(-45, 5),
      dur: rand(0.7, 1.3), size: rand(3, 3 + r * 0.22), color: '#0d1219', shape: 'smoke',
    });
  }
  Sfx.explode(size);
}

function addRing(x, y, r0, r1, color, lw, dur) {
  G.effects.push({ kind: 'ring', x, y, r0, r1, color, lw, t: 0, dur, layer: 'over' });
}
function addFlash(x, y, r, color) {
  G.effects.push({ kind: 'flash', x, y, r, color, t: 0, dur: 0.16, layer: 'over' });
}
function addZap(x1, y1, x2, y2, color) {
  const pts = [{ x: x1, y: y1 }];
  const n = 5;
  for (let i = 1; i < n; i++) {
    const k = i / n;
    const px = lerp(x1, x2, k), py = lerp(y1, y2, k);
    const off = rand(-9, 9);
    const a = angleTo(x1, y1, x2, y2) + Math.PI / 2;
    pts.push({ x: px + Math.cos(a) * off, y: py + Math.sin(a) * off });
  }
  pts.push({ x: x2, y: y2 });
  G.effects.push({ kind: 'zap', pts, color, t: 0, dur: 0.16, layer: 'over' });
}
function addShake(a) { G.shake = Math.min(24, G.shake + a); }
function addPunch(a) { if (G.cam) G.cam.punch = Math.min(1, G.cam.punch + a); }

/* ---------- 동적 라이팅 (어둠 오버레이 + 라이트 펀칭 + 가산 블룸) ---------- */
// 맵별 어둠 톤: [r,g,b 문자열, 어둠 강도]
const MAP_DARK = {
  bastion: ['8,14,26', 0.46], rift: ['26,8,4', 0.5], infest: ['18,8,12', 0.5],
  cryo: ['6,16,30', 0.48], void: ['10,6,24', 0.56],
};
function mapDark() { return MAP_DARK[(G.map && G.map.id) || 'bastion'] || MAP_DARK.bastion; }

function collectLights() {
  const L = G.lights;
  L.length = 0;
  const platR = Math.min(G.lw, G.lh) / 2;
  // 아레나 기본광 (플랫폼이 완전히 묻히지 않게)
  L.push({ x: 0, y: 0, r: platR * 1.02, c: '#ffffff', a: 0.62 });
  // 코어 (맥동 · 저체력 시 적색 경고광)
  const cr = G.core;
  const low = cr.hp > 0 && cr.hp / cr.maxhp < 0.35;
  const over = G.overT > 0; // 과충전: 호박색 과부하 광
  L.push({
    x: 0, y: 0, r: 165 + Math.sin(G.time * 2.3) * (over ? 26 : 14),
    c: low ? '#ff4d5e' : over ? '#ffd9a0' : '#4ce0ff',
    a: 0.6, glow: low ? 0.16 + Math.sin(G.time * 6) * 0.06 : over ? 0.2 : 0.12,
  });
  if (G.state === 'MENU') return;
  const Q = G.quality || 1;
  for (const t of G.turrets) {
    L.push({ x: t.x, y: t.y, r: 60, c: t.def.color, a: 0.34 });
    if (t.flashT > 0) L.push({ x: t.x, y: t.y, r: 100 * t.flashT * 6, c: '#ffd9a0', a: Math.min(1, t.flashT * 8), glow: t.flashT * 1.6 });
  }
  if (Q > 0.5) for (const p of G.projs) L.push({ x: p.x, y: p.y, r: 34, c: '#bfe9ff', a: 0.5, glow: 0.1 });
  for (const e of G.effects) {
    if (e.kind !== 'flash') continue;
    const k = e.t / e.dur;
    L.push({ x: e.x, y: e.y, r: e.r * 2.6 * (1 + k * 0.5), c: e.color, a: (1 - k), glow: (1 - k) * 0.32 });
  }
  for (const u of G.troops) {
    L.push({ x: u.x, y: u.y, r: 36, c: '#4ce0ff', a: 0.34 });
    if (u.flashT > 0) L.push({ x: u.x, y: u.y, r: 70 * u.flashT * 6, c: '#ffd9a0', a: Math.min(1, u.flashT * 7), glow: u.flashT });
  }
  for (const d of G.drones) L.push({ x: d.x, y: d.y, r: 30, c: '#9beeff', a: 0.36 });
  let n = 0;
  for (const e of G.enemies) {
    if (e.boss) { L.push({ x: e.x, y: e.y, r: 120, c: '#ff5566', a: 0.5, glow: 0.14 }); continue; }
    if (!Q || n > 24 * Q) continue;
    const gl = e.type === 'spitter' ? '#a3e635' : e.type === 'blinker' ? '#c084fc' : e.type === 'mender' ? '#ffc654' : null;
    if (gl) { L.push({ x: e.x, y: e.y, r: 42, c: gl, a: 0.3 }); n++; }
  }
  const cn = Math.min(G.crystals.length, 22);
  for (let i = 0; i < cn; i++) {
    const c = G.crystals[i];
    L.push({ x: c.x, y: c.y, r: 20, c: '#7de0ff', a: 0.4 });
  }
}

function drawLighting(ctx) {
  if (!G.light) return;
  collectLights();
  const lc = G.lctx, vs = G.vs * (G.zoom || 1);
  const ox = G.vw / 2 + (G.camx || 0) + (G.shx || 0), oy = G.vh / 2 + (G.camy || 0) + (G.shy || 0);
  const [rgb, dk] = mapDark();
  lc.globalCompositeOperation = 'source-over';
  lc.clearRect(0, 0, G.vw, G.vh);
  lc.fillStyle = `rgba(${rgb},${dk})`;
  lc.fillRect(0, 0, G.vw, G.vh);
  lc.globalCompositeOperation = 'destination-out';
  for (const l of G.lights) drawGlow(lc, ox + l.x * vs, oy + l.y * vs, l.r * vs, '#ffffff', l.a);
  ctx.drawImage(G.light, 0, 0);
  // 가산 블룸 패스 (광원 색 번짐)
  ctx.save();
  ctx.globalCompositeOperation = 'lighter';
  const gq = G.quality || 1;
  for (const l of G.lights) {
    if (!l.glow) continue;
    drawGlow(ctx, ox + l.x * vs, oy + l.y * vs, l.r * vs * 0.8, l.c, l.glow * gq);
  }
  ctx.restore();
}

/* ---------- 앰비언트 파티클 (맵별 부유 불티/포자/눈) ---------- */
const MAP_EMBER = {
  bastion: { c: '#7de0ff', a: 0.5, n: 20, fall: false },
  rift: { c: '#ff9a3d', a: 0.75, n: 30, fall: false },
  infest: { c: '#c9e05a', a: 0.55, n: 22, fall: false },
  cryo: { c: '#cfe9ff', a: 0.7, n: 34, fall: true },
  void: { c: '#c084fc', a: 0.65, n: 24, fall: false },
};
function seedEmbers() {
  const spec = MAP_EMBER[(G.map && G.map.id) || 'bastion'] || MAP_EMBER.bastion;
  const n = Math.round(spec.n * (G.quality || 1));
  G.embers = [];
  for (let i = 0; i < n; i++) {
    G.embers.push({
      x: rand(-G.lw / 2, G.lw / 2), y: rand(-G.lh / 2, G.lh / 2),
      vx: rand(-4, 4), vy: spec.fall ? rand(14, 30) : rand(-16, -6),
      sz: rand(0.9, 2.1), seed: rand(TAU), c: spec.c, a: spec.a,
    });
  }
}
function updateEmbers(dt) {
  if (!G.embers) return;
  const hw = G.lw / 2 + 20, hh = G.lh / 2 + 20;
  for (const m of G.embers) {
    m.x += (m.vx + Math.sin(G.time * 0.7 + m.seed) * 6) * dt;
    m.y += m.vy * dt;
    if (m.y < -hh) { m.y = hh; m.x = rand(-hw, hw); }
    if (m.y > hh) { m.y = -hh; m.x = rand(-hw, hw); }
    if (m.x < -hw) m.x = hw; else if (m.x > hw) m.x = -hw;
  }
}
function drawEmbers(g) {
  if (!G.embers) return;
  g.save();
  g.globalCompositeOperation = 'lighter';
  for (const m of G.embers) {
    const fl = m.a * (0.55 + 0.45 * Math.sin(G.time * 2.6 + m.seed));
    drawGlow(g, m.x, m.y, m.sz * 3.2, m.c, fl);
  }
  g.restore();
}

function scorch(x, y, r) {
  if (!G.dctx) return;
  const g = G.dctx;
  const vs = G.vs || 1;
  r *= vs;
  const cx = x * vs + G.vw / 2, cy = y * vs + G.vh / 2;
  const gr = g.createRadialGradient(cx, cy, 0, cx, cy, r);
  gr.addColorStop(0, 'rgba(0,0,0,0.5)');
  gr.addColorStop(0.6, 'rgba(0,0,0,0.28)');
  gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gr;
  g.beginPath();
  g.arc(cx, cy, r, 0, TAU);
  g.fill();
}

function addFloater(x, y, txt, color) {
  if (G.floaters.length > 60) return;
  G.floaters.push({ x, y, txt: String(txt), color, t: 0, dur: 0.8, vy: -30 });
}

function spawnCrystals(x, y, val) {
  if (G.crystals.length > 90) { G.minerals += val; return; }
  const n = clamp(Math.ceil(val / 9), 1, 4);
  for (let i = 0; i < n; i++) {
    const a = rand(TAU), s = rand(40, 130);
    G.crystals.push({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
      val: val / n, t: 0, rot: rand(TAU), dead: false,
    });
  }
}

function updateCrystal(c, dt) {
  c.t += dt;
  c.rot += dt * 6;
  if (c.t < 0.3) {
    c.vx *= (1 - 3 * dt);
    c.vy *= (1 - 3 * dt);
  } else {
    const tx = G.crystalTarget.x, ty = G.crystalTarget.y;
    const a = angleTo(c.x, c.y, tx, ty);
    c.vx += Math.cos(a) * 2800 * dt;
    c.vy += Math.sin(a) * 2800 * dt;
    const sp = Math.hypot(c.vx, c.vy);
    if (sp > 1500) { c.vx *= 1500 / sp; c.vy *= 1500 / sp; }
    if (dist2(c.x, c.y, tx, ty) < 30 * 30) {
      G.minerals += c.val;
      G.pillPop = true;
      Sfx.crystal(1 + Math.min(24, G.combo || 0) * 0.045); // 콤보가 쌓일수록 음정 상승
      c.dead = true;
      return;
    }
  }
  c.x += c.vx * dt;
  c.y += c.vy * dt;
}

/* ============================================================
   그리기: 적 — 프리렌더 셰이딩 스프라이트
   (상단광 볼륨 + 황갈 갑각/어두운 육질/골색 이빨 + 접지 그림자)
   ============================================================ */
const SS = 3; // 스프라이트 슈퍼샘플 배율
const _eSprites = new Map();

const PAL = {
  zerg: {
    fleshD: '#301008', flesh: '#61251a', fleshL: '#8a3a26',
    cara: '#a3661f', caraL: '#cf9440', caraXL: '#eec272',
    bone: '#d8c8a2', boneL: '#f4ecd6', boneD: '#8a785a',
    armor: '#42566d', armorL: '#61799a', out: '#12070a',
  },
  acid: {
    flesh: '#37500f', fleshL: '#4f6c1c',
    cara: '#5c4a1a', caraL: '#83702f', out: '#0d1206',
  },
  psi: {
    flesh: '#3c1c5c', fleshL: '#5c2f85',
    cry: '#c9b0ec', cryL: '#efe7fb', out: '#14081f',
  },
};

// 음영 타원: 베이스 → 윤곽 → 상단광
function sBlob(g, x, y, rx, ry, base, light, out) {
  g.save();
  g.translate(x, y);
  g.fillStyle = base;
  g.beginPath(); g.ellipse(0, 0, rx, ry, 0, 0, TAU); g.fill();
  if (out) { g.strokeStyle = out; g.lineWidth = 1.1; g.stroke(); }
  g.fillStyle = light;
  g.beginPath(); g.ellipse(-rx * 0.1, -ry * 0.34, rx * 0.66, ry * 0.44, 0, 0, TAU); g.fill();
  g.restore();
}

// 테이퍼 곡선 뼈 낫 (카이저 블레이드)
function sTusk(g, bx, by, cx2, cy2, tx, ty, w, P) {
  const a = Math.atan2(cy2 - by, cx2 - bx) + Math.PI / 2;
  const ox = Math.cos(a) * w / 2, oy = Math.sin(a) * w / 2;
  g.beginPath();
  g.moveTo(bx + ox, by + oy);
  g.quadraticCurveTo(cx2 + ox * 0.4, cy2 + oy * 0.4, tx, ty);
  g.quadraticCurveTo(cx2 - ox * 0.4, cy2 - oy * 0.4, bx - ox, by - oy);
  g.closePath();
  g.fillStyle = P.bone; g.fill();
  g.strokeStyle = P.out; g.lineWidth = 0.9; g.stroke();
  g.strokeStyle = P.boneL; g.lineWidth = 1.1; g.lineCap = 'round';
  g.beginPath();
  g.moveTo(bx - ox * 0.4, by - oy * 0.4);
  g.quadraticCurveTo(cx2 - ox * 0.6, cy2 - oy * 0.6, tx, ty);
  g.stroke();
}

const PAINT = {
  rusher(g) {
    const P = PAL.zerg;
    sBlob(g, -5, 0, 7, 5.2, P.flesh, P.fleshL, P.out);
    sBlob(g, 3, 0, 5.5, 4.2, P.flesh, P.fleshL, P.out);
    sBlob(g, -6.5, 0, 5, 4.4, P.cara, P.caraL, P.out);
    sBlob(g, -1.5, 0, 5.6, 4.8, P.cara, P.caraL, P.out);
    sBlob(g, 3.5, 0, 4.6, 4, P.caraL, P.caraXL, P.out);
    sBlob(g, 8.5, 0, 3.4, 2.8, P.flesh, P.fleshL, P.out);
    g.strokeStyle = P.bone; g.lineWidth = 1.6; g.lineCap = 'round';
    g.beginPath();
    g.moveTo(10, 2); g.quadraticCurveTo(13.5, 3.2, 14.5, 5.4);
    g.moveTo(10, -2); g.quadraticCurveTo(13.5, -3.2, 14.5, -5.4);
    g.stroke();
    g.fillStyle = P.bone;
    g.beginPath(); g.arc(-6, -2.4, 1, 0, TAU); g.fill();
    g.beginPath(); g.arc(-2, -2.8, 1.1, 0, TAU); g.fill();
  },
  swarm(g) {
    const P = PAL.zerg;
    sBlob(g, -2.5, 0, 3.4, 2.8, P.flesh, P.fleshL, P.out);
    sBlob(g, 1, 0, 4, 3.4, P.cara, P.caraL, P.out);
    g.strokeStyle = P.bone; g.lineWidth = 1.1; g.lineCap = 'round';
    g.beginPath();
    g.moveTo(4, 1.4); g.lineTo(6.5, 2.8);
    g.moveTo(4, -1.4); g.lineTo(6.5, -2.8);
    g.stroke();
  },
  spitter(g) {
    const P = PAL.acid, Z = PAL.zerg;
    sBlob(g, -3, 0, 9, 6.6, P.flesh, P.fleshL, P.out);
    sBlob(g, -5, 0, 6, 5, P.cara, P.caraL, P.out);
    sBlob(g, 0.5, 0, 6.4, 5.4, P.cara, P.caraL, P.out);
    sBlob(g, 6, 0, 4, 3.4, P.flesh, P.fleshL, P.out);
    g.fillStyle = Z.bone;
    for (const [sx, sr] of [[-7, 1.2], [-3, 1.4], [1, 1.2]]) {
      g.beginPath();
      g.moveTo(sx - sr, -4.5); g.lineTo(sx, -7.8); g.lineTo(sx + sr, -4.5);
      g.closePath(); g.fill();
    }
  },
  brute(g) {
    const P = PAL.zerg;
    sBlob(g, -10, 0, 9.5, 7.4, P.flesh, P.fleshL, P.out);
    sBlob(g, 13, 0, 5.4, 4.6, P.flesh, P.fleshL, P.out);
    sBlob(g, -9, 0, 8.4, 7, P.cara, P.caraL, P.out);
    sBlob(g, 0, 0, 9.4, 8.2, P.cara, P.caraL, P.out);
    sBlob(g, 8.5, 0, 7, 6.2, P.caraL, P.caraXL, P.out);
    sBlob(g, -9, 0, 4.6, 3.2, P.armor, P.armorL, P.out);
    sBlob(g, 0, 0, 5.2, 3.6, P.armor, P.armorL, P.out);
    sBlob(g, 8, 0, 4, 3, P.armor, P.armorL, P.out);
    sTusk(g, 13, 5, 20, 9, 25, 13.5, 4.6, P);
    sTusk(g, 13, -5, 20, -9, 25, -13.5, 4.6, P);
  },
  carrier(g) {
    const P = PAL.zerg;
    sBlob(g, -2, 0, 11, 8.6, '#8a5a20', '#c98f3f', P.out);   // 알주머니 배
    g.fillStyle = 'rgba(255,179,71,0.55)';                    // 발광 유충
    for (const [lx, ly] of [[-5, -2], [0, 3], [2, -3], [-2, 1], [4, 2]]) {
      g.beginPath(); g.arc(lx, ly, 1.7, 0, TAU); g.fill();
    }
    sBlob(g, -6, 0, 6, 4.6, P.cara, P.caraL, P.out);          // 등 갑각
    sBlob(g, 9, 0, 3.4, 2.8, P.flesh, P.fleshL, P.out);       // 머리
  },
  mender(g) {
    const P = PAL.zerg;
    sBlob(g, -3, 0, 7.5, 5, P.flesh, P.fleshL, P.out);
    sBlob(g, -4, 0, 5, 3.8, P.cara, P.caraL, P.out);
    sBlob(g, 5, 0, 3.6, 3, P.flesh, P.fleshL, P.out);
    g.fillStyle = '#ffc654';                                   // 재생 기관
    for (const [ox, oy] of [[-6, -3], [0, -4], [0, 4], [-6, 3]]) {
      g.beginPath(); g.arc(ox, oy, 1.9, 0, TAU); g.fill();
    }
    g.strokeStyle = P.bone; g.lineWidth = 1.2; g.lineCap = 'round';
    g.beginPath();
    g.moveTo(7, 1.6); g.lineTo(10.5, 3.4);
    g.moveTo(7, -1.6); g.lineTo(10.5, -3.4);
    g.stroke();
  },
  blinker(g) {
    const P = PAL.psi;
    const shard = (x0, y0, x1, y1, w) => {
      const a = Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2;
      const ox = Math.cos(a) * w, oy = Math.sin(a) * w;
      g.beginPath();
      g.moveTo(x0 + ox, y0 + oy); g.lineTo(x1, y1); g.lineTo(x0 - ox, y0 - oy);
      g.closePath();
      g.fillStyle = P.cry; g.fill();
      g.strokeStyle = P.out; g.lineWidth = 0.9; g.stroke();
      g.strokeStyle = P.cryL; g.lineWidth = 1;
      g.beginPath(); g.moveTo(x0, y0); g.lineTo(x1, y1); g.stroke();
    };
    sBlob(g, -1, 0, 6.6, 4.8, P.flesh, P.fleshL, P.out);
    shard(2, 0, 12.5, 0, 2.6);
    shard(-2, 0, -9.5, 0, 2.2);
    shard(0, 2, 1.5, 10, 2);
    shard(0, -2, 1.5, -10, 2);
    sBlob(g, 0, 0, 3.6, 3, P.fleshL, P.cryL, P.out);
  },
  boss(g) {
    const P = PAL.zerg;
    sBlob(g, -20, 0, 17, 13.5, P.flesh, P.fleshL, P.out);
    sBlob(g, 24, 0, 9.5, 8, P.flesh, P.fleshL, P.out);
    sBlob(g, -19, 0, 15.4, 12.6, P.cara, P.caraL, P.out);
    sBlob(g, -6, 0, 17, 14.4, P.cara, P.caraL, P.out);
    sBlob(g, 8, 0, 14.4, 12.4, P.cara, P.caraL, P.out);
    sBlob(g, 18, 0, 10.4, 9, P.caraL, P.caraXL, P.out);
    sBlob(g, -18, 0, 8, 5.4, P.armor, P.armorL, P.out);
    sBlob(g, -5, 0, 9, 6, P.armor, P.armorL, P.out);
    sBlob(g, 7, 0, 7.4, 5, P.armor, P.armorL, P.out);
    g.fillStyle = P.bone;
    for (let i = 0; i < 5; i++) {
      const sx = -28 + i * 9, sy = -11 - (i % 2) * 3;
      g.beginPath();
      g.moveTo(sx - 2.4, sy); g.lineTo(sx + 1, sy - 7); g.lineTo(sx + 4, sy);
      g.closePath(); g.fill();
      g.beginPath();
      g.moveTo(sx - 2.4, -sy); g.lineTo(sx + 1, -sy + 7); g.lineTo(sx + 4, -sy);
      g.closePath(); g.fill();
    }
    sBlob(g, 26, 0, 6, 4.6, P.bone, P.boneL, P.out);
    sTusk(g, 24, 8, 34, 13, 40, 19, 7, P);
    sTusk(g, 24, -8, 34, -13, 40, -19, 7, P);
  },
};

const SPR_PAD = { rusher: 12, swarm: 8, spitter: 12, brute: 16, blinker: 10, carrier: 12, mender: 10, boss: 26, boss2: 26, boss3: 26, boss4: 26 };
const SPR_R = { boss2: 34, boss3: 34, boss4: 34, marine: 8, medic: 9 }; // ENEMIES에 없는 스프라이트 키의 반경

/* ---------- AI 생성 이미지 에셋 파이프라인 ----------
   assets/<이름>.png 이 있으면 그걸 쓰고, 없으면 프로시저럴 드로잉 폴백.
   투명 여백 자동 트림 + 불투명 배경(체커/단색) 자동 키잉. */
const ASSET_SRC = {
  rusher: 'assets/rusher.webp',
  swarm: 'assets/rusher.webp',
  spitter: 'assets/spitter.webp',
  brute: 'assets/brute.webp',
  blinker: 'assets/blinker.webp',
  boss: 'assets/boss.webp',
  core: 'assets/core.webp',
  pulse: 'assets/pulse.webp',
  tesla: 'assets/tesla.webp',
  laser: 'assets/laser.webp',
  missile: 'assets/missile.webp',
  rail: 'assets/rail.webp',
  cryo: 'assets/cryo.webp',
  drone: 'assets/drone.webp',
  carrier: 'assets/carrier.webp',
  mender: 'assets/mender.webp',
  boss2: 'assets/boss2.webp',
  boss3: 'assets/boss3.webp',
  boss4: 'assets/boss4.webp',
  marine: 'assets/marine.webp',
  medic: 'assets/medic.webp',
  arena: 'assets/arena.webp', // 전장 바닥 (buildBackground에서 직접 사용)
  arena2: 'assets/arena2.webp',
  arena3: 'assets/arena3.webp',
  arena4: 'assets/arena4.webp',
  arena5: 'assets/arena5.webp',
};
// 이미지별 보정: rot(라디안, 오른쪽 향하도록), fill(캔버스 대비 채움 비율)
const ASSET_CFG = {
  rusher: { rot: -0.55, fill: 0.95 },
  swarm: { rot: -0.55, fill: 0.95 },
  spitter: { rot: -0.35, fill: 0.95 },
  brute: { rot: -0.85, fill: 0.98 },
  blinker: { rot: 0.7, fill: 0.92 },
  carrier: { rot: 3.14, fill: 0.95 },
  mender: { rot: -2.6, fill: 0.92 },
  boss: { rot: -0.6, fill: 1.0 },
  boss2: { rot: -2.5, fill: 1.0 },
  boss3: { rot: 0, fill: 1.0 },
  boss4: { rot: 0, fill: 1.0 },
  marine: { rot: -0.3, fill: 0.95 },
  medic: { rot: -0.35, fill: 0.95 },
  core: { rot: 0, fill: 1.0 },
  pulse: { rot: -2.4, fill: 0.95 },
  tesla: { rot: 0, fill: 0.95 },
  laser: { rot: 0, fill: 0.95 },
  missile: { rot: 0, fill: 0.95 },
  rail: { rot: 0, fill: 0.98 },
  cryo: { rot: 0, fill: 0.95 },
  drone: { rot: 0, fill: 0.95 },
};
const ASSET_IMG = {};
const _aSprites = new Map();
const _trims = new Map();

function loadAssets() {
  for (const key in ASSET_SRC) {
    const im = new Image();
    im.onload = () => {
      ASSET_IMG[key] = im;
      _eSprites.delete(key);
      _corpses.delete(key);
      _aSprites.clear();
      G.assetsVer = (G.assetsVer || 0) + 1; // 카드 아이콘 갱신 신호
    };
    im.onerror = () => {}; // 에셋 없으면 조용히 폴백
    im.src = ASSET_SRC[key];
  }
}

// 투명 여백 트림 + 코너색 키잉 (픽셀 접근 불가 시 원본 그대로)
function trimImage(key, im) {
  let t = _trims.get(key);
  if (t) return t;
  const w = im.naturalWidth, h = im.naturalHeight;
  try {
    const cv = document.createElement('canvas');
    cv.width = w; cv.height = h;
    const g = cv.getContext('2d');
    g.drawImage(im, 0, 0);
    const data = g.getImageData(0, 0, w, h);
    const d = data.data;
    // 모서리 라운딩(제미나이 다운로드 등)을 피해 6px 안쪽에서 배경 판정
    const off = Math.min(6, w >> 4, h >> 4);
    const pts = [[off, off], [w - 1 - off, off], [off, h - 1 - off], [w - 1 - off, h - 1 - off]];
    const ci = pts.map(([x, y]) => (y * w + x) * 4);
    let opaque = 0;
    for (const i of ci) if (d[i + 3] > 200) opaque++;
    if (opaque >= 3) { // 불투명 배경 → 배경색 기준 키잉
      const br = d[ci[0]], bg2 = d[ci[0] + 1], bb = d[ci[0] + 2];
      for (let i = 0; i < d.length; i += 4) {
        const dr = d[i] - br, dg = d[i + 1] - bg2, db = d[i + 2] - bb;
        if (dr * dr + dg * dg + db * db < 1600) d[i + 3] = 0;
      }
      // 강채도(크로마) 배경이면 경계 프린지 2차 제거
      const sat = Math.max(br, bg2, bb) - Math.min(br, bg2, bb);
      if (sat > 120) {
        for (let i = 0; i < d.length; i += 4) {
          if (d[i + 3] === 0) continue;
          const dr = d[i] - br, dg = d[i + 1] - bg2, db = d[i + 2] - bb;
          if (dr * dr + dg * dg + db * db < 30000) d[i + 3] = 0;
        }
      }
      g.putImageData(data, 0, 0);
    }
    let x0 = w, y0 = h, x1 = 0, y1 = 0;
    for (let y = 0; y < h; y += 2) {
      for (let x = 0; x < w; x += 2) {
        if (d[(y * w + x) * 4 + 3] > 20) {
          if (x < x0) x0 = x;
          if (x > x1) x1 = x;
          if (y < y0) y0 = y;
          if (y > y1) y1 = y;
        }
      }
    }
    t = (x1 <= x0 || y1 <= y0)
      ? { src: im, x: 0, y: 0, w, h }
      : { src: cv, x: x0, y: y0, w: x1 - x0 + 1, h: y1 - y0 + 1 };
  } catch (e) {
    t = { src: im, x: 0, y: 0, w, h }; // file:// 캔버스 오염 등
  }
  _trims.set(key, t);
  return t;
}

function bakeImage(g, key, W) {
  const cfg = ASSET_CFG[key] || { rot: 0, fill: 0.92 };
  const t = trimImage(key, ASSET_IMG[key]);
  const s = W * cfg.fill / Math.max(t.w, t.h);
  g.rotate(cfg.rot);
  g.drawImage(t.src, t.x, t.y, t.w, t.h, -t.w * s / 2, -t.h * s / 2, t.w * s, t.h * s);
}

// 범용 에셋 스프라이트 (코어 등 구조물)
function assetSprite(key, size) {
  if (!ASSET_IMG[key]) return null;
  const ck = key + '_' + size;
  let c = _aSprites.get(ck);
  if (c) return c;
  c = document.createElement('canvas');
  c.width = c.height = Math.ceil(size * SS);
  const g = c.getContext('2d');
  g.translate(c.width / 2, c.height / 2);
  bakeImage(g, key, c.width);
  _aSprites.set(ck, c);
  return c;
}

function enemySprite(type) {
  let c = _eSprites.get(type);
  if (c) return c;
  const half = (ENEMIES[type] ? ENEMIES[type].r : (SPR_R[type] || 20)) + (SPR_PAD[type] || 12);
  c = document.createElement('canvas');
  c.width = c.height = Math.ceil(half * 2 * SS);
  const g = c.getContext('2d');
  g.translate(c.width / 2, c.height / 2);
  if (ASSET_IMG[type]) {
    bakeImage(g, type, c.width);
  } else {
    g.scale(SS, SS);
    g.lineJoin = 'round';
    (PAINT[type] || PAINT.boss)(g); // bossN 등 전용 페인터 없으면 베헤모스 폴백
  }
  _eSprites.set(type, c);
  return c;
}

function drawSprite(g, type) {
  const sp = enemySprite(type);
  const s = sp.width / SS;
  g.drawImage(sp, -s / 2, -s / 2, s, s);
}

// 다리 애니메이션 (몸통 아래 레이어)
function legsZerg(g, e, pairs, len, lw) {
  g.strokeStyle = 'rgba(38,12,7,0.9)';
  g.lineWidth = lw;
  g.lineCap = 'round';
  for (let i = 0; i < pairs; i++) {
    const ly = Math.sin(e.ph + i * 2.1) * len * 0.35;
    const bx = -e.r * 0.55 + i * (e.r * 1.15 / Math.max(1, pairs - 1));
    g.beginPath();
    g.moveTo(bx, e.r * 0.4); g.lineTo(bx - 3, e.r * 0.4 + len + ly);
    g.moveTo(bx, -e.r * 0.4); g.lineTo(bx - 3, -e.r * 0.4 - len - ly);
    g.stroke();
  }
}

function drawEnemy(g, e) {
  g.save();
  g.translate(e.x, e.y);
  // 잠수 중(심연의 베헤모스): 본체 대신 수면 파문만
  if (e.untargetable) {
    const rip = (G.time * 1.6) % 1;
    g.globalAlpha = 0.5;
    g.fillStyle = 'rgba(6,10,24,0.55)';
    g.beginPath(); g.ellipse(0, 0, e.r * 1.2, e.r * 0.5, 0, 0, TAU); g.fill();
    for (const k of [rip, (rip + 0.5) % 1]) {
      g.globalAlpha = (1 - k) * 0.55;
      g.strokeStyle = '#4d7dff';
      g.lineWidth = 2;
      g.beginPath(); g.ellipse(0, 0, e.r * (0.5 + k * 1.3), e.r * (0.2 + k * 0.55), 0, 0, TAU); g.stroke();
    }
    g.globalAlpha = 1;
    g.restore();
    return;
  }
  const sk = e.spawnT > 0 ? 1 - e.spawnT / 0.45 : 1;
  // 접지 그림자
  g.fillStyle = 'rgba(2,4,10,0.42)';
  g.beginPath();
  g.ellipse(0, e.r * 0.55, e.r * 1.05 * sk, e.r * 0.45 * sk, 0, 0, TAU);
  g.fill();
  g.rotate(e.face);
  if (e.spawnT > 0) {
    // 크립에서 솟아나는 연출
    g.globalAlpha = sk;
    g.scale(0.4 + 0.6 * sk, (0.4 + 0.6 * sk) * (0.65 + 0.35 * sk));
  }
  const es = e.elite ? e.r / e.def.r : 1;
  if (es !== 1) g.scale(es, es);
  // 걷기 바운스
  g.rotate(Math.sin(e.ph) * 0.035);
  g.translate(Math.sin(e.ph * 2) * 0.9, 0);
  if (e.lunge > 0) g.translate(Math.sin(e.lunge * Math.PI) * 6, 0);
  // 피격 스쿼시 (진행축 압축·측축 팽창)
  if (e.hitT > 0) {
    const hq = Math.min(1, e.hitT / 0.09);
    g.scale(1 - hq * 0.1, 1 + hq * 0.1);
  }
  e.def.draw(g, e);
  g.globalAlpha = 1;
  if (e.elite) {
    const pu = 0.55 + Math.sin(G.time * 6 + e.seed) * 0.25;
    g.strokeStyle = `rgba(255,198,84,${pu})`;
    g.lineWidth = 1.8;
    g.beginPath(); g.arc(0, 0, e.def.r + 5, 0, TAU); g.stroke();
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, 0, 0, e.def.r + 7, '#ffc654', 0.22);
    g.globalCompositeOperation = 'source-over';
  }
  if (e.slowT > 0 || G.stasisT > 0) {
    g.globalAlpha = 0.25;
    g.fillStyle = '#9beeff';
    g.beginPath(); g.arc(0, 0, e.r + 1, 0, TAU); g.fill();
    g.globalAlpha = 1;
  }
  if (e.hitT > 0) {
    g.globalCompositeOperation = 'lighter';
    g.globalAlpha = Math.min(1, e.hitT * 7);
    drawSprite(g, e.spriteKey || e.type);
    g.globalAlpha = 1;
    g.globalCompositeOperation = 'source-over';
  }
  g.restore();
}

function drawRusher(g, e) {
  legsZerg(g, e, 3, 7, 1.5);
  drawSprite(g, 'rusher');
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 8, 0, 3.2, '#ff6a3d', 0.65 + Math.sin(e.ph * 2) * 0.2);
  g.globalCompositeOperation = 'source-over';
}

function drawSwarm(g, e) {
  g.rotate(Math.sin(e.ph * 3) * 0.35);
  legsZerg(g, e, 2, 4, 1);
  drawSprite(g, 'swarm');
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 3, 0, 2.4, '#ff8a3d', 0.6);
  g.globalCompositeOperation = 'source-over';
}

function drawSpitter(g, e) {
  legsZerg(g, e, 3, 8, 1.4);
  drawSprite(g, 'spitter');
  const sac = 3.6 + Math.sin(e.ph * 2) * 1.1;
  g.fillStyle = '#a3e635';
  g.beginPath(); g.arc(8, 0, sac, 0, TAU); g.fill();
  g.strokeStyle = '#0d1206'; g.lineWidth = 0.9; g.stroke();
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 8, 0, sac + 3, '#a3e635', 0.5);
  g.globalCompositeOperation = 'source-over';
}

function drawBrute(g, e) {
  legsZerg(g, e, 4, 11, 2.6);
  drawSprite(g, 'brute');
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 14, 3, 2.8, '#ff7a45', 0.9);
  drawGlow(g, 14, -3, 2.8, '#ff7a45', 0.9);
  g.globalCompositeOperation = 'source-over';
}

function drawCarrier(g, e) {
  legsZerg(g, e, 3, 8, 2);
  drawSprite(g, 'carrier');
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, -2, 0, 7 + Math.sin(e.ph * 2) * 1.5, '#ffb347', 0.4);
  g.globalCompositeOperation = 'source-over';
}

function drawMender(g, e) {
  legsZerg(g, e, 3, 7, 1.4);
  drawSprite(g, 'mender');
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, 6 + Math.sin(e.ph * 3) * 2, '#ffc654', 0.5);
  g.globalCompositeOperation = 'source-over';
}

function drawEgg(g, e) {
  // 부화 임박할수록 빠르게 맥동하는 호박색 알집
  const urg = e.hatchT !== undefined ? clamp(1 - e.hatchT / 3.5, 0, 1) : 0;
  const pu = 1 + Math.sin(e.ph * (2 + urg * 5)) * (0.06 + urg * 0.1);
  g.fillStyle = '#7a5220';
  g.beginPath(); g.ellipse(0, 0, 8.5 * pu, 7 * pu, 0, 0, TAU); g.fill();
  g.fillStyle = '#b8813a';
  g.beginPath(); g.ellipse(-1, -1, 6.5 * pu, 5.4 * pu, 0, 0, TAU); g.fill();
  g.strokeStyle = '#3a2408'; g.lineWidth = 1.2;
  g.beginPath(); g.ellipse(0, 0, 8.5 * pu, 7 * pu, 0, 0, TAU); g.stroke();
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, 7 + urg * 5, '#ffb347', 0.35 + urg * 0.45);
  g.globalCompositeOperation = 'source-over';
  // 내부 유충 실루엣
  g.fillStyle = `rgba(60,30,10,${0.5 + urg * 0.3})`;
  g.beginPath(); g.arc(1, 0.5, 2.6 + urg * 1.2, 0, TAU); g.fill();
}

function drawBlinker(g, e) {
  g.globalAlpha = 0.68 + 0.28 * Math.sin(e.ph * 4);
  drawSprite(g, 'blinker');
  g.globalAlpha = 1;
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, 5.5, '#c084fc', 0.75);
  g.globalCompositeOperation = 'source-over';
}

function drawBoss(g, e) {
  g.translate(0, Math.sin(e.ph) * 2);
  legsZerg(g, e, 4, 16, 3.4);
  drawSprite(g, e.spriteKey || 'boss');
  // 돌진 예열: 전방 적황색 차지 글로우
  if (e.mechPhase === 'windup') {
    const k = 1 - (e.mechP || 0);
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, e.r * 0.8, 0, 10 + k * 22, '#ff9a3d', 0.5 + k * 0.5);
    g.globalCompositeOperation = 'source-over';
  }
  // 수정 실드 (공명 포식자)
  if (e.shieldHits > 0) {
    const pu = 0.6 + Math.sin(G.time * 8) * 0.25;
    g.strokeStyle = `rgba(192,132,252,${pu})`;
    g.lineWidth = 2.6;
    poly(g, 6, e.r + 9, G.time * 0.8);
    g.stroke();
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, 0, 0, e.r + 14, '#c084fc', 0.3);
    g.globalCompositeOperation = 'source-over';
  }
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 27, 4, 3.6, '#ff3355', 1);
  drawGlow(g, 27, -4, 3.6, '#ff3355', 1);
  drawGlow(g, 21, 8, 2.6, '#ff3355', 0.8);
  drawGlow(g, 21, -8, 2.6, '#ff3355', 0.8);
  const hpk = e.hp / e.maxhp;
  if (hpk < 0.66) {
    drawGlow(g, -8, 6, 7, '#ff9a3d', 0.5 + Math.sin(G.time * 7) * 0.2);
    drawGlow(g, -18, -8, 6, '#ff9a3d', 0.6);
  }
  if (hpk < 0.33) drawGlow(g, 2, -10, 9, '#ff9a3d', 0.7 + Math.sin(G.time * 9) * 0.2);
  g.globalCompositeOperation = 'source-over';
}

/* ---------- 그리기: 터렛 (강철 베이스 프리렌더 + 셰이딩 헤드) ---------- */
const _tBases = new Map();
function turretBaseSprite(type, lvl) {
  const key = type + '_' + lvl;
  let c = _tBases.get(key);
  if (c) return c;
  const def = TURRETS[type];
  const half = 24;
  c = document.createElement('canvas');
  c.width = c.height = half * 2 * SS;
  const g = c.getContext('2d');
  g.translate(c.width / 2, c.height / 2);
  g.scale(SS, SS);
  g.lineJoin = 'round';
  // 강철 패드 (상단광)
  const gr = g.createLinearGradient(0, -14, 0, 14);
  gr.addColorStop(0, '#43566c');
  gr.addColorStop(0.5, '#293a4d');
  gr.addColorStop(1, '#121c28');
  g.fillStyle = gr;
  g.strokeStyle = '#060c14';
  g.lineWidth = 1.6;
  poly(g, 8, 14, Math.PI / 8);
  g.fill(); g.stroke();
  // 상부 베벨 하이라이트
  g.save();
  g.beginPath(); g.rect(-17, -17, 34, 15); g.clip();
  g.strokeStyle = 'rgba(215,235,255,0.2)';
  g.lineWidth = 1.2;
  poly(g, 8, 12.6, Math.PI / 8);
  g.stroke();
  g.restore();
  // 볼트 8개
  for (let i = 0; i < 8; i++) {
    const a = Math.PI / 8 + i / 8 * TAU;
    const bx = Math.cos(a) * 11.2, by = Math.sin(a) * 11.2;
    g.fillStyle = '#08101a';
    g.beginPath(); g.arc(bx, by, 1.5, 0, TAU); g.fill();
    g.fillStyle = 'rgba(220,240,255,0.3)';
    g.beginPath(); g.arc(bx - 0.4, by - 0.5, 0.55, 0, TAU); g.fill();
  }
  // 팀컬러 패널 (좌우 파셋)
  g.globalAlpha = 0.55;
  g.fillStyle = def.color;
  for (const sgn of [-1, 1]) {
    g.beginPath();
    g.moveTo(sgn * 12.8, -5.2); g.lineTo(sgn * 12.8, 5.2);
    g.lineTo(sgn * 10, 4); g.lineTo(sgn * 10, -4);
    g.closePath(); g.fill();
  }
  g.globalAlpha = 1;
  // 중앙 데크
  g.fillStyle = '#0d1826';
  g.beginPath(); g.arc(0, 0, 8.6, 0, TAU); g.fill();
  g.strokeStyle = 'rgba(0,0,0,0.55)'; g.lineWidth = 1; g.stroke();
  g.strokeStyle = 'rgba(190,220,245,0.14)'; g.lineWidth = 1;
  g.beginPath(); g.arc(0, 0, 7.5, Math.PI * 1.08, Math.PI * 1.92); g.stroke();
  // 레벨 라이트 (하단 파셋)
  for (let i = 0; i < lvl; i++) {
    const bx = (i - (lvl - 1) / 2) * 5.4;
    g.fillStyle = '#08101a';
    g.fillRect(bx - 2.1, 14.6, 4.2, 3.6);
    g.fillStyle = def.color;
    g.fillRect(bx - 1.2, 15.3, 2.4, 2.2);
  }
  _tBases.set(key, c);
  return c;
}

function drawTurret(g, t, ghost) {
  g.save();
  g.translate(t.x, t.y);
  if (t.buildT > 0) {
    const k = 1 - t.buildT / 0.35;
    g.scale(0.5 + 0.5 * k + Math.sin(k * Math.PI) * 0.14, 0.5 + 0.5 * k + Math.sin(k * Math.PI) * 0.14);
  }
  const sc = 1 + (t.lvl - 1) * 0.09;
  g.scale(sc, sc);

  // 접지 그림자 + 강철 베이스
  if (!ghost) {
    g.fillStyle = 'rgba(2,4,10,0.45)';
    g.beginPath(); g.ellipse(0, 3.5, 16.5, 8.5, 0, 0, TAU); g.fill();
  }
  const type = t.type;
  const tsp = assetSprite(type, 46);
  if (tsp) {
    // AI 이미지 터렛: 원형 베이스라 전체 회전
    g.save();
    if (type === 'cryo') g.rotate(G.time * 0.3);
    else if (type !== 'tesla') {
      g.rotate(t.rot);
      if (t.recoilT > 0) g.translate(-Math.sin(t.recoilT / 0.2 * Math.PI) * 3.5, 0);
    }
    g.drawImage(tsp, -23, -23, 46, 46);
    g.restore();
    // 레벨 라이트 (비회전)
    g.fillStyle = t.def.color;
    for (let i = 0; i < t.lvl; i++) {
      g.fillRect((i - (t.lvl - 1) / 2) * 5.4 - 1.2, 17.6, 2.4, 2.4);
    }
    // 발광 오버레이
    g.globalCompositeOperation = 'lighter';
    if (type === 'tesla') {
      drawGlow(g, 0, 0, 8 + (t.fireT > 0 ? 6 : 0), '#9beeff', 0.5);
    } else if (type === 'cryo') {
      drawGlow(g, 0, 0, 7 + Math.sin(G.time * 3) * 1.5, '#9beeff', 0.4);
    } else {
      if (t.beamOn) drawGlow(g, Math.cos(t.rot) * 21, Math.sin(t.rot) * 21, 6, '#7ce8ff', 0.8);
      if (t.chargeT > 0) {
        const ck = t.chargeT / t.def.charge;
        drawGlow(g, Math.cos(t.rot) * 12, Math.sin(t.rot) * 12, 3 + ck * 9, '#eaf7ff', 0.4 + ck * 0.5);
      }
      if (t.fireT > 0) drawGlow(g, Math.cos(t.rot) * 21, Math.sin(t.rot) * 21, 8, '#eaf7ff', t.fireT * 8);
    }
    g.globalCompositeOperation = 'source-over';
    if (type === 'tesla' && t.cd < 0.2 && Math.random() < 0.3) {
      g.strokeStyle = 'rgba(155,238,255,0.8)'; g.lineWidth = 1;
      const za = rand(TAU);
      g.beginPath();
      g.moveTo(Math.cos(za) * 4, Math.sin(za) * 4);
      g.lineTo(Math.cos(za) * 11 + rand(-3, 3), Math.sin(za) * 11 + rand(-3, 3));
      g.stroke();
    }
  } else if (type === 'tesla') {
    const bs = turretBaseSprite(t.type, t.lvl);
    const bw = bs.width / SS;
    g.drawImage(bs, -bw / 2, -bw / 2, bw, bw);
    g.strokeStyle = '#5aa8c4'; g.lineWidth = 1.4;
    g.beginPath(); g.arc(0, 0, 6.5, 0, TAU); g.stroke();
    g.beginPath(); g.arc(0, 0, 4, 0, TAU); g.stroke();
    g.fillStyle = '#eaf7ff';
    g.beginPath(); g.arc(0, 0, 3.2, 0, TAU); g.fill();
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, 0, 0, 7 + (t.fireT > 0 ? 6 : 0), '#9beeff', 0.7);
    g.globalCompositeOperation = 'source-over';
    if (t.cd < 0.2 && Math.random() < 0.3) {
      g.strokeStyle = 'rgba(155,238,255,0.8)'; g.lineWidth = 1;
      const a = rand(TAU);
      g.beginPath();
      g.moveTo(Math.cos(a) * 4, Math.sin(a) * 4);
      g.lineTo(Math.cos(a) * 10 + rand(-3, 3), Math.sin(a) * 10 + rand(-3, 3));
      g.stroke();
    }
  } else if (type === 'cryo') {
    const bs = turretBaseSprite(t.type, t.lvl);
    const bw = bs.width / SS;
    g.drawImage(bs, -bw / 2, -bw / 2, bw, bw);
    g.save();
    g.rotate(G.time * 0.8);
    g.strokeStyle = '#9beeff'; g.lineWidth = 1.6;
    poly(g, 6, 8.5); g.stroke();
    g.restore();
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, 0, 0, 6 + Math.sin(G.time * 3) * 1.5, '#9beeff', 0.6);
    g.globalCompositeOperation = 'source-over';
  } else {
    const bs = turretBaseSprite(t.type, t.lvl);
    const bw = bs.width / SS;
    g.drawImage(bs, -bw / 2, -bw / 2, bw, bw);
    g.rotate(t.rot);
    if (t.recoilT > 0) g.translate(-Math.sin(t.recoilT / 0.2 * Math.PI) * 4, 0);
    if (type === 'pulse') {
      g.fillStyle = '#8fbdd1';
      g.fillRect(3, -4.2, 14, 2.8);
      g.fillRect(3, 1.4, 14, 2.8);
      g.fillStyle = '#e2f2fa';
      g.fillRect(3, -4.2, 14, 0.9);
      g.fillRect(3, 1.4, 14, 0.9);
      g.fillStyle = '#33465a';
      g.fillRect(-4, -5, 8, 10);
      g.fillStyle = 'rgba(220,240,255,0.2)';
      g.fillRect(-4, -5, 8, 1.3);
    } else if (type === 'laser') {
      g.fillStyle = '#33465a';
      g.fillRect(-5, -5.5, 10, 11);
      g.fillStyle = 'rgba(220,240,255,0.2)';
      g.fillRect(-5, -5.5, 10, 1.4);
      g.fillStyle = '#8fbdd1';
      g.fillRect(2, -2.2, 19, 4.4);
      g.fillStyle = '#e2f2fa';
      g.fillRect(2, -2.2, 19, 1);
      g.globalCompositeOperation = 'lighter';
      drawGlow(g, 22, 0, 4 + (t.beamOn ? 3 : 0), '#7ce8ff', 0.9);
      g.globalCompositeOperation = 'source-over';
    } else if (type === 'missile') {
      g.fillStyle = '#33465a';
      g.beginPath(); g.roundRect(-6, -8.5, 18, 17, 3); g.fill();
      g.strokeStyle = '#0a121c'; g.lineWidth = 1; g.stroke();
      g.fillStyle = 'rgba(220,240,255,0.16)';
      g.fillRect(-5, -8, 16, 1.6);
      const loaded = t.cd < 0.4;
      for (const [tx, ty] of [[1, -4], [1, 4], [8, -4], [8, 4]]) {
        g.fillStyle = '#0c1622';
        g.beginPath(); g.arc(tx, ty, 3.1, 0, TAU); g.fill();
        g.fillStyle = loaded ? '#bfe9ff' : '#1c2c3c';
        g.beginPath(); g.arc(tx, ty, 2.2, 0, TAU); g.fill();
      }
    } else if (type === 'rail') {
      g.fillStyle = '#33465a';
      g.fillRect(-6, -6, 12, 12);
      g.fillStyle = 'rgba(220,240,255,0.2)';
      g.fillRect(-6, -6, 12, 1.4);
      g.fillStyle = '#a8c4d4';
      g.fillRect(0, -4.6, 27, 2.4);
      g.fillRect(0, 2.2, 27, 2.4);
      g.fillStyle = '#eef8fd';
      g.fillRect(0, -4.6, 27, 0.8);
      g.fillRect(0, 2.2, 27, 0.8);
      if (t.chargeT > 0) {
        const k = t.chargeT / t.def.charge;
        g.globalCompositeOperation = 'lighter';
        drawGlow(g, 8 + k * 12, 0, 3 + k * 9, '#eaf7ff', 0.5 + k * 0.5);
        g.globalCompositeOperation = 'source-over';
      }
    }
    if (t.fireT > 0 && type !== 'rail') {
      g.globalCompositeOperation = 'lighter';
      drawGlow(g, 19, 0, 7, '#eaf7ff', t.fireT * 9);
      g.globalCompositeOperation = 'source-over';
    }
  }

  // 업그레이드 레벨 표시 링 (Lv2 청록 / Lv3 금색+발광)
  if (!ghost && t.lvl >= 2) {
    g.strokeStyle = t.lvl === 3 ? 'rgba(255,198,84,0.85)' : 'rgba(76,224,255,0.65)';
    g.lineWidth = 1.7;
    g.setLineDash(t.lvl === 3 ? [] : [5, 5]);
    g.beginPath(); g.arc(0, 0, 18.5, 0, TAU); g.stroke();
    g.setLineDash([]);
    if (t.lvl === 3) {
      g.globalCompositeOperation = 'lighter';
      drawGlow(g, 0, 0, 21, '#ffc654', 0.16 + Math.sin(G.time * 4 + t.x) * 0.06);
      g.globalCompositeOperation = 'source-over';
    }
  }
  if (t.flashT > 0) {
    const fk = Math.min(1, t.flashT * 8);
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, 0, 0, 21, '#ffffff', fk * 0.55);
    g.globalCompositeOperation = 'source-over';
  }
  g.restore();

  // 레이저 빔 (월드 좌표)
  if (t.beamOn && t.target && !t.target.dead) {
    const tg = t.target;
    const heat = t.heat / 2.2;
    g.save();
    g.globalCompositeOperation = 'lighter';
    g.strokeStyle = 'rgba(124,232,255,0.35)';
    g.lineWidth = 6 + heat * 4;
    g.beginPath(); g.moveTo(t.x, t.y); g.lineTo(tg.x, tg.y); g.stroke();
    g.strokeStyle = heat > 0.7 ? '#ffffff' : '#bff2ff';
    g.lineWidth = 1.6 + heat * 1.6 + Math.sin(G.time * 42) * 0.5;
    g.beginPath(); g.moveTo(t.x, t.y); g.lineTo(tg.x, tg.y); g.stroke();
    drawGlow(g, tg.x, tg.y, 9 + heat * 6, '#7ce8ff', 0.8);
    g.restore();
  }

  // HP 바
  if (!ghost && t.hp < t.maxhp) {
    const w = 26, k = t.hp / t.maxhp;
    g.fillStyle = 'rgba(4,10,18,0.8)';
    g.fillRect(t.x - w / 2, t.y + 20, w, 3.4);
    g.fillStyle = k > 0.4 ? '#4ce0ff' : '#ff4d5e';
    g.fillRect(t.x - w / 2, t.y + 20, w * k, 3.4);
  }
}

function drawCryoAura(g, t) {
  const r = turretRange(t);
  g.save();
  g.globalAlpha = 0.05 + Math.sin(G.time * 2 + t.x) * 0.015;
  g.fillStyle = '#9beeff';
  g.beginPath(); g.arc(t.x, t.y, r, 0, TAU); g.fill();
  g.globalAlpha = 0.3;
  g.strokeStyle = '#9beeff';
  g.lineWidth = 1;
  g.setLineDash([6, 10]);
  g.lineDashOffset = -G.time * 14;
  g.beginPath(); g.arc(t.x, t.y, r, 0, TAU); g.stroke();
  g.setLineDash([]);
  g.restore();
}

/* ---------- 그리기: 드론 · 코어 · 투사체 ---------- */
function drawDrone(g, d) {
  const face = d.target && !d.target.dead ? angleTo(d.x, d.y, d.target.x, d.target.y) : d.ang + Math.PI / 2;
  g.save();
  // 비행 그림자 (지면에서 떨어져 있어 작고 멀리)
  g.fillStyle = 'rgba(2,4,10,0.28)';
  g.beginPath(); g.ellipse(d.x, d.y + 13, 6.5, 2.8, 0, 0, TAU); g.fill();
  g.translate(d.x, d.y);
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, 7, '#4ce0ff', 0.45);
  g.globalCompositeOperation = 'source-over';
  g.rotate(face);
  const dsp = assetSprite('drone', 24);
  if (dsp) {
    g.drawImage(dsp, -12, -12, 24, 24);
  } else {
    g.fillStyle = '#123246';
    g.beginPath();
    g.moveTo(8, 0); g.lineTo(-5, 5); g.lineTo(-2.5, 0); g.lineTo(-5, -5);
    g.closePath(); g.fill();
    g.strokeStyle = '#4ce0ff'; g.lineWidth = 1.1; g.stroke();
  }
  g.restore();
  if (d.hp < d.maxhp) {
    const w = 16, k = d.hp / d.maxhp;
    g.fillStyle = 'rgba(4,10,18,0.8)';
    g.fillRect(d.x - w / 2, d.y + 11, w, 2.6);
    g.fillStyle = k > 0.4 ? '#4ce0ff' : '#ff4d5e';
    g.fillRect(d.x - w / 2, d.y + 11, w * k, 2.6);
  }
}

function drawCore(g) {
  const c = G.core;
  const t = G.time;
  g.save();

  // 접지 그림자
  g.fillStyle = 'rgba(2,4,10,0.5)';
  g.beginPath(); g.ellipse(0, 9, 52, 22, 0, 0, TAU); g.fill();

  // 보호막
  if (c.sh > 0 || c.shFlashT > 0) {
    const shk = c.sh / c.maxsh;
    g.globalAlpha = 0.1 + shk * 0.1 + Math.sin(t * 2.4) * 0.03;
    g.strokeStyle = '#9beeff';
    g.lineWidth = 2;
    poly(g, 24, 58, t * 0.15);
    g.stroke();
    if (c.shFlashT > 0) {
      g.globalAlpha = Math.min(1, c.shFlashT * 3);
      g.strokeStyle = '#eaf7ff';
      g.lineWidth = 3;
      g.beginPath();
      g.arc(0, 0, 58, c.shFlashA - 0.7, c.shFlashA + 0.7);
      g.stroke();
    }
    g.globalAlpha = 1;
  }

  // 본체 (이미지 에셋 있으면 우선 사용)
  const coreSp = assetSprite('core', 112);
  if (coreSp) {
    g.save();
    g.rotate(t * 0.06);
    g.drawImage(coreSp, -56, -56, 112, 112);
    g.restore();
  } else {
    g.save();
    g.rotate(t * 0.12);
    const bodyGr = g.createLinearGradient(0, -40, 0, 40);
    bodyGr.addColorStop(0, '#20385a');
    bodyGr.addColorStop(0.55, '#0f1e34');
    bodyGr.addColorStop(1, '#071020');
    g.fillStyle = bodyGr;
    g.strokeStyle = 'rgba(76,224,255,0.55)';
    g.lineWidth = 2.2;
    poly(g, 6, 40);
    g.fill(); g.stroke();
    for (let i = 0; i < 6; i++) {
      const a = i / 6 * TAU;
      g.globalCompositeOperation = 'lighter';
      drawGlow(g, Math.cos(a) * 40, Math.sin(a) * 40, 4.5, '#4ce0ff', 0.8);
      g.globalCompositeOperation = 'source-over';
    }
    g.restore();
    g.save();
    g.rotate(-t * 0.2);
    g.strokeStyle = 'rgba(76,224,255,0.35)';
    g.lineWidth = 1.4;
    poly(g, 6, 29);
    g.stroke();
    g.strokeStyle = 'rgba(76,224,255,0.5)';
    g.beginPath();
    g.arc(0, 0, 22, t * 0.6, t * 0.6 + 1.8);
    g.stroke();
    g.restore();
  }

  // 중심 오브
  const pr = 11 + Math.sin(t * 3.2) * 2;
  g.globalCompositeOperation = 'lighter';
  drawGlow(g, 0, 0, pr + 16, '#4ce0ff', 0.55);
  drawGlow(g, 0, 0, pr, '#bff2ff', 0.95);
  g.globalCompositeOperation = 'source-over';

  // 코어 피격 스파크 (저체력)
  if (c.hp / c.maxhp < 0.5 && Math.random() < 0.12) {
    const a = rand(TAU);
    sparkBurst(Math.cos(a) * rand(10, 34), Math.sin(a) * rand(10, 34), '#ff9a3d', 2, 90);
  }
  g.restore();
}

function nadeBoom(p) {
  boom(p.x, p.y, 26, '#ff9a3d', 0.5);
  splashDamage(p.x, p.y, p.splash || 50, p.dmg);
  scorch(p.x, p.y, 15);
}

function drawProjectile(g, p) {
  g.save();
  g.globalCompositeOperation = 'lighter';
  if (p.kind === 'nade') {
    drawGlow(g, p.x, p.y, 7, '#ff9a3d', 0.8);
    g.globalCompositeOperation = 'source-over';
    g.fillStyle = '#ffd9a0';
    g.beginPath(); g.arc(p.x, p.y, 2.6 + Math.sin(G.time * 24) * 0.5, 0, TAU); g.fill();
  } else if (p.kind === 'bolt') {
    const a = Math.atan2(p.vy, p.vx);
    drawGlow(g, p.x, p.y, 6, p.color, 0.8);
    g.strokeStyle = '#ffffff';
    g.lineWidth = 2;
    g.beginPath();
    g.moveTo(p.x, p.y);
    g.lineTo(p.x - Math.cos(a) * 9, p.y - Math.sin(a) * 9);
    g.stroke();
  } else if (p.kind === 'missile') {
    const a = Math.atan2(p.vy, p.vx);
    g.globalCompositeOperation = 'source-over';
    g.save();
    g.translate(p.x, p.y);
    g.rotate(a);
    g.fillStyle = '#cfe9f5';
    g.fillRect(-5, -1.8, 10, 3.6);
    g.restore();
    g.globalCompositeOperation = 'lighter';
    drawGlow(g, p.x - Math.cos(a) * 6, p.y - Math.sin(a) * 6, 5 + rand(2), '#bfe9ff', 0.9);
  } else if (p.kind === 'spit') {
    drawGlow(g, p.x, p.y, 6, '#a3e635', 0.7);
    g.globalCompositeOperation = 'source-over';
    g.fillStyle = '#a3e635';
    g.beginPath(); g.arc(p.x, p.y, 3 + Math.sin(G.time * 20) * 0.6, 0, TAU); g.fill();
  }
  g.restore();
}

/* ---------- 파티클/이펙트/플로터/크리스탈 갱신·그리기 ---------- */
function updateParticles(dt) {
  const ps = G.parts;
  for (let i = 0; i < ps.length; i++) {
    const p = ps[i];
    p.life += dt;
    if (p.life >= p.dur) { ps[i] = ps[ps.length - 1]; ps.pop(); i--; continue; }
    p.vx *= (1 - p.drag * dt);
    p.vy *= (1 - p.drag * dt);
    if (p.grav) p.vy += p.grav * dt;
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.rot += p.spin * dt;
  }
}

function drawParticles(g) {
  const ps = G.parts;
  // 일반 (연기)
  for (let i = 0; i < ps.length; i++) {
    const p = ps[i];
    if (p.add) continue;
    const k = p.life / p.dur;
    if (p.shape === 'smoke') {
      g.globalAlpha = 0.18 * (1 - k);
      g.fillStyle = p.color;
      g.beginPath(); g.arc(p.x, p.y, p.size * (1 + k * 2.2), 0, TAU); g.fill();
    } else if (p.shape === 'chunk') {
      g.globalAlpha = 1 - k * 0.5;
      g.fillStyle = p.color;
      g.save();
      g.translate(p.x, p.y);
      g.rotate(p.rot);
      g.beginPath();
      g.moveTo(p.size, 0);
      g.lineTo(-p.size * 0.7, p.size * 0.8);
      g.lineTo(-p.size * 0.7, -p.size * 0.8);
      g.closePath(); g.fill();
      g.restore();
    }
  }
  g.globalAlpha = 1;
  // 가산 (스파크류)
  g.globalCompositeOperation = 'lighter';
  for (let i = 0; i < ps.length; i++) {
    const p = ps[i];
    if (!p.add) continue;
    const k = p.life / p.dur;
    const al = 1 - k;
    if (p.shape === 'spark') {
      g.globalAlpha = al;
      g.strokeStyle = p.color;
      g.lineWidth = p.size;
      g.beginPath();
      g.moveTo(p.x, p.y);
      g.lineTo(p.x - p.vx * 0.03, p.y - p.vy * 0.03);
      g.stroke();
    } else if (p.shape === 'dot' || p.shape === 'snow') {
      drawGlow(g, p.x, p.y, p.size * 2.4 * (1 - k * 0.5), p.color, al);
    }
  }
  g.globalAlpha = 1;
  g.globalCompositeOperation = 'source-over';
}

function updateEffects(dt) {
  const es = G.effects;
  for (let i = 0; i < es.length; i++) {
    es[i].t += dt;
    if (es[i].t >= es[i].dur) { es[i] = es[es.length - 1]; es.pop(); i--; }
  }
}

function drawEffects(g, layer) {
  const es = G.effects;
  for (let i = 0; i < es.length; i++) {
    const e = es[i];
    if (e.layer !== layer) continue;
    const k = e.t / e.dur;
    if (e.kind === 'ring') {
      g.globalAlpha = (1 - k) * 0.8;
      g.strokeStyle = e.color;
      g.lineWidth = e.lw * (1 - k * 0.6);
      g.beginPath();
      g.arc(e.x, e.y, lerp(e.r0, e.r1, 1 - (1 - k) * (1 - k)), 0, TAU);
      g.stroke();
      g.globalAlpha = 1;
    } else if (e.kind === 'flash') {
      g.globalCompositeOperation = 'lighter';
      drawGlow(g, e.x, e.y, e.r * (1 + k * 0.4), e.color, (1 - k) * 0.9);
      g.globalCompositeOperation = 'source-over';
    } else if (e.kind === 'line') {
      g.globalCompositeOperation = 'lighter';
      g.globalAlpha = (1 - k);
      g.strokeStyle = 'rgba(124,232,255,0.5)';
      g.lineWidth = e.lw * 3;
      g.beginPath(); g.moveTo(e.x1, e.y1); g.lineTo(e.x2, e.y2); g.stroke();
      g.strokeStyle = e.color;
      g.lineWidth = e.lw * (1 - k * 0.7);
      g.beginPath(); g.moveTo(e.x1, e.y1); g.lineTo(e.x2, e.y2); g.stroke();
      g.globalAlpha = 1;
      g.globalCompositeOperation = 'source-over';
    } else if (e.kind === 'zap') {
      g.globalCompositeOperation = 'lighter';
      g.globalAlpha = (1 - k);
      g.lineJoin = 'round';
      g.strokeStyle = 'rgba(155,238,255,0.4)';
      g.lineWidth = 5;
      zapPath(g, e.pts); g.stroke();
      g.strokeStyle = '#ffffff';
      g.lineWidth = 1.6;
      zapPath(g, e.pts); g.stroke();
      g.globalAlpha = 1;
      g.globalCompositeOperation = 'source-over';
    } else if (e.kind === 'warn') {
      const R = Math.min(G.lw || G.vw, G.lh || G.vh) / 2 - 30;
      const pulse = 0.35 + 0.3 * Math.sin(e.t * 12);
      g.globalAlpha = pulse * (1 - k * 0.5);
      g.strokeStyle = '#ff4d5e';
      g.lineWidth = 4 / (G.vs || 1);
      g.beginPath();
      g.arc(0, 0, R, e.ang - e.spread / 2, e.ang + e.spread / 2);
      g.stroke();
      g.globalAlpha = Math.min(1, pulse * 1.6);
      g.fillStyle = '#ff4d5e';
      g.font = 'bold ' + Math.round(16 / (G.vs || 1)) + 'px Bahnschrift, sans-serif';
      g.textAlign = 'center';
      g.textBaseline = 'middle';
      g.fillText('⚠', Math.cos(e.ang) * (R - 22), Math.sin(e.ang) * (R - 22));
      g.globalAlpha = 1;
    }
  }
}
function zapPath(g, pts) {
  g.beginPath();
  g.moveTo(pts[0].x, pts[0].y);
  for (let i = 1; i < pts.length; i++) g.lineTo(pts[i].x, pts[i].y);
}

function updateFloaters(dt) {
  const fs = G.floaters;
  for (let i = 0; i < fs.length; i++) {
    const f = fs[i];
    f.t += dt;
    f.y += f.vy * dt;
    if (f.t >= f.dur) { fs[i] = fs[fs.length - 1]; fs.pop(); i--; }
  }
}
function drawFloaters(g) {
  const fs = G.floaters;
  g.font = 'bold ' + Math.round(12 / (G.vs || 1)) + 'px Bahnschrift, sans-serif';
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  for (let i = 0; i < fs.length; i++) {
    const f = fs[i];
    const k = f.t / f.dur;
    g.globalAlpha = k < 0.7 ? 1 : (1 - k) / 0.3;
    g.fillStyle = '#04121e';
    g.fillText(f.txt, f.x + 1, f.y + 1);
    g.fillStyle = f.color;
    g.fillText(f.txt, f.x, f.y);
  }
  g.globalAlpha = 1;
}

function drawCrystals(g) {
  const cs = G.crystals;
  g.globalCompositeOperation = 'lighter';
  for (let i = 0; i < cs.length; i++) {
    const c = cs[i];
    drawGlow(g, c.x, c.y, 6, '#4ce0ff', 0.6);
    g.save();
    g.translate(c.x, c.y);
    g.rotate(c.rot);
    g.fillStyle = '#bff2ff';
    g.beginPath();
    g.moveTo(0, -4.2); g.lineTo(2.8, 0); g.lineTo(0, 4.2); g.lineTo(-2.8, 0);
    g.closePath(); g.fill();
    g.restore();
  }
  g.globalCompositeOperation = 'source-over';
}

/* ---------- 적끼리 밀어내기 (겹침 방지) ---------- */
function separateEnemies() {
  const es = G.enemies;
  for (let i = 0; i < es.length; i++) {
    const e = es[i];
    if (e.boss) continue;
    Grid.query(e.x, e.y, e.r + 20, _q);
    for (let j = 0; j < _q.length; j++) {
      const o = _q[j];
      if (o === e || o.dead) continue;
      const rr = e.r + o.r;
      const d2 = dist2(e.x, e.y, o.x, o.y);
      if (d2 < rr * rr && d2 > 0.001) {
        const d = Math.sqrt(d2);
        const push = (rr - d) * 0.5 * (o.boss ? 2 : 1);
        const nx = (e.x - o.x) / d, ny = (e.y - o.y) / d;
        e.x += nx * push;
        e.y += ny * push;
      }
    }
  }
}
