/* ==========================================================================
   LightOn Plus Lab — shared client behavior
   - Mobile menu toggle
   - Scroll-reveal animations
   - Footer year stamp
   - Active nav highlight
   ========================================================================== */

(function(){
  'use strict';

  /* -------- Year stamp -------- */
  var y = document.getElementById('year');
  if(y) y.textContent = new Date().getFullYear();

  /* -------- Mobile menu -------- */
  (function(){
    var btn = document.getElementById('hamburger');
    var menu = document.getElementById('mobileMenu');
    if(!btn || !menu) return;
    btn.addEventListener('click', function(){
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    menu.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  })();

  /* -------- Active nav highlighting -------- */
  (function(){
    var file = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(function(a){
      var href = a.getAttribute('href');
      if(!href) return;
      if(href === file || (file === '' && href === 'index.html') || (file === 'index.html' && (href === '/' || href === './'))){
        a.classList.add('active');
      }
    });
  })();

  /* -------- Scroll reveal -------- */
  (function(){
    var els = document.querySelectorAll('.reveal');
    if(!els.length) return;
    if(!('IntersectionObserver' in window)){
      els.forEach(function(el){ el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    els.forEach(function(el){ io.observe(el); });
  })();

  /* -------- Counter animation -------- */
  (function(){
    var els = document.querySelectorAll('[data-counter]');
    if(!els.length || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(!e.isIntersecting) return;
        var el = e.target;
        var target = +el.dataset.counter;
        var duration = 1400;
        var start = performance.now();
        function tick(now){
          var p = Math.min((now-start)/duration, 1);
          var ease = 1 - Math.pow(1-p, 3);
          el.textContent = Math.round(target*ease);
          if(p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        io.unobserve(el);
      });
    }, { threshold: 0.5 });
    els.forEach(function(el){ io.observe(el); });
  })();

  /* -------- 광고 영상 — 눌러야 재생된다 --------
     내레이션이 있는 광고라 소리 없이는 뜻이 없다. 브라우저는 소리 있는 자동재생을
     막으므로, 사용자가 누른 그 클릭으로 재생을 시작해 소리를 허용받는다. */
  (function(){
    document.addEventListener('click', function(e){
      var btn = e.target.closest ? e.target.closest('.vplay') : null;
      if(!btn) return;
      var img = btn.querySelector('img');
      var v = document.createElement('video');
      v.src = btn.getAttribute('data-video');
      if(img) v.poster = img.getAttribute('src');
      v.controls = true; v.autoplay = true; v.preload = 'auto';
      v.setAttribute('playsinline','');
      btn.parentNode.replaceChild(v, btn);
      v.play().catch(function(){});
      // 한 편이 시작하면 나머지는 멈춘다
      v.addEventListener('play', function(){
        var others = document.querySelectorAll('.store-media video');
        Array.prototype.forEach.call(others, function(o){ if(o !== v) o.pause(); });
      });
    });
  })();

  /* -------- Ambient card videos -------- */
  (function(){
    var vids = document.querySelectorAll('video[data-ambient]');
    if(!vids.length) return;
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return; // poster only
    // 좁은 화면에서는 포스터만. 영상 6개는 모바일 데이터·배터리를 쓰는데
    // 작은 화면에서 얻는 값이 그만큼 되지 않는다.
    if(window.matchMedia('(max-width: 768px)').matches) return;
    if(!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        var v = e.target;
        if(e.isIntersecting){ v.play().catch(function(){}); }
        else { v.pause(); }
      });
    }, { threshold: 0.25 });
    vids.forEach(function(v){ io.observe(v); });
  })();

})();
