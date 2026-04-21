/* ==========================================================================
   LightOn Plus Lab — shared client behavior
   - Constellation starfield background (every page)
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

  /* -------- Constellation starfield -------- */
  (function(){
    var canvas = document.getElementById('starfield');
    if(!canvas) return;
    var ctx = canvas.getContext('2d');
    if(!ctx) return;

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var stars = [];
    var mouse = { x: null, y: null };
    var STAR_COUNT = 0;
    var LINK_DIST = 140;

    function resize(){
      var w = window.innerWidth;
      var h = window.innerHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // scale star count with viewport area, capped
      var count = Math.min(Math.round((w*h)/9000), 220);
      if(count !== STAR_COUNT){
        STAR_COUNT = count;
        stars = [];
        for(var i=0; i<STAR_COUNT; i++){
          stars.push({
            x: Math.random()*w,
            y: Math.random()*h,
            vx: (Math.random()-.5)*.18,
            vy: (Math.random()-.5)*.18,
            r: Math.random()*1.4 + .25,
            tw: Math.random()*Math.PI*2, // twinkle phase
            hue: Math.random() // 0..1 for subtle color variety
          });
        }
      }
    }

    function tick(t){
      var w = window.innerWidth;
      var h = window.innerHeight;
      ctx.clearRect(0, 0, w, h);

      for(var i=0; i<stars.length; i++){
        var s = stars[i];

        // drift
        s.x += s.vx;
        s.y += s.vy;

        // wrap edges
        if(s.x < -5) s.x = w+5;
        if(s.x > w+5) s.x = -5;
        if(s.y < -5) s.y = h+5;
        if(s.y > h+5) s.y = -5;

        // gentle pull toward mouse (subtle)
        if(mouse.x !== null){
          var dx = mouse.x - s.x;
          var dy = mouse.y - s.y;
          var d = Math.sqrt(dx*dx + dy*dy);
          if(d < 200){
            var f = (1 - d/200) * .04;
            s.x += dx*f*.01;
            s.y += dy*f*.01;
          }
        }

        // twinkle
        s.tw += 0.012;
        var alpha = 0.4 + Math.sin(s.tw) * 0.35;

        // color pick from palette (mint/cyan/purple/white mix)
        var color;
        if(s.hue < 0.55) color = 'rgba(232,236,244,'+alpha.toFixed(3)+')';      // white
        else if(s.hue < 0.75) color = 'rgba(34,211,238,'+alpha.toFixed(3)+')';  // cyan
        else if(s.hue < 0.9) color = 'rgba(167,139,250,'+(alpha*.8).toFixed(3)+')'; // purple
        else color = 'rgba(45,212,191,'+alpha.toFixed(3)+')';                   // mint

        ctx.beginPath();
        ctx.fillStyle = color;
        ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
        ctx.fill();
      }

      // Connect nearby stars — constellation effect
      for(var i=0; i<stars.length; i++){
        var a = stars[i];
        for(var j=i+1; j<stars.length; j++){
          var b = stars[j];
          var dx = a.x - b.x;
          var dy = a.y - b.y;
          var d2 = dx*dx + dy*dy;
          if(d2 < LINK_DIST*LINK_DIST){
            var dd = Math.sqrt(d2);
            var op = (1 - dd/LINK_DIST) * 0.12;
            ctx.strokeStyle = 'rgba(167,180,216,'+op.toFixed(3)+')';
            ctx.lineWidth = .5;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      if(!reduceMotion) requestAnimationFrame(tick);
    }

    window.addEventListener('resize', resize, { passive: true });
    window.addEventListener('mousemove', function(e){
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    }, { passive: true });
    window.addEventListener('mouseleave', function(){ mouse.x = null; mouse.y = null; });

    resize();
    if(reduceMotion){
      // render one static frame
      tick(0);
    } else {
      requestAnimationFrame(tick);
    }
  })();

})();
