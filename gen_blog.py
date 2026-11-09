# -*- coding: utf-8 -*-
# Generate blog pages (list + articles) reusing the site shell.
import io, datetime, json

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="google-adsense-account" content="ca-pub-7180935400084577">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — LightOn Plus Lab</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title} — LightOn Plus Lab" />
<meta property="og:type" content="article" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="https://lightonpluslab.com/{slug}.html" />
<meta property="og:image" content="{ogimg}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#FBFAF8" />
<link rel="icon" href="img/logo-mark-180.png" />
<link rel="apple-touch-icon" href="img/logo-mark.png" />
<link rel="canonical" href="https://lightonpluslab.com/{slug}.html" />
<link rel="alternate" type="application/rss+xml" title="LightOn Plus Lab Blog" href="https://lightonpluslab.com/feed.xml" />
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" crossorigin="anonymous" />
<link rel="stylesheet" href="styles.css?v=20260815" />
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D9LHH5465Q"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-D9LHH5465Q');</script>
<style>
.page-hero{{padding:72px 0 24px;text-align:center}}
.page-hero .eyebrow{{margin-bottom:20px}}
.page-hero h1{{font-size:clamp(30px,4.2vw,52px);font-weight:700;letter-spacing:-.03em;line-height:1.12;margin-bottom:16px}}
.page-hero h1 em{{font-style:normal;color:var(--ink)}}
.page-hero p{{color:var(--text-3);max-width:56ch;margin:0 auto;font-size:15px;line-height:1.7}}
.article-meta{{color:var(--text-3);font-size:13px;margin-top:14px}}
.prose{{max-width:720px;margin:0 auto;padding:8px 0 72px;font-size:15.5px;line-height:1.85;color:var(--text-2,#cdd5e1)}}
.prose h2{{font-size:21px;font-weight:700;letter-spacing:-.02em;margin:44px 0 14px;color:var(--text-1,#eef2f8)}}
.prose h3{{font-size:17px;font-weight:600;margin:30px 0 10px;color:var(--text-1,#eef2f8)}}
.prose p{{margin:0 0 16px}}
.prose ul,.prose ol{{margin:0 0 18px;padding-left:22px}}
.prose li{{margin:6px 0}}
.prose strong{{color:var(--text-1,#eef2f8)}}
.prose table{{width:100%;border-collapse:collapse;margin:8px 0 20px;font-size:14px}}
.prose th,.prose td{{border:1px solid var(--panel-border,#232b3d);padding:9px 12px;text-align:left;vertical-align:top}}
.prose th{{color:var(--text-1,#eef2f8);background:var(--panel,#0b1020)}}
.prose .tip{{padding:16px 18px;border-radius:14px;background:var(--panel,#0b1020);border:1px solid var(--panel-border,#232b3d);margin:0 0 18px}}
.prose a{{color:var(--cyan,#5eead4)}}
.prose pre{{margin:0 0 18px;padding:16px 18px;border-radius:8px;background:var(--paper-2);border:1px solid var(--rule);overflow-x:auto;font-size:13px;line-height:1.7}}
.prose pre code{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--ink);background:none;padding:0;border:0;white-space:pre}}
.prose code{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;padding:2px 6px;border-radius:4px;background:var(--paper-2);border:1px solid var(--rule);color:var(--accent)}}
.prose img,.post-hero img{{max-width:100%;height:auto;border-radius:16px;display:block;margin:0 auto}}
.post-hero{{margin:18px 0 26px}}
.post-hero img{{width:min(560px,100%)}}
.back-link{{display:inline-block;margin:28px 0 0;font-size:14px;color:var(--cyan,#5eead4);text-decoration:none}}
.post-list{{max-width:760px;margin:0 auto;padding:8px 0 72px;display:grid;gap:14px}}
.post-card{{display:block;padding:24px 26px;border-radius:16px;background:var(--panel);border:1px solid var(--panel-border);text-decoration:none;transition:background .25s,border-color .25s,transform .25s}}
.post-card:hover{{background:var(--panel-hover);border-color:var(--panel-border-hover);transform:translateY(-3px)}}
.post-card h2{{font-size:17px;font-weight:600;letter-spacing:-.01em;margin:0 0 8px;color:var(--text-1,#eef2f8)}}
.post-card p{{font-size:14px;color:var(--text-3);line-height:1.7;margin:0 0 10px}}
.post-card .pc-meta{{font-size:12.5px;color:var(--text-3);opacity:.8}}
</style>
</head>
<body>

<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="index.html">
      <img class="brand-img" src="img/logo-mark.png" alt="LightOn Plus Lab" width="36" height="36" />
            <span class="brand-text"><span class="brand-name">LightOn<span class="plus">+</span>Lab</span><span class="brand-sub">AI Apps · Innovation</span></span>
    </a>
    <nav class="nav-links" aria-label="메뉴">
      <a href="products.html">Apps</a>
      <a href="lens.html">Lens</a>
<a href="services.html">Services</a>
      <a href="blog.html">Blog</a>
      <a href="about.html">Studio</a>
      <a href="contact.html">Contact</a>
    </nav>
    <a class="nav-cta" href="contact.html">
      Launch Lab
      <svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M7 17L17 7M7 7h10v10" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
    <button class="hamburger" id="hamburger" aria-label="메뉴" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 8h16M4 16h16" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
<nav class="mobile-menu" id="mobileMenu" aria-label="모바일 메뉴">
  <a href="products.html">Apps</a>
  <a href="lens.html">Lens</a>
<a href="services.html">Services</a>
  <a href="blog.html">Blog</a>
  <a href="about.html">Studio</a>
  <a href="contact.html">Contact</a>
  <a href="contact.html" style="color:var(--purple);font-weight:600">Launch Lab →</a>
</nav>

<main id="main">
"""

FOOTER = """
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-brand">
          <a class="brand" href="index.html">
            <img class="brand-img" src="img/logo-mark.png" alt="LightOn Plus Lab" width="36" height="36" />
            <span class="brand-text"><span class="brand-name">LightOn<span class="plus">+</span>Lab</span><span class="brand-sub">AI Apps · Innovation</span></span>
          </a>
        </div>
        <div class="footer-tagline">AI를 실제 제품으로 만드는 1인 스튜디오. 경기도 안양.</div>
      </div>
      <div class="footer-col">
        <h5>Studio</h5>
        <a href="about.html">About</a>
        <a href="services.html">Services</a>
        <a href="blog.html">Blog</a>
      </div>
      <div class="footer-col">
        <h5>Work</h5>
        <a href="products.html">전체 앱</a>
<a href="https://lens.lightonpluslab.com" target="_blank" rel="noopener">Lens 렌즈 해석</a>
<a href="lens-docs.html">Lens 문서</a>
        <a href="momoi.html">모모아이</a>
        <a href="lighton-ai-note.html">라이트온 AI 노트</a>
        <a href="contact.html">New project</a>
      </div>
      <div class="footer-col">
        <h5>Reach out</h5>
        <a href="mailto:support@lightonpluslab.com">support@lightonpluslab.com</a>
        <a href="https://pf.kakao.com/_QxjxeiX/chat" target="_blank" rel="noopener">카카오톡 1:1 문의</a>
        <a href="tel:07080985734">070-8098-5734</a>
      </div>
    </div>
    <div class="footer-legal">
      <div>© <span id="year"></span> LightOn Plus Lab. All rights reserved. · <a href="privacy.html">개인정보처리방침</a> · <a href="terms.html">이용약관</a></div>
    </div>
    <div class="footer-biz">
      상호: 라이트온 플러스 랩 · 대표: 박승혁 · 사업자등록번호 229-15-70907 · 통신판매업신고: 제 2026-안양동안-0514 호 · 경기도 안양시 동안구 관평로 333, 6동 504호(관양동)
    </div>
  </div>
</footer>

<script src="app.js?v=20260815"></script>
</body>
</html>
"""

ARTICLES = [
{
"slug": "blog-paper-coupon-management",
"date": "2026-06-25",
"eyebrow": "Guide",
"title": "종이 쿠폰과 도장판, 스마트폰 하나로 관리하는 현실적인 방법",
"desc": "지갑 속에서 사라지는 종이 쿠폰·도장판·회수권을 잃어버리지 않고 관리하는 세 가지 방법을 비교하고, 만료일 관리 요령을 정리했습니다.",
"img": "img/onb-wallet.webp",
"img_alt": "스마트폰 지갑 속 쿠폰 일러스트",
"body": """
<p>카페 도장판, 마사지 회수권, 미용실 쿠폰, 세차장 선불권. 대부분 지갑이나 서랍 어딘가에 있지만, 정작 그 가게 앞에 서면 "몇 개 모았더라?"가 기억나지 않습니다. 소상공인 매장의 적립 수단은 여전히 종이가 압도적으로 많고, 종이는 잃어버리기 쉽고 만료일을 알려주지 않습니다. 이 글은 종이 적립 수단을 디지털로 옮겨 관리하는 세 가지 방법을 비교하고, 실제로 오래 유지되는 관리 습관을 정리한 것입니다.</p>
<h2>방법 1: 사진첩에 찍어두기</h2>
<p>가장 많이 쓰는 방법입니다. 쿠폰을 받자마자 사진을 찍어두면 최소한 분실은 막을 수 있습니다. 하지만 두 가지 문제가 남습니다. 첫째, 사진첩은 검색이 어렵습니다. 몇 달 지나면 음식 사진과 스크린샷 사이에서 쿠폰 사진을 찾는 것 자체가 일이 됩니다. 둘째, 상태 갱신이 안 됩니다. 도장을 하나 더 받았을 때 사진을 다시 찍지 않으면 사진 속 정보는 금방 낡은 정보가 됩니다.</p>
<h2>방법 2: 메모 앱에 적어두기</h2>
<p>메모 앱에 "○○카페 도장 7/10, 12월 말 만료"처럼 적는 방식입니다. 텍스트라 검색은 되지만, 이 방식의 약점은 알림입니다. 만료일이 다가와도 메모 앱은 먼저 말을 걸지 않습니다. 결국 만료된 뒤에 메모를 발견하는 일이 반복됩니다. 또 잔여 횟수를 매번 수동으로 고쳐 적어야 해서, 몇 주 지나면 기록과 실제가 어긋나기 시작합니다.</p>
<h2>방법 3: 전용 쿠폰 관리 앱</h2>
<p>쿠폰·적립 관리에 특화된 앱을 쓰는 방법입니다. 저희가 만든 <strong>쿠폰북</strong>을 예로 들면, 종이 쿠폰 관리에서 반복되는 문제를 다음과 같이 처리합니다.</p>
<ul>
<li><strong>등록 형태 선택</strong> — 도장판(횟수 적립형), 회수권(차감형), 금액권(잔액형)을 구분해 등록합니다. 유형이 다르면 관리 방식도 달라야 하기 때문입니다.</li>
<li><strong>원터치 사용 기록</strong> — 가게에서 도장을 받거나 회수권을 쓸 때 카드에서 버튼 한 번으로 기록합니다. 사용 내역이 시간순으로 남아 "언제 마지막으로 갔는지"도 확인됩니다.</li>
<li><strong>만료 임박 알림</strong> — 만료일 7일 전, 3일 전, 1일 전에 미리 알려줍니다. 종이 쿠폰이 해결하지 못하는 가장 큰 문제가 이 부분입니다.</li>
<li><strong>위치 기반 알림</strong> — 등록한 가게 근처에 가면 "여기 쿠폰 있어요"라고 알려주는 기능도 있습니다. 쿠폰은 기억나지 않는 순간에 쓸모가 생기기 때문입니다.</li>
</ul>
<h2>어떤 방법이든 지켜야 하는 두 가지</h2>
<h3>1. 받는 즉시 기록</h3>
<p>어떤 도구를 쓰든 "나중에 정리해야지"는 실패합니다. 계산대 앞에서 쿠폰을 받는 10초 안에 기록하는 것이 유일하게 유지되는 습관입니다. 도구 선택 기준도 여기서 나옵니다. 등록에 30초 이상 걸리는 도구는 결국 안 쓰게 됩니다.</p>
<h3>2. 만료일은 도구에게 맡기기</h3>
<p>만료일을 머리로 기억하려는 시도는 대부분 실패합니다. 기록할 때 만료일을 반드시 함께 적고, 알림은 도구가 보내게 하세요. 만료일이 적히지 않은 쿠폰은 가게에 전화해서라도 확인해 두는 편이 낫습니다. 소멸되는 적립금은 생각보다 큽니다.</p>
<div class="tip"><strong>쿠폰북으로 시작하기</strong> — 쿠폰북은 회원가입 없이 무료로 쓸 수 있고, 모든 데이터는 서버가 아닌 사용자 기기에만 저장됩니다. <a href="https://coupon.lightonpluslab.com/" target="_blank" rel="noopener">웹 버전</a>을 바로 열어 쓰거나, Google Play(출시 준비 중)에서 설치할 수 있습니다.</div>
"""
},
{
"slug": "blog-twa-play-store",
"date": "2026-07-03",
"eyebrow": "Dev Note",
"title": "웹앱을 구글 플레이에 올리기 — TWA 출시 실전 기록",
"desc": "PWA를 TWA로 감싸 Google Play에 출시하며 실제로 겪은 절차와 함정들 — assetlinks, AAB 서명, target API, 비공개 테스트 요건까지.",
"img": "img/couponbook-banner.webp",
"img_alt": "쿠폰북 구글 플레이 배너",
"body": """
<p>웹으로 만든 앱을 구글 플레이에 올리는 표준 방법은 TWA(Trusted Web Activity)입니다. 크롬이 주소창 없이 전체 화면으로 웹앱을 렌더링하고, 스토어에는 얇은 안드로이드 래퍼만 올라갑니다. 저희 쿠폰북을 실제로 TWA로 패키징해 Play Console에 제출하기까지의 과정을, 문서에는 잘 안 나오는 함정 위주로 기록합니다.</p>
<h2>전제: PWA 요건 갖추기</h2>
<p>TWA는 "설치형처럼 동작하는 웹앱"이 전제입니다. 최소 요건은 세 가지입니다. HTTPS로 서빙될 것, 올바른 manifest.json(이름·아이콘·display: standalone)이 있을 것, 서비스 워커로 오프라인에서도 기본 동작할 것. 이 요건은 스토어 심사 품질과도 직결됩니다. 단순 웹뷰 래핑 앱은 Play 정책상 반려될 수 있습니다.</p>
<h2>패키징: Bubblewrap</h2>
<p>구글이 제공하는 <strong>Bubblewrap CLI</strong>로 매니페스트 URL을 넘기면 안드로이드 프로젝트가 생성됩니다. JDK 17과 Android SDK가 필요합니다. 여기서 정하는 <strong>패키지명은 이후 변경이 불가능</strong>하니 처음부터 신중하게 정해야 합니다.</p>
<h2>함정 1: Digital Asset Links</h2>
<p>TWA가 주소창 없이 뜨려면 도메인이 앱을 신뢰한다는 선언이 필요합니다. <code>/.well-known/assetlinks.json</code>에 패키지명과 서명 키의 SHA-256 지문을 넣어 서빙해야 하며, 지문이 하나라도 틀리면 앱 상단에 주소창이 나타납니다. 업로드 키와 Play 앱 서명 키의 지문이 다를 수 있으므로 <strong>두 지문을 모두</strong> 넣어두는 것이 안전합니다.</p>
<h2>함정 2: gradle 빌드만으로는 서명이 안 된다</h2>
<p>Bubblewrap이 만들어 준 프로젝트를 <code>gradlew bundleRelease</code>로 직접 빌드하면 AAB가 나오지만, 이 파일은 <strong>서명되지 않은 상태</strong>입니다. Play Console에 올리면 "업로드된 모든 번들에 서명해야 합니다"라는 오류가 납니다. Bubblewrap의 build 명령은 빌드 후 서명까지 해 주지만, gradle을 직접 돌렸다면 jarsigner로 업로드 키스토어 서명을 별도로 해야 합니다. 서명 키는 분실하면 앱 업데이트가 영영 불가능해지니 반드시 백업하세요.</p>
<h2>함정 3: target API 레벨 시한</h2>
<p>Google Play는 매년 8월 31일을 기준으로 신규 앱·업데이트의 target API 최소 레벨을 올립니다. 2026년 기준으로는 API 36(Android 16)입니다. TWA 래퍼는 실질 로직이 없어서 target을 올려도 거의 영향이 없으므로, 빌드 시점에 미리 최신으로 올려 두는 것이 재빌드 수고를 줄입니다.</p>
<h2>함정 4: 개인 계정의 비공개 테스트 요건</h2>
<p>개인 개발자 계정으로 새 앱을 프로덕션에 올리려면, 먼저 <strong>테스터 12명 이상이 14일간 연속으로 옵트인한 비공개 테스트</strong>를 거쳐야 합니다. 앱이 완성됐어도 이 기간은 줄일 수 없으므로 출시 일정에 최소 2주를 미리 반영해야 합니다. 테스터 목록은 계정 단위로 재사용되니 한 번 모아두면 다음 앱에서도 씁니다.</p>
<h2>그 외 체크리스트</h2>
<ul>
<li>개인정보처리방침 공개 URL — 앱이 광고를 쓴다면 광고 데이터 수집 고지가 포함돼야 합니다.</li>
<li>데이터 보안 설문 — 광고 SDK·웹 광고가 있으면 "수집 없음"으로 내면 안 됩니다. 기기 ID·광고 상호작용의 수집/공유를 사실대로 신고해야 합니다.</li>
<li>스토어 등록정보 — 스크린샷은 최소 2장, 비율 제한(최대 2:1)이 있습니다. 피처 그래픽은 1024×500 고정입니다.</li>
<li>웹 업데이트는 즉시 반영 — TWA는 라이브 사이트를 로드하므로 웹만 고치면 스토어 재심사 없이 반영됩니다. 이것이 TWA의 가장 큰 운영상 장점입니다.</li>
</ul>
<p>정리하면: TWA 출시의 기술 난이도는 낮지만, 서명·자산 링크·스토어 정책이라는 세 가지 관문에서 대부분의 시간이 소요됩니다. 이 글의 함정 네 개를 미리 알고 시작하면 하루 안에 제출까지 갈 수 있습니다.</p>
"""
},
{
"slug": "blog-local-first-apps",
"date": "2026-06-18",
"eyebrow": "Product",
"title": "서버 없는 앱, '로컬 퍼스트'의 장점과 정직한 한계",
"desc": "회원가입도 서버도 없는 로컬 퍼스트 앱은 무엇이 좋고 무엇을 포기하는가. IndexedDB 기반 앱을 만들며 정리한 설계 기준.",
"img": "img/empty-ticket.webp",
"img_alt": "로컬에 저장되는 티켓 일러스트",
"body": """
<p>저희가 만드는 개인용 도구 앱들은 대부분 서버가 없습니다. 회원가입도 없고, 사용자가 입력한 데이터는 전부 사용자 기기 안(브라우저의 IndexedDB나 앱의 로컬 저장소)에만 저장됩니다. 이런 구조를 <strong>로컬 퍼스트(local-first)</strong>라고 부릅니다. 쿠폰북을 이 구조로 만들며 정리한, 로컬 퍼스트의 실질적인 장점과 정직한 한계를 공유합니다.</p>
<h2>장점 1: 개인정보 문제가 구조적으로 사라진다</h2>
<p>서버가 없으면 유출될 서버도 없습니다. 사용자가 어떤 가게에 다니는지, 얼마짜리 회수권을 쓰는지는 꽤 사적인 정보인데, 이 정보가 개발자에게조차 전송되지 않습니다. 개인정보처리방침이 짧고 명확해지고, 사용자에게 "우리는 당신의 데이터를 볼 수 없습니다"라고 사실대로 말할 수 있습니다. 신뢰를 마케팅이 아니라 구조로 증명하는 방식입니다.</p>
<h2>장점 2: 오프라인에서 그냥 동작한다</h2>
<p>데이터가 기기에 있으니 네트워크가 없어도 앱이 완전하게 동작합니다. 지하 주차장에서도, 비행기에서도 도장 개수는 확인됩니다. 서버 왕복이 없으니 반응 속도도 일관되게 빠릅니다.</p>
<h2>장점 3: 운영 비용이 0에 수렴한다</h2>
<p>1인 스튜디오에게 중요한 부분입니다. 서버 비용, DB 백업, 보안 패치, 장애 대응이 없습니다. 무료 앱을 오래 유지하려면 유지비가 0이어야 하고, 로컬 퍼스트는 그것을 가능하게 합니다. 사용자가 10만 명이 되어도 서버비는 그대로 0원입니다.</p>
<h2>한계 1: 기기를 바꾸면 데이터가 따라가지 않는다</h2>
<p>가장 큰 트레이드오프입니다. 데이터가 기기에만 있으므로, 폰을 바꾸거나 브라우저 데이터를 삭제하면 기록이 사라질 수 있습니다. 완화 장치는 두 가지입니다. 첫째, <strong>수동 백업/복원</strong> — 쿠폰북은 JSON 파일로 내보내고 새 기기에서 불러올 수 있게 했습니다. 둘째, <strong>영속 저장소 요청</strong> — 브라우저에 "이 데이터는 지우지 말라"고 요청하는 Persistent Storage API를 사용합니다. 그래도 클라우드 동기화만큼 매끄럽지는 않습니다. 이 부분은 숨기지 말고 앱 안에서 먼저 안내해야 한다고 생각합니다. 쿠폰북이 첫 쿠폰 등록 직후에 백업을 권하는 이유입니다.</p>
<h2>한계 2: 여러 기기 동시 사용이 안 된다</h2>
<p>폰과 태블릿에서 같은 데이터를 보려면 동기화 서버가 필요합니다. 로컬 퍼스트로 시작한 앱이 성장하면 결국 "선택적 동기화"를 요구받는데, 이때는 종단간 암호화 동기화 같은 절충안을 검토하게 됩니다. 처음부터 모든 것을 만들기보다, 사용자가 실제로 요구할 때 추가하는 편이 낫습니다.</p>
<h2>어떤 앱에 로컬 퍼스트가 맞는가</h2>
<ul>
<li><strong>맞는 경우</strong> — 개인 기록·관리 도구(쿠폰, 가계부, 습관, 메모), 데이터가 사적이고 협업이 필요 없는 앱.</li>
<li><strong>맞지 않는 경우</strong> — 여러 사람이 같은 데이터를 보는 앱(팀 협업, 커뮤니티), 기기 간 실시간 동기화가 핵심 가치인 앱.</li>
</ul>
<p>로컬 퍼스트는 "서버를 만들 돈이 없어서"가 아니라, 개인 도구라는 제품 성격에 가장 정직한 구조라서 선택하는 것입니다. 대신 데이터 소실 리스크를 사용자에게 투명하게 알리고 백업 수단을 제공하는 것까지가 설계의 일부입니다.</p>
"""
},
{
"slug": "blog-two-week-mvp",
"date": "2026-06-10",
"eyebrow": "Studio",
"title": "1인 스튜디오가 2주 만에 MVP를 출시하는 프로세스",
"desc": "Brief → Prototype → Launch → Improve. LightOn Plus Lab이 실제로 쓰는 4단계 MVP 프로세스와 단계별 산출물, 그리고 중단 기준.",
"img": "img/onb-stamps.webp",
"img_alt": "단계별 진행 일러스트",
"body": """
<p>LightOn Plus Lab은 아이디어를 2~6주 안에 검증 가능한 제품으로 만드는 것을 원칙으로 합니다. 빠르게 만드는 것 자체가 목적이 아니라, <strong>시장의 반응을 확인하기 전까지 투입 비용을 최소화</strong>하는 것이 목적입니다. 실제로 쓰는 4단계 프로세스를 단계별 산출물과 함께 공개합니다.</p>
<h2>1주차 전반: Brief — 문제 정의</h2>
<p>만들기 전에 세 문장을 씁니다. ① 누가(구체적인 한 사람) ② 어떤 순간에 어떤 불편을 겪고 ③ 이 제품이 그 순간을 어떻게 바꾸는가. 예를 들어 쿠폰북의 브리프는 이랬습니다. "카페 도장판을 모으는 직장인이 / 가게 앞에서 몇 개 모았는지 기억나지 않을 때 / 폰에서 3초 안에 확인하게 한다." 이 단계의 산출물은 기능 목록이 아니라 <strong>하지 않을 것 목록</strong>입니다. MVP에서 뺄 것을 정하는 것이 이 단계의 전부입니다.</p>
<h2>1주차 후반: Prototype — 동작하는 최소 제품</h2>
<p>디자인 시안을 만들지 않고 바로 동작하는 화면을 만듭니다. AI 코딩 도구를 적극적으로 쓰되, 아키텍처 결정(데이터 구조, 상태 관리, 저장 방식)은 사람이 먼저 내립니다. 이 순서가 바뀌면 나중에 고치는 비용이 훨씬 큽니다. 산출물은 "핵심 시나리오 1개가 끝까지 동작하는 앱"입니다. 쿠폰북이라면 '쿠폰 등록 → 사용 → 완성'이 끝까지 되는 상태입니다.</p>
<h2>2주차: Launch — 실제 배포</h2>
<p>내부 완성도를 높이는 대신 실제 사용자가 닿는 곳에 내보냅니다. 웹앱이면 도메인에 배포하고, 스토어가 필요하면 TWA로 감싸 비공개 테스트 트랙에 올립니다. 이 단계의 산출물은 <strong>설치(접속) 가능한 링크</strong>와 <strong>피드백 수집 채널</strong>입니다. 완벽하지 않은 상태로 내보내는 것이 핵심인데, 사용자는 우리가 걱정하는 부분이 아니라 전혀 다른 부분에서 걸려 넘어지기 때문입니다.</p>
<h2>이후: Improve — 데이터로 반복</h2>
<p>출시 후에는 두 가지 신호만 봅니다. ① 재방문 — 한 번 쓰고 마는가, 다시 오는가. ② 완주율 — 핵심 시나리오를 끝까지 마치는가. 기능 추가 요청은 이 두 신호가 건강할 때만 받습니다. 신호가 나쁘면 기능을 더하는 것이 아니라 핵심 시나리오를 고칩니다.</p>
<h2>중단 기준 — 가장 중요한 부분</h2>
<p>2주 프로세스의 진짜 가치는 빨리 만드는 것이 아니라 <strong>빨리 접을 수 있다는 것</strong>입니다. 저희 기준은 단순합니다. 출시 4주 후에도 만든 사람 본인이 그 앱을 일상적으로 쓰지 않으면 접습니다. 본인도 안 쓰는 도구를 남이 쓸 가능성은 거의 없기 때문입니다. 접은 프로젝트의 코드는 다음 프로젝트의 부품이 되므로, 실패해도 투입 비용의 상당 부분이 회수됩니다.</p>
<div class="tip"><strong>외주가 아니라 공동 실험</strong> — 이 프로세스로 외부 프로젝트도 진행합니다. 아이디어 검증이 필요하다면 <a href="contact.html">Contact</a>로 문의해 주세요. 2주 안에 동작하는 프로토타입으로 대화를 시작합니다.</div>
"""
},
{
"slug": "blog-momoi-call-summary",
"date": "2026-06-05",
"eyebrow": "Product",
"title": "통화가 끝나면 요약이 남는다 — 모모아이(momoi) 활용 가이드",
"desc": "AI 통화 요약 앱 모모아이를 잘 쓰는 법. 어떤 통화에 효과적인지, 요약 품질을 높이는 팁, 그리고 프라이버시 원칙.",
"body": """
<p><strong>모모아이(momoi)</strong>는 통화 내용을 AI가 요약해 기록으로 남겨주는 앱입니다. 통화는 업무에서 가장 많은 결정이 오가는 채널이지만, 끊고 나면 "그래서 언제까지 뭘 하기로 했지?"만 남는 경우가 많습니다. 모모아이는 그 간극을 메우기 위해 만들었습니다. 이 글은 모모아이를 실제로 잘 쓰는 방법을 정리한 가이드입니다.</p>
<h2>어떤 통화에서 효과가 큰가</h2>
<ul>
<li><strong>업무 협의 전화</strong> — 일정, 금액, 담당, 다음 액션이 오가는 통화. 요약의 가치가 가장 큰 영역입니다.</li>
<li><strong>고객 상담·문의 응대</strong> — 같은 고객과의 이전 통화 내용을 다시 확인할 수 있어 응대 품질이 올라갑니다.</li>
<li><strong>부동산·계약 관련 통화</strong> — 조건이 구두로 오가는 통화는 기록 자체가 자산이 됩니다.</li>
<li><strong>병원 예약·행정 전화</strong> — 준비물, 날짜, 위치 같은 세부 정보를 받아 적을 필요가 없어집니다.</li>
</ul>
<h2>요약 품질을 높이는 세 가지 습관</h2>
<h3>1. 통화 끝에 한 줄 정리를 말하기</h3>
<p>끊기 전에 "그럼 정리하면, 금요일까지 견적서 보내주시고 저는 검토 후 월요일에 연락드릴게요"처럼 한 문장으로 정리하는 습관을 들이면, AI 요약의 정확도가 눈에 띄게 올라갑니다. 사람에게도 AI에게도 좋은 습관입니다.</p>
<h3>2. 요약은 통화 직후에 확인</h3>
<p>요약이 기억과 다른 부분이 있는지 통화 직후 30초만 확인하세요. AI 요약은 대체로 정확하지만 숫자·고유명사는 틀릴 수 있습니다. 기억이 생생할 때 바로잡는 것이 가장 쌉니다.</p>
<h3>3. 중요한 통화는 태그·메모로 묶기</h3>
<p>거래처별, 프로젝트별로 통화 기록이 묶여 있으면 다음 통화 전에 훑어보는 것만으로 맥락이 복원됩니다. "지난번에 뭐라고 하셨죠?"라고 물을 일이 없어집니다.</p>
<h2>프라이버시 원칙</h2>
<p>통화는 매우 사적인 데이터입니다. 모모아이는 다음 원칙을 지킵니다. 요약 생성에 필요한 최소한의 처리만 수행하고, 통화 기록의 소유권은 전적으로 사용자에게 있으며, 사용자가 원하면 기록을 완전히 삭제할 수 있습니다. 또한 상대방 동의가 필요한 녹음 관련 법규는 국가·지역마다 다르므로, 업무 통화에서는 상대에게 기록 사실을 알리는 것을 권장합니다.</p>
<h2>이런 분께 권합니다</h2>
<p>하루에 업무 전화를 세 통 이상 하는 분, 통화 후 메모를 옮겨 적는 데 시간을 쓰고 있는 분, "말했다 / 안 했다"로 곤란해진 경험이 있는 분. 모모아이에 대한 더 자세한 소개는 <a href="momoi.html">모모아이 페이지</a>에서 확인할 수 있습니다.</p>
"""
},
{
"slug": "blog-pwa-vs-native",
"date": "2026-05-28",
"eyebrow": "Dev Note",
"title": "PWA냐 네이티브냐 — 1인 개발 관점의 선택 기준",
"desc": "혼자 만들고 혼자 운영하는 앱이라면 어떤 스택을 골라야 할까. PWA와 네이티브(Flutter 포함)를 유지비 관점에서 비교합니다.",
"body": """
<p>"앱을 만들려면 뭘로 만들어야 하나요?"라는 질문에 대한 정답은 팀 규모에 따라 다릅니다. 이 글은 <strong>혼자 만들고 혼자 운영하는</strong> 1인 개발 관점에서 PWA(웹앱)와 네이티브 계열(Flutter 등 크로스플랫폼 포함)을 비교합니다. 저희는 두 방식 모두로 제품을 출시해 봤습니다. 쿠폰북은 PWA+TWA로, 라이트온 AI 노트는 Flutter로 만들었습니다.</p>
<h2>비교 기준은 '만드는 비용'이 아니라 '유지하는 비용'</h2>
<p>1인 개발의 병목은 첫 출시가 아니라 그 이후입니다. 앱이 3개, 5개로 늘어나면 유지보수 시간이 전부를 결정합니다. 그래서 비교 축을 이렇게 잡았습니다.</p>
<table>
<tr><th>기준</th><th>PWA (+TWA)</th><th>Flutter 네이티브</th></tr>
<tr><td>업데이트 배포</td><td>웹 배포 즉시 반영. 스토어 재심사 불필요</td><td>매번 스토어 심사 통과 필요</td></tr>
<tr><td>플랫폼 커버리지</td><td>웹·안드로이드는 강함. iOS는 설치 UX가 약함</td><td>iOS·안드로이드 동등하게 강함</td></tr>
<tr><td>기기 기능 접근</td><td>카메라·위치·알림 등 표준 API는 충분. 통화·백그라운드 등 깊은 기능은 제한</td><td>사실상 전부 접근 가능</td></tr>
<tr><td>성능 체감</td><td>도구 앱 수준에서는 차이 없음</td><td>애니메이션 무거운 화면에서 우위</td></tr>
<tr><td>빌드 인프라</td><td>없음(정적 호스팅이면 끝)</td><td>SDK·서명·스토어 파이프라인 유지 필요</td></tr>
</table>
<h2>PWA를 고르는 경우</h2>
<p>기록·조회 중심의 도구 앱이라면 PWA가 압도적으로 유리합니다. 쿠폰북이 전형적인 예입니다. 데이터는 IndexedDB에 로컬 저장하고, 서비스 워커로 오프라인을 지원하고, 스토어 노출이 필요해지면 TWA로 감싸면 됩니다. 무엇보다 버그 수정이 <strong>웹 배포 한 번으로 모든 사용자에게 즉시</strong> 반영된다는 점이 1인 운영에서는 결정적입니다.</p>
<h2>네이티브(Flutter)를 고르는 경우</h2>
<p>다음 중 하나라도 해당하면 네이티브로 갑니다. ① 통화, 백그라운드 오디오, 위젯, 시스템 연동처럼 웹이 닿지 못하는 기능이 핵심일 때 ② iOS 사용자가 주 타깃일 때(iOS의 PWA 설치 경험은 여전히 불친절합니다) ③ 오프라인에서 무거운 미디어 처리가 필요할 때. 모모아이가 통화라는 시스템 기능을 다루기 때문에 네이티브 계열인 것이 그 예입니다.</p>
<h2>실무 요약</h2>
<ul>
<li>확신이 없으면 <strong>PWA로 시작</strong>하세요. 검증에 실패해도 매몰 비용이 가장 작고, 성공하면 TWA로 스토어 진출이 가능합니다.</li>
<li>시스템 기능(통화·백그라운드·위젯)이 제품의 핵심이면 처음부터 네이티브로 가세요. 나중에 갈아타는 비용이 더 큽니다.</li>
<li>어느 쪽이든 <strong>데이터 계층을 UI에서 분리</strong>해 두면, 훗날 스택을 옮겨도 도메인 로직은 재사용됩니다.</li>
</ul>
"""
},
{
"slug": "blog-notification-ux",
"date": "2026-05-20",
"eyebrow": "Design",
"title": "알림은 몇 번이 적당한가 — 만료 임박 알림을 설계하며 배운 것",
"desc": "쿠폰 만료 알림을 D-7/D-3/D-1 세 번으로 정한 이유. 유용함과 성가심 사이에서 알림 UX를 설계하는 원칙들.",
"img": "img/onb-bell.webp",
"img_alt": "만료 알림 일러스트",
"body": """
<p>알림은 앱이 사용자에게 먼저 말을 걸 수 있는 거의 유일한 수단이면서, 앱 삭제의 가장 큰 원인이기도 합니다. 쿠폰북의 만료 임박 알림을 설계하면서 "언제, 몇 번, 어떤 말로 알릴 것인가"를 정해야 했습니다. 그 과정에서 정리된 원칙들을 공유합니다.</p>
<h2>왜 D-7 / D-3 / D-1 세 번인가</h2>
<p>만료 알림의 목적은 "알게 하는 것"이 아니라 <strong>"방문 계획을 세우게 하는 것"</strong>입니다. 그 관점에서 시점별 역할이 다릅니다.</p>
<ul>
<li><strong>D-7</strong> — 계획 알림. "이번 주 안에 갈 일 있으면 들르자"고 일정에 끼워 넣을 수 있는 여유가 있는 시점입니다.</li>
<li><strong>D-3</strong> — 결정 알림. 주말·평일 중 언제 갈지 정하게 만드는 시점입니다. D-7 알림을 놓친 사용자를 위한 보험이기도 합니다.</li>
<li><strong>D-1</strong> — 마지막 기회 알림. 여기서부터는 유용함보다 긴박함이 커지므로, 이보다 잦으면 성가심으로 넘어갑니다.</li>
</ul>
<p>당일(D-0) 알림은 뺐습니다. 당일에 처음 알게 되면 대부분 실행이 불가능해서, "알려줬는데 못 쓴" 나쁜 경험만 남기기 때문입니다. 알림은 실행 가능성이 있을 때만 가치가 있습니다.</p>
<h2>원칙 1: 알림마다 실행 가능한 다음 행동이 있어야 한다</h2>
<p>"쿠폰이 곧 만료됩니다"는 정보이고, "태양 찜질방 이용권이 3일 뒤 만료돼요 — 8회 남음"은 행동을 부릅니다. 남은 횟수·잔액을 알림 문구에 넣은 이유입니다. 사용자가 알림만 보고 갈지 말지를 결정할 수 있어야 합니다.</p>
<h2>원칙 2: 기본값은 보수적으로, 제어권은 사용자에게</h2>
<p>쿠폰북은 알림 시점(D-7/3/1)을 설정에서 조절할 수 있게 했습니다. 알림을 늘리는 것은 사용자의 선택이어야 하고, 기본값은 "이 정도면 놓치지 않는다"의 최소치여야 합니다. 기본값이 공격적인 앱은 처음 며칠은 참아주지만 결국 알림 자체가 꺼집니다. 알림 권한이 꺼진 앱은 사실상 목소리를 잃은 앱입니다.</p>
<h2>원칙 3: 푸시가 필요 없는 알림은 푸시를 쓰지 않는다</h2>
<p>모든 알림이 잠금화면까지 갈 필요는 없습니다. 쿠폰북은 위치 기반 "근처 가게" 안내를 앱 사용 중 팝업으로만 보여줍니다. 지나가다 우연히 열었을 때 도움이 되는 정보이지, 하던 일을 끊고 알려야 할 정보는 아니기 때문입니다. 알림의 등급(잠금화면 푸시 > 인앱 배너 > 배지)을 정보의 긴급도와 맞추는 것만으로 성가심의 대부분이 사라집니다.</p>
<h2>측정: 알림이 일하는지 어떻게 아는가</h2>
<p>알림 클릭률만 보면 안 됩니다. 저희가 보는 것은 두 가지입니다. ① 알림 후 48시간 내 해당 쿠폰의 사용 기록이 생겼는가(알림 → 실제 방문 전환) ② 알림 설정을 끄는 사용자 비율이 늘고 있는가(성가심의 조기 신호). 첫 번째가 오르고 두 번째가 평평하면 알림이 일을 하고 있는 것입니다.</p>
"""
},
{
"slug": "blog-ai-assisted-development",
"date": "2026-05-12",
"eyebrow": "Dev Note",
"title": "AI 코딩 도구로 실제 제품 만들기 — 속도는 얻고 품질은 지키는 법",
"desc": "LLM 코딩 도구를 실제 제품 개발에 쓰면서 정한 규칙들. 어디까지 맡기고, 무엇은 사람이 쥐고 있어야 하는가.",
"img": "img/app-home.webp",
"img_alt": "AI로 만든 쿠폰북 앱 홈 화면",
"body": """
<p>LightOn Plus Lab의 제품들은 AI 코딩 도구를 적극적으로 활용해 만들어집니다. 2주 MVP 프로세스가 가능한 이유의 절반은 AI입니다. 하지만 "AI가 다 짜줬다"는 코드로 제품을 운영해 보면, 속도의 대가로 품질 부채가 쌓이는 지점이 분명히 보입니다. 실제 제품 몇 개를 AI와 함께 만들고 운영하며 정한 규칙들입니다.</p>
<h2>사람이 쥐고 있어야 하는 것</h2>
<h3>1. 데이터 구조와 아키텍처 결정</h3>
<p>저장 스키마, 상태 관리 방식, 모듈 경계 같은 구조적 결정은 사람이 먼저 내리고 AI에게는 그 안에서 구현을 맡깁니다. 구조가 잘못된 채 쌓인 코드는 AI로도 빠르게 못 고칩니다. 쿠폰북은 core/data/domain/services/ui/views의 계층 규칙을 문서로 먼저 정해 두고, AI에게 코드를 요청할 때마다 이 규칙을 함께 줬습니다. 결과물의 일관성이 완전히 달라집니다.</p>
<h3>2. 요구사항의 경계</h3>
<p>AI는 요청을 넘어서 "친절하게" 기능을 더하는 경향이 있습니다. MVP에서는 이것이 독입니다. "하지 않을 것 목록"을 프롬프트에 명시하는 것이 코드 리뷰 시간을 가장 크게 줄였습니다.</p>
<h2>AI에게 맡기면 압도적으로 빠른 것</h2>
<ul>
<li><strong>보일러플레이트와 반복 패턴</strong> — CRUD, 폼 검증, 설정 화면 같은 정형 코드.</li>
<li><strong>테스트 코드 초안</strong> — 요구사항을 주면 경계값·에러 케이스를 사람보다 꼼꼼하게 나열합니다. 단, 통과 기준은 사람이 검토해야 합니다.</li>
<li><strong>플랫폼 지식이 필요한 작업</strong> — 스토어 정책, 매니페스트 설정, 브라우저 API의 호환성 처리처럼 문서를 뒤져야 하는 일.</li>
<li><strong>일관된 리팩터링</strong> — 규칙을 정해주면 수십 개 파일에 동일한 변경을 지치지 않고 적용합니다.</li>
</ul>
<h2>품질을 지키는 두 개의 안전망</h2>
<h3>안전망 1: 요구사항 기반 테스트</h3>
<p>AI가 짠 코드는 AI가 짠 테스트가 아니라 <strong>요구사항에서 도출한 테스트</strong>로 검증합니다. "구현을 보고 만든 테스트"는 구현의 버그까지 통과시키기 때문입니다. 쿠폰북은 도메인 로직(잔여 계산, 만료 판정, 정렬)에 단위 테스트를 두고, 화면 흐름은 스모크 E2E 하나로 지킵니다. 1인 프로젝트에서 유지 가능한 최소한이면서, AI에게 대담한 변경을 시킬 수 있는 근거가 됩니다.</p>
<h3>안전망 2: 배포 전 실기기 확인</h3>
<p>AI는 코드가 돌아가는지는 확인해 줘도 <strong>제품이 말이 되는지</strong>는 모릅니다. 배포 전에 실제 폰에서 핵심 시나리오를 한 번 걷는 것은 사람의 일로 남겨뒀습니다. 이 10분이 사용자 신뢰를 지키는 마지막 관문입니다.</p>
<h2>정리</h2>
<p>AI 코딩 도구는 "개발자를 대체하는 것"이 아니라 <strong>1인 스튜디오에게 팀의 손을 빌려주는 것</strong>에 가깝습니다. 구조와 경계와 검증 기준을 사람이 쥐고 있는 한, 속도는 몇 배가 되고 품질은 지켜집니다. 반대로 그 세 가지를 놓으면, 빠르게 만든 만큼 빠르게 무너집니다.</p>
"""
},
# Raw string preserves the literal backslash-n sequence in the code sample.
{
"slug": "blog-lyrics-alignment-drift",
"date": "2026-08-13",
"eyebrow": "Dev Note",
"title": "가사 싱크가 최대 16초 밀린 이유 — 세지 말고 대조하라",
"desc": "가라오케 가사가 곡 후반으로 갈수록 밀렸고, 한국어 곡에서 유독 심했습니다. 원인은 타임스탬프가 아니라 단어를 세는 방식이었습니다. 비례식 추정을 문자 오프셋 대조로 바꾼 기록.",
"img": "img/proj-songbit.jpg",
"img_alt": "송빗 가라오케 가사 화면",
"body": r"""
<p><a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.songbit" target="_blank" rel="noopener">송빗</a>은 AI가 만든 곡을 가라오케처럼 한 줄씩 하이라이트하며 보여줍니다. 그런데 곡 앞부분은 잘 맞다가 뒤로 갈수록 가사가 밀리는 문제가 있었습니다. 그리고 이상하게도, <strong>한국어 곡에서만 심했습니다.</strong></p>
<p>원인은 타임스탬프가 부정확해서가 아니었습니다. 우리가 그 타임스탬프를 가사에 갖다 붙이는 방식이 틀려 있었습니다.</p>
<h2>실측: 얼마나 어긋났나</h2>
<p>한 곡씩 줄 단위로 오차를 재봤습니다.</p>
<table>
<thead><tr><th>언어</th><th>1초 이상 어긋난 줄</th><th>최대 오차</th></tr></thead>
<tbody>
<tr><td>한국어</td><td><strong>40줄 중 24줄 (60%)</strong></td><td><strong>16.71초</strong></td></tr>
<tr><td>영어</td><td>46줄 중 3줄</td><td>—</td></tr>
</tbody>
</table>
<p>16.71초는 가라오케로서는 완전히 망가진 수준입니다. 그런데 이 표에서 가장 중요한 정보는 최대 오차가 아니라 <strong>언어에 따라 증상이 다르다</strong>는 사실입니다. 타임스탬프 자체가 부정확했다면 언어를 가리지 않아야 합니다. 언어를 탄다는 건 텍스트를 쪼개는 방식에 문제가 있다는 신호입니다.</p>
<h2>원인 1 — 비례식으로 추정하고 있었다</h2>
<p>기존 코드는 가사 줄의 시작 시각을 이렇게 구했습니다.</p>
<pre><code>토큰_인덱스 = (지금까지_누적_단어수 / 전체_단어수) × 전체_토큰수</code></pre>
<p>"전체의 30% 지점에 있는 단어라면 토큰도 30% 지점에 있겠지"라는 발상입니다. 이 식은 <strong>단어와 토큰이 1:1로 대응한다</strong>는 가정 위에서만 성립합니다.</p>
<p>그리고 그 가정을 검증하는 코드는 어디에도 없었습니다. 가정이 깨져도 예외가 나지 않고, 그냥 조금씩 어긋난 값이 나옵니다. 곡이 길수록 오차가 커지는 것도 이 때문입니다. 비율로 계산하니 뒤로 갈수록 벌어집니다.</p>
<h2>원인 2 — 토큰 안에 태그가 섞여 있었다</h2>
<p>음악 생성 API가 돌려주는 단어별 타임스탬프(<code>alignedWords</code>)를 실제로 열어보면 이렇게 생겼습니다.</p>
<pre><code>{ word: '[Female ',        startS: 0.957 }
{ word: 'Vocalist]\n\n\n',   startS: 1.1   }
{ word: '[Intro]\n하늘을 ',   startS: 1.287 }   ← 섹션 태그 + 첫 가사가 한 토큰
{ word: '나는 ',             startS: 1.8   }</code></pre>
<p>두 가지가 눈에 띕니다.</p>
<p>첫째, <code>word</code>에는 <strong>공백과 개행이 그대로 들어 있습니다.</strong> 깔끔하게 잘린 단어가 아닙니다.</p>
<p>둘째, <code>[Female Vocalist]</code>나 <code>[Intro]</code> 같은 <strong>보컬·섹션 태그가 토큰에 섞여 있고</strong>, 심지어 태그와 첫 가사 단어가 같은 토큰에 들어옵니다.</p>
<p>우리 클라이언트는 화면에 표시할 때 이 태그들을 걷어내고 세고 있었습니다. 그래서 <strong>클라이언트는 145단어, API는 147토큰.</strong> 두 개 차이입니다. 그런데 그 두 개가 비례식을 타고 곡 전체에 퍼집니다.</p>
<p>한국어가 유독 심했던 것도 여기서 설명됩니다. 어절을 쪼개는 방식이 생성 모델의 토크나이저와 더 크게 어긋나서, 단어 수와 토큰 수의 격차가 영어보다 컸습니다.</p>
<h2>해결 — 세는 걸 그만두고 대조한다</h2>
<p>돌파구는 토큰 배열을 다시 들여다보다 나왔습니다. <strong>토큰의 <code>word</code>들을 순서대로 그냥 이어붙이면 원본 가사가 그대로 복원됩니다.</strong></p>
<pre><code>aligned.map(t =&gt; t.word).join('')   // → 원본 가사 전체</code></pre>
<p>즉 토큰 배열은 별개의 데이터가 아니라 <strong>가사 문자열을 잘라놓은 것</strong>일 뿐입니다. 그렇다면 "이 줄이 몇 번째 단어인가"를 셀 이유가 없습니다. <strong>"이 줄이 문자열의 몇 번째 글자에서 시작하는가"</strong>를 찾으면 됩니다. 문자 오프셋만 알면 토큰은 역산됩니다.</p>
<p>세는 방식은 앞에서 하나만 어긋나도 뒤가 전부 밀립니다. 대조 방식은 각 줄이 독립적으로 자기 위치를 찾으므로 오차가 누적되지 않습니다.</p>
<p>구현에서 걸린 지점은 셋이었습니다.</p>
<h3>1. 공백 정규화와 오프셋 역매핑</h3>
<p>토큰의 개행·연속 공백을 하나로 접어야 화면의 가사 줄과 문자열 비교가 됩니다. 그런데 접고 나면 원본 위치를 잃어버립니다. 그래서 정규화하면서 <em>정규화된 인덱스 → 원본 인덱스</em> 지도를 같이 만듭니다.</p>
<pre><code>function normalizeWithOffsets(text: string):
  { text: string; originalOffsets: number[] }</code></pre>
<h3>2. 반복되는 후렴</h3>
<p>후렴이 세 번 나오는 곡에서 그냥 <code>indexOf</code>를 쓰면 세 줄 모두 첫 번째 위치를 가리킵니다. 그래서 이전 매칭이 끝난 지점을 커서로 들고, 그 뒤에서만 찾습니다.</p>
<pre><code>let matchIndex = normalizedTokens.text.indexOf(line, cursor)
if (matchIndex &lt; 0) matchIndex = normalizedTokens.text.indexOf(line)  // 폴백
...
cursor = matchIndex + line.length</code></pre>
<h3>3. 오프셋 → 토큰 인덱스</h3>
<p>토큰별 누적 끝 오프셋 배열을 만들어두고 이진 탐색으로 찾습니다. 그 토큰의 <code>startS</code>가 그 줄의 시작 시각입니다.</p>
<p>여기에 방어 두 가지를 더 얹었습니다. 타임스탬프가 뒤집혀 오는 경우가 있어 마지막에 <strong>단조 증가로 보정</strong>하고, 매칭에 실패한 줄은 전체를 버리지 않고 <strong>그 줄만 폴백 값을 유지</strong>합니다.</p>
<h2>결과</h2>
<table>
<thead><tr><th></th><th>수정 전</th><th>수정 후</th></tr></thead>
<tbody>
<tr><td>한국어</td><td>40줄 중 24줄 오차</td><td><strong>40 / 40 매칭</strong></td></tr>
<tr><td>영어</td><td>46줄 중 3줄 오차</td><td><strong>46 / 46 매칭</strong></td></tr>
</tbody>
</table>
<p>정렬 로직은 부수 효과 없는 순수 함수로 분리했습니다. 웹은 <code>lib/lyrics-alignment.ts</code>, 앱은 같은 로직을 Dart로 포팅했습니다. 덕분에 <strong>같은 입력에 대해 웹과 앱이 같은 값을 내는지</strong>를 테스트로 확인할 수 있습니다(첫 줄 1.287초로 양쪽 일치).</p>
<p>테스트는 실제로 문제가 됐던 형태를 그대로 케이스로 만들었습니다 — 태그가 섞인 토큰, 반복 후렴, 역순 타임스탬프, 타임스탬프가 아예 없는 경우.</p>
<h2>남는 교훈</h2>
<p><strong>"비례해서 추정"은 숨은 가정이다.</strong> 두 시퀀스의 길이가 같다는 가정이 식 안에 감춰져 있습니다. 이런 코드는 가정이 깨져도 예외를 던지지 않고 조용히 틀린 값을 냅니다. 최소한 두 길이가 다를 때 로그라도 남겼다면 훨씬 일찍 찾았을 겁니다.</p>
<p><strong>외부 API의 토큰은 내 토크나이저와 다르다.</strong> 당연한 말 같지만, 양쪽 개수를 실제로 찍어보기 전까지는 대체로 같다고 가정하고 짭니다. 이어붙였을 때 원본이 복원되는지부터 확인하면 세는 방식 대신 대조 방식으로 갈 길이 열립니다.</p>
<p><strong>언어마다 증상이 다르면 텍스트 분할을 의심하라.</strong> 이번 건에서 가장 빨랐던 단서가 "한국어만 심하다"였습니다. 로직이 언어를 탈 이유가 없는데 타고 있다면, 문제는 로직이 아니라 로직에 들어가는 텍스트가 쪼개진 방식입니다.</p>
<div class="tip"><strong>송빗</strong> — 장르·분위기·키워드만 고르면 AI가 가사부터 보컬 완곡까지 만들어 줍니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.songbit" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-why-summary-is-not-memory",
"date": "2026-08-13",
"eyebrow": "Product",
"title": "강의를 녹음하고 요약해도 왜 안 외워질까",
"desc": "전사와 요약은 이제 흔한 기능이 됐습니다. 그런데 노트가 깔끔할수록 다시 안 보게 되는 역설이 있습니다. 망각 곡선과 간격 반복이 그 빈틈을 어떻게 메우는지 정리했습니다.",
"img": "img/proj-lecture.jpg",
"img_alt": "라이트온 AI 노트 강의 녹음 화면",
"body": """
<p>녹음을 넣으면 텍스트가 나오고, 텍스트를 넣으면 요약이 나옵니다. 몇 년 전만 해도 제품의 차별점이던 기능이 지금은 기본기가 됐습니다.</p>
<p>그런데 이 기능들을 다 갖춘 노트를 쓰면서도, 시험 전날 노트를 펴고 "이걸 내가 들었었나" 싶은 경험은 그대로입니다. 도구는 좋아졌는데 결과가 그만큼 좋아지지 않는 구간이 있습니다. 그 구간이 어디인지, 왜 생기는지 정리해 봤습니다.</p>
<h2>잘 정리된 노트가 오히려 위험한 이유</h2>
<p>요약이 암기로 이어지지 않는 데는 두 가지 서로 다른 실패가 겹쳐 있습니다.</p>
<h3>1. 익숙함을 이해로 착각한다</h3>
<p>잘 정리된 요약을 읽으면 술술 읽힙니다. 그 매끄러움이 "나는 이걸 안다"는 느낌을 만듭니다. 하지만 읽으면서 드는 그 느낌은 <strong>알아보는 것</strong>이지 <strong>꺼내는 것</strong>이 아닙니다.</p>
<p>시험장에서 요구되는 건 후자입니다. 백지 상태에서 꺼내야 하는데, 연습한 건 눈앞에 답이 있는 상태에서 고개를 끄덕이는 일이었던 겁니다. 노트가 깔끔할수록 이 착각은 더 강해집니다. 읽기가 편할수록 "다시 볼 필요 없겠다"고 판단하게 되니까요.</p>
<h3>2. 다시 볼 시점을 아무도 정해주지 않는다</h3>
<p>배운 직후부터 기억은 빠르게 떨어집니다. 그 감소는 완만하지 않고, 초반이 가장 가파릅니다. 그래서 "언젠가 복습해야지"는 대부분 늦습니다. 이미 상당 부분이 사라진 뒤에 처음부터 다시 배우는 셈이 됩니다.</p>
<p>여기서 진짜 문제는 의지가 아니라 <strong>스케줄링</strong>입니다. 오늘 무엇을 복습해야 하는지 사람이 매번 판단해야 한다면, 그 판단 비용 때문에 복습 자체를 안 하게 됩니다.</p>
<h2>인지심리학은 이미 답을 냈다</h2>
<p>이 두 실패에는 각각 오래 검증된 대응책이 있습니다.</p>
<p><strong>간격 효과.</strong> 같은 총 학습 시간이라도 하루에 몰아서 하는 것보다 여러 날에 나눠서 하는 쪽이 오래 남습니다. 벼락치기가 시험 당일까지는 버티지만 그 다음 주에 아무것도 안 남는 이유입니다.</p>
<p><strong>시험 효과.</strong> 다시 읽는 것보다 스스로 꺼내보는 쪽이 훨씬 강하게 남습니다. 꺼내는 행위 자체가 기억을 강화합니다. 그리고 꺼내기에 실패하면 그 순간 "모른다"는 사실이 드러나므로, 앞서 말한 착각도 같이 깨집니다.</p>
<p><strong>간격 반복(SRS)</strong>은 이 둘을 합친 방식입니다. 스스로 꺼내보게 하되, 그 시점을 잊어버리기 직전으로 배치합니다. 쉽게 맞힌 항목은 간격을 늘리고, 틀린 항목은 다시 자주 보여줍니다.</p>
<h2>그래서 노트 앱이 할 일이 바뀐다</h2>
<p>간격 반복은 새로운 개념이 아닙니다. 종이 카드로도, 기존 암기 앱으로도 할 수 있습니다. 그런데도 대부분의 사람이 못 하는 이유는 셋입니다.</p>
<ul>
<li><strong>카드 만들기가 귀찮다.</strong> 강의를 듣고, 노트를 정리하고, 그 노트를 다시 카드로 쪼개는 세 번째 단계에서 거의 모두가 멈춥니다.</li>
<li><strong>오늘 뭘 볼지 정하기가 귀찮다.</strong> 카드가 쌓이면 그 자체가 부담이 됩니다.</li>
<li><strong>복습을 잊어버린다.</strong> 잊지 않으려고 하는 일인데, 그 일 자체를 잊습니다.</li>
</ul>
<p>즉 노트 앱이 "저장 도구"에 머무르면 이 세 지점을 아무도 못 넘습니다. 필요한 건 <strong>복습 스케줄러</strong>입니다. 노트에서 카드가 자동으로 나오고, 오늘 볼 것을 앱이 정하고, 시간이 되면 앱이 먼저 말을 걸어야 합니다.</p>
<h2>라이트온 AI 노트가 잡은 지점</h2>
<p>이 판단으로 만든 게 <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.ailecturenote" target="_blank" rel="noopener">라이트온 AI 노트</a>입니다. 녹음에서 복습까지를 한 앱 안에서 끊기지 않게 이었습니다.</p>
<ul>
<li><strong>정확하게 받아적기</strong> — 실시간 전사로 강의를 바로 텍스트로 옮기고, 발표자가 여러 명이면 정밀 모드가 화자를 구분합니다. 한국어·영어·중국어·일본어를 자동 인식합니다.</li>
<li><strong>이해 단계를 돕기</strong> — 핵심 요약을 만들고, 모르는 대목은 AI 튜터에게 물을 수 있습니다. 외국어 강의는 요약 번역으로 넘깁니다.</li>
<li><strong>꺼내는 연습으로 넘기기</strong> — 노트에서 플래시카드와 퀴즈를 자동으로 만듭니다. 사람이 카드를 만드는 단계를 없앤 것이 핵심입니다.</li>
<li><strong>시점은 앱이 관리</strong> — 간격 반복으로 복습 타이밍을 자동 관리하고, 오늘 복습할 카드를 모아 알림으로 알려줍니다.</li>
<li><strong>노트는 기기에</strong> — 노트는 기기에 암호화 저장되고 클라우드로 동기화하지 않습니다. 광고와 행동 추적도 없습니다. 강의자료(PDF)를 가져오거나 PDF·Word·텍스트로 내보낼 수 있습니다.</li>
</ul>
<h2>정직하게, 이 방식이 안 되는 것</h2>
<p>간격 반복이 만능은 아닙니다. 쓰기 전에 알고 있어야 할 한계가 있습니다.</p>
<p><strong>사실·용어·정의에 강하고, 긴 논증에는 약합니다.</strong> "이 개념의 정의는?" 같은 항목은 카드로 잘 쪼개집니다. 하지만 "이 이론이 왜 저 이론을 대체했는가"처럼 여러 단계를 이어야 하는 이해는 카드 한 장에 담기지 않습니다. 수학·물리의 풀이 절차도 마찬가지로, 카드보다 직접 풀어보는 편이 낫습니다.</p>
<p><strong>카드 품질은 원본 강의를 넘지 못합니다.</strong> 자동 생성은 정리 부담을 없애주지만 없는 내용을 만들어내지는 않습니다. 강의에서 흐릿하게 지나간 개념은 카드에서도 흐릿합니다.</p>
<p><strong>몰아서 하면 효과가 사라집니다.</strong> 간격 효과는 말 그대로 간격에서 나옵니다. 일주일 치 복습 카드를 시험 전날 한 번에 처리하면 벼락치기와 같아집니다. 하루 몇 분씩 꾸준히 하는 사람에게만 의미가 있습니다.</p>
<h2>정리</h2>
<p>전사와 요약은 강의를 <strong>기록</strong>하는 문제를 풀었습니다. 하지만 기록은 학습의 시작이지 끝이 아닙니다. 남은 절반 — 꺼내보기와 복습 시점 — 은 사람의 의지에 맡겨져 있었고, 그래서 대부분 실패했습니다.</p>
<p>노트 앱이 이 절반까지 가져가면, 사용자가 해야 할 일은 "매일 몇 분, 앱이 보여주는 카드에 답하기" 하나로 줄어듭니다. 그 정도면 유지할 수 있습니다.</p>
<div class="tip"><strong>라이트온 AI 노트</strong> — 녹음·전사·요약부터 플래시카드와 간격 반복 복습까지 한 앱에서 이어집니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.ailecturenote" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-samsung-side-key-app-shortcut",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "갤럭시 측면 버튼 '앱 열기'에 activity-alias 아이콘이 안 뜨는 이유",
"desc": "기능 하나만 여는 두 번째 런처 아이콘을 만들었는데 갤럭시 측면 버튼 목록에는 앱 항목 하나만 보였습니다. 목록이 앱마다 첫 진입점만 저장하는 동작을 확인하고, 선언 순서와 INFO 카테고리로 고친 기록입니다.",
"body": """
<p>모모아이는 통화와 회의 녹음을 올리면 AI가 전사·요약·할 일을 정리해 주는 앱입니다. Android 버전에 앱 안에서 바로 녹음하는 네이티브 녹음기를 넣으면서, 녹음 시작까지 걸리는 동작을 하나로 줄이는 데 공을 들였습니다. 빠른 설정 타일, 홈 화면 위젯, 아이콘 길게 누르기 바로가기, 잠금 화면 위에 뜨는 녹음 화면을 만들었고, 마지막으로 갤럭시의 <strong>측면 버튼 두 번 누르기</strong>에 녹음을 연결하려고 했습니다.</p><p>이 마지막 항목만 설계대로 동작하지 않았습니다. <code>activity-alias</code>로 런처 아이콘을 하나 더 만들어 측면 버튼에 연결하려는 분이라면 같은 함정을 밟을 수 있어 기록해 둡니다.</p><h2>설계: 기능 하나만 여는 두 번째 런처 아이콘</h2><p>갤럭시의 설정 &gt; 유용한 기능 &gt; 측면 버튼 &gt; 두 번 누르기에는 '앱 열기'라는 선택지가 있습니다. 이름 그대로 <em>앱</em>을 고르는 기능이라, 앱 안의 특정 동작으로 바로 보내려면 그 동작만 하는 런처 진입점이 따로 있어야 한다고 판단했습니다.</p><p>그래서 녹음 화면으로 곧장 가는 진입점을 <code>activity-alias</code>로 하나 더 만들고, 측면 버튼 목록에서 그걸 고르게 하기로 했습니다.</p><pre><code>&lt;!-- 녹음 화면: 바깥에는 닫혀 있고, 잠금 화면 위에 뜬다 (일부 속성 생략) --&gt;
&lt;activity
    android:name=".recorder.RecorderActivity"
    android:exported="false"
    android:launchMode="singleTask"
    android:showWhenLocked="true"
    android:turnScreenOn="true"
    android:theme="@style/RecorderTheme" /&gt;

&lt;!-- '모모아이 녹음' 런처 아이콘. 기본은 꺼져 있다 --&gt;
&lt;activity-alias
    android:name=".recorder.RecorderLauncher"
    android:enabled="false"
    android:exported="true"
    android:icon="@drawable/ic_recorder_launcher"
    android:label="@string/recorder_label"
    android:targetActivity=".recorder.RecorderActivity"&gt;
    &lt;intent-filter&gt;
        &lt;action android:name="android.intent.action.MAIN" /&gt;
        &lt;category android:name="android.intent.category.LAUNCHER" /&gt;
    &lt;/intent-filter&gt;
&lt;/activity-alias&gt;</code></pre><p><a href="https://developer.android.com/guide/topics/manifest/activity-alias-element" target="_blank" rel="noopener">공식 문서</a>에 따르면 별칭은 대상 액티비티를 <strong>독립된 컴포넌트처럼</strong> 보여 주고, 자기만의 인텐트 필터를 가질 수 있습니다. 대상 액티비티에 런처 필터가 없어도 별칭에 MAIN/LAUNCHER를 달면 런처에 아이콘이 생깁니다. 그래서 녹음 화면은 <code>exported="false"</code>로 닫아 두고, 바깥에서 들어오는 문은 별칭 하나만 열었습니다.</p><p>또 <code>icon</code>, <code>label</code>처럼 별칭에도 있는 속성은 대상의 값을 물려받지 않지만, 별칭에 없는 속성(<code>showWhenLocked</code>, <code>launchMode</code>, <code>theme</code> 등)은 대상의 값이 그대로 적용됩니다. 그래서 별칭으로 열어도 녹음 화면은 잠금 화면 위에 뜨고 꺼진 화면을 켭니다.</p><p>녹음 화면은 <code>ACTION_MAIN</code>으로 열리면 곧바로 녹음을 시작합니다. MAIN으로 들어오는 길은 별칭뿐이기 때문입니다. 최근 앱 목록에서 다시 연 경우는 뺐습니다.</p><pre><code>private fun handleLaunch(intent: Intent?) {
    val fromHistory = (intent?.flags ?: 0) and Intent.FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY != 0
    val wantsStart = when (intent?.action) {
        ACTION_START -&gt; true        // 타일·위젯이 보내는 앱 전용 액션
        Intent.ACTION_MAIN -&gt; true  // '모모아이 녹음' 아이콘(측면 버튼 '앱 열기')
        else -&gt; false
    }
    if (wantsStart &amp;&amp; !fromHistory &amp;&amp; !RecorderState.snapshot.isActive) {
        startRecordingWithPermission()
    }
}</code></pre><p>녹음 화면의 "측면 버튼으로 바로 녹음" 카드에서 기능을 켜면 별칭이 켜지고 삼성 측면 버튼 설정이 열립니다. 처음 안내 문구는 "'앱 열기' → '모모아이 녹음'을 고르세요"였습니다.</p><h2>증상: 목록에는 앱 이름 하나뿐</h2><p>실제로 써 보니 안내대로 할 수 없었습니다. 별칭을 켜면 앱 서랍에는 '모모아이 녹음' 아이콘이 생기는데, 측면 버튼의 '앱 열기' 목록에는 'Momoi' 항목 하나만 있었습니다. 그걸 고르면 측면 버튼은 녹음 화면이 아니라 앱 본 화면을 열었습니다.</p><p>앱 서랍과 측면 버튼 목록이 같은 목록일 거라는 가정이 틀린 것이었습니다.</p><h2>진단 1: 별칭이 런처 진입점으로 등록됐나</h2><p>먼저 MAIN/LAUNCHER에 응답하는 컴포넌트를 adb로 조회합니다. 이 명령은 <strong>순서</strong>까지 보여 주는데, 뒤에서 보듯 이번 문제의 핵심이 그 순서였습니다.</p><pre><code>adb shell cmd package query-activities --brief --components \\
  -a android.intent.action.MAIN -c android.intent.category.LAUNCHER | grep com.example.app

# 출력 형식 예시: 한 줄에 '앱 ID/컴포넌트' 하나
com.example.app/com.example.app.MainActivity</code></pre><p>앱 ID(<code>applicationId</code>)와 코드 패키지(<code>namespace</code>)가 다른 앱은 <code>앱 ID/코드 패키지.클래스</code> 꼴로 나옵니다. 셸 명령에 컴포넌트를 적을 때도 이 형식을 따라야 합니다.</p><h2>진단 2: 측면 버튼은 무엇을 저장했나</h2><p>다음은 측면 버튼 설정이 실제로 저장한 값입니다. 제가 쓴 갤럭시 탭에서는 이 값이 Global 설정에 문자열로 남아 있어 adb로 읽을 수 있었습니다(읽기만 합니다).</p><pre><code>adb shell settings list global | grep function_key

# 출력 예시 (값은 바꿈)
function_key_config_doublepress=1
function_key_config_doublepress_type=2
function_key_config_doublepress_value=com.example.app/com.example.app.MainActivity</code></pre><p>제 기기에서는 <code>_type</code>이 2일 때가 '앱 열기'였고, <code>_value</code>에는 컴포넌트 이름이 그대로 들어 있었습니다. 측면 버튼은 앱이 아니라 <strong>컴포넌트</strong>를 저장합니다. 고른 순간 열 컴포넌트가 정해지고, 앱이 업데이트로 매니페스트를 바꿔도 저장된 값은 그대로입니다. 이 키와 형식은 삼성이 공개한 것이 아니라 제 기기에서 본 것이라 다른 기기에서는 다를 수 있습니다.</p><h2>진단 3: 목록은 어떻게 만들어지나</h2><p>남은 질문은 "왜 별칭이 목록에 안 나오나"였습니다. 삼성 문서에서는 이 목록이 어떻게 만들어지는지 찾지 못해서, 갤럭시 탭 S7(Android 13, One UI 5.1.1)에서 설정 앱과 <code>services.jar</code>를 꺼내 dexdump로 읽어 보았습니다. 제가 확인한 범위의 동작은 이렇습니다.</p><ul><li>목록을 채우는 로더는 <code>LauncherApps.getActivityList()</code>로 런처 진입점을 전부 받아 옵니다. 여기까지는 일반 런처와 같습니다.</li><li>그런데 결과를 <strong>패키지 이름을 키로 하는 맵</strong>에 넣으면서, 같은 패키지가 이미 들어 있으면 건너뜁니다. 한 앱에서 진입점이 몇 개가 나오든 첫 번째 하나만 남습니다.</li><li>항목을 고르면 그 진입점의 컴포넌트를 앞에서 본 설정 값에 저장합니다.</li><li>측면 버튼은 저장된 컴포넌트를 <code>ACTION_MAIN</code> + <code>CATEGORY_LAUNCHER</code>, 플래그 <code>0x10200000</code>(<code>FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_RESET_TASK_IF_NEEDED</code>)으로 엽니다. 엑스트라는 붙이지 않습니다.</li></ul><p>즉 이 목록은 런처 아이콘 목록이 아니라 <strong>앱 목록</strong>입니다. 앱마다 <code>getActivityList()</code>가 돌려준 순서에서 맨 앞에 온 진입점 하나가 대표가 됩니다.</p><p>마지막 항목은 다른 우회로도 막습니다. 인텐트에 홈 화면 아이콘과 같은 액션·카테고리만 있고 엑스트라가 없으니, 앱 본 화면이 측면 버튼 실행을 알아채고 녹음으로 분기할 수 없습니다. 단서는 <strong>어떤 컴포넌트가 열렸는가</strong>뿐이라, 별칭이 저장되게 하는 수밖에 없습니다. 아이콘 길게 누르기 바로가기(<code>shortcuts.xml</code>)도 답이 아니었습니다. 제가 본 로더는 런처 진입점만 돌았습니다.</p><p>같은 앱 안의 순서는 Android 문서가 보장하지 않지만, 제 기기에서는 매니페스트에 <strong>선언한 순서</strong>를 따랐습니다. 고치기 전에는 MainActivity가 먼저, 별칭이 그 뒤였습니다. 그래서 목록의 항목은 늘 MainActivity를 가리켰고 별칭은 두 번째라 빠졌습니다.</p><h2>우선순위로는 안 된다</h2><p>먼저 떠오르는 건 인텐트 필터의 <code>android:priority</code>입니다. 하지만 <a href="https://developer.android.com/guide/topics/manifest/intent-filter-element" target="_blank" rel="noopener">&lt;intent-filter&gt; 문서</a>에 따르면 권한 없는(non-privileged) 앱이 0보다 큰 우선순위를 요청하면 그 값은 무시되고 0으로 잘립니다. 일반 앱에는 막힌 길입니다.</p><p>같은 문서에는 한 앱 안의 필터 순서를 정하는 <code>android:order</code>(API 28 이상)도 있지만, 이 값이 삼성 목록에 영향을 주는지는 시험하지 않았습니다. 이번에는 확인된 동작인 선언 순서만으로 고쳤습니다.</p><h2>해결 1: 별칭을 MainActivity보다 먼저 선언한다</h2><p>녹음 화면과 별칭을 <code>&lt;application&gt;</code> 안에서 MainActivity보다 위로 옮겼습니다. 녹음 화면(대상)은 별칭보다도 먼저 두어야 합니다. 문서에는 <code>targetActivity</code>가 별칭보다 <em>앞에</em> 선언된 <code>&lt;activity&gt;</code>의 이름과 같아야 한다고 적혀 있습니다.</p><pre><code>&lt;application ...&gt;
    &lt;!-- 1. 별칭의 대상. 별칭보다 먼저 선언해야 한다 --&gt;
    &lt;activity android:name=".recorder.RecorderActivity" android:exported="false" ... /&gt;

    &lt;!-- 2. 별칭. MainActivity보다 먼저 선언해야
         측면 버튼 목록의 이 앱 항목이 켜진 별칭을 가리킨다 --&gt;
    &lt;activity-alias
        android:name=".recorder.RecorderLauncher"
        android:enabled="false"
        android:exported="true"
        android:targetActivity=".recorder.RecorderActivity" ...&gt;
        &lt;intent-filter&gt;
            &lt;action android:name="android.intent.action.MAIN" /&gt;
            &lt;category android:name="android.intent.category.LAUNCHER" /&gt;
        &lt;/intent-filter&gt;
    &lt;/activity-alias&gt;

    &lt;!-- 3. 앱 본 화면 --&gt;
    &lt;activity android:name=".MainActivity" android:exported="true" ...&gt;
        ...
    &lt;/activity&gt;
&lt;/application&gt;</code></pre><p>이제 동작은 별칭의 상태에 따라 갈립니다.</p><ul><li><strong>별칭이 꺼져 있을 때</strong>: 꺼진 컴포넌트는 런처 진입점 조회에 나오지 않으므로 첫 진입점은 MainActivity입니다. 목록의 앱 항목은 예전처럼 앱을 엽니다.</li><li><strong>별칭이 켜져 있을 때</strong>: 첫 진입점이 별칭이 됩니다. 목록에는 여전히 이 앱의 항목 하나만 보이지만, 그걸 고르면 별칭이 저장되고 측면 버튼이 녹음 화면을 엽니다.</li></ul><p>그 한 항목이 어떤 이름으로 보일지는 목록 구현에 달려 있어, 안내 문구를 "목록에 '모모아이 녹음'이 있으면 그걸, 없으면 'Momoi'를 고르세요"로 바꾸고 <strong>전에 Momoi를 골라 뒀어도 한 번 더 눌러 달라</strong>는 문장을 더했습니다. 업데이트 전에 골라 둔 사람의 설정에는 MainActivity가 그대로 남아 있기 때문입니다.</p><h2>해결 2: 앱의 정문을 INFO로 따로 세운다</h2><p>순서를 바꾸면 다른 문제가 생깁니다. 패키지 이름만으로 앱을 여는 코드는 대개 <code>PackageManager.getLaunchIntentForPackage()</code>를 씁니다. 이 메서드의 <a href="https://developer.android.com/reference/android/content/pm/PackageManager#getLaunchIntentForPackage(java.lang.String)" target="_blank" rel="noopener">문서</a>에는 현재 구현이 <code>CATEGORY_INFO</code>인 MAIN 액티비티를 먼저 찾고, 없으면 <code>CATEGORY_LAUNCHER</code>인 MAIN 액티비티를 찾는다고 적혀 있습니다. AOSP 구현은 조회 결과의 첫 항목을 고르기 때문에, INFO가 없는 앱에서 별칭이 첫 런처 진입점이 되면 이 메서드는 녹음 화면을 돌려줄 수 있습니다.</p><p>모모아이 안에서 이 메서드를 쓰는 곳만 셋이었습니다.</p><ul><li><strong>FCM 알림</strong>: firebase-messaging의 알림 빌더는 메시지에 <code>click_action</code>이나 링크가 없으면 <code>getLaunchIntentForPackage()</code>로 열 화면을 정합니다(25.1.2 바이트코드에서 확인).</li><li><strong>로컬 알림</strong>: flutter_local_notifications 17.2.4의 Android 구현도 알림을 눌렀을 때의 인텐트를 같은 메서드로 만듭니다.</li><li><strong>직접 만든 알림</strong>: 통화가 끝나면 "통화 요약할까요?" 알림을 띄우는 서비스도 원래 같은 메서드를 썼습니다.</li></ul><p>그대로 두면 측면 버튼 기능을 켠 사람은 알림을 누를 때마다 녹음이 시작됩니다.</p><p>직접 만든 알림은 별칭을 처음 추가할 때 이미 MainActivity를 명시한 인텐트로 바꿔 두었습니다. 라이브러리 안의 호출은 고칠 수 없으니 MainActivity에 <code>MAIN</code> + <code>CATEGORY_INFO</code> 필터를 하나 더 달았습니다.</p><pre><code>&lt;activity android:name=".MainActivity" android:exported="true" ...&gt;
    &lt;intent-filter&gt;
        &lt;action android:name="android.intent.action.MAIN"/&gt;
        &lt;category android:name="android.intent.category.LAUNCHER"/&gt;
    &lt;/intent-filter&gt;
    &lt;!-- 앱의 '정문'. getLaunchIntentForPackage()는 INFO 진입점을 먼저 고른다.
         이게 없으면 별칭이 켜졌을 때 알림 탭이 녹음 화면을 연다 --&gt;
    &lt;intent-filter&gt;
        &lt;action android:name="android.intent.action.MAIN"/&gt;
        &lt;category android:name="android.intent.category.INFO"/&gt;
    &lt;/intent-filter&gt;
    ...
&lt;/activity&gt;</code></pre><pre><code>// 앱 안에서 만드는 알림은 정문에도 기대지 않고 대상을 명시한다
fun openAppIntent(context: Context): Intent =
    Intent(context, MainActivity::class.java)
        .setAction(Intent.ACTION_MAIN)
        .addCategory(Intent.CATEGORY_LAUNCHER)
        .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)</code></pre><p><a href="https://developer.android.com/reference/android/content/Intent#CATEGORY_INFO" target="_blank" rel="noopener">CATEGORY_INFO</a>는 문서에서 런처 목록에 나타나지 않으면서 사용자에게 정문을 제공하는 용도로 설명하는 카테고리입니다. LAUNCHER가 아니므로 아이콘이 늘지 않고 측면 버튼 목록에도 영향이 없습니다. 반면 <code>getLaunchIntentForPackage()</code>는 INFO를 먼저 보므로 별칭 순서와 상관없이 MainActivity를 돌려줍니다. 런처 순서는 측면 버튼 목록용으로, 패키지 단위로 여는 경로는 INFO로 떼어 놓은 셈입니다.</p><h2>부작용: 런처 아이콘이 두 개가 된다</h2><p>별칭 방식의 대가는 앱 서랍에 아이콘이 하나 더 생긴다는 점입니다. 측면 버튼을 쓰지 않는 사람에게는 정체를 알 수 없는 중복 아이콘입니다.</p><h3>기본은 꺼 두고, 쓰겠다고 할 때만 켠다</h3><p>별칭은 <code>enabled="false"</code>로 시작하고, 사용자가 녹음 화면의 카드에서 켤 때만 <code>setComponentEnabledSetting()</code>으로 켭니다. 이때 <code>DONT_KILL_APP</code> 플래그를 넘깁니다. 문서상 이 플래그는 컴포넌트를 담은 앱을 종료하지 말라는 뜻이라, 빼면 버튼을 누르는 순간 앱이 꺼질 수 있습니다.</p><pre><code>fun setLauncherAliasEnabled(context: Context, enabled: Boolean) {
    context.packageManager.setComponentEnabledSetting(
        ComponentName(context, LAUNCHER_ALIAS),  // 별칭의 전체 이름(코드 패키지 기준)
        if (enabled) PackageManager.COMPONENT_ENABLED_STATE_ENABLED
        else PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
        PackageManager.DONT_KILL_APP,
    )
}</code></pre><h3>켜는 순간 설정 화면으로 데려간다</h3><p>켜기 버튼은 별칭을 켠 뒤 측면 버튼 설정을 바로 엽니다. 이 화면은 <code>com.samsung.android.intent.action.SIDE_KEY_SETTINGS</code> 액션으로 열 수 있는데, 다른 제조사 기기에는 없으므로 <code>resolveActivity()</code>로 먼저 확인합니다. Android 11 이상에서는 패키지 가시성 규칙 때문에 매니페스트의 <code>&lt;queries&gt;</code>에 이 액션을 선언해 두어야 조회가 됩니다. 조회에 실패하면 삼성이 아닌 기기로 보고, 버튼에 앱을 연결하는 설정이 있다면 '모모아이 녹음'을 고르라는 일반 안내로 바꿉니다.</p><pre><code>&lt;queries&gt;
    &lt;intent&gt;
        &lt;action android:name="com.samsung.android.intent.action.SIDE_KEY_SETTINGS" /&gt;
    &lt;/intent&gt;
&lt;/queries&gt;</code></pre><pre><code>private fun sideKeySettingsIntent(): Intent? {
    val intent = Intent(SAMSUNG_SIDE_KEY_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    return if (intent.resolveActivity(packageManager) != null) intent else null
}</code></pre><h3>끌 때는 측면 버튼 설정도 되돌리게 한다</h3><p>별칭을 꺼도 측면 버튼 설정에는 별칭의 컴포넌트 이름이 남습니다. 그대로 두면 눌러도 아무것도 열리지 않을 수 있어, 끄기 버튼은 "'두 번 누르기'를 다른 동작으로 바꿔 달라"는 안내를 띄우고 측면 버튼 설정을 다시 엽니다. 외부 설정 값은 앱이 고칠 수 없으니 고칠 화면까지 데려다주는 데서 멈췄습니다.</p><h3>두 번째 아이콘에도 쓸모를 준다</h3><p>켜진 '모모아이 녹음' 아이콘은 누르면 바로 녹음이 시작되는 아이콘이기도 합니다. 중복 아이콘이 아니라 기능이 분명한 아이콘으로 읽히도록 이름과 아이콘 모양을 따로 주었습니다.</p><h2>검증</h2><h3>1. 선언 순서를 테스트로 묶는다</h3><p>이유를 모르는 사람 눈에 선언 순서는 아무래도 좋은 것으로 보입니다. 누군가 정리한다며 MainActivity를 맨 위로 올리면 빌드도 앱도 멀쩡한 채로 조용히 원래대로 돌아갑니다. 그래서 매니페스트를 XML로 읽어 순서와 필터를 확인하는 JVM 단위 테스트를 넣었습니다.</p><pre><code>class RecorderLauncherManifestTest {
    private val android = "http://schemas.android.com/apk/res/android"

    // &lt;application&gt; 바로 아래의 activity / activity-alias 를 선언 순서대로
    private val components: List&lt;Element&gt; by lazy {
        val factory = DocumentBuilderFactory.newInstance().apply { isNamespaceAware = true }
        val doc = factory.newDocumentBuilder().parse(File("src/main/AndroidManifest.xml"))
        val app = doc.getElementsByTagName("application").item(0) as Element
        val nodes = app.childNodes
        (0 until nodes.length)
            .mapNotNull { nodes.item(it) as? Element }
            .filter { it.tagName == "activity" || it.tagName == "activity-alias" }
    }

    private fun indexOf(name: String): Int =
        components.indexOfFirst { it.getAttributeNS(android, "name") == name }
            .also { assertTrue("$name 이 매니페스트에 없다", it &gt;= 0) }

    @Test
    fun `녹음 별칭이 앱 본 화면보다 먼저 선언된다`() {
        assertTrue(indexOf(".recorder.RecorderLauncher") &lt; indexOf(".MainActivity"))
    }

    @Test
    fun `별칭의 대상 화면은 별칭보다 먼저 선언된다`() {
        assertTrue(indexOf(".recorder.RecorderActivity") &lt; indexOf(".recorder.RecorderLauncher"))
    }

    // 이 밖에 별칭이 MAIN/LAUNCHER 를 갖고 기본으로 꺼져 있는지,
    // MainActivity 에 MAIN/INFO 정문이 있는지도 같은 방식으로 확인한다.
}</code></pre><p>이 테스트는 소스 매니페스트만 보므로, 병합된 최종 APK의 순서는 기기에서 따로 확인했습니다.</p><h3>2. 기기에서 진입점 순서와 정문 확인</h3><pre><code># 런처 진입점: 별칭이 켜져 있으면 별칭이 먼저 나와야 한다
adb shell cmd package query-activities --brief --components \\
  -a android.intent.action.MAIN -c android.intent.category.LAUNCHER | grep com.example.app

# 정문: 별칭 상태와 상관없이 MainActivity 하나여야 한다
adb shell cmd package query-activities --brief --components \\
  -a android.intent.action.MAIN -c android.intent.category.INFO | grep com.example.app</code></pre><p>갤럭시 탭 S7(Android 13)에서 별칭을 켠 상태로 조회하니 런처 진입점은 RecorderLauncher, MainActivity 순서로 나왔고, INFO 조회는 MainActivity로 풀렸습니다. 별칭을 끄면 런처 조회에는 MainActivity만 남고 INFO는 그대로 MainActivity입니다.</p><p>셸에서 별칭을 직접 켜고 끄려면 제 환경에서는 testOnly 빌드가 필요했습니다. 일반 빌드에서는 셸의 컴포넌트 상태 변경이 거부됩니다.</p><pre><code>./gradlew assembleDebug -Pandroid.injected.testOnly=true
adb install -r -t app-debug.apk
adb shell pm enable com.example.app/com.example.app.recorder.RecorderLauncher</code></pre><h3>3. 측면 버튼이 보내는 인텐트를 그대로 재현</h3><p>확인한 인텐트 모양을 <code>am start</code>로 똑같이 만들어, 화면을 끄고 잠근 상태에서 보냈습니다.</p><pre><code>adb shell am start -a android.intent.action.MAIN \\
  -c android.intent.category.LAUNCHER -f 0x10200000 \\
  -n com.example.app/com.example.app.recorder.RecorderLauncher</code></pre><p>태블릿에서는 녹음 화면이 잠금 화면 위에 뜨고 녹음이 시작됐습니다. 다만 이것은 측면 버튼이 별칭을 저장했다는 전제 위의 재현이라, 목록에서 다시 고른 뒤 무엇이 저장됐는지는 앞의 <code>settings list global</code>로 보는 것이 확실합니다. 또 모든 확인은 One UI 5.1.1 태블릿 한 대에서 했고, 최신 One UI 휴대폰이 같은 방식인지는 확인하지 못했습니다.</p><h2>같은 문제를 피하는 체크리스트</h2><ul><li>제조사 설정의 '앱 고르기' 목록은 앱 서랍과 같은 목록이 아닐 수 있습니다. 앱 서랍에 아이콘이 보인다고 그 목록에도 나올 거라고 가정하지 마세요.</li><li>시스템이 앱을 열 때 보내는 인텐트에 무엇이 들어 있는지부터 확인하세요. 엑스트라가 없다면 앱이 구별할 수 있는 건 컴포넌트 이름뿐입니다.</li><li>측면 버튼 같은 설정은 고른 시점의 컴포넌트를 문자열로 저장합니다. 매니페스트를 바꿔도 이미 저장된 값은 바뀌지 않으니, 사용자에게 다시 고르라고 안내해야 합니다.</li><li>런처 진입점이 둘 이상인 앱은 <code>MAIN</code> + <code>INFO</code> 정문을 하나 두세요. <code>getLaunchIntentForPackage()</code>를 쓰는 SDK가 엉뚱한 진입점을 고르지 않게 됩니다.</li><li>선언 순서처럼 겉보기에 의미 없는 매니페스트 사항이 동작을 좌우한다면 테스트로 묶어 두세요.</li><li>두 번째 런처 아이콘은 기본으로 꺼 두고, 끌 때는 외부 설정에 남은 참조까지 정리하도록 안내하세요.</li></ul><p>앱 서랍은 진입점을 보여 주고, 측면 버튼 설정은 앱을 보여 줍니다. 이 차이를 확인하고 나니 고치는 데는 선언 순서 변경과 INFO 필터 하나면 충분했습니다.</p><div class="tip"><strong>모모아이</strong> — 통화·회의 녹음을 올리면 AI가 전사·요약·할 일·일정을 정리합니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.momoi.twa" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-storekit-test-without-device",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "실기기 없이 iOS 인앱결제 검증하기 — 시뮬레이터 샌드박스 로그인 실패와 SKTestSession",
"desc": "시뮬레이터에서는 샌드박스 테스터 로그인이 AMSErrorDomain 100으로 실패했습니다. .storekit 구성과 앱 호스티드 SKTestSession 테스트로 xcodebuild만으로 구매·복원을 검증한 방법과, 이 방식으로 확인할 수 없는 것의 경계를 정리했습니다.",
"body": """
<p>인앱결제 코드를 고친 날, 정작 결제를 눌러볼 아이폰이 손에 없었습니다. 원격으로 작업하던 중이라 쓸 수 있는 건 Mac 한 대와 iOS 시뮬레이터뿐이었습니다. 시뮬레이터에 샌드박스 계정으로 로그인해서 사보면 되겠다고 생각했는데, 바로 거기서 막혔습니다.</p>
<p>그 뒤로 자리 잡은 방법은 <strong>앱 호스티드 테스트 + <code>SKTestSession</code></strong>을 <code>xcodebuild</code>만으로 돌리는 것입니다. 거기까지 가는 과정과, 이 방식으로 확인할 수 없는 것의 경계를 함께 적었습니다. 경계를 모른 채 "시뮬레이터에서 다 통과했다"고 믿으면 서버의 영수증 검증처럼 정말 위험한 부분을 건너뛰게 됩니다.</p>

<h2>증상: 결제 시트의 로그인이 계속 튕긴다</h2>
<p>Capacitor로 만든 앱의 iOS 빌드에서 구독 버튼을 누르면 시스템 결제 시트가 "Sign in to Apple Account"를 요구합니다. App Store Connect에서 만든 샌드박스 테스터 계정을 넣으면 이렇게 거절됩니다.</p>
<pre><code>AMSErrorDomain 100 Authentication Failed / Password reuse not available</code></pre>
<p>처음엔 비밀번호나 테스터 계정 상태를 의심했습니다. 그런데 테스터를 새로 만들어 넣어도 같은 오류가 났고, 기존 계정이든 새 계정이든 결과가 같았습니다. 결정적인 단서는 <strong>같은 계정이 실기기에서는 정상으로 로그인된다</strong>는 사실이었습니다. 문제는 계정이 아니라 시뮬레이터라는 환경이었습니다.</p>
<p>Apple 문서도 샌드박스 테스트를 기기 기준으로 설명합니다. 개발 서명 앱에서 처음 구매를 시도하면 iOS 설정 &gt; 개발자에 샌드박스 계정 항목이 생기고 거기서 로그인하는 흐름입니다. 시뮬레이터에서 이 로그인이 된다고 기대할 근거는 문서에 없었습니다. 그래서 로그인을 고치는 대신 로그인이 필요 없는 테스트 환경으로 방향을 바꿨습니다.</p>

<h2>선택지: 로컬 StoreKit 테스트 환경</h2>
<p>Apple이 제공하는 인앱결제 테스트 환경은 셋입니다. Xcode의 StoreKit Testing, 샌드박스, 그리고 샌드박스를 쓰는 TestFlight입니다. 이 중 <a href="https://developer.apple.com/documentation/xcode/setting-up-storekit-testing-in-xcode" target="_blank" rel="noopener">StoreKit Testing in Xcode</a>는 App Store 서버에 연결하지 않는 로컬 환경입니다. 상품 정보를 <code>.storekit</code> 파일에 적어두면 앱의 StoreKit 호출이 그 데이터를 쓰고, 거래도 로컬에서 만들어집니다. 로그인이 필요 없고 시뮬레이터에서도 동작합니다.</p>
<p>처음부터 기억해 둘 점이 하나 있습니다. 이 환경이 만드는 영수증과 JWS 거래는 <strong>App Store가 아니라 Xcode가 서명</strong>합니다(<a href="https://developer.apple.com/documentation/storekit/testing-at-all-stages-of-development-with-xcode-and-the-sandbox" target="_blank" rel="noopener">Apple의 테스트 환경 비교</a>). 이 한 줄이 뒤에 나올 "검증할 수 없는 것"을 거의 다 결정합니다.</p>

<h2>방법 1: 스킴의 Run 액션에 .storekit 연결하기</h2>
<p>기본 방법은 스킴 편집기의 Run 액션 &gt; Options &gt; StoreKit Configuration에서 파일을 고르는 것입니다. <code>.storekit</code>의 상품 ID, 구독 그룹, 가격은 App Store Connect와 똑같이 적었습니다. 스토어프론트와 로케일도 정할 수 있어서, 시뮬레이터 샌드박스에서 달러로 나오던 가격을 원화로 볼 수 있었습니다.</p>
<p>스킴 파일을 직접 다루거나 XcodeGen으로 생성하면 결과는 이렇게 생깁니다.</p>
<pre><code>&lt;!-- App.xcodeproj/xcshareddata/xcschemes/App.xcscheme --&gt;
&lt;LaunchAction buildConfiguration = "Debug" ...&gt;
   ...
   &lt;StoreKitConfigurationFileReference
      identifier = "../../App.storekit"&gt;
   &lt;/StoreKitConfigurationFileReference&gt;
&lt;/LaunchAction&gt;

# XcodeGen 이라면 project.yml 의 스킴에
schemes:
  App:
    run:
      config: Debug
      storeKitConfiguration: App/Support/Products.storekit</code></pre>
<p>여기서 첫 번째 함정을 밟았습니다. <code>identifier</code>의 상대 경로 기준이 직관과 다릅니다. 스킴 파일은 <code>xcshareddata/xcschemes/</code> 안에 있지만, 제가 동작을 확인한 두 프로젝트 모두 <code>../../</code>가 <strong>.xcodeproj를 담고 있는 폴더</strong>를 가리켰습니다. 처음에 <code>../App.storekit</code>으로 적었을 때는 오류도 경고도 없이 무시됐고, 앱은 그대로 샌드박스로 가서 다시 로그인 시트를 띄웠습니다. 경로가 틀렸다고 알려주는 장치가 없으므로, <strong>결제 시트에 Apple 계정 로그인이 뜨면 로컬 구성이 적용되지 않은 것</strong>으로 판단하는 편이 가장 빠릅니다.</p>

<h3>두 번째 함정: xcodebuild로 띄우면 적용되지 않는다</h3>
<p>스킴에 파일을 연결한 뒤 평소처럼 <code>xcodebuild</code>로 빌드하고 <code>simctl</code>로 설치·실행했습니다. 결과는 또 샌드박스였습니다. 스킴의 StoreKit 구성은 <strong>Xcode IDE에서 Run 했을 때만</strong> 적용됩니다. <a href="https://www.revenuecat.com/docs/test-and-launch/sandbox/apple-app-store" target="_blank" rel="noopener">RevenueCat 문서</a>도 같은 한계를 적어 두었습니다. <code>xcodebuild</code>로 앱을 띄우는 도구(<code>flutter run</code> 등)는 스킴의 StoreKit 구성 파일을 쓰지 않는다는 내용입니다. <code>xcodebuild test</code>와 거기서 나온 <code>.xctestrun</code>도 열어봤지만 StoreKit 관련 키는 어디에도 실리지 않았습니다.</p>
<p>기기 없이, 그리고 Xcode 창을 직접 클릭하지 않고 IDE Run을 걸려면 AppleScript가 현실적인 답이었습니다. Xcode의 스크립팅 사전에는 워크스페이스 문서에 보내는 <code>run</code> 명령이 있어서, 현재 활성 스킴과 실행 대상으로 Run 액션을 실행합니다. 아래는 예시입니다.</p>
<pre><code>-- run-in-xcode.applescript (예시)
tell application "Xcode"
    open POSIX file "/path/to/ios/App/App.xcodeproj"
    -- open 의 반환값은 비어 있을 때가 있다(스크립팅 사전에 적힌 알려진 문제)
    set ws to active workspace document
    repeat until loaded of ws
        delay 1
    end repeat
    set r to run ws   -- 완료를 기다리지 않고 바로 돌아온다
end tell</code></pre>
<p>처음 한 번은 macOS가 Xcode 제어에 대한 자동화 권한을 묻습니다. 앱이 정말 Xcode를 거쳐 떴는지는 프로세스 환경 변수로 확인했습니다. Xcode가 띄운 앱 프로세스에는 <code>__XCODE_BUILT_PRODUCTS_DIR_PATHS</code>가 들어 있었습니다.</p>
<pre><code># 예시: 앱 프로세스 환경 변수에 Xcode 흔적이 있는지
ps -E -p "$(pgrep -f 'App.app/App' | head -1)" | tr ' ' '\\n' | grep __XCODE_BUILT_PRODUCTS_DIR_PATHS</code></pre>
<p>이 방식은 실제 화면과 결제 시트를 씁니다. 시트에서 구독 버튼을 한 번 누르면 거래가 끝나고, 결제 SDK의 검증과 권한 부여를 거쳐 앱 잠금이 풀리는 데까지 실제 경로를 탑니다. 화면 흐름이나 스토어 스크린샷 확인에 맞습니다.</p>
<p>RevenueCat을 쓴다면 할 일이 하나 더 있습니다. StoreKit 테스트 인증서를 RevenueCat 앱 설정의 StoreKit testing framework 항목에 올려야 하고, 없으면 Xcode가 서명한 거래가 거부됩니다. 인증서는 <code>.storekit</code>을 연 상태에서 Editor &gt; Save Public Certificate로 저장합니다. Apple 문서 설명대로 체인이 없는 루트 인증서이고, 제 Xcode에 든 것은 발급자와 주체가 모두 <code>StoreKit</code>인 자체 서명 인증서(2040년까지 유효)였습니다.</p>
<p>단점은 Xcode GUI가 떠 있어야 하고, 자동화 권한이 필요하고, 결제 시트를 누르는 단계가 남는다는 점입니다. CI에 넣기에는 무겁습니다.</p>

<h2>방법 2: 앱 호스티드 테스트에서 SKTestSession 쓰기</h2>
<p>그 뒤 SwiftUI로 만든 구독 앱에서 더 단순한 방법을 찾았습니다. 핵심은 <strong>테스트 코드를 앱 프로세스 안에서 돌리는 것</strong>입니다.</p>
<p>StoreKitTest 프레임워크의 <a href="https://developer.apple.com/documentation/storekittest/sktestsession" target="_blank" rel="noopener"><code>SKTestSession</code></a>은 Xcode에서 손으로 바꾸던 StoreKit 테스트 설정을 코드로 제어합니다. 구성 파일로 세션을 만들고 <code>disableDialogs</code>를 켜면 테스트 환경 UI 없이 돕니다. 문제는 이 세션이 <em>어느 프로세스</em>의 StoreKit 호출에 닿느냐였습니다. UI 테스트는 앱과 별개인 테스트 러너 프로세스에서 도는데, 처음에 그쪽에서 세션을 만들었을 때는 앱이 보는 상품 목록에 아무 변화가 없었습니다.</p>
<p>반면 Host Application(TEST_HOST)이 앱으로 지정된 유닛 테스트 번들은 앱 프로세스에 주입되어 실행됩니다. 여기서 세션을 만들면 같은 프로세스의 앱 코드가 부르는 <code>Product.products(for:)</code>와 <code>purchase()</code>가 로컬 구성을 씁니다. Xcode IDE도 AppleScript도 없이 <code>xcodebuild</code> 하나로 상품 로드, 구매, 미완료 거래, 복원까지 돌릴 수 있었습니다.</p>

<h3>프로젝트 구성</h3>
<p>XcodeGen 기준으로 테스트 타깃 하나를 추가합니다. 실제 설정에서 이름만 바꾸고 줄였습니다.</p>
<pre><code>targets:
  App:
    type: application
    sources:
      - path: App
        excludes:
          - "Support/Products.storekit"   # 앱 번들에는 넣지 않는다

  # 앱 프로세스 안에서 돌아야 SKTestSession 이 앱의 StoreKit 호출에 적용된다
  AppStoreTests:
    type: bundle.unit-test
    platform: iOS
    sources:
      - path: AppStoreTests
      - path: App/Support/Products.storekit
        buildPhase: resources
    dependencies:
      - target: App

schemes:
  App:
    run:
      storeKitConfiguration: App/Support/Products.storekit   # IDE Run 용
    test:
      targets:
        - AppStoreTests</code></pre>
<p>XcodeGen은 앱에 의존하는 유닛 테스트 타깃에 <code>TEST_HOST</code>와 <code>BUNDLE_LOADER</code>를 자동으로 넣습니다. Xcode에서 만든다면 Host Application이 앱으로 잡혀 있는지만 보면 됩니다.</p>
<p><code>.storekit</code>을 앱 타깃이 아니라 테스트 번들의 리소스로 넣은 것은 출시 빌드에 테스트용 상품 정의가 실리지 않게 하려는 의도입니다. Apple 문서는 <code>init(configurationFileNamed:)</code>의 파일을 "앱 번들에 포함한 파일"로 설명하지만 제 환경에서는 테스트 번들 리소스의 파일도 찾았습니다. 문서에 없는 동작이니 세션 생성이 예외 없이 되는지부터 확인하시길 권합니다.</p>

<h3>테스트 코드</h3>
<p>먼저 앱 쪽 규칙입니다. 서버가 구매 증명(JWS)을 확인하기 전에는 <code>finish()</code>를 부르지 않습니다. 서버 호출이 실패하면 예외가 나서 <code>finish()</code>까지 가지 않고, 거래는 <code>Transaction.unfinished</code>에 남아 다음 실행 때 다시 보내집니다.</p>
<pre><code>private func deliver(_ result: VerificationResult&lt;Transaction&gt;) async throws {
    guard case .verified(let transaction) = result else { throw StoreError.unverified }
    // 서버가 JWS 를 확인해야 다음 줄로 간다. 실패하면 throw 되어 finish 하지 않는다
    try await api.post("payment/apple/verify",
                       json: ["signedTransactionInfo": result.jwsRepresentation])
    await transaction.finish()
}</code></pre>
<p>테스트는 실제로 쓰는 코드에서 이름만 바꿔 줄였습니다.</p>
<pre><code>import StoreKit
import StoreKitTest
import XCTest
@testable import App

@MainActor
final class StoreTests: XCTestCase {
    private var session: SKTestSession!
    private var expectation: String {
        ProcessInfo.processInfo.environment["STORE_EXPECT"] ?? "rejected"
    }

    override func setUp() async throws {
        session = try SKTestSession(configurationFileNamed: "Products")
        session.disableDialogs = true
        session.clearTransactions()
    }

    override func tearDown() async throws {
        session.clearTransactions()
    }

    // 로그인·서버 없이 돈다: 앱 코드의 상품 ID 가 .storekit 에 모두 있는가
    func test1_productsMatch() async throws {
        await Store.shared.loadProducts()
        for id in Store.allProductIDs {
            let product = try XCTUnwrap(Store.shared.products[id], "\\(id) 없음")
            let period = try XCTUnwrap(product.subscription?.subscriptionPeriod)
            XCTAssertEqual(period.unit, id.hasSuffix("yearly") ? .year : .month, id)
            XCTAssertFalse(product.displayPrice.isEmpty, id)
        }
    }

    // 로컬 서버가 필요하다
    func test2_purchasePath() async throws {
        await Store.shared.loadProducts()
        let product = try XCTUnwrap(Store.shared.product(tier: .pro, cycle: .monthly))

        if expectation == "rejected" {
            // 서버가 확인하지 못하면 거래를 끝내지 않아야 다음 실행 때 다시 보낸다
            do {
                _ = try await Store.shared.purchase(product)
                XCTFail("서버가 거절했는데 구매가 완료됨")
            } catch {}
            let stillOpen = try await unfinishedExists(product.id)
            XCTAssertTrue(stillOpen, "서버 확인 전에 거래가 끝남")
            return
        }

        let outcome = try await Store.shared.purchase(product)
        guard case .completed = outcome else { return XCTFail("구매 미완료: \\(outcome)") }
        let stillOpen = try await unfinishedExists(product.id)
        XCTAssertFalse(stillOpen, "서버가 받았는데 거래가 끝나지 않음")

        // 거래에 계정이 묶여 있어야 한다
        let latest = await Transaction.latest(for: product.id)
        guard case .verified(let transaction)? = latest else { return XCTFail("거래 없음") }
        XCTAssertEqual(transaction.appAccountToken?.uuidString.lowercased(),
                       Session.current?.userID.lowercased())

        let restored = try await Store.shared.restore()
        XCTAssertTrue(restored, "복원이 구매를 찾지 못함")
    }

    private func unfinishedExists(_ productID: String) async throws -&gt; Bool {
        for await result in Transaction.unfinished {
            if case .verified(let t) = result, t.productID == productID { return true }
        }
        return false
    }
}</code></pre>
<p>첫 번째 테스트는 로그인도 서버도 필요 없습니다. 앱 코드에 박힌 상품 ID가 <code>.storekit</code>에 모두 있는지, 월간·연간 기간이 맞는지만 봅니다. 처음에 상품 ID를 다른 플랫폼의 요금제 이름으로 가정해 넣었다가 App Store Connect에 실제로 등록한 ID에 맞춰 앱 코드, <code>.storekit</code>, 서버 기본값을 한꺼번에 바꾼 적이 있는데, 그런 변경 뒤에 앱과 <code>.storekit</code>이 어긋나지 않았는지를 몇 초 만에 확인할 수 있습니다. <code>.storekit</code>과 App Store Connect가 같은지는 이 테스트가 보지 못하므로 사람이 맞추거나, Xcode 14부터 있는 동기화 구성 파일을 씁니다.</p>
<p>두 번째 테스트는 앞의 <code>finish()</code> 규칙을 검증합니다. 로컬 서버가 503을 돌려주면 구매는 실패하고 거래는 미완료로 남아야 합니다. 서버가 받아 주면 거래가 끝나고, <code>appAccountToken</code>이 사용자 ID와 같고, 복원이 같은 구독을 찾아야 합니다. 실제 코드는 서버의 요금제 값이 바뀌었는지도 봅니다.</p>
<p>어느 시나리오를 돌릴지는 환경 변수로 나눴습니다. <code>xcodebuild</code>는 <code>TEST_RUNNER_</code> 접두어가 붙은 환경 변수를 접두어를 떼고 테스트 러너 프로세스에 넘깁니다. 호스티드 유닛 테스트에서는 그 러너가 곧 앱 프로세스입니다.</p>
<pre><code># 예시: 서버가 거절하는 경우(기본값)
xcodebuild test \\
  -project App.xcodeproj -scheme App \\
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro Max' \\
  -only-testing:AppStoreTests

# 로컬 서버가 받아 주는 경우
TEST_RUNNER_STORE_EXPECT=accepted xcodebuild test \\
  -project App.xcodeproj -scheme App \\
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro Max' \\
  -only-testing:AppStoreTests/StoreTests/test2_purchasePath</code></pre>

<h3>돌려보며 알게 된 것</h3>
<ul>
<li><strong>테스트 플랜의 StoreKit 설정은 효과가 없었습니다.</strong> <code>.xctestplan</code>에 <code>storeKitConfiguration</code>을 넣어봤지만 <code>xcodebuild</code> 실행에서는 아무 차이가 없었습니다. 코드에서 세션을 만드는 쪽이 확실했습니다.</li>
<li><strong>설정은 시뮬레이터에 남습니다.</strong> 이 테스트를 한 번 돌린 시뮬레이터에서는 이후 UI 테스트에서도 상품 가격이 떴습니다. Apple 문서도 테스트 환경은 하나뿐이고 모든 <code>SKTestSession</code>이 같은 환경을 제어한다고 설명합니다. 그래서 <code>clearTransactions()</code>로 시작하고 끝내며, 환경을 바꾸는 테스트는 병렬로 돌리지 않습니다.</li>
<li><strong>시뮬레이터 런타임을 고정해야 합니다.</strong> 제가 이 방식을 확인한 환경은 Xcode 26.0.1과 iOS 26.0 시뮬레이터 런타임입니다. Apple 개발자 포럼에는 iOS 26.5 시뮬레이터 런타임에서 Xcode 디버그 세션 밖에서 실행한 <code>SKTestSession</code>이 구성 파일을 저장하지 못한다는 보고가 있고, Apple 측이 알려진 문제라고 답했습니다(<a href="https://developer.apple.com/forums/thread/826971" target="_blank" rel="noopener">포럼 스레드</a>). CI에 넣는다면 런타임을 명시적으로 고정하고, 런타임을 올릴 때 이 테스트부터 돌려보는 편이 안전합니다.</li>
</ul>
<p>권하고 싶은 단언이 하나 더 있습니다. 위 코드에는 없지만, 구매 직후 <code>transaction.environment == .xcode</code>를 확인해 두면 구성이 조용히 빠져 샌드박스로 새는 경우를 테스트가 바로 잡습니다. <code>AppStore.Environment</code>에는 production, sandbox, xcode 세 값이 있고 iOS 16부터 쓸 수 있습니다.</p>
<p>로컬 환경이 오히려 나은 경우도 있습니다. Apple 비교표에 따르면 강제 StoreKit 오류, 승인 요청(Ask to Buy)의 승인·거절, 구독 가격 인상 시험은 샌드박스에서는 안 되고 Xcode 환경에서만 됩니다. <code>SKTestSession</code>의 <code>failTransactionsEnabled</code>, <code>askToBuyEnabled</code>, <code>expireSubscription(productIdentifier:)</code>, <code>refundTransaction(identifier:)</code>로 이런 시나리오를 코드로 만들 수 있습니다.</p>

<h2>서버 검증은 여기서 끊긴다</h2>
<p>Xcode가 서명한 JWS는 Apple 루트 인증서 체인 검증을 통과하지 못하고, 제대로 만든 서버라면 거절하는 게 정상입니다. 그래서 구매부터 복원까지의 성공 경로는 <strong>로컬 개발 서버에서만</strong> 서명 확인을 건너뛰게 해서 돌렸고, 운영 서버의 검증은 건드리지 않았습니다.</p>
<p>Apple의 공식 서버 라이브러리(App Store Server Library)도 이 구분을 갖고 있습니다. 검증기를 Xcode 환경으로 만들면 App Store가 서명한 데이터가 아니라는 이유로 서명 확인을 생략하고, 거래의 environment 값이 검증기 환경과 다르면 <code>INVALID_ENVIRONMENT</code>로 거절합니다. 그러니 Xcode 검증기는 명시적인 개발 플래그 뒤에만 두는 편이 안전합니다. 예시 코드입니다.</p>
<pre><code>// 예시: 환경별 검증기를 두고, Xcode 검증기는 로컬 개발에서만 켠다
import { SignedDataVerifier, Environment, VerificationException, VerificationStatus }
  from '@apple/app-store-server-library'

const verifiers = [
  new SignedDataVerifier(appleRoots, true, Environment.PRODUCTION, bundleId, appAppleId),
  new SignedDataVerifier(appleRoots, true, Environment.SANDBOX, bundleId),
]

// Xcode 검증기는 서명을 보지 않는다
if (process.env.ALLOW_XCODE_IAP === '1' &amp;&amp; process.env.NODE_ENV !== 'production') {
  verifiers.push(new SignedDataVerifier([], false, Environment.XCODE, bundleId))
}

export async function verifyTransaction(jws: string) {
  for (const v of verifiers) {
    try {
      return await v.verifyAndDecodeTransaction(jws)
    } catch (e) {
      if (e instanceof VerificationException &amp;&amp;
          e.status === VerificationStatus.INVALID_ENVIRONMENT) continue
      throw e
    }
  }
  throw new Error('no verifier matched the transaction environment')
}</code></pre>
<p>이 플래그가 운영에서 켜지면 누구나 직접 만든 JWS로 구독을 얻게 됩니다. 앱 쪽에도 비슷한 안전장치를 두었습니다. 디버그 빌드는 Info.plist에서 로컬 서버 주소를 읽을 수 있게 했고, 출시 스크립트는 만들어진 IPA 안의 Info.plist에 그 키가 남아 있으면 실패로 멈춥니다.</p>
<p>실제 Apple 인증서 체인 검증과 서버 알림은 결국 샌드박스에서 따로 확인했습니다. TestFlight 빌드를 실기기에 설치해 월간 구독을 사보니, 운영 서버가 이를 Sandbox 환경 구매로 처리했고 <code>SUBSCRIBED</code> 서버 알림이 반영되어 구독 기록이 생겼습니다. TestFlight는 샌드박스를 쓰므로 청구는 되지 않습니다. 이 단계만큼은 기기를 대신할 방법이 없었습니다.</p>

<h2>복원 테스트의 함정</h2>
<p>RevenueCat을 쓰는 앱에서 복원을 시험하다 헛걸음을 했습니다. 새 사용자로 시작하려고 <code>simctl uninstall</code>로 앱을 지웠더니 다시 깔고 복원을 눌러도 아무것도 나오지 않았습니다. 앱을 지우면 StoreKit 테스트 거래도 같이 사라지기 때문입니다.</p>
<p>필요한 건 "거래는 남고 앱 쪽 사용자만 새로운" 상태였습니다. 앱은 그대로 두고 앱 컨테이너의 <code>Library/Preferences/com.revenuecat.user_defaults.plist</code>만 지우면 RevenueCat이 새 익명 사용자로 시작합니다. 이 상태에서 복원을 누르면 RevenueCat이 권한을 새 사용자에게 옮겨 주고, 구독이 돌아왔다는 안내가 뜨는 것까지 확인할 수 있었습니다.</p>

<h2>검증할 수 있는 것과 없는 것</h2>
<p>로컬 StoreKit 테스트는 <strong>앱과 내 서버 사이의 로직</strong>을 검증하는 도구입니다. Apple 서버가 관여하는 부분은 검증하지 못합니다.</p>
<table>
<thead><tr><th>항목</th><th>로컬 StoreKit 테스트</th><th>대신 필요한 것</th></tr></thead>
<tbody>
<tr><td>상품 ID·기간·표시 가격·통화</td><td>가능</td><td>가격은 <code>.storekit</code>의 자리표시 값이라 실제 가격 등급과 무관</td></tr>
<tr><td>구매 성공·취소·실패(강제 오류)</td><td>가능</td><td>—</td></tr>
<tr><td>승인 요청(Ask to Buy) 승인·거절, 가격 인상 동의</td><td>가능</td><td>샌드박스에서는 불가</td></tr>
<tr><td><code>finish()</code> 시점, 미완료 거래·업데이트 처리</td><td>가능</td><td>—</td></tr>
<tr><td><code>appAccountToken</code> 연결, 복원</td><td>가능</td><td>—</td></tr>
<tr><td>갱신·만료·환불</td><td>가능</td><td>—</td></tr>
<tr><td>내 서버와의 연동 흐름</td><td>서명 확인을 끈 로컬 서버에서만</td><td>운영 경로는 샌드박스</td></tr>
<tr><td>App Store 서명 체인 검증</td><td>불가</td><td>TestFlight·실기기 샌드박스</td></tr>
<tr><td>App Store Server Notifications, App Store Server API 조회</td><td>불가(거래가 로컬에만 존재)</td><td>샌드박스</td></tr>
<tr><td>가족 공유</td><td>불가</td><td>샌드박스 테스트 가족과 구성원별 로그인</td></tr>
<tr><td>실제 결제·청구</td><td>불가</td><td>어떤 테스트 환경도 청구하지 않음. 출시 후 실거래</td></tr>
</tbody>
</table>
<p>가족 공유는 따로 적어 둘 만합니다. <code>.storekit</code>에도 상품별 Family Sharing 표시가 있지만, Apple이 안내하는 <a href="https://developer.apple.com/documentation/storekit/testing-family-sharing" target="_blank" rel="noopener">가족 공유 테스트</a>는 App Store Connect에서 샌드박스 테스트 가족을 만들고 구성원 계정마다 로그인해 확인하는 방식입니다. 공유받은 쪽의 <code>familyShared</code> 거래와 공유 해제 시의 회수를 보려면 샌드박스 로그인이 되는 기기가 필요하고, 그게 없다면 이 항목은 미검증으로 남겨 두는 게 정직합니다.</p>

<h2>체크리스트</h2>
<ul>
<li>시뮬레이터에서 결제 시트가 Apple 계정 로그인을 요구하면 로컬 구성이 적용되지 않은 것이다. 계정을 의심하기 전에 실행 경로부터 본다.</li>
<li>스킴의 <code>StoreKitConfigurationFileReference</code>는 <code>../../</code>가 .xcodeproj를 담은 폴더를 가리켰다. 틀려도 경고가 없다.</li>
<li>스킴의 StoreKit 구성은 Xcode IDE Run에서만 적용된다. <code>xcodebuild</code>, <code>simctl launch</code>, <code>flutter run</code>은 샌드박스로 간다.</li>
<li>헤드리스로 돌리려면 Host Application이 앱인 유닛 테스트에서 <code>SKTestSession</code>을 만든다. UI 테스트 러너에서 만든 세션은 앱에 닿지 않았다.</li>
<li><code>.storekit</code>은 테스트 번들 리소스에 두고, 출시 빌드에 실리지 않았는지 확인한다.</li>
<li>테스트에서 <code>transaction.environment == .xcode</code>를 단언해 샌드박스로 새는 경우를 잡는다.</li>
<li>시뮬레이터 런타임을 고정하고, 런타임을 올리면 이 테스트부터 돌린다.</li>
<li>서버의 Xcode 거래 허용은 개발 플래그 뒤에만 두고, 운영에서 켜질 수 없게 막는다.</li>
<li>서명 체인 검증, 서버 알림, 가족 공유는 TestFlight나 실기기 샌드박스로 따로 확인한다. 로컬 테스트 통과를 그 근거로 쓰지 않는다.</li>
</ul>
<p>지금은 결제 코드를 고치면 <code>xcodebuild</code>로 이 테스트부터 돌리고, 서버 서명과 알림처럼 Apple 서버가 끼는 부분만 TestFlight 빌드로 한 번 더 확인합니다. 두 단계가 각자 무엇을 보증하는지 섞지 않는 한, 기기 없이도 결제 코드를 꽤 자신 있게 고칠 수 있습니다.</p>
"""
},
{
"slug": "blog-live-transcript-follow-scroll",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "실시간 전사가 멈춘 것처럼 보이고 다른 언어가 섞이던 세 가지 원인",
"desc": "강의 녹음 중 전사 화면이 멈춘 듯 보이고 가끔 엉뚱한 언어가 찍혔습니다. 캐럿 기준 자동 스크롤, 휴지에만 기대는 확정, 느슨한 언어 감지를 고치고 시뮬레이터와 say 명령으로 검증한 기록입니다.",
"body": """
<p>라이트온 AI 노트는 강의나 설교를 녹음하면서 실시간으로 받아 적는 앱입니다. 1.2.7 버전으로 30분 분량의 설교를 안드로이드에서 녹음해 본 테스트에서 두 가지 보고가 올라왔습니다.</p>
<ul>
<li>"전사 중에 화면이 멈춰 있다. 업데이트하면서 자동 스크롤이 빠진 것 같다."</li>
<li>"30분쯤 지나면 이상한 언어가 잠깐 전사된다."</li>
</ul>
<p>따라가 보니 원인은 셋이었고, 어느 것도 코드가 빠져서 생긴 일이 아니었습니다. 자동 스크롤을 켜고 끄는 조건, 전사 엔진이 내려 준 확정 텍스트를 앱이 붙잡아 두는 규칙, 언어 자동 감지 설정입니다. 실시간 전사 화면을 만든다면 한 번쯤 밟을 자리라서 진단과 수정 과정을 그대로 적어 둡니다.</p>
<h2>먼저 의심한 것들, 그리고 아니었던 이유</h2>
<p><strong>자동 스크롤 코드가 빠졌나?</strong> git 이력을 보니 한 달 전에 넣은 "받아쓰는 동안 문서 끝을 따라가는" 코드는 그대로 있었습니다. 있는데 동작하지 않는 상황이었습니다.</p>
<p><strong>30분짜리 타이머가 있나?</strong> "30분쯤"이라는 단서가 구체적이어서 시간에 걸린 로직부터 찾았습니다. 앱 코드에는 30분에 반응하는 타이머가 없었고, 전사 엔진인 Soniox도 공식 문서상 실시간 세션 상한이 300분입니다. 시간이 아니라면 그 무렵 마이크로 들어온 소리를 의심해야 합니다.</p>
<h2>재현 환경: iOS 시뮬레이터와 macOS say</h2>
<p>보고는 안드로이드에서 왔지만 스크롤과 확정 로직은 모두 Dart 코드라 플랫폼을 타지 않습니다. 그래서 맥에서 바로 띄우는 iOS 시뮬레이터로 재현했습니다.</p>
<p>마이크 기능은 사람이 직접 말해야 검증되니 자꾸 뒤로 밀립니다. 그래서 맥이 말하게 했습니다. macOS <code>say</code>로 한국어 원고를 읽히면 맥 스피커의 소리가 맥 마이크로 들어가고, 시뮬레이터는 맥의 오디오 입력을 마이크로 씁니다. 녹음 버튼만 눌러 두면 같은 원고를 몇 번이든 같은 조건으로 흘려 넣을 수 있습니다.</p>
<pre><code># 1) 시뮬레이터용 디버그 빌드 → 설치 → 실행
flutter build ios --simulator --debug --dart-define-from-file=&lt;환경 파일&gt;
xcrun simctl install $UDID build/ios/iphonesimulator/Runner.app
xcrun simctl launch  $UDID &lt;번들 ID&gt;

# 2) 앱에서 녹음을 시작한 뒤, 맥이 원고를 읽게 한다 (Yuna = macOS 한국어 음성)
say -v Yuna -r 170 -f sermon.txt

# "쉬지 않는 화자" 만들기: 마침표와 줄바꿈을 지워 문장 사이 쉼을 줄인다
tr -d '.\\n' &lt; sermon.txt &gt; sermon_nopause.txt
say -v Yuna -r 175 -f sermon_nopause.txt

# 3) 앱 로그에서 확정 발화만 뽑는다
xcrun simctl spawn $UDID log show --last 2m \\
  --predicate 'process == "Runner"' --style compact \\
  | grep -E '\\[SonioxStream\\] (FINAL|dropping)'</code></pre>
<p>판단은 로그로 했습니다. 앱은 확정 발화마다 오디오 구간(초)과 텍스트를 한 줄로 남깁니다.</p>
<pre><code>[SonioxStream] FINAL spk=null→A lang=ko [1.26..8.64] "…"</code></pre>
<p>이 구간 숫자만 모으면 확정이 몇 초 간격으로 들어오는지 보입니다. 스크린샷으로는 "멈춘 것 같다"까지만 알 수 있지만, 로그로는 멈춘 게 스크롤인지 데이터인지를 가를 수 있습니다.</p>
<p>단, 테스트하던 맥에서 뉴스 영상 소리가 함께 재생되고 있어 마이크에는 낭독과 뉴스 음성이 겹쳐 들어갔습니다. 이 환경으로 전사 <em>품질</em>은 평가할 수 없지만, "언제 확정되는가, 화면이 따라가는가"라는 <em>동작</em>을 보기에는 충분했고 배경 소리가 깔리는 현장과 오히려 비슷했습니다.</p>
<h2>원인 1 — 팔로우 조건이 캐럿 위치에 묶여 있었다</h2>
<p>편집 화면은 바깥 <code>SingleChildScrollView</code> 안에 <code>maxLines: null</code>인 본문 <code>TextField</code>가 있고, 그 아래에 회색 임시 자막 줄이 붙는 구조입니다. 여기서는 컨트롤러로 캐럿을 끝에 옮겨도 화면이 따라 내려가지 않아서, 확정 문장을 삽입한 뒤 바깥 스크롤을 직접 끝으로 점프시키게 했습니다. 문제는 점프 여부를 정하는 조건이었습니다.</p>
<pre><code>// 수정 전: 확정 발화를 본문 끝에 붙일 때 (실제 코드 발췌)
final oldSel = _contentController.selection;
final caretFollowingEnd = !oldSel.isValid ||
    (oldSel.isCollapsed &amp;&amp; oldSel.baseOffset &gt;= currentText.length);
newSelection = caretFollowingEnd
    ? TextSelection.collapsed(offset: newText.length)
    : oldSel;                 // 캐럿이 끝이 아니면 그 자리에 둔다
followToEnd = caretFollowingEnd;</code></pre>
<p>의도는 좋았습니다. 문서 중간에서 오타를 고치는 사람을 새 문장이 들어올 때마다 끝으로 끌어내리면 방해가 됩니다. 그래서 "캐럿이 끝에 있다"를 "따라가며 보고 있다"로 해석했습니다.</p>
<p>그런데 이 조건은 한 번 꺼지면 다시 켜지지 않습니다. 캐럿이 끝에 없으면 선택 영역을 그대로 두고 새 텍스트는 문서 끝에 붙으니, 캐럿은 점점 끝에서 멀어지고 조건은 계속 거짓으로 남습니다. 사용자가 직접 캐럿을 맨 끝으로 옮기기 전까지 그 녹음 내내 팔로우가 꺼집니다.</p>
<p>캐럿이 끝에서 떨어지는 일도 흔했습니다. 본문을 한 번 탭하면 충분하고, 화면이 잠겼다 풀릴 때 키보드(IME)가 예전 입력 상태를 되돌려 주면서 캐럿이 옮겨지기도 합니다. 설교를 녹음하며 폰을 잠그는 건 평범한 사용인데, 아무것도 편집하지 않은 사용자를 앱은 "편집 중"으로 보고 있었습니다.</p>
<h2>원인 2 — 휴지(&lt;end&gt;)가 와야만 확정했다</h2>
<p>캐럿을 건드리지 않았는데도 쉬지 않고 읽히면 화면이 멈춘 것처럼 보였습니다. 확정 규칙을 고치기 전 빌드의 로그가 이유를 보여 줬습니다. 녹음을 시작하고 약 10초 뒤 확정 한 줄(<code>[1.26..8.64]</code>)이 찍힌 다음, 1초마다 찍히는 오디오 전송량 로그가 180초 가까이 올라가는 동안 확정 로그가 한 줄도 추가되지 않았습니다. 오디오는 계속 올라가는데 확정만 내려오지 않았습니다.</p>
<p>Soniox 실시간 API는 토큰을 두 종류로 보냅니다. 확정 전(non-final) 토큰은 바로 나타나지만 오디오가 더 들어오면 바뀌거나 사라질 수 있고, 확정(final) 토큰은 한 번 확정되면 다시 바뀌지 않습니다. 엔드포인트 감지(<code>enable_endpoint_detection</code>)를 켜면 말이 끝났다고 판단한 지점에서 구간을 확정하고 <code>&lt;end&gt;</code>라는 특별한 토큰을 보냅니다.</p>
<p>앱은 그 위에 한 겹을 더 두고 있었습니다. 확정 토큰도 바로 본문에 넣지 않고 버퍼에 모았다가, <code>&lt;end&gt;</code>가 오면 한 발화로 묶어 내보냈습니다. 앱에서 발화 한 건은 화자 라벨, 언어, 시간 구간, 오디오 조각이 함께 묶이는 단위라 휴지로 끊는 설계 자체는 합리적이었습니다. 버퍼의 확정 토큰과 확정 전 꼬리는 합쳐서 회색 임시 줄로 보여 줬습니다.</p>
<p>문제는 <code>&lt;end&gt;</code>가 휴지에 달려 있다는 점입니다. 설교자가 쉬지 않고 말하거나 배경 음악, 다른 목소리가 계속 깔리면 휴지가 감지되지 않고, 확정 토큰은 버퍼에 몇 분씩 쌓입니다. 자동 스크롤은 본문 삽입 때만 움직였으니 화면도 그대로이고, 회색 임시 줄은 화면 아래 보이지 않는 곳에서 길어집니다. 사용자 눈에는 정확히 "화면이 멈춘 것"입니다.</p>
<p>Soniox의 <code>max_endpoint_delay_ms</code> 같은 파라미터는 문서상 <em>말이 끝난 뒤</em> 엔드포인트를 얼마나 빨리 돌려줄지를 정하므로, 말이 끝나지 않는 상황에는 소용이 없습니다. 게다가 토큰은 이미 확정 상태로 와 있었고 붙잡고 있던 건 앱이었습니다. 고칠 곳은 앱의 버퍼 규칙이었습니다.</p>
<h2>원인 3 — 언어 힌트는 제한이 아니었다</h2>
<p>음성 인식 언어가 기본값 "자동"일 때 앱이 보내던 설정입니다.</p>
<pre><code>// 수정 전: 언어 설정이 "자동"일 때의 요청 일부
'language_hints': ['ko', 'en', 'zh', 'ja'],
'enable_language_identification': true,
'enable_endpoint_detection': true,
// language_hints_strict 없음</code></pre>
<p>Soniox 문서는 언어 힌트를 분명하게 설명합니다. 힌트는 인식을 그 언어들 쪽으로 <em>기울일</em> 뿐, 그 언어로 <em>제한하지 않습니다</em>. Soniox는 60개가 넘는 언어를 인식하므로 힌트 밖의 언어도 나올 수 있습니다. 평소 한국어는 한국어로 잘 나오지만, 소음이나 음악이 섞이거나 마이크가 다시 시작된 직후처럼 오디오가 애매한 구간은 다른 언어로 판정될 수 있고, 그러면 그 언어의 문자로 그럴듯한 문장이 몇 초 찍힙니다. "30분쯤"은 그런 구간이 마침 그 무렵에 있었다는 뜻이었지, 30분이라는 시간에 의미가 있던 게 아니었습니다.</p>
<h2>수정 1 — 팔로우를 스크롤 위치로 판단한다</h2>
<p>캐럿은 사용자의 의도를 대신 알려 주는 지표로 너무 약했습니다. 의도가 직접 드러나는 신호는 따로 있습니다. 손가락으로 화면을 끌어 올렸는가입니다.</p>
<pre><code>// 실제 코드 발췌. 한국어 주석은 설명을 위해 덧붙였습니다.
static const double _followSlackPx = 48;   // 본문 아래 여백은 200px

bool _onContentScroll(ScrollNotification n) {
  if (n.depth != 0) return false;           // 안쪽 뷰포트에서 올라온 알림은 무시
  final m = n.metrics;
  if (!m.hasContentDimensions) return false;
  final atBottom = m.pixels &gt;= m.maxScrollExtent - _followSlackPx;
  if (n is ScrollUpdateNotification &amp;&amp; n.dragDetails != null) {
    _userScrolledAway = !atBottom;          // 손가락으로 끌었을 때만 판단
  } else if (n is ScrollEndNotification &amp;&amp; atBottom) {
    _userScrolledAway = false;              // 바닥에서 멈추면 다시 따라간다
  }
  return false;
}</code></pre>
<p>핵심은 <code>dragDetails</code>입니다. Flutter 문서에 따르면 <code>ScrollUpdateNotification.dragDetails</code>는 드래그 때문에 스크롤 위치가 바뀌었을 때만 채워지고, 그 밖에는 <code>null</code>입니다. 그래서 앱이 <code>jumpTo</code>로 내려간 것을 사용자의 스크롤로 오인하지 않습니다. 위로 끌어 올리면 팔로우를 멈추고, 스크롤이 바닥 근처에서 멈추면 다시 켭니다. 본문 아래 여백이 200px이라 48px 정도 어긋나도 가려지는 글은 없습니다.</p>
<p>캐럿을 아예 무시하지는 않았습니다. 대신 "최근에 사용자가 직접 만졌는가"라는 조건을 붙였습니다.</p>
<pre><code>DateTime? _lastEditorTouchAt;               // 탭·타이핑·포커스 때 갱신
static const Duration _editingGrace = Duration(seconds: 45);

bool get _recentlyEditing =&gt;
    _lastEditorTouchAt != null &amp;&amp;
    DateTime.now().difference(_lastEditorTouchAt!) &lt; _editingGrace;

// 수정 후: 확정 발화를 본문 끝에 붙일 때
final caretAtEnd = !oldSel.isValid ||
    (oldSel.isCollapsed &amp;&amp; oldSel.baseOffset &gt;= currentText.length);
final editingElsewhere = !caretAtEnd &amp;&amp; _recentlyEditing;
newSelection = editingElsewhere
    ? oldSel
    : TextSelection.collapsed(offset: newText.length);
followToEnd = !editingElsewhere &amp;&amp; !_painting &amp;&amp; !_userScrolledAway;</code></pre>
<p>탭, 타이핑, 포커스 시각을 기록해 두고 그로부터 45초 안에서만 중간의 캐럿을 "편집 중"으로 봅니다. 그 밖이라면 떠밀린 캐럿이니 끝으로 옮기고 계속 따라갑니다. 오타를 고친 뒤 45초가 지나면 저절로 다시 따라가므로 영영 꺼지는 일이 없습니다. <code>_painting</code>은 형광펜 모드로, 이때는 따라가지 않습니다.</p>
<p>회색 임시 줄도 따라가게 했습니다. 그래야 원인 2 같은 상황에서도 화면이 움직입니다. 새 녹음을 시작하면 위로 올려 둔 상태도 초기화합니다.</p>
<pre><code>ref.listen&lt;SpeechState&gt;(speechProvider, (previous, next) {
  // 새 녹음은 항상 따라가는 상태로 시작한다
  if (next.isListening &amp;&amp; previous?.isListening != true) {
    _userScrolledAway = false;
  }
  // 회색 임시 줄이 바뀔 때도 끝으로 내린다
  if (next.currentText.isNotEmpty &amp;&amp;
      next.currentText != previous?.currentText &amp;&amp;
      _followingTranscript()) {
    _scrollTranscriptToEnd();
  }
  // ... 확정 발화 삽입 처리
});

void _scrollTranscriptToEnd() {
  WidgetsBinding.instance.addPostFrameCallback((_) {
    if (!mounted || !_contentScrollController.hasClients) return;
    final max = _contentScrollController.position.maxScrollExtent;
    if (_contentScrollController.offset &gt;= max) return;
    _contentScrollController.jumpTo(max);
  });
}</code></pre>
<p>스크롤은 기존대로 다음 프레임에 <code>maxScrollExtent</code>로 점프합니다. 프레임이 끝나야 새 텍스트 높이가 반영되고, 전사 조각은 애니메이션이 끝나기 전에 다음 것이 들어와서 <code>animateTo</code>를 쓰면 애니메이션끼리 겹칩니다.</p>
<h2>수정 2 — 휴지가 오지 않아도 확정한다</h2>
<p>버퍼에 상한을 두었습니다. 쌓인 확정 토큰이 오디오 시간으로 12초를 넘기면, 12초 지점을 지난 마지막 문장 끝(<code>.</code> <code>!</code> <code>?</code> <code>。</code> 등)에서 잘라 그 앞까지를 한 발화로 내보냅니다. 문장부호가 전혀 없으면 30초에서 무조건 내보냅니다. 자른 지점 뒤의 토큰은 버퍼에 그대로 남아 다음 휴지나 다음 조기 확정 때 함께 나갑니다.</p>
<pre><code>// 실제 코드 발췌 (Soniox 스트리밍 서비스)
static const int _softFlushAfterMs = 12000;
static const int _hardFlushAfterMs = 30000;
static final RegExp _sentenceEnd = RegExp(r'[.!?。！？]\\s*$');

bool _flushEarlyIfDue() {
  if (_pendingFinals.isEmpty) return false;
  final first = _startOf(_pendingFinals.first);
  final span = _endOf(_pendingFinals.last) - first;   // 오디오 시간(ms)
  if (span &lt; _softFlushAfterMs) return false;

  var cut = -1;
  for (var i = _pendingFinals.length - 1; i &gt;= 0; i--) {
    final t = _pendingFinals[i];
    if (!_sentenceEnd.hasMatch((t['text'] as String?) ?? '')) continue;
    if (_endOf(t) - first &gt;= _softFlushAfterMs) cut = i;
    break; // 마지막 문장 끝만 후보
  }
  if (cut &lt; 0) {
    if (span &lt; _hardFlushAfterMs) return false;
    cut = _pendingFinals.length - 1;                  // 30초: 전부 내보낸다
  }

  final tail = _pendingFinals.sublist(cut + 1);
  _pendingFinals.removeRange(cut + 1, _pendingFinals.length);
  _flushUtterance(keepSeenFinals: true);
  _pendingFinals.addAll(tail);                        // 자른 뒤는 계속 보류
  return true;
}

// 메시지 처리부 (분기를 합쳐 요약)
if (sawEnd) {
  _flushUtterance();                  // 휴지: 버퍼 전체를 한 발화로
} else {
  _flushEarlyIfDue();                 // 휴지가 없어도 상한을 넘겼으면 일부 확정
  // 남은 확정 토큰 + 확정 전 꼬리 = 회색 임시 줄
  _maybeEmitInterim(
    _pendingFinals.map((t) =&gt; t['text']).join() + newInterimParts.join(),
  );
}</code></pre>
<p>기준은 벽시계가 아니라 토큰의 <code>start_ms</code>/<code>end_ms</code>, 즉 오디오 시간입니다. 네트워크가 느려도 같은 오디오에는 같은 결과가 나오고, 소켓 없이 메시지만 흘려 넣는 테스트로 규칙을 검증할 수 있습니다.</p>
<p>첫 구현은 버퍼의 <em>맨 마지막</em> 토큰이 문장부호로 끝날 때만 12초 조건으로 잘랐습니다. 이 버전에 쉼을 줄인 원고를 흘리자 로그에 <code>[21.72..53.28]</code>, 31초가 넘는 발화가 한 덩어리로 찍혔습니다. 30초 강제 확정은 동작했지만, 그 31초 동안 문장 끝 조건은 한 번도 맞지 않았다는 뜻입니다. 메시지는 문장 경계에 맞춰 끊겨 오지 않으니, 도착한 순간 마지막 토큰이 마침표로 끝나 있을 가능성은 낮습니다. 그래서 버퍼를 뒤에서부터 훑어 마지막 문장 끝에서 자르도록 바꿨습니다.</p>
<p>놓치기 쉬운 부분도 있습니다. 기존 코드는 같은 <code>start_ms</code>의 확정 토큰이 인접 메시지에서 다시 들어오는 경우를 막으려고 본 시작 시각을 집합에 들고 있다가 발화를 내보낼 때마다 비웠습니다. 조기 확정은 말하는 도중에 자르는 것이라 여기서 비우면 중복 방어가 풀리므로 <code>keepSeenFinals: true</code>로 유지합니다.</p>
<h2>수정 3 — strict 힌트와 문자 체계 가드</h2>
<p>요청에 <code>language_hints_strict</code>를 추가했습니다.</p>
<pre><code>'language_hints': hints,
'language_hints_strict': true,
'enable_language_identification': true,
'enable_endpoint_detection': true,</code></pre>
<p>Soniox 문서는 이 옵션을 켜면 모델이 지정한 언어로만 출력하는 쪽을 강하게 선호한다고 설명하면서, 최선 노력일 뿐 보장은 아니며 언어를 하나만 지정했을 때 가장 견고하다고 적어 둡니다. 자동 모드는 언어를 넷 지정하니 strict만 믿을 수는 없었습니다.</p>
<p>그래서 앱 쪽에 방어선을 하나 더 두었습니다. 확정 발화를 내보내기 직전에 글자마다 문자 체계(한글, 라틴, 가나, 한자, 그 밖)를 판별하고, 힌트 언어들이 쓰지 않는 문자가 절반 이상이면 그 발화를 버립니다.</p>
<pre><code>// 실제 코드 발췌 (문자 체계 가드)
static const double dropRatio = 0.5;

static bool isOutsideHints(String text, List&lt;String&gt; hints) {
  if (hints.isEmpty) return false;
  final allowed = &lt;_Script&gt;{_Script.latin};          // 라틴은 항상 허용
  for (final h in hints) {
    final s = _scriptsFor(h.toLowerCase());
    if (s == null) return false;                     // 모르는 언어면 가드 해제
    allowed.addAll(s);
  }
  var letters = 0;
  var foreign = 0;
  for (final rune in text.runes) {
    final script = _classify(rune);
    if (script == null) continue;                    // 숫자·문장부호·공백
    letters++;
    if (!allowed.contains(script)) foreign++;
  }
  if (letters == 0) return false;
  return foreign / letters &gt;= dropRatio;
}

static Set&lt;_Script&gt;? _scriptsFor(String code) =&gt; switch (code) {
      'ko' =&gt; const {_Script.hangul},
      'en' =&gt; const {_Script.latin},
      'ja' =&gt; const {_Script.kana, _Script.han},
      'zh' =&gt; const {_Script.han},
      _ =&gt; null,
    };</code></pre>
<p>규칙을 정하면서 고민한 지점은 셋입니다.</p>
<ul>
<li><strong>라틴 문자는 항상 허용합니다.</strong> 한국어 강의에도 "AI", "GPT" 같은 용어가 계속 나옵니다.</li>
<li><strong>숫자, 문장부호, 공백은 세지 않습니다.</strong> "3:16" 같은 장절 표기만 있는 발화가 버려지면 안 됩니다.</li>
<li><strong>모르는 언어 코드가 힌트에 있으면 가드를 끕니다.</strong> 어떤 문자를 쓰는지 모르면서 버리느니 두는 편이 안전합니다.</li>
</ul>
<p>한계도 분명합니다. 자동 모드에서는 가나와 한자가 허용되므로, 한국어를 일본어로 잘못 판정한 출력은 그대로 통과합니다. 자동 모드의 가드가 잡는 건 태국·키릴 문자처럼 네 언어 어디에도 없는 문자뿐입니다. 한국어 강의라면 설정에서 음성 인식 언어를 "한국어"로 지정하는 것이 가장 확실합니다. 힌트가 하나면 strict가 가장 견고하고, 가드도 분류해 둔 다른 문자(가나·한자·키릴·태국 등)를 모두 걸러 냅니다. 버린 발화는 화면에 남지 않지만, 다른 문자로 찍힌 몇 초짜리 문장은 어차피 읽을 수 없어서 버리는 쪽을 택했습니다.</p>
<h2>어떻게 검증했나</h2>
<p><strong>유닛 테스트.</strong> 조기 확정 규칙은 서버 메시지를 소켓 없이 흘려 넣는 테스트용 진입점(<code>handleServerMessage</code>)을 만들어 다섯 가지 경우로 고정했습니다.</p>
<ul>
<li>평소처럼 쉬어 가며 말하면 지금처럼 <code>&lt;end&gt;</code>까지 기다린다.</li>
<li>12초를 넘겨도 문장 중간이면 기다리고, 12초 지점 이후 문장 끝이 오면 거기까지만 확정한다. 남은 토큰은 임시 줄에 남았다가 다음 <code>&lt;end&gt;</code>에 나간다.</li>
<li>문장 끝이 있어도 그 위치가 12초 이전이면 자르지 않는다.</li>
<li>문장 끝이 전혀 없으면 30초에서 무조건 확정한다.</li>
<li>조기 확정 뒤 같은 토큰이 다시 와도 두 번 나가지 않는다.</li>
</ul>
<p>문자 체계 가드는 아홉 가지 경우로 고정했습니다. 한국어 속 영어 용어나 문장 끝에 섞인 가나 한 글자는 통과하고, 한국어 힌트에서 가나·한자 문장과 자동 힌트에서 태국·키릴 문장은 버려지며, 모르는 힌트 코드에서는 가드가 꺼지는 식입니다.</p>
<p><strong>시뮬레이터.</strong> 수정한 빌드로 긴 노트를 열고 녹음하자 첫 문장에서 바닥으로 내려갔고, 위로 끌어 올리면 멈췄다가 바닥으로 내리면 다시 따라갔습니다. 쉼을 줄인 원고에서도 확정이 계속 들어오고 임시 줄이 화면 안에 머물렀습니다. 정적 분석 경고 0건, 전체 테스트 224개 통과를 확인하고 1.2.8로 내보냈습니다.</p>
<p>시뮬레이터가 보여 주는 건 동작까지입니다. 30분이 넘는 실제 설교에서 다른 언어가 섞이지 않는지는 실기기 녹음으로 따로 확인해야 합니다.</p>
<h2>같은 문제를 피하는 체크리스트</h2>
<ul>
<li><strong>대리 지표로 사용자 의도를 추정한다면, 그 지표를 움직이는 다른 경로를 전부 적어 본다.</strong> 캐럿은 탭이나 IME 상태 복원으로도 움직입니다. 의도가 직접 드러나는 신호(드래그)가 있으면 그쪽을 씁니다.</li>
<li><strong>꺼진 기능이 저절로 다시 켜지는지 확인한다.</strong> "조건이 거짓이면 상태를 유지"하는 코드는 그 상태가 조건을 계속 거짓으로 만들면 영구히 꺼집니다.</li>
<li><strong>실시간 화면은 임시 텍스트까지 따라가야 한다.</strong> 사용자는 확정과 임시를 구분하지 않습니다.</li>
<li><strong>외부 신호를 기다리는 버퍼에는 상한을 둔다.</strong> 휴지나 서버 이벤트처럼 언젠가 올 거라 믿는 신호는 오지 않을 수 있습니다. 상한은 데이터 자체의 시간(오디오 ms)으로 재면 테스트하기 쉽습니다.</li>
<li><strong>언어 힌트가 편향인지 제한인지, strict가 보장인지 최선 노력인지 공급자 문서로 확인한다.</strong> 그리고 앱 쪽에 값싼 검증을 하나 둡니다. 문자 체계 검사는 단순하지만 엉뚱한 문자가 찍히는 것은 막아 줍니다.</li>
<li><strong>마이크 기능은 <code>say</code>로 자동화한다.</strong> 원고 파일 하나로 같은 조건을 반복할 수 있고, 문장부호를 지워 쉬지 않는 화자를 흉내 낼 수 있습니다.</li>
</ul>
<div class="tip"><strong>라이트온 AI 노트</strong> — 강의·설교를 녹음하면서 실시간으로 받아 적고, 요약과 복습 카드까지 이어 줍니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.ailecturenote" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-flutter-scheduled-notification-missing",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "flutter_local_notifications 예약 알림이 안 뜰 때 — 원인 4가지와 점검표",
"desc": "매일 복습 알림이 출시 후 한 번도 뜨지 않았습니다. 빠진 리시버, 비어 있던 저장본, 서울로 고정된 시간대, 연결되지 않은 iOS를 adb와 시뮬레이터로 하나씩 확인한 기록과 점검표입니다.",
"body": """
<p>라이트온 AI 노트는 강의 노트에서 플래시카드를 만들어 간격 반복으로 복습하게 하는 앱이고, 설정에서 켜 두면 매일 정한 시각에 복습할 때를 알려 주는 <strong>복습 알림</strong>이 있습니다. 그런데 이 알림은 안드로이드에서 기능을 넣은 뒤로 <strong>한 번도 뜬 적이 없었고</strong>, iOS에서는 토글이 켜지지도 않았습니다. 따라가 보니 원인은 넷이었고, 모두 에러 메시지 하나 없이 조용히 어긋나는 종류였습니다.</p>

<h2>증상</h2>
<p>예약은 <code>flutter_local_notifications</code> 17.2.4의 <code>zonedSchedule</code>로 합니다. 매일 반복은 <code>matchDateTimeComponents</code>로 걸고, 안드로이드는 정확한 알람 권한이 필요 없는 inexact 모드를 씁니다.</p>
<pre><code>await _plugin.zonedSchedule(
  _dailyReviewId,
  _title,
  _body,
  _nextInstanceOf(hour, minute),
  details,
  androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
  uiLocalNotificationDateInterpretation:
      UILocalNotificationDateInterpretation.absoluteTime,
  matchDateTimeComponents: DateTimeComponents.time,
);</code></pre>
<p>안드로이드에서는 토글을 켜고 시각을 골라도 그 시각에도, 다음 날에도 알림이 오지 않았습니다. iOS에서는 토글을 누르면 설정에서 알림을 허용하라는 안내만 떴는데, 정작 시스템 권한 창은 한 번도 나온 적이 없었습니다.</p>

<h2>먼저 가를 것: 알람이 울렸나, 알림이 게시됐나</h2>
<p>안드로이드의 예약 알림은 두 단계로 움직입니다. 플러그인이 <code>AlarmManager</code>에 알람을 걸고, 시각이 되면 시스템이 브로드캐스트한 인텐트를 플러그인의 리시버가 받아 알림을 게시합니다. 알림이 안 뜨면 어느 단계에서 끊겼는지부터 갈라야 합니다.</p>
<p>문제의 1.2.8을 릴리스 빌드로 다시 만들어 API 36 에뮬레이터에 깔고, 시계를 건드리지 않은 채 설정 화면에서 알림 시각을 3분 뒤로 잡았습니다.</p>
<pre><code>$ adb shell dumpsys alarm | grep -A3 'ailecturenote}'
  tag=*walarm*:com.lightonpluslab.ailecturenote/com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver
  type=RTC_WAKEUP origWhen=2026-10-16 14:37:00.000 window=+2m15s896ms repeatInterval=0 ...</code></pre>
<p>알람은 걸렸고, 시각이 지나자 대기 목록에서 사라졌으며, 같은 출력의 알람 통계에는 <code>1 wakes 1 alarms</code>로 전달된 기록이 남았습니다. <strong>알람은 울렸습니다.</strong> 그런데 게시된 알림은 0건이었습니다.</p>
<pre><code>$ adb shell dumpsys notification --noredact | grep -c 'pkg=com.lightonpluslab.ailecturenote'
0</code></pre>
<p>이것만으로 도즈·배터리 최적화(전달 기록이 있음)와 inexact 지연(창이 끝났음)은 빠집니다. 알람은 울렸는데, 그걸 받아 알림을 만드는 쪽이 일하지 않은 겁니다. logcat을 앱과 플러그인 이름으로 걸러 봐도 관련된 줄은 없었습니다.</p>

<h2>원인 1: 아무도 받지 않는 브로드캐스트</h2>
<p>dumpsys의 <code>tag</code>가 가리키는 대상은 <code>ScheduledNotificationReceiver</code>라는 명시적 컴포넌트입니다. 그런데 빌드된 APK의 매니페스트에는 플러그인 이름이 한 번도 나오지 않았습니다.</p>
<pre><code>$ aapt2 dump xmltree --file AndroidManifest.xml app-1.2.8.apk | grep -c -i flutterlocalnotifications
0</code></pre>
<p>이 플러그인은 16 버전부터 자기 매니페스트에 <code>VIBRATE</code>와 <code>POST_NOTIFICATIONS</code>만 선언하고, 예약 알림에 필요한 리시버 두 개는 앱이 직접 넣도록 README에 적어 둡니다. 처음 기능을 넣을 때 그 절을 놓쳤습니다. 명시적 인텐트의 대상이 매니페스트에 없으니 브로드캐스트는 갈 곳이 없고, 실행되지 않은 플러그인 코드는 예외도 로그도 남기지 않습니다.</p>
<p>다음 날 알람이 생기지 않은 것도 같은 이유입니다. 안드로이드에서 매일 반복은 운영체제의 반복 알람이 아닙니다. 한 번짜리 알람을 받은 리시버가 알림을 띄운 직후 <strong>다음 회차를 직접 다시 겁니다.</strong></p>
<pre><code>// flutter_local_notifications 17.2.4, ScheduledNotificationReceiver.onReceive
FlutterLocalNotificationsPlugin.showNotification(context, notificationDetails);
FlutterLocalNotificationsPlugin.scheduleNextNotification(context, notificationDetails);</code></pre>
<p>수정은 README에 적힌 그대로입니다.</p>
<pre><code>&lt;uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/&gt;

&lt;!-- &lt;application&gt; 안 --&gt;
&lt;receiver
    android:exported="false"
    android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver" /&gt;
&lt;receiver
    android:exported="false"
    android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"&gt;
    &lt;intent-filter&gt;
        &lt;action android:name="android.intent.action.BOOT_COMPLETED"/&gt;
        &lt;action android:name="android.intent.action.MY_PACKAGE_REPLACED"/&gt;
        &lt;action android:name="android.intent.action.QUICKBOOT_POWERON" /&gt;
        &lt;action android:name="com.htc.intent.action.QUICKBOOT_POWERON"/&gt;
    &lt;/intent-filter&gt;
&lt;/receiver&gt;</code></pre>
<p><code>RECEIVE_BOOT_COMPLETED</code>는 다른 플러그인이 병합해 오고 있었지만, 그 플러그인이 빠지는 날 부트 리시버가 다시 조용히 죽지 않도록 직접 선언했습니다. 플러그인이 런타임에 이름으로 찾는 알림 아이콘 <code>@mipmap/ic_launcher</code>도 리소스 축소기가 지우지 않게 <code>res/raw/keep.xml</code>에 넣었습니다. README는 아이콘이 지워지면 알림이 조용히 실패할 수 있다고 경고합니다.</p>

<h2>원인 2: 리시버를 넣어도 돌아오지 않은 알림</h2>
<p>여기서 끝난 줄 알았습니다. 그런데 <strong>1.2.8에서 알림을 켜 둔 채 업데이트하는 경우</strong>를 재현하자 결과가 이상했습니다. 리시버를 넣은 빌드를 <code>adb install -r</code>로 덮어 설치하자 부트 리시버가 실행된 흔적은 logcat에 찍혔는데, <code>dumpsys alarm</code>에는 알람이 없었습니다.</p>
<pre><code>I/ActivityManager: Start proc ...:com.lightonpluslab.ailecturenote/... for broadcast
  {com.lightonpluslab.ailecturenote/com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver}</code></pre>
<p>플러그인은 예약한 알림의 사본을 SharedPreferences에 Gson JSON으로 저장하고, 부트 리시버는 재부팅이나 업데이트 때 그 사본으로 알람을 다시 겁니다. <code>AlarmManager</code> 문서에 적혀 있듯 알람은 재부팅하면 지워지므로 플러그인에게는 이 사본이 유일한 복구 수단입니다. 사본은 이렇게 읽습니다.</p>
<pre><code>// flutter_local_notifications 17.2.4, loadScheduledNotifications
Type type = new TypeToken&lt;ArrayList&lt;NotificationDetails&gt;&gt;() {}.getType();
scheduledNotifications = gson.fromJson(json, type);</code></pre>
<p>가장 유력하게 본 용의자는 이 <code>TypeToken</code>입니다. TypeToken은 익명 하위 클래스에 남은 제네릭 시그니처를 리플렉션으로 읽는데, AGP 8.0부터 기본인 R8 full mode는 <code>-keepattributes Signature</code>가 있어도 keep 규칙에 걸린 클래스에만 시그니처를 남깁니다. 시그니처를 잃은 TypeToken은 이렇게 시작하는 예외를 던집니다.</p>
<pre><code>TypeToken must be created with a type argument: new TypeToken&lt;...&gt;() {};</code></pre>
<p>앱 빌드가 쓰던 Gson 2.10.1 jar에는 R8 규칙이 들어 있지 않고(2.11.0부터 <code>META-INF/proguard/gson.pro</code>가 포함됩니다), README도 플러그인 v18 이하는 Gson 규칙을 앱이 직접 넣으라고 안내합니다. 1.2.8의 앱 규칙 파일에는 Gson 규칙이 없었습니다. 이 가설대로라면 순서는 이렇습니다. 앱은 예약 전에 항상 <code>cancel</code>을 부르고, cancel은 저장본이 없으면 TypeToken을 거치지 않고 빈 목록 <code>[]</code>을 씁니다. 이어지는 <code>zonedSchedule</code>은 <strong>알람을 먼저 건 뒤</strong> 사본을 저장하려고 그 <code>[]</code>을 읽다가 예외를 내고, 예외는 Dart로 올라와 <code>NotificationService</code>의 <code>catch</code>에서 사라집니다. 알람은 걸리고 사본은 빈 채로 남습니다.</p>
<p>다만 이 가설은 끝까지 확인하지 못했습니다. 릴리스 빌드는 <code>run-as</code>가 막혀 사본 파일을 열어 볼 수 없었고, 1.2.8의 R8 매핑도 남아 있지 않았습니다. 게다가 1.2.8에는 모든 내부 클래스를 지키는 넓은 규칙(<code>-keep class **.*$* { *; }</code>)이 있었고 익명 TypeToken 하위 클래스도 여기에 걸리므로, 시그니처가 정말 지워졌다고 단정할 수는 없습니다. 확인된 것은 1.2.8에서 켠 알림이 부트 리시버로는 돌아오지 않는다는 사실, 그리고 Gson 규칙이 들어간 빌드에서는 재부팅 복구가 동작한다는 결과입니다.</p>
<p>원인이 어느 쪽이든 대응은 같았습니다. 지난 버전이 플러그인 사본에 남긴 상태는 새 버전의 규칙으로 고칠 수 없습니다(Gson 규칙은 1.2.9에서 이미 추가돼 있었습니다). 그래서 앱이 가진 진실의 원천, 즉 설정 화면이 Hive에 저장한 켜짐 여부와 시각으로 <strong>매 실행마다 다시 예약</strong>하게 했습니다. 같은 ID를 취소하고 다시 거는 동작이라 여러 번 불러도 안전합니다.</p>
<pre><code>// main.dart, 시작 시
await NotificationService.init();
unawaited(NotificationService.restoreDailyReviewReminder());

// NotificationService
static Future&lt;void&gt; restoreDailyReviewReminder() async {
  final enabled =
      DatabaseService.getSetting&lt;bool&gt;(enabledSettingKey) ?? false;
  if (!enabled) return;
  await scheduleDailyReviewReminder(
    hour: DatabaseService.getSetting&lt;int&gt;(hourSettingKey) ?? defaultHour,
    minute:
        DatabaseService.getSetting&lt;int&gt;(minuteSettingKey) ?? defaultMinute,
  );
}</code></pre>
<p>코드 경로상 예상되는 부수 효과도 하나 있습니다. 1.2.9에서 켠 알림은 사본은 남지만 리시버가 없어 그 시각이 과거에 멈춰 있습니다. 업데이트 순간 부트 리시버가 그 과거 시각으로 알람을 걸면 <code>AlarmManager</code>는 문서대로 즉시 울리므로, 지난 알림이 한 번 뜰 수 있습니다. 해롭지 않다고 보고 두었습니다.</p>

<h2>원인 3: 서울에 고정된 시간대</h2>
<p>리시버가 생기자 가려져 있던 문제가 드러났습니다. 기기 시간대를 읽는 함수가 나중에 채울 자리로 남은 채 서울을 돌려주고 있었습니다.</p>
<pre><code>static Future&lt;String&gt; _localTimeZoneName() async {
  // Without a dedicated tz plugin we cannot reliably read the device zone,
  // so we use the app's primary locale zone. Kept as a hook for future use.
  return 'Asia/Seoul';
}</code></pre>
<p><code>timezone</code> 패키지는 기기 시간대를 알려 주지 않으므로, README 안내대로 플랫폼 채널이나 <code>flutter_timezone</code> 같은 패키지로 얻어 <code>tz.setLocalLocation</code>에 넣어야 합니다. 이 이름은 첫 회차만 정하지 않습니다. 플러그인의 안드로이드 코드는 <code>ZoneId.of(timeZoneName)</code>로 <strong>매일의 다음 회차를 그 시간대에서</strong> 계산하고, iOS도 반복 트리거에 그 시간대를 넣습니다. 캘리포니아에서 20:00으로 맞춘 알림이 현지 새벽 4시에 울리는 구조였지만, 알림이 아예 안 울리던 동안에는 보일 리 없었습니다.</p>
<p>플러그인을 더하지 않고, 앱이 이미 쓰던 MethodChannel 패턴으로 기기 시간대를 넘겼습니다. 안드로이드는 <code>TimeZone.getDefault().id</code>, iOS는 <code>TimeZone.current.identifier</code>를 돌려줍니다. 받은 이름이 IANA DB에 없으면 서울로 떨어집니다. 자바 <code>TimeZone</code>은 <code>GMT+09:00</code> 같은 사용자 지정 ID도 허용하기 때문입니다.</p>
<pre><code>// MainActivity.kt
MethodChannel(flutterEngine.dartExecutor.binaryMessenger, timeZoneChannelName)
    .setMethodCallHandler { call, result -&gt;
        when (call.method) {
            "getLocalTimeZone" -&gt; result.success(TimeZone.getDefault().id)
            else -&gt; result.notImplemented()
        }
    }

// notification_service.dart
@visibleForTesting
static tz.Location locationFor(String? name) {
  if (name != null) {
    try {
      return tz.getLocation(name);
    } on tz.LocationNotFoundException {
      // fall through
    }
  }
  return tz.getLocation(_fallbackTimeZone);
}</code></pre>
<p>이 함수에는 옛 ID인 <code>Asia/Calcutta</code>, 빈 값, <code>GMT+09:00</code>을 포함한 단위 테스트 네 개를 붙였습니다. 매 실행 재예약 덕분에 여행으로 시간대가 바뀌어도 다음에 앱을 열면 알림이 새 시간대로 옮겨집니다.</p>

<h2>원인 4: iOS는 처음부터 연결돼 있지 않았다</h2>
<p>iOS는 두 누락이 겹쳤습니다. 초기화에 iOS 설정을 넘기지 않아 플러그인이 <code>ArgumentError('iOS settings must be set when targeting iOS platform.')</code>를 던졌고, 앱 시작을 막지 않으려고 모든 예외를 잡던 <code>init()</code>이 이를 삼켰습니다. 또 권한 요청이 안드로이드 구현만 찾아서 iOS에서는 묻지도 않고 <code>false</code>를 돌려줬고, 설정 화면은 그걸 거부로 읽었습니다. 고친 것은 넷입니다.</p>
<ul>
<li><code>DarwinInitializationSettings</code>를 넘기되 권한 요청은 모두 <code>false</code>로 두어, 앱을 열 때가 아니라 토글을 켤 때 권한 창이 뜨게 했습니다.</li>
<li>안드로이드 구현이 없으면 <code>IOSFlutterLocalNotificationsPlugin</code>의 <code>requestPermissions(alert: true, sound: true)</code>를 부릅니다.</li>
<li>예약할 때 <code>DarwinNotificationDetails</code>를 함께 넣습니다.</li>
<li><code>AppDelegate</code>에서 <code>UNUserNotificationCenter.current().delegate = self</code>를 설정했습니다. README가 요구하는 부분이고, iOS는 따로 설정하지 않으면 앱이 포그라운드일 때 알림을 표시하지 않습니다.</li>
</ul>
<pre><code>const darwinSettings = DarwinInitializationSettings(
  requestAlertPermission: false,
  requestSoundPermission: false,
  requestBadgePermission: false,
);
const initSettings = InitializationSettings(
  android: androidSettings,
  iOS: darwinSettings,
);</code></pre>
<p>iOS에서는 플러그인이 <code>UNCalendarNotificationTrigger</code>를 반복으로 등록해 운영체제가 매일 반복을 처리합니다. 안드로이드식 리시버나 부트 복구는 필요 없고, 시작 시 재예약은 시간대를 현재 값으로 옮기는 역할만 합니다.</p>

<h2>검증</h2>
<p>원인 2의 용의자가 R8이라 축소를 하지 않는 디버그 빌드로는 재현을 믿을 수 없습니다. 그래서 안드로이드는 전부 릴리스 빌드로 확인했고, 시계를 돌리는 대신 알림 시각을 2~3분 뒤로 잡았습니다.</p>
<table>
<thead><tr><th>시나리오</th><th>결과</th></tr></thead>
<tbody>
<tr><td>1.2.8, 3분 뒤 예약</td><td>알람은 전달, 게시된 알림 0건, 다음 날 알람 없음</td></tr>
<tr><td>1.2.8에서 켠 채 리시버만 넣은 빌드로 업데이트</td><td>부트 리시버는 실행, 크래시 없음, 복구된 알람 없음</td></tr>
<tr><td>시작 시 재예약 빌드로 업데이트 후 실행</td><td>다음 날 같은 시각 알람 복구</td></tr>
<tr><td>14:56 예약</td><td>14:57 무렵 게시, 다음 날 14:56 알람 자동 생성</td></tr>
<tr><td>재부팅</td><td>앱을 열지 않아도 알람 복구, Gson 관련 오류 없음</td></tr>
<tr><td>로스앤젤레스 시간대</td><td>수정 전 14:56 알림이 현지 22:56, 수정 후 현지 14:56. 현지 00:33 예약은 00:33에 게시</td></tr>
<tr><td>앱을 멈춘 채 서울 시간대로 바꾸고 실행</td><td>다음 알람이 서울 00:33으로 이동</td></tr>
<tr><td>iOS 시뮬레이터, 로스앤젤레스 시간대</td><td>권한 창, 포그라운드 배너, 백그라운드 알림 모두 현지 시각에 표시</td></tr>
</tbody>
</table>
<pre><code># 산출물 매니페스트에 리시버가 있는지
aapt2 dump xmltree --file AndroidManifest.xml app-release.apk | grep -c -i flutterlocalnotifications

# 걸린 알람과 창, 실제 게시 여부
adb shell dumpsys alarm | grep -A3 '&lt;패키지명&gt;}'
adb shell dumpsys notification --noredact | grep -A3 'pkg=&lt;패키지명&gt;'

# 업데이트 경로: 옛 버전에서 알림을 켠 뒤 덮어 설치 / 재부팅 경로
adb install old.apk
adb install -r new.apk
adb reboot

# 시간대
emulator -avd &lt;AVD 이름&gt; -timezone America/Los_Angeles
adb shell settings put global auto_time_zone 0
adb shell cmd alarm set-timezone Asia/Seoul

# iOS 시뮬레이터: 앱 프로세스에만 TZ를 넣는다(시스템 시계는 맥 기준)
SIMCTL_CHILD_TZ=America/Los_Angeles xcrun simctl launch &lt;UDID&gt; &lt;번들 ID&gt;</code></pre>
<p>몇 가지를 덧붙입니다.</p>
<ul>
<li><strong>inexact 창은 넓습니다.</strong> 3분 뒤 알람의 창은 <code>+2m15s</code>, 다음 날 알람의 창은 <code>+1h</code>였습니다. 안 뜬다고 판단하기 전에 창이 끝났는지부터 봅니다.</li>
<li><strong>업데이트는 별도의 경로입니다.</strong> 새로 설치해서 켜는 테스트만 했다면 원인 2는 보이지 않았습니다.</li>
<li><strong>강제 종료는 결과를 흐립니다.</strong> 시간대를 바꾸고 앱을 강제 종료한 직후에는 대기 알람이 목록에 없었습니다. 어느 쪽이 지웠는지는 나눠 보지 않았지만, 다시 실행하자 재예약 코드가 새 시간대로 알람을 걸었습니다.</li>
<li><strong><code>SIMCTL_CHILD_TZ</code>는 앱 프로세스의 시간대만 바꿉니다.</strong> 현지 01:00 알림이 맥 시계로 17:00에 떴습니다. 시뮬레이터는 릴리스 빌드를 돌리지 못해 동작은 디버그 빌드로 봤습니다.</li>
</ul>

<h2>예약 알림을 넣을 때 쓰는 점검표</h2>
<h3>안드로이드</h3>
<ul>
<li>빌드 산출물(병합된 매니페스트나 APK)에 <code>ScheduledNotificationReceiver</code>와 <code>ScheduledNotificationBootReceiver</code>가 있는가.</li>
<li><code>RECEIVE_BOOT_COMPLETED</code>를 앱 매니페스트에 직접 선언했는가.</li>
<li>정확한 시각이 꼭 필요한가. 필요하면 <code>SCHEDULE_EXACT_ALARM</code>과 <code>requestExactAlarmsPermission()</code>, 또는 스토어 심사 대상인 <code>USE_EXACT_ALARM</code>이 필요합니다. README에 따르면 정확한 알람 권한이 취소되면 반복 알림의 다음 회차도 예약되지 않습니다.</li>
<li>Android 13 이상에서 <code>POST_NOTIFICATIONS</code>를 런타임에 요청하는가.</li>
<li>플러그인 v18 이하라면 Gson 규칙을 넣었는가. 릴리스 빌드에서 재부팅 후 알람이 복구되는지로 확인합니다.</li>
<li>알림 아이콘을 이름으로 넘긴다면 <code>keep.xml</code>로 지켰는가.</li>
<li>백그라운드 실행을 막는 제조사 기기(README의 Caveats)를 도움말에 안내했는가.</li>
</ul>
<h3>iOS</h3>
<ul>
<li><code>InitializationSettings</code>에 <code>iOS:</code>를 넘겼는가.</li>
<li>권한 요청이 iOS 구현도 부르는가.</li>
<li><code>AppDelegate</code>에서 <code>UNUserNotificationCenter</code> delegate를 설정했는가.</li>
</ul>
<h3>공통</h3>
<ul>
<li><code>tz.setLocalLocation()</code>에 기기 시간대를 넣고, 모르는 ID에 대비했는가.</li>
<li>플러그인 사본이 아니라 앱 설정을 진실의 원천으로 두고, 시작할 때마다 다시 예약하는가.</li>
<li>알림 관련 예외를 삼키더라도 어딘가에 남기는가. 이번 iOS 초기화 실패는 앱 코드의 <code>catch</code>에서 흔적 없이 사라졌습니다.</li>
<li>새 설치뿐 아니라 업데이트, 재부팅, 시간대 변경을 각각 릴리스 빌드로 돌려 봤는가.</li>
</ul>

<h2>남는 교훈</h2>
<p><strong>예약 호출의 성공은 알림의 성공이 아닙니다.</strong> 알람이 울리는지, 누가 받는지, 받은 쪽이 다음 회차를 거는지는 별개의 단계입니다. <code>dumpsys alarm</code>과 <code>dumpsys notification</code>을 나란히 보면 어디서 끊겼는지가 바로 갈립니다.</p>
<p><strong>시작을 막지 않되, 기록은 남겨야 합니다.</strong> 부가 기능의 실패가 앱 시작을 막으면 안 된다는 판단은 맞았지만, 삼킨 예외가 아무 데도 남지 않으면 그 기능은 몇 달이고 죽은 채로 출시됩니다.</p>
<p><strong>문제는 겹쳐서 숨습니다.</strong> 시간대 버그는 알림이 울리지 않는 동안 보이지 않았습니다. 하나를 고치면 그 수정이 새로 연 경로를 곧바로 돌려 봐야 합니다.</p>
<div class="tip"><strong>라이트온 AI 노트</strong> — 강의 녹음·전사·요약부터 플래시카드와 간격 반복 복습까지 한 앱에서 이어집니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.ailecturenote" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-flutter-notification-icon-shrink",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "Flutter 릴리스 빌드만 스플래시에서 멈출 때: 리소스 축소가 지운 알림 아이콘",
"desc": "디버그와 프로파일에선 멀쩡한 Flutter 앱이 릴리스 APK에서만 스플래시에 멈췄습니다. 리소스 축소가 Dart 문자열로만 참조한 알림 아이콘을 지운 것이 원인이었고, 진단법과 keep.xml 해결을 정리했습니다.",
"body": """
<p>경품·이벤트 소식을 알림으로 알려 주는 안드로이드 앱(경품 레이더)을 Flutter로 만들 때 일입니다. <code>flutter run</code>으로 띄운 디버그 빌드도, 성능을 보려고 만든 프로파일 빌드도 멀쩡했는데, 릴리스 APK만 스플래시 화면에서 더 나아가지 않았습니다. 크래시 대화상자도 없고 앱이 꺼지지도 않았습니다.</p>
<p>원인은 Android의 리소스 축소(<code>isShrinkResources</code>)였습니다. Dart 코드에서 문자열로만 이름을 넘긴 알림 아이콘을 축소기가 안 쓰는 리소스로 보고 지웠고, 아이콘을 못 찾은 <code>flutter_local_notifications</code> 초기화가 <code>runApp</code> 앞에서 예외를 던졌습니다.</p>
<h2>배경: 리소스 축소를 켠 이유</h2>
<p>Play Console은 2027년 2월부터 메모리 표준을 넘는 앱의 공개 상태나 게시 기능을 제한할 수 있다고 예고했고, 그 기준 하나가 R8 같은 도구로 얻는 DEX 최적화 커버리지 25% 이상입니다. 스튜디오의 다른 앱들도 차례로 R8을 켜던 중이라, 이 앱은 첫 커밋부터 R8과 리소스 축소를 켰습니다.</p>
<pre><code>buildTypes {
    release {
        // (서명 설정 생략)
        // Play 메모리 표준(DEX 최적화 25% 이상) — R8 최적화 + 리소스 축소
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro",
        )
    }
}</code></pre>
<p>사실 이 두 줄을 쓰지 않아도 Flutter 앱의 릴리스 빌드는 대개 이미 리소스를 축소하고 있습니다. 뒤에서 다시 다룹니다.</p>
<h2>크래시가 아니라 첫 프레임이 없는 것</h2>
<p>릴리스 전용 문제라면 R8이 리플렉션용 클래스를 지운 경우를 먼저 떠올리지만, 그런 문제는 대개 프로세스가 죽으며 크래시로 남습니다. 이번에는 프로세스가 살아 있었으니, Dart 쪽에서 무언가 실패해 첫 프레임까지 못 갔다고 보는 편이 맞습니다.</p>
<p>Flutter 템플릿의 <code>LaunchTheme</code>은 창 배경으로 <code>launch_background</code>를 깔고, 템플릿 주석대로 이 배경은 엔진이 첫 프레임을 그릴 때 사라집니다. 스플래시에서 멈춘다는 건 첫 프레임이 없다는 뜻이고, 그렇다면 <code>runApp</code>이 불렸는지부터 봐야 합니다. 당시 <code>main()</code>은 이랬습니다.</p>
<pre><code>Future&lt;void&gt; main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final controller = AppController();
  await Notifier.init(onTap: (url) {
    if (url != null) controller.openFromNotification(url);
  });
  await Workmanager().initialize(callbackDispatcher);
  await registerBackgroundPoll();
  runApp(PrizeRadarApp(controller: controller));
  // ...
}</code></pre>
<p>알림 초기화와 백그라운드 작업 등록을 모두 기다린 뒤에야 <code>runApp</code>을 부릅니다. 하나라도 예외를 던지면 <code>main()</code>의 Future가 실패로 끝나고 <code>runApp</code>에는 끝내 닿지 못합니다. Dart의 처리되지 않은 비동기 예외는 프로세스를 죽이지 않습니다. 엔진이 로그 한 줄을 남길 뿐이고, 시스템은 이것을 크래시로 보지 않습니다.</p>
<h2>진단 1: logcat의 flutter 태그</h2>
<p>릴리스 빌드에서도 처리되지 않은 Dart 예외는 logcat에 <code>flutter</code> 태그로 찍힙니다.</p>
<pre><code>flutter build apk --release
adb install -r build/app/outputs/flutter-apk/app-release.apk
adb logcat -s flutter</code></pre>
<p>앱을 띄우면 아래 모양의 줄이 나옵니다. 메시지는 플러그인 소스에 있는 문구 그대로입니다(읽기 좋게 줄을 나눴습니다).</p>
<pre><code>E flutter : [ERROR:flutter/runtime/dart_vm_initializer.cc(..)] Unhandled Exception:
PlatformException(invalid_icon, The resource @drawable/ic_stat_radar could not be found.
Please make sure it has been added as a drawable resource to your Android head project., null, null)</code></pre>
<p>알림 초기화에서 넘긴 값은 이것이었습니다.</p>
<pre><code>await _plugin.initialize(
  settings: const InitializationSettings(
    android: AndroidInitializationSettings('@drawable/ic_stat_radar'),
  ),
  // ...
);</code></pre>
<p>에러 코드 <code>invalid_icon</code>을 플러그인의 안드로이드 소스에서 찾으면 이 지점이 나옵니다(flutter_local_notifications 22.3.2, 발췌).</p>
<pre><code>private void initialize(MethodCall call, Result result) {
  Map&lt;String, Object&gt; arguments = call.arguments();
  String defaultIcon = (String) arguments.get(DEFAULT_ICON);
  if (!isValidDrawableResource(
      applicationContext, defaultIcon, result, INVALID_ICON_ERROR_CODE)) {
    return;
  }
  // ...
}
private static boolean isValidDrawableResource(
    Context context, String name, Result result, String errorCode) {
  int resourceId = context.getResources().getIdentifier(name, DRAWABLE, context.getPackageName());
  if (resourceId == 0) {
    result.error(errorCode, String.format(INVALID_DRAWABLE_RESOURCE_ERROR_MESSAGE, name), null);
    return false;
  }
  return true;
}</code></pre>
<p>Dart에서 넘긴 이름이 메서드 채널을 타고 <code>Resources.getIdentifier()</code>에 그대로 들어가고, 그 이름의 리소스가 없으면 0이 돌아와 초기화가 곧바로 실패합니다. 아이콘 파일은 <code>res/drawable/ic_stat_radar.xml</code>에 분명히 있었으니, 남은 질문은 빌드 결과물에도 있느냐였습니다.</p>
<h2>진단 2: 파일 목록 말고 리소스 테이블을 본다</h2>
<p>APK를 zip으로 열어 파일 이름을 찾는 방법은 릴리스 빌드에서 믿을 수 없습니다. 디버그 APK와 릴리스 APK를 비교하면 이렇습니다(고친 뒤 빌드의 출력입니다).</p>
<pre><code>$ unzip -l app-debug.apk | grep ic_stat_radar
     1064  01-01-1981 01:01   res/drawable/ic_stat_radar.xml
$ unzip -l app-release.apk | grep ic_stat_radar
(출력 없음)
$ aapt2 dump resources app-release.apk | grep -A1 "drawable/ic_stat_radar"
    resource 0x7f070082 drawable/ic_stat_radar
      () (file) res/K2.xml type=XML</code></pre>
<p>릴리스 APK에서는 리소스 파일 경로가 <code>res/K2.xml</code>처럼 짧게 바뀌어 있어서, 리소스가 살아 있어도 파일 목록에서는 보이지 않습니다. 판단은 <code>aapt2 dump resources</code>가 보여 주는 리소스 테이블로 해야 합니다. <code>aapt2</code>는 Android SDK의 <code>build-tools/&lt;버전&gt;/</code> 아래에 있습니다. <code>getIdentifier()</code>가 0을 돌려줬다는 것은 이 테이블에 그 이름의 항목이 없었다는 뜻입니다.</p>
<p>AAB는 더 조심해야 합니다. 나중에 다른 앱에서 확인해 보니 AAB의 리소스 테이블에는 지워진 리소스 이름이 원본 경로 문자열로 남아 있어, 문자열 검색으로는 판별되지 않았습니다. <code>resource 0x… type/name</code> 줄을 정확히 맞춰 비교해야 합니다.</p>
<h3>축소기의 판단 기록: resources.txt</h3>
<p>축소기가 무엇을 남기고 지웠는지는 <code>build/app/outputs/mapping/release/resources.txt</code>에 남습니다. 앞부분에 이번 문제의 핵심이 있습니다.</p>
<pre><code>android.content.res.Resources#getIdentifier present: true
Web content present: true
Referenced Strings:
cancel
Rap
callerContext
...
Marking drawable:admob_close_button_black_circle_white_cross:2131165270 used because it matches string pool constant admob</code></pre>
<p>축소기는 코드에 <code>getIdentifier()</code> 호출이 있다는 것을 알고(<code>present: true</code>), 코드의 문자열 상수(<code>Referenced Strings</code>)를 리소스 이름과 맞춰 봅니다. <code>admob</code>이라는 상수 때문에 <code>admob_</code>으로 시작하는 drawable을 살려 뒀다는 기록도 보입니다. 그런데 이 문자열 목록 어디에도 <code>ic_stat_radar</code>는 없습니다.</p>
<h2>근본 원인: 축소기는 Dart 코드를 읽지 못한다</h2>
<p>축소기가 리소스를 쓰인다고 보는 근거는 코드의 리소스 ID 참조(<code>R.drawable.ic_xxx</code>), 매니페스트·레이아웃 같은 XML의 참조, keep 파일입니다. 기본값인 안전 모드에서는 <a href="https://developer.android.com/topic/performance/app-optimization/customize-which-resources-to-keep" target="_blank" rel="noopener">공식 문서</a> 설명대로, 동적으로 불러올 리소스 이름을 만드는 데 쓰일 법한 문자열 상수가 있으면 그 리소스도 도달 가능한 것으로 표시될 수 있습니다. 위의 <code>admob</code> 기록이 그 흔적입니다.</p>
<p>문제는 여기서 말하는 코드가 DEX, 곧 Java·Kotlin 바이트코드라는 점입니다. Flutter 릴리스 빌드에서 Dart 코드는 AOT 컴파일되어 <code>libapp.so</code>라는 네이티브 라이브러리에 들어갑니다. 릴리스 APK를 풀어 문자열을 찾아보면 위치가 분명히 갈립니다.</p>
<pre><code>$ strings -a lib/arm64-v8a/libapp.so | grep ic_stat_radar
@drawable/ic_stat_radar
$ strings -a classes.dex classes2.dex | grep -c ic_stat_radar
0</code></pre>
<p>아이콘 이름은 <code>libapp.so</code>에만 있고 DEX에는 한 번도 나오지 않습니다. 이 아이콘에 이르는 경로는 "Dart 문자열 → 메서드 채널 → 플러그인의 <code>getIdentifier()</code>" 하나뿐인데, 이 경로는 실행 중에만 존재합니다. 빌드 시점의 축소기에게는 아무도 가리키지 않는 drawable이었고, 규칙대로 지웠습니다. 축소기가 틀린 게 아니라, 판단에 필요한 정보가 축소기가 읽을 수 없는 곳에 있었습니다.</p>
<h3>런처 아이콘을 쓰면 괜찮아 보이는 이유</h3>
<p>알림 아이콘으로 <code>@mipmap/ic_launcher</code>를 넘기면 이 문제가 드러나지 않습니다. 매니페스트의 <code>android:icon</code>이 같은 리소스를 가리켜 살아남기 때문인데, 알림 쪽 참조를 알아본 게 아니라 우연입니다. 라이트온 AI 노트가 이렇게 쓰고 있어서, 런처 아이콘 이름을 바꾸는 순간 알림이 조용히 깨지지 않도록 그 앱에도 keep 파일을 넣었습니다. 반대로 상태 표시줄용 단색 아이콘을 따로 만드는 정석을 따를수록 이 함정에 바로 걸립니다. 플러그인 README도 릴리스 빌드에서는 알림 아이콘을 keep 파일로 남기라고 안내합니다.</p>
<h3>디버그와 프로파일에서 재현되지 않는 이유</h3>
<p>디버그 빌드는 리소스를 축소하지 않습니다. 의외였던 건 프로파일입니다. Flutter Gradle 플러그인 소스(<code>FlutterPlugin.kt</code>)는 <code>profile</code> 빌드 타입을 <code>initWith(debug)</code>로 만듭니다. Dart는 AOT로 컴파일돼도 안드로이드 빌드 설정은 디버그의 복사본이라 R8도 리소스 축소도 돌지 않습니다. 실제로 프로파일 APK에는 아이콘이 원래 경로 그대로 들어 있었습니다.</p>
<p>같은 파일에서 릴리스 쪽 동작도 보입니다. Flutter 3.47.9 기준으로 이 플러그인은 앱이 덮어쓰지 않는 한 release 빌드 타입에 <code>isMinifyEnabled = true</code>와 <code>isShrinkResources = true</code>를 넣고, <code>flutter build</code>의 <code>--no-shrink</code> 플래그는 도움말에 효과가 없다고 적혀 있습니다. 축소 설정을 적지 않은 Flutter 앱도 릴리스에서는 이미 리소스를 줄이고 있습니다.</p>
<h2>고친 방법</h2>
<h3>1. res/raw/keep.xml로 남길 리소스를 알려 준다</h3>
<pre><code>&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;!-- 알림 아이콘은 Dart 에서 이름(문자열)으로만 참조해 리소스 축소가 지워 버린다 — 릴리스에서 유지 --&gt;
&lt;resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@drawable/ic_stat_radar" /&gt;</code></pre>
<p><code>tools:keep</code>에는 남길 리소스를 쉼표로 나열하고 <code>@drawable/ic_stat_*</code>처럼 와일드카드도 쓸 수 있습니다. <a href="https://developer.android.com/topic/performance/app-optimization/customize-which-resources-to-keep" target="_blank" rel="noopener">공식 문서</a>에 따르면 keep 파일 자체는 앱에 패키징되지 않고, 전역으로 적용되니 패키지 이름을 넣은 고유한 파일 이름을 쓰라고 권합니다. 플러그인 예제 앱은 drawable 전부를 남기지만, 아이콘이 몇 개뿐이라면 이름을 적는 쪽이 낭비가 적습니다.</p>
<h3>2. 부가 기능의 초기화가 앱 시작을 막지 않게 한다</h3>
<pre><code>Future&lt;void&gt; main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final controller = AppController();
  // 알림·백그라운드 작업 설정이 실패해도 앱은 떠야 한다
  try {
    await Notifier.init(onTap: (url) {
      if (url != null) controller.openFromNotification(url);
    });
  } catch (e) {
    debugPrint('알림 초기화 실패: $e');
  }
  try {
    await Workmanager().initialize(callbackDispatcher);
    await registerBackgroundPoll();
  } catch (e) {
    debugPrint('백그라운드 작업 등록 실패: $e');
  }
  runApp(PrizeRadarApp(controller: controller));
  await controller.start();
  final launchUrl = await Notifier.launchPayload().catchError((_) =&gt; null);
  if (launchUrl != null) unawaited(controller.openFromNotification(launchUrl));
  unawaited(Ads.init());
}</code></pre>
<p>keep 파일이 원인을 고친다면, 이 수정은 다음 사고의 크기를 줄입니다. 초기화가 예외를 잡고 있었다면 이번 일도 "앱이 안 열린다"가 아니라 "알림이 안 온다"로 끝났을 겁니다. 알림을 눌러 실행됐는지 확인하는 <code>launchPayload()</code>도 같은 플러그인을 타므로 <code>catchError</code>로 감쌌습니다. 다만 <code>try/catch</code>만 넣고 keep 파일을 빠뜨리면 증상이 조용해질 뿐이니, 둘은 함께 들어가야 합니다.</p>
<h2>검증</h2>
<p>다시 만든 릴리스 APK의 리소스 테이블에 <code>drawable/ic_stat_radar</code>가 돌아왔고, <code>resources.txt</code>에서는 참조와 상관없이 살려 두는 <code>The root reachable resources are:</code> 목록에 올라 있었습니다. keep 파일 자체(<code>raw:keep</code>)는 <code>Unused resources are:</code> 쪽에 있어 문서대로 패키징되지 않았습니다. 다시 설치한 릴리스 APK는 스플래시를 지나 정상적으로 시작했습니다.</p>
<h2>같은 함정이 숨어 있는 다른 자리</h2>
<p>조건은 두 가지입니다. 리소스를 이름으로 찾고, 그 이름이 축소기가 읽지 못하는 곳(Dart 코드, 서버 응답, 설정 파일)에 있는 경우입니다. Flutter에서는 플러그인이 메서드 채널로 이름을 받아 네이티브에서 <code>getIdentifier()</code>를 부르는 구조가 전형입니다.</p>
<h3>flutter_local_notifications의 다른 인자</h3>
<p>알림마다 지정하는 <code>icon</code>, <code>DrawableResourceAndroidBitmap</code>으로 넘기는 큰 아이콘, BigPicture 스타일의 drawable, <code>RawResourceAndroidNotificationSound</code>로 넘기는 알림음도 모두 이름으로 조회됩니다. 알림음은 <code>raw</code> 타입으로 찾고, 없으면 <code>invalid_sound</code> 에러를 돌려줍니다. README는 최악의 경우 알림이 조용히 안 뜰 수 있다고 경고합니다.</p>
<h3>audio_service: 플러그인이 자기 리소스를 이름으로 찾는다</h3>
<p>음악 앱 송빗에서 겪은 경우는 더 까다로웠습니다. audio_service는 미디어 컨트롤 아이콘을 Dart 쪽에서 이름으로 지정하고, 그 아이콘 PNG는 플러그인이 직접 들고 있습니다.</p>
<pre><code>// audio_service (Dart) — 미디어 컨트롤 아이콘을 이름으로 지정
androidIcon: 'drawable/audio_service_play_arrow',
// audio_service (Java) — "type/name" 을 잘라 이름으로 조회
int getResourceId(String resource) {
    String[] parts = resource.split("/");
    String resourceType = parts[0];
    String resourceName = parts[1];
    return getResources().getIdentifier(resourceName, resourceType, getApplicationContext().getPackageName());
}</code></pre>
<p>AGP 9로 올린 빌드를 태블릿에서 확인해 보니 소리는 나는데 알림창에 미디어 컨트롤이 없었고, 상태가 바뀔 때마다 <code>You must specify an icon resource id to build a CustomAction</code>이 찍혔습니다. AGP 9에서 기본으로 켜지는 최적화된 리소스 축소가 이전 버전이 남기던 리소스 444개를 더 지웠고, audio_service 아이콘 일곱 개가 모두 그 안에 있었습니다. 전에 살아 있었다는 사실은 아무것도 보장하지 않았습니다.</p>
<p>이때는 keep 목록 대신 최적화된 리소스 축소를 껐습니다. keep 목록은 이름을 아는 조회만 막을 수 있는데 Google 라이브러리는 소스가 닫혀 있고, 로그인과 결제를 새 도구 체인에서 아직 시험하지 못했기 때문입니다. 대가는 APK 약 250KB였습니다.</p>
<pre><code># AGP 9 turns on R8's optimized resource shrinking. It cannot see resources found by name at runtime,
# so it removed every audio_service icon (the names are in Dart) and 1.8.40 (74) lost its media controls.
android.r8.optimizedResourceShrinking=false</code></pre>
<p>대신 이름으로 찾는 리소스 아홉 개(audio_service 아이콘, <code>mipmap/ic_launcher</code>, Google 로그인 플러그인이 찾는 <code>string/default_web_client_id</code>)를 목록으로 적고, 릴리스 빌드 끝에 <code>aapt2</code>로 테이블을 읽어 하나라도 빠지면 빌드가 실패하게 했습니다.</p>
<h3>빌드 도구가 올라갈수록 범위가 넓어진다</h3>
<p><a href="https://developer.android.com/topic/performance/app-optimization/enable-app-optimization" target="_blank" rel="noopener">Android 문서</a>에 따르면 AGP 9.0부터는 <code>isShrinkResources = true</code>만으로 최적화된 리소스 축소가 적용되고, AGP 9.3의 새 <code>optimization { enable = true }</code> DSL은 코드와 리소스 최적화를 한 번에 켭니다. 새 DSL에서는 코드 최적화를 켜면 리소스 축소가 기본으로 따라오는 구조입니다.</p>
<h2>출시 전 체크리스트</h2>
<ol>
<li><strong>Dart 코드에서 리소스 이름 문자열을 찾는다.</strong> <code>'@drawable/…'</code>, <code>'mipmap/…'</code>, <code>'raw/…'</code> 같은 리터럴이 가리키는 리소스는 축소기가 보지 못합니다.</li>
<li><strong>쓰는 플러그인의 안드로이드 소스에서 <code>getIdentifier()</code>를 찾는다.</strong> 플러그인이 자기 리소스를 찾는 경우는 앱 코드에 드러나지 않습니다. 소스가 닫힌 라이브러리는 이렇게 볼 수 없습니다.</li>
<li><strong>찾은 이름을 <code>res/raw/keep.xml</code>에 적는다.</strong> 런처 아이콘을 알림에 쓰고 있어도 적어 둡니다.</li>
<li><strong>릴리스 산출물의 리소스 테이블로 확인한다.</strong> zip 파일 목록이 아니라 <code>aapt2 dump resources</code>의 <code>type/name</code> 항목으로 보고, 가능하면 빌드 단계에 넣습니다.</li>
<li><strong><code>runApp</code> 앞의 <code>await</code>를 줄인다.</strong> 앱이 뜨는 데 꼭 필요하지 않은 초기화는 예외를 잡거나 <code>runApp</code> 뒤로 옮깁니다.</li>
<li><strong>출시 전에 릴리스 APK를 기기에서 한 번 띄운다.</strong> 멈추면 <code>adb logcat -s flutter</code>부터 봅니다.</li>
</ol>
<pre><code># Dart 코드에 박힌 리소스 이름 찾기
grep -rnE "'@?(drawable|mipmap|raw)/[a-z0-9_]+'" lib</code></pre>
<pre><code># 이 프로젝트가 실제로 쓰는 플러그인의 안드로이드 소스에서 이름 조회 찾기 (예시)
python3 - &lt;&lt;'EOF'
import json, pathlib, subprocess
from urllib.parse import urlparse, unquote
cfg = json.load(open('.dart_tool/package_config.json'))
for p in cfg['packages']:
    uri = p['rootUri']
    if not uri.startswith('file://'):
        continue
    src = pathlib.Path(unquote(urlparse(uri).path)) / 'android' / 'src'
    if src.exists():
        subprocess.run(['grep', '-rnE', r'\\.getIdentifier\\(', str(src)])
EOF</code></pre>
<p>패턴을 <code>.getIdentifier(</code>로 좁힌 것은 <code>getIdentifier</code>만으로 찾으면 webview_flutter_android의 <code>getIdentifierForStrongReference</code>처럼 리소스와 무관한 이름도 걸리기 때문입니다. 걸린 줄은 열어서 조회하는 이름이 어디서 오는지 확인해야 합니다.</p>
<h2>남는 교훈</h2>
<p><strong>축소기는 자기가 읽을 수 있는 코드만 믿습니다.</strong> Flutter 앱의 로직은 대부분 그 바깥, <code>libapp.so</code>에 있습니다. 리소스를 이름으로 넘기는 순간 그 연결은 빌드 도구에게 보이지 않으니, 사람이 keep 파일로 적어 줘야 합니다.</p>
<p><strong>"디버그에서 된다"는 릴리스에 대해 아무것도 말해 주지 않습니다.</strong> 프로파일조차 안드로이드 쪽 설정은 디버그의 복사본이었습니다. 릴리스에서만 켜지는 단계가 있다면, 그 단계를 거친 산출물을 한 번은 직접 실행해 봐야 합니다.</p>
<div class="tip"><strong>한 줄 요약</strong> — Dart에서 문자열로 넘기는 Android 리소스 이름은 리소스 축소기가 보지 못합니다. <code>res/raw/keep.xml</code>의 <code>tools:keep</code>에 적고, 출시 전에 릴리스 APK를 기기에서 한 번 띄워 보세요.</div>
"""
},
{
"slug": "blog-capacitor-plugin-await-hang",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "Capacitor 플러그인을 return 하면 await 가 멈추는 이유 — thenable 함정",
"desc": "iOS 에서 'Try Pro' 버튼이 무반응이었습니다. 스토어도 SDK 도 정상이었고, 원인은 Proxy 로 만든 Capacitor 플러그인이 thenable 로 취급돼 await 가 끝나지 않은 것이었습니다. 진단 과정과 명세 수준의 원리, 재발 방지법.",
"body": """
<p>Hangul Lab 은 외국인 성인이 한글을 배우는 앱입니다. 웹으로 만든 화면을 Capacitor 로 감싸 Android 와 iOS 에 내놓고, iOS 의 Pro 구독 결제는 RevenueCat SDK(<code>@revenuecat/purchases-capacitor</code>)에 맡깁니다.</p>
<p>그 iOS 빌드에서 <strong>'Try Pro' 버튼을 눌러도 아무 일도 일어나지 않는다</strong>는 보고를 받았습니다. 결제창도, 오류 문구도, 크래시도 없었습니다. 원인은 결제 초기화 함수 마지막 줄의 <code>return Purchases</code> 였습니다. 이 한 줄이 왜 <code>await</code> 를 영원히 멈추게 하는지 기록해 둡니다. 버전은 <code>@capacitor/core</code> 8.5.0, <code>@revenuecat/purchases-capacitor</code> 13.5.0 기준입니다.</p>

<h2>증상: 가격이 빠진 버튼</h2>
<p>보고에 딸린 화면에서 먼저 눈에 띈 건 버튼 문구였습니다. 업셀 버튼은 상품 정보를 받으면 <code>Try Pro — (가격)</code>, 못 받으면 <code>Try Pro</code> 로 그립니다. 앱 시작 때의 상품 조회가 끝나지 않았다는 뜻입니다.</p>
<p>눌러도 반응이 없는 이유는 당시 버튼 핸들러에 그대로 있었습니다.</p>
<pre><code>// 당시 useEntitlement.js 의 버튼 핸들러
const subscribe = useCallback(async () =&gt; {
  if (state.billingReady) {
    const r = await purchase();
    // ...
    return;
  }
  // 여기 오면 스토어 결제를 못 쓰는 상태다(웹 개발 환경 등).
  if (!BETA_GRANT) return;             // &lt;- 상품을 못 받았으면 조용히 끝난다
  // ...
}, []);</code></pre>

<p>상품 조회가 끝나지 않으면 <code>billingReady</code> 가 <code>false</code> 로 남고, 버튼은 개발용 분기로 빠져 조용히 돌아갑니다. 그러니 진짜 질문은 <em>상품 조회가 왜 끝나지 않는가</em>였습니다.</p>
<p>같은 빌드를 iPad 시뮬레이터에 올리자 똑같이 재현됐습니다.</p>

<h2>처음 의심한 것들, 그리고 아니었던 이유</h2>
<h3>1. 스토어·RevenueCat 설정</h3>
<p>RevenueCat 의 오퍼링과 상품 연결, App Store Connect 의 구독 상품 상태, 유료 앱 계약, 번들 ID, 인앱 결제 키, 웹 번들에 들어간 RevenueCat 공개 키까지 전부 정상이었습니다. RevenueCat 쪽에는 문제가 난 기기의 익명 고객 레코드도 생겨 있었습니다. SDK 가 <code>configure</code> 까지는 했다는 뜻입니다.</p>
<h3>2. 새 OS 의 StoreKit 샌드박스</h3>
<p>새 iOS 직후 시뮬레이터에서 오퍼링이 안 내려오던 사례가 실제로 있어서(RevenueCat purchases-ios #4954, iOS 18.4), 시뮬레이터의 통합 로그를 직접 받아 봤습니다.</p>
<pre><code>xcrun simctl spawn &lt;UDID&gt; log stream --style compact --predicate 'process == "App"'</code></pre>

<p>StoreKit 로그에는 상품 요청 뒤 <code>Parsing 1 products in response</code> 가 찍혀 있었습니다. 상품이 정상으로 왔습니다. 함께 보인 <code>ASDErrorDomain Code=509 "No active account"</code> 는 샌드박스 계정이 없는 시뮬레이터에서 거래 내역 조회가 실패한 것이라 상품 조회와는 무관했습니다. 그리고 이 상품 요청은 JS 가 아무것도 묻기 전, <code>configure</code> 직후에 네이티브 SDK 가 스스로 보낸 것이었습니다. 스토어도 SDK 도 살아 있었습니다.</p>
<h3>3. 브리지 콜백 ID <code>-1</code></h3>
<p>Capacitor 는 JS 에서 네이티브로 넘어가는 호출을 Xcode 콘솔에 남깁니다.</p>
<pre><code>⚡️  To Native -&gt;  App addListener 34321175
⚡️  To Native -&gt;  Purchases setLogLevel -1
⚡️  To Native -&gt;  Purchases configure -1</code></pre>

<p>끝의 숫자는 콜백 ID 입니다. RevenueCat 호출만 <code>-1</code> 이라 "응답 콜백이 없어서 <code>await configure()</code> 가 안 끝난다"고 의심했는데, 틀렸습니다. 플러그인의 Swift 소스에서 <code>configure</code> 는 응답 없는 호출(<code>CAPPluginReturnNone</code>)이고, 브리지는 콜백이 없는 호출에 원래 <code>'-1'</code> 을 붙입니다. 이런 호출은 보내는 즉시 끝나므로 <code>await</code> 도 바로 풀립니다.</p>
<p>대신 같은 로그에 진짜 단서가 있었습니다. <strong><code>configure</code> 다음에 와야 할 <code>getOfferings</code> 호출이 한 번도 네이티브로 넘어오지 않았습니다.</strong> 네이티브는 멀쩡한데 JS 가 다음 질문을 하지 않고 있었던 겁니다.</p>

<h2>진단: 체크포인트를 화면에 그리기</h2>
<p>JS 가 어느 <code>await</code> 에서 멈추는지 보려 했지만, <code>xcrun simctl launch --console-pty</code> 로 받은 앱 출력은 브리지 로그 몇 줄 뒤로 끊겼고 <code>console.log</code> 는 한 줄도 보이지 않았습니다. 로그 경로와 씨름하는 대신, 단계마다 체크포인트를 배열에 쌓아 화면에 그리기로 했습니다. 진단 빌드에서만 켜지게 빌드 변수로 막았습니다.</p>
<pre><code>// 진단용 체크포인트 (당시 코드를 줄인 것). VITE_RC_DEBUG=1 빌드에서만 쌓인다.
const TRACE = [];
export const getTrace = () =&gt; TRACE.join(' &gt; ');
const trace = (s) =&gt; { if (import.meta.env.VITE_RC_DEBUG === '1') TRACE.push(s); };

async function rc() {
  trace('rc');
  const { Purchases } = await import('@revenuecat/purchases-capacitor');
  trace('import-ok');
  if (!rcInit) {
    rcInit = (async () =&gt; {
      // (setLogLevel 단계도 같은 식으로 찍었다)
      trace('configure');
      const r = await Purchases.configure({ apiKey: IOS_KEY });
      trace('configure-ok:' + String(r));
    })();
  }
  await rcInit;
  trace('rcInit-ok');
  return Purchases;
}

// 호출하는 쪽: const Purchases = await rc(); trace('getOfferings'); ...
// 화면 쪽: 1초마다 getTrace() 를 읽어 &lt;p&gt;trace: {trace}&lt;/p&gt; 로 그린다.</code></pre>

<p>시뮬레이터 화면에 찍힌 결과는 이랬습니다.</p>
<pre><code>debug: ready=false price=null reason=null
trace: rc &gt; rc &gt; rc &gt; import-ok &gt; setLogLevel &gt; import-ok &gt; import-ok &gt;
       setLogLevel-ok:-1 &gt; configure &gt; configure-ok:-1 &gt;
       rcInit-ok &gt; rcInit-ok &gt; rcInit-ok</code></pre>

<p>앱 시작 때 상품 조회, 구독 복원, 리스너 등록이 동시에 <code>rc()</code> 를 불러 <code>rc</code> 가 세 번 찍혔고, 셋 다 <code>await rcInit</code> 를 통과했습니다(<code>rcInit-ok</code> 세 번). 그런데 호출한 쪽에서 찍혀야 할 <code>getOfferings</code> 는 하나도 없습니다. <code>reason=null</code> 은 상품 조회가 성공도 실패도 하지 않았다는 뜻입니다. <code>try/catch</code> 의 <code>catch</code> 에도 걸린 게 없었습니다.</p>
<p><code>rcInit-ok</code> 와 호출한 쪽의 다음 줄 사이에 있는 코드는 단 한 줄입니다.</p>
<pre><code>// 당시 billing.js (iOS 경로)
let rcInit = null;
async function rc() {
  const { Purchases } = await import('@revenuecat/purchases-capacitor');
  if (!rcInit) rcInit = Purchases.configure({ apiKey: IOS_KEY });
  await rcInit;
  return Purchases;                    // &lt;- 이 한 줄
}

export async function getSubscription() {
  // ...
  try {
    const Purchases = await rc();      // &lt;- 여기서 영원히 멈춘다
    const pkg = await monthlyPackage(Purchases);
    if (!pkg) return { available: false, reason: 'no-offering' };
    return { available: true, price: pkg.product?.priceString || null };
  } catch (e) {
    return { available: false, reason: String(e?.message || e) };
  }
}</code></pre>

<p>초기화가 끝난 객체를 돌려줄 뿐인데, 돌려받는 쪽의 <code>await rc()</code> 가 끝나지 않습니다.</p>

<h2>원인: 모든 질문에 "예"라고 답하는 객체</h2>
<h3>Capacitor 플러그인은 Proxy 다</h3>
<p><code>registerPlugin()</code> 이 돌려주는 플러그인 객체는 메서드가 미리 정의된 평범한 객체가 아닙니다.</p>
<pre><code>// @capacitor/core 8.5.0 — registerPlugin() 안쪽
const proxy = new Proxy({}, {
  get(_, prop) {
    switch (prop) {
      // https://github.com/facebook/react/issues/20030
      case '$$typeof':
        return undefined;
      case 'toJSON':
        return () =&gt; ({});
      case 'addListener':
        return pluginHeader ? addListenerNative : addListener;
      case 'removeListener':
        return removeListener;
      default:
        return createPluginMethodWrapper(prop);   // 그 밖의 이름은 전부 함수
    }
  },
});</code></pre>

<p>몇 가지 예외를 빼면 <strong>어떤 이름을 물어도 그 이름의 메서드 래퍼를 돌려줍니다.</strong> 네이티브 메서드 목록을 JS 가 미리 알 필요가 없게 하려는 설계입니다. 그래서 존재하지 않는 <code>Purchases.then</code> 도 함수입니다. RevenueCat 이 내보내는 <code>Purchases</code> 는 이 Proxy 를 한 번 더 Proxy 로 감쌌지만, 메서드 하나만 가로채고 나머지는 그대로 넘기므로 결과는 같습니다.</p>
<p><code>$$typeof</code> 를 막아 둔 줄의 링크(facebook/react#20030)가 힌트입니다. React 가 묻는 속성에 플러그인이 함수로 답해서 생긴 문제를 막은 것입니다. 같은 일이 <code>then</code> 에서도 일어나는데, 이번에 묻는 쪽은 언어 자체입니다.</p>

<h3>async 함수의 return 은 resolve 를 거친다</h3>
<p>async 함수가 <code>return</code> 한 값은 곧바로 결과가 되지 않고, 함수가 돌려준 프로미스의 resolve 함수에 넘겨집니다(ECMAScript 명세의 AsyncBlockStart). resolve 함수는 값을 이렇게 처리합니다(CreateResolvingFunctions 의 resolve 단계).</p>
<ol>
<li>값이 객체가 아니면 그 값으로 이행(fulfill)하고 끝낸다.</li>
<li>객체면 <code>then</code> 속성을 읽는다.</li>
<li><code>then</code> 이 호출 가능하지 않으면 그 객체로 이행하고 끝낸다.</li>
<li>호출 가능하면 작업(NewPromiseResolveThenableJob)을 마이크로태스크로 예약하고, <strong>거기서 <code>then</code> 을 이 프로미스의 <code>resolve</code>·<code>reject</code> 를 인자로 해서 부른다.</strong> 이제 프로미스의 운명은 그 <code>then</code> 이 둘 중 하나를 불러 주는 데 달렸다.</li>
</ol>
<p>Promises/A+ 명세가 "Promise Resolution Procedure"(2.3절)라고 부르는 절차입니다. 다른 구현의 프로미스와 섞어 쓸 수 있도록 언어는 <code>then</code> 메서드가 있는지만 보고 상대를 프로미스처럼 다룹니다(MDN 의 Thenable). 그리고 이 절차 어디에도 <strong>타임아웃은 없습니다.</strong> <code>then</code> 이 두 콜백 중 어느 것도 부르지 않으면 프로미스는 영원히 대기합니다.</p>
<p><code>await x</code> 도 먼저 <code>PromiseResolve(%Promise%, x)</code> 로 x 를 프로미스로 바꾸는데, x 가 진짜 프로미스가 아니면 새 프로미스를 만들어 같은 resolve 절차에 넘깁니다. 그래서 <code>await Purchases</code> 나 <code>Promise.resolve(Purchases)</code> 도 결과가 같습니다.</p>

<h3>Capacitor 의 then 래퍼는 resolve 를 부르지 않는다</h3>
<p>그러면 <code>Purchases.then(resolve, reject)</code> 는 무엇을 할까요. Proxy 가 돌려주는 래퍼는 이렇습니다.</p>
<pre><code>// @capacitor/core 8.5.0 — createPluginMethodWrapper (일부 생략, 주석은 덧붙인 것)
const wrapper = (...args) =&gt; {            // then(resolve, reject) 이면 args = [resolve, reject]
  const p = loadPluginImplementation().then((impl) =&gt; {
    const fn = createPluginMethod(impl, prop);   // 네이티브 메서드 목록에서 'then' 을 찾는다
    if (fn) {
      return fn(...args);
    } else {
      throw new CapacitorException(
        `"${pluginName}.${prop}()" is not implemented on ${platform}`,
        ExceptionCode.Unimplemented);
    }
  });
  return p;                               // 이 프로미스가 거부될 뿐, resolve/reject 는 안 불린다
};</code></pre>

<ol>
<li>래퍼는 <code>resolve</code> 와 <code>reject</code> 를 "네이티브에 넘길 인자"로 받아 둘 뿐, 어느 쪽도 부르지 않습니다.</li>
<li>네이티브가 등록한 메서드 목록에서 <code>then</code> 을 찾습니다. 당연히 없고, iOS 용 JS 구현도 없으니 메서드를 만들지 못합니다.</li>
<li><code>"Purchases.then()" is not implemented on ios</code> 예외가 납니다. 그런데 이 예외는 <strong>래퍼가 돌려준 별개의 프로미스 안에서, 비동기로</strong> 납니다.</li>
</ol>
<p>NewPromiseResolveThenableJob 은 <code>then</code> 호출이 <em>동기적으로</em> 예외를 던질 때만 <code>reject</code> 를 대신 불러 주고, <code>then</code> 의 반환값은 보지 않습니다. 결국 원래 프로미스는 <code>resolve</code> 도 <code>reject</code> 도 받지 못한 채 대기하고, 에러는 아무도 구독하지 않는 프로미스에 실려 처리되지 않은 거부(unhandled rejection)가 됩니다. 이 호출은 브리지를 건너기 전에 JS 안에서 거부되므로 네이티브 로그에도 <code>then</code> 은 나오지 않습니다. 로그가 <code>configure</code> 에서 끊겨 있던 이유입니다.</p>

<h3>동기냐 비동기냐가 갈랐다</h3>
<p>이 차이를 확인하려고 Capacitor 의 Proxy 를 흉내 낸 객체로 Node 22 에서 실험했습니다.</p>
<pre><code>// 예시: Capacitor 플러그인 Proxy 를 흉내 낸 최소 재현 (Node 22)
function fakePlugin(name, syncThrow = false) {
  return new Proxy({}, {
    get(_, prop) {
      if (prop === '$$typeof') return undefined;
      if (prop === 'toJSON') return () =&gt; ({});
      return (...args) =&gt; {
        const err = new Error(`"${name}.${String(prop)}()" is not implemented on ios`);
        if (syncThrow) throw err;                         // 동기로 던지면
        return Promise.resolve().then(() =&gt; { throw err; }); // 비동기로 거부하면 (Capacitor 와 같은 모양)
      };
    },
  });
}

// 브라우저처럼 처리되지 않은 거부가 프로세스를 끝내지 않게 한다
process.on('unhandledRejection', (e) =&gt; console.log('unhandledRejection:', e.message));

async function getPlugin() { return fakePlugin('Purchases', process.argv[2] === 'sync'); }

try {
  console.log('before');
  const p = await getPlugin();
  console.log('after');
} catch (e) {
  console.log('caught:', e.message);
}

// $ node repro.mjs sync
//   before
//   caught: "Purchases.then()" is not implemented on ios
// $ node repro.mjs async
//   before
//   unhandledRejection: "Purchases.then()" is not implemented on ios
//   (after 도 caught 도 찍히지 않고, Node 가 끝나지 않은 최상위 await 를 경고한다)</code></pre>

<p>래퍼가 예외를 바로 던지면 <code>catch</code> 에 잡히고, 비동기로 거부하면 <code>before</code> 만 찍히고 끝납니다. Node 는 이를 경고로 알려 주지만 앱의 WebView 에서는 반응 없는 버튼으로 보일 뿐입니다.</p>
<p>같은 가짜 플러그인으로 흔한 모양들이 0.5초 안에 끝나는지 본 결과입니다.</p>
<table>
<thead><tr><th>코드 모양</th><th>결과</th></tr></thead>
<tbody>
<tr><td><code>await P</code></td><td><strong>멈춤</strong></td></tr>
<tr><td><code>async () =&gt; P</code> 의 결과를 await</td><td><strong>멈춤</strong></td></tr>
<tr><td><code>Promise.resolve(P)</code></td><td><strong>멈춤</strong></td></tr>
<tr><td><code>Promise.all([P])</code></td><td><strong>멈춤</strong></td></tr>
<tr><td><code>.then(() =&gt; P)</code></td><td><strong>멈춤</strong></td></tr>
<tr><td><code>async () =&gt; ({ plugin: P })</code></td><td>정상</td></tr>
<tr><td>모듈 변수에 담고 아무것도 반환하지 않음</td><td>정상</td></tr>
</tbody>
</table>
<p><code>const { Purchases } = await import(...)</code> 는 안전합니다. await 대상이 <code>then</code> 을 내보내지 않는 모듈 네임스페이스 객체이기 때문입니다.</p>

<h2>고친 방법</h2>
<p>원칙은 하나입니다. <strong>플러그인 객체를 프로미스의 결과값 자리에 두지 않는다.</strong> 초기화 함수는 아무것도 반환하지 않고, 플러그인 객체는 모듈 변수에만 담습니다.</p>
<pre><code>// 고친 billing.js — 플러그인 객체는 모듈 변수에만 담고, 어떤 async 함수도 그것을 반환하지 않는다.
let RC = null;
let rcInit = null;
async function ensureRC() {
  if (!rcInit) {
    rcInit = (async () =&gt; {
      const { Purchases, LOG_LEVEL } = await import('@revenuecat/purchases-capacitor');
      // 진단 빌드에서만 SDK 로그를 푼다.
      if (import.meta.env.VITE_RC_DEBUG === '1') await Purchases.setLogLevel({ level: LOG_LEVEL.VERBOSE });
      await Purchases.configure({ apiKey: IOS_KEY });
      RC = Purchases;
    })().catch((e) =&gt; {
      rcInit = null;                 // 다음 시도에서 다시 초기화할 수 있게
      throw e;
    });
  }
  await rcInit;                      // 반환값 없음
}

async function monthlyPackage() {
  const { current } = await RC.getOfferings();
  const pkgs = current?.availablePackages || [];
  return pkgs.find((p) =&gt; p.identifier === '$rc_monthly') || pkgs[0] || null;
}

export async function getSubscription() {
  // ...
  try {
    await ensureRC();
    const pkg = await monthlyPackage();
    // ...
  } catch (e) { /* ... */ }
}</code></pre>

<p>초기화 약속은 하나만 두어 동시에 불려도 <code>configure</code> 가 한 번만 돌고, 실패하면 비워서 다시 시도합니다. Android 쪽 자체 결제 플러그인(<code>Billing</code>)도 같은 Proxy 라 같은 규칙을 적용했습니다.</p>

<h3>함께 고친 것: 조용한 버튼</h3>
<p>사용자 입장에서 더 나빴던 건 "아무 일도 일어나지 않는다"는 점이라 버튼 쪽도 손봤습니다.</p>
<ul>
<li>스토어와 통신하는 동안 버튼을 잠그고 <code>Connecting…</code> 으로 바꿉니다.</li>
<li>상품 조회를 0초·4초·15초에 시도하고 버튼을 누르는 순간에도 한 번 더 봅니다. 그래도 없으면 연결을 확인해 달라는 문구를, 구매가 실패하면 실패 문구를 띄웁니다. 사용자가 결제 시트를 직접 닫은 경우만 조용히 넘어갑니다.</li>
<li>앱을 켤 때마다 부르던 <code>restorePurchases()</code> 를 <code>getCustomerInfo()</code> 로 바꾸고 '구매 복원' 버튼을 따로 달았습니다. RevenueCat 문서는 <code>restorePurchases</code> 가 OS 로그인 창을 띄울 수 있으니 사용자 동작으로만 부르라고 안내합니다.</li>
</ul>
<pre><code>// 유료 화면 세 곳이 같이 쓰는 구독 버튼
export default function UpsellCta() {
  const { price, subscribe, restorePurchases, busy, notice } = useEntitlement();
  return (
    &lt;&gt;
      &lt;button className="upsell-cta" disabled={busy} onClick={subscribe}&gt;
        {busy ? 'Connecting…' : price ? `Try Pro — ${price}` : 'Try Pro'}
      &lt;/button&gt;
      {notice &amp;&amp; &lt;p className="upsell-notice" role="status"&gt;{notice}&lt;/p&gt;}
      &lt;p className="upsell-note"&gt;
        Cancel any time in your app store.{' '}
        &lt;button className="upsell-restore" disabled={busy} onClick={restorePurchases}&gt;Restore purchases&lt;/button&gt;
      &lt;/p&gt;
    &lt;/&gt;
  );
}</code></pre>


<h2>검증</h2>
<p>같은 시뮬레이터에서 버튼에 가격이 붙어 <code>Try Pro — (가격)</code> 으로 그려졌고, 누르면 StoreKit 결제 흐름이 시작돼 Apple 계정 로그인 창이 떴습니다(샌드박스 계정이 없는 시뮬레이터라 여기까지가 정상). 창을 닫으면 버튼이 원래대로 돌아왔고, 회화 탭의 업셀 버튼도 같았습니다. 체크포인트 코드는 정식 빌드에서 걷어내고 SDK 상세 로그만 빌드 변수로 켤 수 있게 남겼습니다.</p>

<h2>Capacitor 쪽은 아직 그대로다</h2>
<p>같은 문제가 Capacitor 저장소에 이슈로 올라가 있고(<a href="https://github.com/ionic-team/capacitor/issues/8469" target="_blank" rel="noopener">ionic-team/capacitor#8469</a>), <code>then</code> 에 <code>undefined</code> 를 돌려주게 하는 수정 PR 도 두 개(#8473, #8582) 있습니다. 다만 2026년 11월 확인 시점에 셋 다 열린 상태였고 main 브랜치의 Proxy 도 위 코드와 같았습니다. 버전을 올린다고 사라지는 문제가 아직 아니므로 앱 코드에서 피해야 합니다.</p>

<h2>재발 방지 체크리스트</h2>
<h3>코드 규칙</h3>
<ul>
<li><strong>플러그인 객체를 async 함수에서 return 하지 않는다.</strong> <code>await</code>, <code>Promise.resolve()</code>, <code>Promise.all()</code>, <code>.then()</code> 콜백의 반환값도 같은 자리입니다. 값을 프로미스로 감싸 돌려주는 지연 로딩·싱글턴 헬퍼가 특히 위험합니다.</li>
<li>꼭 넘겨야 하면 <strong>평범한 객체로 감싼다.</strong> resolve 절차가 <code>then</code> 을 묻는 대상은 바깥 객체이고, 거기엔 <code>then</code> 이 없습니다.</li>
<li>Proxy 로 감쌀 거라면 <strong><code>then</code> 을 명시적으로 막는다.</strong> 그대로 통과시키는 래퍼는 소용없습니다.</li>
<li><strong>타입 검사기는 잡아 주지 않는다.</strong> 인터페이스에 <code>then</code> 이 없으니 TypeScript 에게 <code>Promise&lt;PurchasesPlugin&gt;</code> 은 멀쩡한 타입입니다. 문제는 런타임 Proxy 에 있습니다.</li>
</ul>
<pre><code>// 예시 1: 꼭 반환해야 한다면 평범한 객체로 감싼다
async function loadPurchases() {
  const { Purchases } = await import('@revenuecat/purchases-capacitor');
  await Purchases.configure({ apiKey: IOS_KEY });
  return { plugin: Purchases };      // resolve 절차가 then 을 묻는 대상은 바깥 객체다
}
const { plugin } = await loadPurchases();

// 예시 2: Proxy 로 한 번 더 감쌀 거라면 then 을 명시적으로 막는다
const nonThenable = (plugin) =&gt;
  new Proxy(plugin, {
    get: (target, prop, receiver) =&gt;
      prop === 'then' ? undefined : Reflect.get(target, prop, receiver),
  });</code></pre>

<h3>진단할 때 볼 지문</h3>
<ul>
<li>네이티브 브리지 로그에 초기화 호출까지만 있고 <strong>그다음 호출이 넘어오지 않는다.</strong> <code>try/catch</code> 에도 아무것도 안 걸린다.</li>
<li>처리되지 않은 거부에 <code>"플러그인이름.then()" is not implemented</code> 가 있다. 디버그 빌드에서 <code>unhandledrejection</code> 이벤트를 화면에 내보내 두면 바로 보입니다.</li>
<li>WebView 의 <code>console.log</code> 가 잘 잡히지 않으면 단계별 체크포인트를 화면에 그리는 편이 빠릅니다.</li>
</ul>
<h3>UI 규칙</h3>
<ul>
<li>결제 버튼은 누르면 반드시 무언가를 보여 줘야 합니다. 진행 중 상태가 있었다면 이 버그는 "반응 없음"이 아니라 "계속 연결 중"으로 보였을 겁니다.</li>
<li>스토어 호출에 타임아웃을 걸면 무한 대기를 오류로 바꿀 수 있습니다. 명세에 대기의 끝이 없으니 끝은 앱이 정해야 합니다.</li>
</ul>

<h2>남는 교훈</h2>
<p><strong>모든 속성에 답하는 객체는 덕 타이핑과 상극이다.</strong> 프로미스 절차는 <code>then</code> 을, <code>JSON.stringify</code> 는 <code>toJSON</code> 을, React 는 <code>$$typeof</code> 를 묻습니다. Capacitor 는 뒤의 둘만 막아 두었습니다. Proxy 기반 객체를 다룬다면 그 객체가 어디까지 흘러가는지 따져 봐야 합니다.</p>
<p><strong>"끝나지 않음"은 "실패"보다 찾기 어렵다.</strong> 실패는 스택 트레이스를 남기지만 끝나지 않는 <code>await</code> 는 아무것도 남기지 않습니다. 이번에 답을 준 것도 에러 메시지가 아니라 "어디까지 왔는가"를 순서대로 찍은 기록이었습니다.</p>
<div class="tip"><strong>Hangul Lab</strong> — 외국인을 위한 한글 학습 앱입니다. 자모와 받침, 음절 소리부터 생활 회화까지 단계별로 익힙니다. <a href="https://play.google.com/store/apps/details?id=com.lightonpluslab.hangullab" target="_blank" rel="noopener">Google Play에서 받기</a></div>
"""
},
{
"slug": "blog-play-memory-r8-dex-optimization",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "Play DEX 최적화 25% 기준 대응기 — R8을 꺼 버린 라이브러리 규칙 한 줄",
"desc": "2027년 2월 시행되는 Play 메모리 기준에 맞춰 여러 앱의 R8을 손봤습니다. minify를 켰는데도 최적화가 꺼져 있던 원인, 비율을 깎던 keep 규칙, AGP 9 전환의 함정과 점검 순서를 정리했습니다.",
"body": """
<p>2026년 10월, Play Console 에 "Play 표준 변경사항이 적용되기 전에 앱의 메모리 사용량을 최적화하세요"라는 알림이 떴습니다. 프로덕션 앱 8개의 Android vitals 대시보드 전부에 경고가 붙어 있었습니다. Flutter·Capacitor·웹뷰 래퍼 앱이 섞여 있었고, 경고는 비슷해도 원인은 앱마다 달랐습니다.</p>
<p>가장 오래 걸린 건 <code>minifyEnabled true</code> 와 <code>proguard-android-optimize.txt</code> 가 제대로 적혀 있는데도 "최적화가 꺼져 있다"고 나온 앱이었습니다. 원인은 제 빌드 파일이 아니라 결제 SDK 가 끌어온 라이브러리의 ProGuard 규칙 한 줄이었습니다.</p>

<h2>Play 가 요구하는 것</h2>
<p><a href="https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html" target="_blank" rel="noopener">Android Developers Blog</a>에 따르면 2027년 2월부터 앱은 동적 메모리(익명 RSS + 스왑), 백그라운드 비트맵 메모리, DEX 코드 최적화 기준을 맞춰야 하고, 못 맞추면 노출과 게시 기능이 제한될 수 있습니다. DEX 쪽은 R8 같은 도구로 최적화·축소·난독화 커버리지를 최소 25% 확보하라는 요구입니다.</p>
<p><a href="https://support.google.com/googleplay/android-developer/answer/17492799" target="_blank" rel="noopener">Play 고객센터 문서</a>에는 이 요건이 DEX 10MB 초과 앱(게임은 50MB)에만 강제된다고 적혀 있습니다. 그런데 Vitals 권장 조치는 크기와 상관없이 떴습니다. DEX 7.1MB 앱에도 "앱이 최적화되지 않았습니다"가 붙었습니다. 메모리 항목은 아직 현장 데이터가 집계되지 않아, 빌드 결과물만으로 판정되는 DEX 최적화부터 잡았습니다.</p>
<table>
<thead><tr><th>Vitals 의 R8 항목</th><th>앱</th></tr></thead>
<tbody>
<tr><td>"앱이 최적화되지 않았습니다"</td><td>Capacitor 1개, Flutter 1개</td></tr>
<tr><td>R8 은 도는데 최적화가 꺼져 있다는 판정</td><td>Flutter 1개</td></tr>
<tr><td>AGP 9.0 업그레이드, 최적화된 리소스 축소 권장</td><td>나머지 5개</td></tr>
</tbody>
</table>

<h2>판정 근거는 AAB 안에 있다</h2>
<p>콘솔에 올리기 전에 로컬에서 같은 숫자를 봐야 반복이 빨라집니다. AAB 안의 <code>BUNDLE-METADATA/com.android.tools/r8.json</code> 에 R8 이 어떤 옵션으로 돌았는지와 결과 통계가 들어 있습니다.</p>
<pre><code>unzip -p app-release.aab BUNDLE-METADATA/com.android.tools/r8.json | python3 -m json.tool

"options": { ..., "isOptimizationsEnabled": true, ... },
"stats": {
    "noObfuscationPercentage": 70.37,
    "noOptimizationPercentage": 70.9,
    "noShrinkingPercentage": 70.45
},
"resourceOptimization": { "isOptimizedShrinkingEnabled": true }</code></pre>
<p>위 값은 Vitals 가 "낮은 최적화 비율 29%"라고 한 앱의 번들입니다. 100 − 70.9 = 29.1 입니다. 다른 두 앱도 67.92 → 32%, 55.58 → 44% 로 Vitals 숫자와 일치했습니다. 공식 문서에서 이 대응을 본 적은 없지만 제 앱 세 개에서는 어긋난 적이 없습니다.</p>
<p>이 파일에서 두 경우를 구분하면 진단 방향이 갈립니다.</p>
<ul>
<li><strong><code>isOptimizationsEnabled: false</code></strong> — 스위치 자체가 꺼진 상태입니다. keep 규칙은 특정 클래스·멤버만 지키므로 이 스위치를 끄지 못합니다. 어딘가에 <code>-dontoptimize</code> 같은 전역 옵션이 있습니다.</li>
<li><strong>스위치는 켜졌는데 비율이 낮음</strong> — 넓은 keep 규칙이 코드 상당 부분을 최적화에서 빼고 있습니다.</li>
</ul>

<h2>사례 1 — 템플릿 기본값 그대로였던 두 앱</h2>
<p>Capacitor 로 만든 유아용 한글 앱은 Capacitor CLI 안드로이드 템플릿(8.5 기준)의 기본 설정 그대로였습니다.</p>
<pre><code>release {
    minifyEnabled false
    proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
}</code></pre>
<p>여기서 <code>minifyEnabled</code> 만 켜면 절반만 고친 것입니다. AGP 기본 파일 <code>proguard-android.txt</code> 안에 <code>-dontoptimize</code> 가 들어 있어서, 축소·난독화는 되지만 최적화는 꺼진 채 나갑니다. <code>proguard-android-optimize.txt</code> 로 바꾸고 <code>shrinkResources true</code> 를 더했습니다. 플러그인을 리플렉션으로 찾는 Capacitor 가 깨질까 걱정했지만, <code>@capacitor/android</code> 의 consumer 규칙이 <code>Plugin</code> 하위 클래스와 <code>@PluginMethod</code> 를 이미 지키고 있어 앱 규칙은 더할 필요가 없었습니다.</p>
<p>Flutter 보드게임 앱은 <code>isMinifyEnabled = false</code> 가 명시돼 있었습니다. 켜고 optimize 파일을 지정한 것이 전부입니다. 엔진용 keep 규칙은 Flutter Gradle 플러그인이 붙여 줍니다.</p>
<p>DEX 는 7.1MB → 0.8MB, 9.0MB → 1.0MB 로 줄었고 최적화 비율은 약 81%, 87% 가 됐습니다. 출시 당일 두 앱의 Vitals 항목은 경미 단계로 내려갔습니다.</p>

<h2>사례 2 — 설정은 맞는데 최적화가 꺼져 있던 앱</h2>
<p>강의 노트 앱(Flutter)은 처음부터 minify 와 optimize 파일이 켜져 있었는데 r8.json 이 <code>isOptimizationsEnabled: false</code> 였습니다.</p>
<h3>처음 의심한 것</h3>
<pre><code># Riverpod + freezed codegen — preserve generated classes referenced by name.
-keep class **.*$* { *; }</code></pre>
<p><code>**</code> 는 패키지 구분자를 포함한 아무 이름이므로, 이 규칙은 모든 라이브러리의 내부·익명 클래스를 통째로 지킵니다. 목적도 성립하지 않습니다. Riverpod·freezed 는 Dart 코드이고 릴리스에서 Dart 는 <code>libapp.so</code> 로 AOT 컴파일됩니다. R8 은 Java/Kotlin 바이트코드만 봅니다. 나쁜 규칙이지만, 앞의 기준으로 보면 비율을 깎을 뿐 스위치를 끄지는 못합니다. 다른 곳에 전역 옵션이 있어야 했습니다.</p>
<h3>진단: 합쳐진 설정 파일을 본다</h3>
<p>R8 이 받는 규칙은 앱 파일, AGP 기본 파일, Flutter 규칙, 모든 의존성 AAR 의 consumer 규칙을 합친 것입니다. 제 빌드 환경에서는 릴리스 빌드를 하면 이 합본이 <code>configuration.txt</code> 로 남고, 구간마다 출처 주석이 붙었습니다.</p>
<pre><code>grep -n -- '-dontoptimize' build/app/outputs/mapping/release/configuration.txt   # Flutter
grep -n -- '-dontoptimize' app/build/outputs/mapping/release/configuration.txt   # 일반 프로젝트

# The proguard configuration file for the following section is …/purchases-store-amazon-10.14.1/proguard.txt
-dontwarn com.amazon.**
-keep class com.amazon.** {*;}
-keepattributes *Annotation*
-dontoptimize</code></pre>
<p>RevenueCat <code>purchases_flutter</code> 10.4.3 이 끌어온 <code>purchases-store-amazon</code> 10.14.1 의 마지막 줄이었습니다. Amazon 앱스토어에 나가지도 않는 앱에서, 의존성으로 딸려 온 모듈 하나가 앱 전체의 최적화를 끄고 있었습니다.</p>
<p>R8 의 <a href="https://developer.android.com/topic/performance/app-optimization/global-options" target="_blank" rel="noopener">전역 옵션</a>은 어느 파일에 적혔든 앱 전체에 적용됩니다. <a href="https://developer.android.com/topic/performance/app-optimization/choose-libraries-wisely" target="_blank" rel="noopener">라이브러리 선택 가이드</a>도 keep 규칙은 더해지기만 하고, 라이브러리가 최적화를 끄는 규칙을 넣으면 프로젝트 전체가 꺼진다고 설명합니다. Gradle 캐시에서 비교해 보니 10.19.1 에는 이 줄이 없었고, 그 버전을 끌어오는 <code>purchases_flutter</code> 10.11.0 이상으로 올렸습니다. 누가 되돌리지 않도록 버전 제약 옆에 이유를 주석으로 남겼습니다.</p>
<p>AGP 9 에서는 <code>android.r8.globalOptionsInConsumerRules.disallowed</code> 가 기본으로 켜져, AAR·JAR 의존성의 전역 옵션이 무시되고 <code>configuration.txt</code> 에 <code># REMOVED CONSUMER RULE: -dontoptimize</code> 주석이 남는다고 <a href="https://developer.android.com/build/releases/agp-9-0-0-release-notes" target="_blank" rel="noopener">AGP 9.0 릴리스 노트</a>에 나와 있습니다. 이 함정은 주로 AGP 8.x 프로젝트의 문제이고, 당시 이 앱은 AGP 8.9 였습니다.</p>
<h3>넓은 규칙을 지운 자리</h3>
<p><code>**.*$*</code> 와 Dart 대상 규칙을 지우고, Java 쪽에서 실제로 리플렉션을 쓰는 곳만 지켰습니다. <code>flutter_local_notifications</code> 는 예약 알림을 Gson JSON 으로 저장했다가 다시 읽는데, 난독화된 필드 이름은 빌드마다 달라질 수 있어 지켜 두지 않으면 업데이트 후 이전 예약을 못 읽습니다.</p>
<pre><code>-keep class com.dexterous.flutterlocalnotifications.models.** { *; }
-keepattributes Signature
-keep,allowobfuscation,allowshrinking class * extends com.google.gson.reflect.TypeToken</code></pre>
<p>새로 설치하는 테스트로는 안 보이는 문제라, keep 을 지울 때는 이전 버전이 남긴 데이터를 읽을 수 있는지도 따져야 합니다. 결과는 DEX 19.2MB → 8.2MB, 최적화 비율 약 46% 였습니다.</p>

<h2>사례 3 — 켜져 있지만 29% 였던 앱</h2>
<p>외국인용 한글 학습 앱(Capacitor)은 "낮은 최적화 비율 29%"였습니다. 기준은 넘지만 여유가 4%p 였습니다. 원인은 두 갈래였습니다.</p>
<ul>
<li><strong>라이브러리의 패키지 전체 keep</strong> — RevenueCat 안드로이드 SDK 의 consumer 규칙 <code>-keep class com.revenuecat.** { *; }</code>. 전역 옵션이 아니라 AGP 9 에서도 그대로 적용됩니다.</li>
<li><strong>앱이 쓴 통째 keep</strong> — <code>com.getcapacitor.**</code>, <code>org.apache.cordova.**</code>, Play Billing, 앱 패키지 전체. Capacitor 와 Play Billing 의 consumer 규칙, <code>@JavascriptInterface</code> 를 지키는 AGP 기본 파일이 이미 하는 일이라 지웠습니다.</li>
</ul>
<p>이 앱은 안드로이드 결제를 Play Billing 직접 호출 플러그인으로 처리하고 RevenueCat 은 iOS 에서만 씁니다. 그런데 Capacitor 는 따로 지정하지 않으면 <code>package.json</code> 의 플러그인을 다 넣습니다. <a href="https://capacitorjs.com/docs/config" target="_blank" rel="noopener">Capacitor 설정</a>의 <code>android.includePlugins</code> 로 안드로이드 쪽만 골랐습니다.</p>
<pre><code>"android": {
  "includePlugins": ["@capacitor/app"]
}</code></pre>
<p><code>noOptimizationPercentage</code> 는 70.9 → 14.9(최적화 약 85%), DEX 는 4.6MB → 1.2MB 가 됐습니다. 안드로이드에서도 RevenueCat 을 쓰는 두 앱(32%, 44%)은 이 방법을 못 씁니다. AGP 8.4 이상의 <code>optimization.keepRules { it.ignoreFrom(...) }</code> 로 라이브러리 규칙을 걸러낼 수는 있지만 그러면 SDK 의 리플렉션 지점을 제가 대신 지켜야 해서, 결제 코드에는 적용하지 않았습니다.</p>

<h2>AGP 9 로 올리면서 생긴 일</h2>
<p>남은 두 권장 항목 때문에 앱 5개를 AGP 9.4.1·Gradle 9.6.1 로 올렸습니다. 릴리스 노트상 R8 관련 기본값 중 영향을 준 것은 이렇습니다(모두 false → true).</p>
<table>
<thead><tr><th>속성</th><th>바뀐 내용</th></tr></thead>
<tbody>
<tr><td><code>android.r8.proguardAndroidTxt.disallowed</code></td><td><code>proguard-android.txt</code> 지원 중단</td></tr>
<tr><td><code>android.r8.globalOptionsInConsumerRules.disallowed</code></td><td>의존성의 전역 옵션 무시</td></tr>
<tr><td><code>android.r8.optimizedResourceShrinking</code></td><td>코드와 리소스를 함께 보고 리소스를 더 적게 남김</td></tr>
<tr><td><code>android.r8.strictFullModeForKeepRules</code></td><td><code>-keep class A</code> 가 기본 생성자를 지키지 않음</td></tr>
</tbody>
</table>
<p>Flutter 앱은 당시 Flutter 3.41 의 플러그인들이 Kotlin Gradle 플러그인과 이전 DSL 을 써서 <code>android.builtInKotlin=false</code>, <code>android.newDsl=false</code> 를 넣었습니다. 또 AGP 9 는 라이브러리가 요구하는 compileSdk 를 검사해서, compileSdk 34 로 고정된 플러그인 때문에 빌드가 멈췄습니다. 루트 <code>build.gradle</code> 에서 36 미만인 라이브러리 모듈만 36 으로 컴파일하게 했습니다.</p>
<pre><code>subprojects {   // evaluationDependsOn(":app") 블록보다 위에 둔다
    afterEvaluate { project -&gt;
        def android = project.extensions.findByName("android")
        if (android != null &amp;&amp; project.plugins.hasPlugin("com.android.library")) {
            def sdk = (android.compileSdkVersion ?: "").replaceAll("[^0-9]", "")
            if (sdk &amp;&amp; sdk.toInteger() &lt; 36) android.compileSdkVersion 36
        }
    }
}</code></pre>
<p>r8.json 의 <code>isOptimizedShrinkingEnabled</code> 는 <code>true</code> 가 됐습니다. 문제는 표의 아래 두 줄이었습니다.</p>
<h3>함정 1: 이름으로 찾는 리소스가 사라진다</h3>
<p>음악 생성 앱(Flutter)의 AGP 9 빌드를 출시 전 태블릿에서 점검하다가, 소리는 나는데 알림창에 재생 컨트롤이 없는 것을 발견했습니다. <code>dumpsys media_session</code> 은 <code>active=false</code>, 로그에는 이 예외가 반복됐습니다.</p>
<pre><code>You must specify an icon resource id to build a CustomAction</code></pre>
<p><code>audio_service</code> 아이콘 이름은 Dart 에 문자열로 있고 네이티브 쪽은 이름으로 리소스를 찾으니, 축소기 눈에는 안 쓰는 리소스입니다. 직전 AGP 8 빌드에 남아 있던 리소스 444개가 지워졌고 그 안에 이 아이콘들이 있었습니다. analyze·테스트·재생 안 하는 실행으로는 안 잡힙니다.</p>
<p><code>tools:keep</code> 으로 하나씩 지킬 수도 있지만 그건 제가 아는 조회만 지킵니다. 소스를 볼 수 없는 구글 라이브러리가 이름으로 무엇을 찾는지는 알 수 없어서, 이 앱은 <code>android.r8.optimizedResourceShrinking=false</code> 로 되돌렸습니다(APK 약 250KB 증가, Vitals 항목은 알고서 남김). 대신 이름으로 찾는 리소스 목록을 두고, 릴리스 빌드 뒤 <code>aapt2 dump resources</code> 로 하나라도 없으면 빌드를 실패시킵니다. AAB 는 지워진 리소스 이름이 경로 문자열로 남아 문자열 검색으로는 "있다"고 나오므로, <code>base/resources.pb</code> 의 항목을 <code>type/name</code> 으로 대조해야 합니다.</p>
<h3>함정 2: <code>-keep class</code> 가 생성자를 지키지 않는다</h3>
<p>웹뷰 래퍼 앱은 AGP 9 첫 빌드가 실행 즉시 죽었습니다.</p>
<pre><code>Failed to create an instance of androidx.work.impl.WorkDatabase

# Room 2.2.5 의 consumer 규칙
-keep class * extends androidx.room.RoomDatabase</code></pre>
<p>광고 SDK 가 WorkManager 2.7.0 을, 그것이 Room 2.2.5 를 끌어옵니다. Room 은 생성된 <code>WorkDatabase_Impl</code> 을 리플렉션으로 만드는데, strict full mode 에서는 위 규칙이 클래스만 지키고 생성자는 지키지 않습니다. 릴리스 노트가 권하는 방법은 <code>-keep class A { &lt;init&gt;(); }</code> 형태로 바꾸는 것이고, 저는 이번엔 <code>android.r8.strictFullModeForKeepRules=false</code> 로 출시본과 같은 의미를 유지했습니다. 최적화와 리소스 축소는 켜진 채라는 것을 r8.json 으로 확인했습니다.</p>
<p>두 함정 모두 빌드와 정적 검사는 통과하고, 이름이나 리플렉션으로 무언가를 찾는 실행 경로에서만 드러납니다.</p>

<h2>어떻게 검증했나</h2>
<p>에뮬레이터에 릴리스 빌드를 올려 리플렉션과 이름 조회에 기대는 기능을 밟았습니다. 웹뷰의 플러그인 호출, 결제 플러그인의 구독 조회·구매 복원, 파일 선택기, 알림 예약과 실제 알람 등록, 재시작 후 설정 유지 같은 것들입니다. 에뮬레이터 결제는 <code>BILLING_UNAVAILABLE</code> 로 떨어져서 그 안내까지만 볼 수 있고, 실기기 결제 확인은 일부 앱에서 아직 남아 있습니다. 출시 후에는 Vitals 문구로 확인했습니다. 완전 미최적화였던 두 앱과 29% 였던 앱은 이후 판에서 R8 관련 권장 조치가 사라졌습니다.</p>

<h2>점검 순서</h2>
<ol>
<li><strong>r8.json 부터 연다.</strong> <code>isOptimizationsEnabled</code>, <code>noOptimizationPercentage</code>, <code>isOptimizedShrinkingEnabled</code> 를 적어 두고 고친 뒤 같은 값으로 비교합니다.</li>
<li><strong>스위치가 꺼져 있으면 전역 옵션을 찾는다.</strong> <code>minifyEnabled</code> 와 기본 파일 이름을 보고, <code>configuration.txt</code> 에서 <code>-dontoptimize</code>·<code>-dontshrink</code>·<code>-dontobfuscate</code> 를 검색해 출처를 확인합니다. 라이브러리면 그 줄이 없는 버전으로 올리고 이유를 남깁니다.</li>
<li><strong>비율이 낮으면 넓은 keep 을 찾는다.</strong> <code>**</code> 패턴, Dart·JS 를 지키려는 규칙, consumer 규칙과 겹치는 규칙. 그 플랫폼에서 안 쓰는 라이브러리는 빼고, 쓰는 라이브러리는 <code>ignoreFrom</code> 의 대가를 따집니다. AGP 9.3 이상이면 <a href="https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer" target="_blank" rel="noopener">R8 Configuration Analyzer</a> 가 규칙별 영향을 보여 줍니다(저는 이번엔 쓰지 않았습니다).</li>
<li><strong>지운 자리에 진짜 리플렉션 지점만 남긴다.</strong> JNI <code>native</code> 메서드, Gson 같은 저장 포맷, 이전 버전 데이터 호환.</li>
<li><strong>AGP 9 에서는 두 기본값을 의심한다.</strong> 이름으로 찾는 리소스를 목록으로 만들어 결과물과 대조하고, <code>-keep class</code> 에 기대는 리플렉션 생성을 찾습니다. 되돌릴 땐 그 플래그만 끕니다.</li>
<li><strong>릴리스 빌드를 기기에서 돌린다.</strong> 결제·알림·미디어 세션·백그라운드 작업·업데이트 후 데이터를 직접 밟습니다.</li>
<li><strong>출시 후 Vitals 문구로 확인하고</strong>, 다음 판에서 1번으로 돌아갑니다.</li>
</ol>
<p><code>minifyEnabled true</code> 는 R8 이 돈다는 뜻이지 최적화된다는 뜻이 아니었습니다. 판정은 내가 쓴 설정 파일이 아니라, 결과물(r8.json)과 R8 이 실제로 받은 합본(configuration.txt)으로 해야 합니다.</p>
"""
},
{
"slug": "blog-mtf-spot-diagram-reading",
"date": "2026-11-09",
"eyebrow": "Guide",
"title": "스팟 다이어그램·MTF 읽는 법 — 에어리 원과 센서 나이퀴스트로 렌즈 판정하기",
"desc": "렌즈 설계 결과의 스팟 다이어그램과 MTF를 무엇과 겹쳐 읽어야 하는지 정리했습니다. RMS·GEO 반경과 에어리 원, 수차별 스팟 모양, 픽셀 피치에서 구한 나이퀴스트 주파수와 MTF 목표값까지 다룹니다.",
"img": "img/lens-shot-spot.jpg",
"img_alt": "Lens에서 연 렌즈 설계 파일의 스팟 다이어그램 화면",
"body": """
<p>렌즈 설계 파일을 해석 도구로 열면 스팟 다이어그램과 MTF가 가장 먼저 눈에 들어옵니다. 그런데 둘 다 숫자 하나로는 좋고 나쁨을 말해 주지 않습니다. RMS 스팟 6 µm가 좋은 값인지는 F수와 픽셀 크기를 알아야 판단할 수 있고, MTF 0.4도 어느 주파수에서 읽었는지에 따라 충분하기도 하고 모자라기도 합니다.</p>
<p>저는 CODE V·Zemax 파일을 브라우저에서 여는 도구를 만들면서 그래프마다 정의를 하나씩 정해야 했습니다. 그때 공식보다 자주 따진 것은 <strong>"이 그래프를 무엇과 겹쳐 봐야 하는가"</strong>였습니다. 스팟은 에어리 원과 픽셀 크기와, MTF는 회절 한계 곡선과 센서의 나이퀴스트 주파수와 견줘야 뜻이 생깁니다. 이 두 그래프를 중심으로 읽는 순서와 자주 틀리는 지점을 적습니다.</p>

<h2>먼저 맞춰 둘 조건</h2>
<ul>
<li><strong>파장</strong> — 단색(흔히 d선 587.6 nm)인지, 여러 파장을 가중 평균한 다색인지. 다색에는 색수차가 섞이므로 단색보다 나쁘게 나오는 것이 정상입니다.</li>
<li><strong>초점 위치</strong> — 근축 상면인지, 성능이 가장 좋은 위치로 옮긴 상면인지. 스팟과 MTF는 상면을 조금만 옮겨도 달라집니다.</li>
<li><strong>작동 F수</strong> — 회절 계산에는 상공간 개구수로 정한 F수(N = 1/(2NA))가 들어갑니다. 무한 물체에서는 사양서의 F/#와 거의 같지만, 가까운 물체를 찍을 때는 커집니다.</li>
</ul>

<h2>스팟 다이어그램 읽기</h2>
<p>스팟 다이어그램은 한 필드 점에서 출발한 광선을 입사동 전체에 고르게 뿌려 추적하고, 상면에 닿은 자리를 점으로 찍은 그림입니다. 회절이 빠진 기하광학 결과라서 "빛이 어디로 가는가"는 정확히 보여 주지만, "상이 어떻게 보이는가"는 조건부로만 알려 줍니다.</p>

<h3>기준점과 두 가지 반경</h3>
<p>점은 보통 기준 파장의 주광선이 닿은 자리를 원점으로 찍히고, RMS는 광선들의 무게중심을 기준으로 내는 경우가 많습니다. 주광선 기준 RMS의 제곱은 무게중심 기준 RMS의 제곱에 둘 사이 거리의 제곱을 더한 값이라 항상 같거나 큽니다. 코마가 큰 필드일수록 차이가 벌어집니다. 어느 쪽이든 원점이 실제로 빛이 도착한 자리이므로, 상이 이상적인 위치에서 벗어나는 왜곡은 스팟에 나타나지 않습니다.</p>
<p>RMS 반경은 광선과 기준점 사이 거리를 제곱해 평균한 뒤 제곱근을 취한 값으로, 에너지가 대체로 얼마나 퍼졌는지를 대표합니다. GEO 반경은 가장 먼 광선까지의 거리입니다. 광선 하나가 정하는 값이라 성긴 꼬리에 크게 흔들리고, 추적 광선 수를 늘리면 더 먼 광선이 잡혀 커지기도 합니다. 순수한 초점 어긋남처럼 원판이 고르게 채워진 스팟은 GEO가 RMS의 약 1.4배(√2)입니다. 이 비율이 훨씬 크면 작은 중심에 에너지가 몰리고 소수의 광선이 멀리 흩어진 상태이고, 흩어진 빛은 상 주변에 얇게 깔려 대비를 떨어뜨립니다.</p>
<p>어느 반경을 기준으로 삼을지는 용도가 정합니다. 제가 다뤄 본 거리 측정용 수신 렌즈는 사양이 RMS가 아니라 모든 광선이 들어가는 100 % 스팟 지름으로 적혀 있었습니다. 검출기 밖으로 나간 빛은 신호가 되지 않기 때문입니다. 다만 이 100 %는 기하광학의 값입니다. 회절이 들어간 실제 점상은 바깥 고리가 계속 이어져 에너지 비율이 100 %에 아주 천천히 다가가므로, 스팟이 에어리 원보다 충분히 클 때만 실제 빛 분포와 비슷한 뜻을 가집니다.</p>
<p>반경인지 직경인지도 확인합니다. 도구를 바꿔 비교할 때 가장 흔한 2배 실수입니다. 제가 만든 Lens는 무게중심 기준 RMS <em>직경</em>을 숫자로 적고, 칸 안의 점선 원은 무게중심에 그린 RMS <em>반경</em> 원입니다.</p>

<h3>에어리 원과 겹쳐 보기</h3>
<p>수차가 전혀 없어도 원형 조리개의 점상은 회절 때문에 에어리 패턴으로 퍼지고, 첫 어두운 고리의 반경은 다음과 같습니다.</p>
<pre><code>에어리 반경  r = 1.22 × λ × N      (λ: 파장, N: 작동 F수)</code></pre>
<ul>
<li><strong>스팟이 에어리 원보다 훨씬 크다</strong> — 기하수차가 상을 지배합니다. 스팟 그림이 실제 번짐을 꽤 잘 대표하고, 스팟을 줄이면 그대로 화질이 좋아집니다.</li>
<li><strong>스팟이 에어리 원과 비슷하거나 그 안에 들어온다</strong> — 회절이 지배합니다. 스팟을 더 줄여도 상은 거의 변하지 않으므로, 이때는 파면 오차, Strehl 비, MTF로 판단합니다.</li>
</ul>
<p>그래서 <strong>"스팟이 작을수록 좋다"는 에어리 원 바깥에서만 맞는 말</strong>입니다. 에어리 원 안에서 RMS 1 µm와 0.5 µm의 차이는 두 설계의 우열을 가리는 근거가 되기 어렵습니다. GEO 스팟 전체가 에어리 원 안에 들어오면 회절 한계에 가깝다고 보는 눈대중이 있지만, 최종 판정은 파면 오차로 합니다. Lens는 스팟 칸의 자동 축척을 적어도 에어리 반경이 들어가게 잡으므로, 모든 필드의 점 무리가 칸 가운데 작게 뭉쳐 있다면 회절이 지배하는 설계라는 뜻입니다.</p>

<h3>필드별·파장별 모양으로 수차 알아보기</h3>
<p>스팟 한 칸의 모양보다, 필드를 따라 모양과 크기가 어떻게 변하는지가 더 많은 것을 알려 줍니다. 3차 수차 이론에서 각 수차는 상높이 h에 따라 커지는 방식이 다릅니다.</p>
<table>
<thead><tr><th>수차</th><th>축상 필드</th><th>필드에 따른 크기</th><th>스팟 모양</th></tr></thead>
<tbody>
<tr><td>구면수차</td><td>있음</td><td>필드와 거의 무관</td><td>원형 대칭, 밝은 중심에 성긴 테두리</td></tr>
<tr><td>코마</td><td>없음</td><td>h에 비례</td><td>반경 방향으로 꼬리를 끄는 혜성</td></tr>
<tr><td>비점수차</td><td>없음</td><td>h²에 비례</td><td>타원이나 짧은 선, 초점을 옮기면 긴 방향이 90° 돌아감</td></tr>
<tr><td>상면 만곡</td><td>없음</td><td>h²에 비례</td><td>둥근 채로 커지고, 그 필드만 초점을 옮기면 작아짐</td></tr>
<tr><td>축상 색수차</td><td>있음</td><td>필드와 거의 무관</td><td>색마다 크기만 다른 동심원</td></tr>
<tr><td>배율 색수차</td><td>없음</td><td>h에 비례</td><td>색마다 중심이 반경 방향으로 어긋남</td></tr>
</tbody>
</table>
<p>읽는 순서는 이렇습니다. 축상 스팟이 이미 크면 구면수차나 축상 색수차부터 의심하고, 파장별 점 색으로 둘을 가릅니다. 축상은 작은데 가장자리로 갈수록 커진다면 축외 수차입니다. 비대칭이면 코마, 길쭉하면 비점수차, 둥근 채로 커지면 상면 만곡 쪽입니다. 상높이별 RMS 곡선이 직선처럼 오르는지(h에 비례) 포물선처럼 휘어 오르는지(h²에 비례)도 단서가 됩니다. 실제 렌즈는 여러 수차와 고차 항이 섞이므로 이 표는 출발점이고, 광선 수차 곡선과 필드 곡률 그래프로 확인합니다.</p>
<p>가장자리 필드의 점 무리 한쪽이 칼로 자른 듯 평평하다면 렌즈나 경통 테두리가 광속을 자른 것(비네팅)입니다. 수차가 큰 바깥쪽 광선이 잘려 나가 스팟이 실제 설계 실력보다 작아 보일 수 있습니다. Lens에서는 칸 아래의 통과 광선 수와 상대 조도를 같이 봅니다.</p>

<h2>MTF를 센서와 맞춰 읽기</h2>
<p>MTF는 사인파 무늬를 찍었을 때 상에 남는 명암 대비의 비율을 공간 주파수(lp/mm, 1 mm 안의 밝고 어두운 줄 쌍 수)별로 그린 곡선입니다. 먼저 회절을 넣어 계산한 회절 MTF인지, 광선만으로 근사한 기하 MTF인지 확인합니다. 기하 MTF는 회절을 무시하므로 수차가 작은 렌즈에서는 실제보다 높게 나옵니다.</p>

<h3>기준선 1 — 회절 한계 곡선과의 간격</h3>
<pre><code>회절 차단 주파수  f_c = 1 / (λ × N)</code></pre>
<p>수차는 MTF를 깎을 뿐 올리지 못하므로, 설계 곡선은 같은 동공의 회절 한계 곡선 아래에 놓입니다. 볼 것은 높이 자체보다 그 곡선과의 간격입니다. 다색 MTF에서는 가장 짧은 파장이 차단 주파수를 정하며, Lens가 MTF 그래프와 함께 표시하는 차단 주파수도 그 기준입니다.</p>
<p>회절 한계에 붙어 있다고 좋은 렌즈인 것은 아닙니다. 회절 한계 자체가 F수에 묶여 있어서, d선에서 F/8 렌즈는 수차가 없어도 약 213 lp/mm보다 촘촘한 무늬를 전달하지 못합니다. 간격은 "이 F수에서 얼마나 잘 만들었나"를 말할 뿐이고, "이 센서에 충분한가"는 다음 기준선이 답합니다.</p>

<h3>기준선 2 — 픽셀 피치에서 나온 나이퀴스트 주파수</h3>
<pre><code>나이퀴스트 주파수  f_N = 1 / (2p)      (p: 픽셀 피치)</code></pre>
<p>세 식을 한 조합에 대입해 보면 관계가 보입니다.</p>
<pre><code>예시: λ = 0.5876 µm (d선), N = 2.8, p = 1.4 µm

에어리 반경       1.22 × 0.5876 µm × 2.8    ≈ 2.0 µm  (지름 약 4.0 µm, 픽셀 세 개 가까이)
회절 차단 주파수  1 / (0.0005876 mm × 2.8)   ≈ 608 lp/mm
나이퀴스트        1 / (2 × 0.0014 mm)        ≈ 357 lp/mm
회절 한계 MTF     f_N(357 lp/mm)에서 약 0.30, f_N/2(179 lp/mm)에서 약 0.63</code></pre>
<p>이 조합에서는 렌즈 차단 주파수가 나이퀴스트보다 높습니다. 357~608 lp/mm의 무늬는 렌즈를 통과하지만 센서가 표현하지 못하고, 낮은 주파수로 접혀 들어가 모아레가 됩니다(에일리어싱). 나이퀴스트 근처 MTF가 높다는 것이 언제나 장점만은 아닌 이유입니다. 반대로 픽셀이 0.8 µm면 나이퀴스트가 625 lp/mm로 d선 차단 주파수를 넘어, 수차를 다 없애도 센서의 가장 촘촘한 영역을 채우지 못합니다. 픽셀을 줄일 때 F수를 같이 따져야 하는 이유입니다. 베이어 컬러 센서는 빨강·파랑 화소가 한 칸 건너 하나씩이라 그 채널의 샘플 간격이 2p이고, 색 모아레는 흑백 기준 나이퀴스트보다 낮은 주파수에서도 생깁니다.</p>

<h3>어느 주파수에서 몇 %를 볼까</h3>
<p>읽을 주파수는 렌즈가 아니라 센서에서 정합니다. 흔히 나이퀴스트와 그 절반을 고르고, 그 주파수에서 중심·0.7 필드·모서리처럼 몇 개 상높이의 T와 S 값을 같은 초점에서 읽습니다. 이 용도에는 주파수별 곡선보다 상높이별 MTF가 맞습니다.</p>
<p>몇 %면 좋은가에는 정답이 없고, 기준은 같은 주파수의 회절 한계 값입니다. 위 예시에서 f_N/2 값이 0.45라면 회절 한계 0.63의 약 70 %이니 수차로 꽤 잃은 것입니다. 같은 0.45라도 회절 한계가 0.5인 조합에서는 거의 다 끌어낸 값이 됩니다. 요구값이 회절 한계를 넘으면 수차를 0으로 만들어도 맞출 수 없는데, 이 예시에서 "나이퀴스트에서 0.5 이상"이 그런 요구입니다.</p>
<p>"MTF 50%"라는 말도 풀어서 확인합니다. 어떤 주파수에서 값이 0.5라는 뜻(그 무늬의 명암 차가 절반 남는다)인지, MTF가 0.5로 떨어지는 주파수(MTF50, 단위 lp/mm)인지에 따라 전혀 다른 숫자입니다. 어느 쪽도 선명도가 50 %라는 뜻은 아닙니다. 카메라 리뷰의 MTF50은 대개 찍은 영상에서 잰 값이라 센서와 샤프닝이 들어 있어, 렌즈만 계산한 설계 MTF와 바로 비교할 수 없습니다.</p>

<h3>스팟 크기를 픽셀 수로 바꿔 읽기</h3>
<p>스팟과 MTF는 따로 보는 그래프 같지만, 기하수차가 지배하는 영역에서는 스팟 크기로 MTF를 어림할 수 있습니다. 스팟을 가우시안 모양으로 근사하면 MTF는 RMS 지름 D와 주파수 f의 곱으로만 정해지고, 픽셀 피치로 나타내면 다음과 같습니다.</p>
<pre><code>가우시안 근사 예시 (기하수차 지배, 렌즈만, 회절·픽셀 개구 제외)
RMS 지름 D = 1p    →  f_N에서 약 0.54
RMS 지름 D = 1.5p  →  f_N에서 약 0.25
RMS 지름 D = 2p    →  f_N에서 약 0.08,  f_N/2에서 약 0.54</code></pre>
<p>RMS 지름이 픽셀 두 개쯤이면 나이퀴스트에서는 대비가 거의 남지 않고, 그 절반 주파수가 실질적인 한계가 된다는 뜻입니다. 반대로 스팟이 픽셀보다 훨씬 작으면 렌즈가 센서보다 촘촘한 무늬를 넘기므로 에일리어싱을 걱정할 쪽입니다.</p>
<p>실제 스팟은 꼬리나 비대칭이 있어 이 어림과 어긋나는데, 어긋나는 방향이 정보가 됩니다. MTF가 어림보다 높다면 작은 중심에 에너지가 몰려 있고 멀리 흩어진 소수 광선이 RMS를 부풀린 경우입니다. MTF가 어림보다 낮다면 스팟이 회절을 무시할 수 없는 크기이거나, 초점 어긋남처럼 에너지가 가장자리까지 고르게 퍼진 모양일 수 있습니다. 회절이 원인이라면 같은 주파수의 회절 한계 MTF를 곱한 정도까지 내려간다고 어림합니다.</p>

<h3>T와 S, 그리고 곡선 모양</h3>
<p>접선(T) MTF는 명암이 광축에서 필드 점을 향하는 방향(필드가 Y축 위면 Y 방향)으로 바뀌는 무늬, 곧 줄이 광축 중심의 원에 접하게 놓인 무늬의 값입니다. 시상(S) MTF는 줄이 광축을 향해 방사형으로 놓인 무늬의 값입니다. 축상에서는 둘이 겹치고, 축외에서 벌어지면 비점수차와 상면 만곡이 흔한 원인입니다. 스팟이 한 방향으로 길쭉해지는 필드와 T·S가 갈라지는 필드가 같은지 맞춰 보면 확인됩니다. 한 방향 세부만 뭉개지는 현상은 평균에 드러나지 않으므로 두 값을 평균하지 않습니다.</p>
<ul>
<li><strong>저주파부터 한 단 내려앉은 곡선</strong> — 빛의 일부가 넓게 흩어진 상태입니다. 스팟의 GEO/RMS 비율이 큰 경우와 짝을 이룹니다.</li>
<li><strong>0까지 떨어졌다 다시 오르는 곡선</strong> — 다시 오른 구간은 흑백이 뒤집혀 맺히는 가짜 해상입니다. 그래프가 크기만 그리기 때문에 생기는 모양이라 해상력으로 세지 않습니다. 초점이 크게 어긋났을 때 흔합니다.</li>
<li><strong>중심만 좋고 가장자리가 나쁜 결과</strong> — 정해 둔 상면 하나에서의 값입니다. 수차 탓인지 상면을 중심에 맞춘 탓인지는 스루포커스 MTF로 가립니다.</li>
</ul>

<h2>PSF·에너지·상대 조도는 이어서 확인한다</h2>
<p>스팟이 에어리 원 근처까지 작아지면 상의 모양은 회절을 넣은 PSF로 봐야 하고, 필드끼리의 비교는 Strehl 비로 합니다. 검출기처럼 받는 쪽 크기가 정해진 용도라면 둘러싸인 에너지(encircled energy)가 MTF보다 직접적인 기준이 되며, 정사각형 픽셀 하나에 드는 빛을 엄밀히 보려면 정사각형 안의 에너지(ensquared energy)를 봅니다. 정의와 수치 예는 <a href="https://lens.lightonpluslab.com/guide/ko/mtf-psf-strehl" target="_blank" rel="noopener">MTF·PSF·Strehl 비·에너지 집중도 가이드</a>에 정리해 두었습니다.</p>
<p>상대 조도는 가장자리 스팟과 MTF를 믿어도 되는지 확인하려고 같이 엽니다. 가장자리 성능이 의외로 좋은데 같은 상높이에서 상대 조도가 급히 꺾인다면, 비네팅으로 얻은 성능일 수 있습니다. 곡선 읽는 법은 <a href="https://lens.lightonpluslab.com/guide/ko/relative-illumination" target="_blank" rel="noopener">상대 조도 가이드</a>에 있습니다.</p>

<h2>읽는 순서 정리</h2>
<ol>
<li>파장, 작동 F수, 초점 위치, 반경·직경과 기준점을 먼저 맞춘다.</li>
<li>스팟을 에어리 원과 비교해 기하수차가 지배하는지 회절이 지배하는지 정한다.</li>
<li>필드를 따라 스팟 모양과 크기가 변하는 방식으로 수차 종류를 좁힌다.</li>
<li>픽셀 피치에서 나이퀴스트를 구하고, 그 주파수와 절반에서 상높이별 T·S MTF를 읽는다.</li>
<li>목표값은 같은 주파수의 회절 한계 값과 견줘 정한다.</li>
<li>스팟 크기를 픽셀 수로 바꿔 MTF와 앞뒤가 맞는지 본다.</li>
<li>가장자리 성능은 상대 조도와 통과 광선 수로 비네팅의 대가인지 확인한다.</li>
</ol>
<p>스팟과 MTF는 같은 빛을 다른 축에서 본 그래프입니다. 한 그래프에서 본 이상은 다른 그래프에서도 같은 모양으로 나타나야 원인으로 믿을 수 있습니다. 헤일로라면 GEO/RMS 비율과 저주파 MTF가 함께 움직이고, 비점수차라면 길쭉한 스팟과 T·S 간격이 함께 움직입니다. 두 그래프가 서로 맞지 않으면 렌즈보다 먼저 계산 조건이 같은지를 확인합니다.</p>
<div class="tip"><strong>Lens</strong> — CODE V .seq와 Zemax .zmx 파일을 브라우저에서 열어 스팟 다이어그램, 상높이별 MTF, PSF, 상대 조도를 바로 볼 수 있는 무료 도구입니다. 파일은 서버로 올라가지 않습니다. <a href="https://lens.lightonpluslab.com/ko" target="_blank" rel="noopener">Lens 열기</a></div>
"""
},
{
"slug": "blog-pdf-lib-korean-font-subset",
"date": "2026-11-09",
"eyebrow": "Dev Note",
"title": "pdf-lib 한글 PDF 글자 누락: subset:true와 fontkit long loca 버그",
"desc": "pdf-lib에서 나눔명조를 subset: true로 넣으면 일부 한글이 빈칸이 됩니다. 원인은 fontkit 포크가 loca 오프셋을 2로 나누며 생긴 1바이트 오차였고, HarfBuzz로 미리 서브셋해 해결했습니다.",
"body": """
<p>제가 만든 녹취록AI는 통화 녹음을 법원 제출용 녹취록 PDF로 만들어 줍니다. 처음에 쓰던 jsPDF는 기본 폰트에 한글 글리프가 없어 글자가 깨졌고, 그래서 PDF 생성을 서버로 옮겨 pdf-lib에 나눔명조 TTF를 직접 넣었습니다. 흔한 예제 그대로입니다.</p>
<pre><code>pdf.registerFontkit(fontkit);
const font = await pdf.embedFont(fontBytes, { subset: true });</code></pre>
<p>그런데 <code>subset: true</code>(문서에 쓴 글자만 남겨 넣는 옵션)를 켠 PDF에서 <strong>일부 글자가 빈칸으로</strong> 나왔습니다. 원인은 pdf-lib이 쓰는 fontkit 포크가 loca 오프셋을 2로 나누며 생기는 1바이트 오차였고, HarfBuzz로 미리 서브셋한 폰트를 <code>subset: false</code>로 넣어 해결했습니다. 그 과정에서 만난 함정 두 개까지 정리합니다.</p>
<h2>증상: 글자 폭만큼 빈칸이 남는다</h2>
<p>나눔명조 Regular를 <code>subset: true</code>로 넣고 "통화 녹음 1분 녹취록 화자", "안녕하세요 지난주에 말씀드렸던 계약 건"을 찍어 macOS PDF 렌더러로 그려 보면, 첫 줄은 "녹음"과 "녹"만, 둘째 줄은 "녕하세"와 "약 건"만 보입니다. 사라진 자리는 글자 폭만큼 비어 있습니다.</p>
<ul>
<li><strong>빠지는 글자가 일정하지 않습니다.</strong> 위에서 멀쩡한 "통"이 다른 문서에서는 빠집니다. 숫자와 가운뎃점도 빠졌습니다.</li>
<li><strong>짧은 문서에서만 납니다.</strong> 서로 다른 음절 100개를 넣으면 85개가 깨졌는데 150개를 넣으면 하나도 깨지지 않았습니다. 긴 샘플로만 테스트하면 놓칩니다.</li>
<li><strong><code>subset: false</code>면 전부 정상</strong>이지만 한 쪽짜리 PDF가 1.4MB가 됩니다.</li>
</ul>
<h2>subset을 끄면 왜 1.4MB가 되나</h2>
<p>PDF는 보는 쪽 기기에 폰트가 있다고 가정할 수 없어서 글리프를 파일 안에 넣습니다. PDF 표준 14 폰트에는 한글이 없으니 임베드는 사실상 필수입니다. 그런데 현대 한글은 완성형 음절만 11,172자이고 음절마다 외곽선이 따로 있습니다. 나눔명조 Regular는 글리프 14,538개, 파일 1,856,572바이트 중 외곽선을 담은 <code>glyf</code> 테이블이 1,737,728바이트입니다. Regular와 Bold를 통째로 넣으면 본문 424자짜리 한 쪽 예시 문서가 pdf-lib의 Flate 압축을 거치고도 1,432,236바이트입니다. 모바일에서 주고받을 파일로는 너무 커서 서브셋은 포기할 수 없었습니다.</p>
<h2>먼저 배제한 것들</h2>
<p>빈칸 증상의 후보는 여럿이지만 빠르게 걸러낼 수 있습니다. 폰트에 글자가 없는 경우라면 <code>subset: false</code>에서도 안 보여야 합니다. 텍스트가 NFD(자모 분리형)라면 <code>text.normalize('NFC') !== text</code>로 바로 드러납니다. 뷰어 문제인지는 PDF에 넣는 폰트를 fontkit으로 다시 읽어 보면 뷰어 없이 판정됩니다. 이 마지막 방법이 핵심 진단 도구였습니다.</p>
<pre><code>// 예시: pdf-lib 이 내부에서 하는 서브셋을 fontkit 으로 똑같이 만들고, 다시 읽어 원본과 비교
const fontkit = require('@pdf-lib/fontkit');
const fs = require('fs');
const font = fontkit.create(fs.readFileSync('NanumMyeongjo-Regular.ttf'));
const text = '통화 녹음 1분 녹취록 화자';
const subset = font.createSubset();
const pairs = font.layout(text).glyphs.map((g) =&gt; [g, subset.includeGlyph(g)]);
const chunks = [];
subset.encodeStream()
  .on('data', (b) =&gt; chunks.push(Buffer.from(b)))
  .on('end', () =&gt; {
    const sub = fontkit.create(Buffer.concat(chunks));
    console.log('loca 형식', font.head.indexToLocFormat, '→', sub.head.indexToLocFormat);
    for (const [g, id] of pairs) {
      let same = false;
      try {
        same = sub.getGlyph(id).path.toSVG() === g.path.toSVG();
      } catch (e) {
        // 손상된 글리프는 다시 읽는 단계에서 예외가 나기도 한다
      }
      if (!same) console.log('손상:', String.fromCodePoint(...g.codePoints));
    }
  });
// 출력
// loca 형식 1 → 0
// 손상: 화 / 분 / 취 / 록 / 화 / 자</code></pre>
<p>원본은 <code>indexToLocFormat</code>이 1(long)인데 서브셋은 0(short)으로 바뀌어 있었고, 공백을 포함한 글리프 10개 중 5개가 원본과 달랐습니다. 다른 문장에서는 다시 읽다가 <code>Trying to access beyond buffer length</code> 예외가 나는 글리프도 많았습니다. 뷰어가 아니라 폰트 파일 자체가 망가져 있었습니다. 이 에러 메시지는 뒤에서 다른 원인으로 한 번 더 나옵니다.</p>
<h2>원인: loca 오프셋을 2로 나누는 순간</h2>
<h3>loca와 glyf</h3>
<p>TrueType에서 외곽선은 <code>glyf</code> 테이블에 이어 붙어 있고, n번 글리프의 위치는 <code>loca</code> 테이블이 알려 줍니다. 데이터는 <code>loca[n]</code>부터 <code>loca[n+1]</code> 직전까지이고, 공백처럼 외곽선이 없으면 두 값이 같습니다. <a href="https://learn.microsoft.com/en-us/typography/opentype/spec/loca" target="_blank" rel="noopener">OpenType 명세</a>는 <code>head</code> 테이블의 <code>indexToLocFormat</code>에 따라 두 형식을 둡니다.</p>
<table>
<thead><tr><th>indexToLocFormat</th><th>형식</th><th>저장하는 값</th><th>표현 가능한 glyf 크기</th></tr></thead>
<tbody>
<tr><td>0</td><td>short (Offset16)</td><td>실제 오프셋 ÷ 2</td><td>최대 131,070바이트</td></tr>
<tr><td>1</td><td>long (Offset32)</td><td>실제 오프셋</td><td>사실상 제한 없음</td></tr>
</tbody>
</table>
<p>short는 2로 나눈 값을 저장하므로 <strong>짝수 오프셋만 표현할 수 있고</strong>, 그래서 short 형식 폰트는 모든 글리프 길이가 짝수입니다. long에는 그런 제약이 없습니다. glyf가 1.7MB인 나눔명조는 long 형식이고, 14,538개 중 2,890개 글리프의 길이가 홀수였습니다.</p>
<h3>@pdf-lib/fontkit의 서브셋 코드</h3>
<p>pdf-lib은 fontkit을 포크한 <code>@pdf-lib/fontkit</code>에 폰트 처리를 맡깁니다. 최신 버전 1.1.1의 TrueType 서브셋은 글리프 바이트를 <strong>패딩 없이</strong> 이어 붙이고, 마지막 오프셋이 0xFFFF 이하이면 short 형식을 골라 모든 오프셋을 2로 나눕니다.</p>
<pre><code>// @pdf-lib/fontkit 1.1.1 (배포 번들에서 발췌)
// 서브셋: 글리프 바이트를 패딩 없이 이어 붙이며 누적 오프셋을 기록
this.glyf.push(buffer);
this.loca.offsets.push(this.offset);
this.offset += buffer.length;
// loca 인코딩: 마지막 오프셋이 0xFFFF 이하면 short 형식을 고르고 전부 2로 나눔
loca.preEncode = function () {
  if (this.version != null) return;
  this.version = this.offsets[this.offsets.length - 1] &gt; 0xffff ? 1 : 0;
  if (this.version === 0) {
    for (var i = 0; i &lt; this.offsets.length; i++) {
      this.offsets[i] &gt;&gt;&gt;= 1;
    }
  }
};</code></pre>
<p>패딩 없이 붙였으니 누적 오프셋이 홀수일 수 있고, <code>&gt;&gt;&gt;= 1</code>은 그 나머지를 버립니다. 읽는 쪽은 2를 곱하므로 <strong>그 글리프는 1바이트 앞에서 시작하는 것으로 읽힙니다.</strong> 헤더의 첫 2바이트(윤곽선 개수)에 앞 글리프의 마지막 바이트가 섞이니 해석이 무너집니다. 진단 문장의 서브셋을 풀어 보면 이렇습니다.</p>
<table>
<thead><tr><th>글자</th><th>글리프 길이</th><th>실제 시작 위치</th><th>저장 후 다시 읽은 위치</th></tr></thead>
<tbody>
<tr><td>통</td><td>371</td><td>0</td><td>0</td></tr>
<tr><td>화</td><td>377</td><td>371</td><td><strong>370</strong></td></tr>
<tr><td>(공백)</td><td>0</td><td>748</td><td>748</td></tr>
<tr><td>녹</td><td>284</td><td>748</td><td>748</td></tr>
<tr><td>음</td><td>350</td><td>1032</td><td>1032</td></tr>
<tr><td>1</td><td>73</td><td>1382</td><td>1382</td></tr>
<tr><td>분</td><td>396</td><td>1455</td><td><strong>1454</strong></td></tr>
<tr><td>취</td><td>320</td><td>1851</td><td><strong>1850</strong></td></tr>
<tr><td>록</td><td>382</td><td>2171</td><td><strong>2170</strong></td></tr>
<tr><td>자</td><td>224</td><td>2553</td><td><strong>2552</strong></td></tr>
</tbody>
</table>
<p>위치가 어긋난 다섯 글자가 진단 스크립트가 보고한 글자와 정확히 같습니다. 증상도 모두 설명됩니다. 어느 글리프가 홀수 위치에서 시작하는지는 앞에 놓인 글리프 길이 합의 홀짝으로 정해지므로, 같은 "통"도 문서마다 운명이 다릅니다. 서브셋의 glyf가 65,535바이트를 넘으면 long 형식이 선택되어 나누기가 없으니 긴 문서는 멀쩡합니다. 원본이 short 형식인 폰트는 길이가 전부 짝수라 안전합니다. 음절 수를 늘려 가며 재 보면 경계가 그대로 보입니다.</p>
<table>
<thead><tr><th>서로 다른 음절 수</th><th>선택된 형식</th><th>서브셋 glyf 크기</th><th>손상된 글리프</th></tr></thead>
<tbody>
<tr><td>50</td><td>short</td><td>21,980바이트</td><td>43 / 50</td></tr>
<tr><td>100</td><td>short</td><td>45,578바이트</td><td>85 / 100</td></tr>
<tr><td>150</td><td>long</td><td>70,272바이트</td><td>0 / 150</td></tr>
<tr><td>200</td><td>long</td><td>90,523바이트</td><td>0 / 200</td></tr>
</tbody>
</table>
<p>제목과 표 머리글에만 쓰는 굵은 글씨 폰트는 글자 수가 적어 거의 항상 short 쪽으로 떨어집니다.</p>
<h3>상위 fontkit은 2019년에 고쳤다</h3>
<p>원본 fontkit은 이 문제를 <a href="https://github.com/foliojs/fontkit/pull/191" target="_blank" rel="noopener">PR #191</a>(2019년 3월 병합)에서 고쳤습니다. 서브셋이 원본의 loca 형식을 그대로 쓰게 바꾼 수정입니다. 하지만 2020년 11월에 배포된 <code>@pdf-lib/fontkit</code> 1.1.1에는 이 수정이 없습니다. pdf-lib의 <a href="https://github.com/Hopding/pdf-lib/issues/1232" target="_blank" rel="noopener">이슈 #1232</a>는 2022년부터 열려 있고, 상위 변경을 가져오자는 <a href="https://github.com/Hopding/fontkit/pull/5" target="_blank" rel="noopener">포크 쪽 PR</a>도 병합되지 않았습니다(2026년 11월 확인).</p>
<p>fontkit 2.0.4에는 수정이 들어 있지만, pdf-lib 1.17.1은 서브셋을 직렬화할 때 fontkit 2에 없는 <code>encodeStream()</code>을 호출해서 <code>subset: true</code>로 넣으면 <code>_this.subset.encodeStream is not a function</code>으로 실패합니다. 이슈 스레드에 언급된 커뮤니티 포크는 검증하지 않았습니다.</p>
<h2>해결: HarfBuzz로 먼저 줄이고, pdf-lib에는 통째로 넣는다</h2>
<p>서브셋을 pdf-lib 밖에서 하기로 했습니다. <code>subset-font</code>는 HarfBuzz의 서브셋 기능을 WebAssembly로 빌드한 <code>harfbuzzjs</code>를 감싼 Node 패키지입니다. 문서에 쓰인 글자만 남긴 TTF를 만들고 pdf-lib에는 <code>subset: false</code>로 넣습니다. 이때 pdf-lib은 받은 폰트 바이트를 그대로 넣으므로 작은 폰트는 작게 들어갑니다.</p>
<pre><code>// fonts-server.ts (발췌)
import 'server-only';
import subsetFont from 'subset-font';
import { padGlyfTable } from '@/lib/export/ttf-pad';
/** 본문/굵은 글씨에 실제로 쓰이는 문자열을 넘기면 서브셋 폰트 한 쌍을 돌려준다 */
export async function prepareFonts(regularText: string, boldText: string): Promise&lt;PdfFonts&gt; {
  const [regularSrc, boldSrc] = await Promise.all([
    loadFont('NanumMyeongjo-Regular.ttf'),
    loadFont('NanumMyeongjo-Bold.ttf'),
  ]);
  // 숫자·구두점·기본 라틴은 항상 포함 (쪽 번호, 시각 등)
  const base = ' 0123456789:./-()[]【】「」·,?!%₩"\\'_';
  const [regular, bold] = await Promise.all([
    subsetFont(regularSrc, regularText + base, { targetFormat: 'sfnt', dropTables: ['GSUB', 'GPOS', 'gasp'], keepFeatures: [] }),
    subsetFont(boldSrc, boldText + base, { targetFormat: 'sfnt', dropTables: ['GSUB', 'GPOS', 'gasp'], keepFeatures: [] }),
  ]);
  return { regular: padGlyfTable(new Uint8Array(regular)), bold: padGlyfTable(new Uint8Array(bold)) };
}
// pdf.ts (발췌)
pdf.registerFontkit(fontkit);
// 이미 서브셋된 폰트 — fontkit 의 자체 서브셋(long-loca 버그)은 쓰지 않는다
const regular = await pdf.embedFont(fonts.regular, { subset: false });
const bold = await pdf.embedFont(fonts.bold, { subset: false });</code></pre>
<p>HarfBuzz도 short 형식을 골랐지만 홀수 길이 글리프 뒤에 1바이트를 채워 오프셋을 짝수로 맞춥니다. "통"은 371바이트에서 372바이트로, "화"는 377바이트에서 378바이트로 늘어 있었습니다.</p>
<ul>
<li><strong>서브셋 입력은 렌더링과 같은 문서 모델에서 뽑습니다.</strong> 쪽 번호처럼 렌더링 중에 생기는 문자는 기본 문자열로 항상 넣습니다. pdf-lib은 폰트에 없는 글자를 만나도 예외 없이 0번 글리프(.notdef)를 찍고, 나눔명조의 .notdef는 외곽선이 없습니다. 입력에서 빠진 글자도 fontkit 버그와 <strong>똑같은 빈칸</strong>이 됩니다.</li>
<li><strong>GSUB·GPOS를 뺐습니다.</strong> 완성형 한글 음절은 cmap만으로 글리프가 정해지므로 영향이 없지만, 옛한글이나 합자가 필요하면 다시 봐야 합니다.</li>
</ul>
<h2>두 번째 함정: 같은 에러, 다른 원인</h2>
<p>HarfBuzz 서브셋을 넣자 이번에는 PDF를 만드는 도중에 <code>RangeError: Trying to access beyond buffer length</code>가 났고, 스택은 fontkit의 <code>TTFGlyph._getCBox</code>를 가리켰습니다. fontkit은 외곽선을 해석할 때(<code>_decode</code>)는 <code>loca[n] === loca[n+1]</code>이면 빈 글리프로 보고 돌아가지만, 바운딩 박스를 구할 때(<code>_getCBox</code>)는 이 확인 없이 10바이트 헤더를 읽습니다. 글자 폭을 구하는 <code>_getMetrics</code>가 이 함수를 부르므로 글자를 찍기만 해도 이 경로를 탑니다. 여기에 세 조건이 겹쳤습니다.</p>
<ol>
<li>나눔명조에서 공백은 마지막 글리프(14,537번)이고 외곽선이 없습니다.</li>
<li>HarfBuzz는 원본의 글리프 순서를 유지한 채 번호를 다시 매기므로 공백이 서브셋에서도 마지막이 되고, 시작 오프셋이 glyf 길이와 같습니다.</li>
<li>제가 확인한 HarfBuzz 출력에서는 모두 glyf가 파일 맨 끝 테이블이었습니다. 한 예시에서 glyf는 1,024바이트 위치부터 1,854바이트, 파일 전체는 2,880바이트였습니다.</li>
</ol>
<p>그래서 공백의 헤더를 읽다가 파일 끝을 넘습니다. 원본 폰트는 glyf가 파일 맨 앞이라 넘친 읽기가 다음 테이블에 떨어질 뿐 예외가 나지 않았습니다. 해결은 glyf 끝에 0을 16바이트 붙이는 것입니다. loca는 그대로라 글리프 해석은 바뀌지 않고, 넘친 읽기는 0으로 된 헤더를 얻습니다. 뒤 테이블 위치가 밀리므로 테이블 디렉터리를 다시 씁니다.</p>
<pre><code>// ttf-pad.ts
const PAD_BYTES = 16;
function align4(n: number): number {
  return (n + 3) &amp; ~3;
}
export function padGlyfTable(font: Uint8Array): Uint8Array {
  const view = new DataView(font.buffer, font.byteOffset, font.byteLength);
  const numTables = view.getUint16(4);
  const entries: Array&lt;{ tag: string; checksum: number; offset: number; length: number }&gt; = [];
  for (let i = 0; i &lt; numTables; i++) {
    const p = 12 + i * 16;
    const tag = String.fromCharCode(font[p], font[p + 1], font[p + 2], font[p + 3]);
    entries.push({ tag, checksum: view.getUint32(p + 4), offset: view.getUint32(p + 8), length: view.getUint32(p + 12) });
  }
  if (!entries.some((e) =&gt; e.tag === 'glyf')) return font;
  // 새 크기 계산 (디렉터리 뒤에 원래 순서대로 4바이트 정렬)
  const headerSize = 12 + numTables * 16;
  let total = align4(headerSize);
  const placed = entries.map((e) =&gt; {
    const length = e.tag === 'glyf' ? e.length + PAD_BYTES : e.length;
    const offset = total;
    total = align4(total + length);
    return { ...e, newOffset: offset, newLength: length };
  });
  const out = new Uint8Array(total);
  out.set(font.subarray(0, 12), 0);
  const outView = new DataView(out.buffer);
  placed.forEach((e, i) =&gt; {
    const p = 12 + i * 16;
    out.set(font.subarray(12 + i * 16, 12 + i * 16 + 4), p); // tag
    outView.setUint32(p + 4, e.checksum);
    outView.setUint32(p + 8, e.newOffset);
    outView.setUint32(p + 12, e.newLength);
    out.set(font.subarray(e.offset, e.offset + e.length), e.newOffset);
  });
  return out;
}</code></pre>
<p>0 바이트는 32비트 합으로 계산하는 테이블 체크섬을 바꾸지 않으므로 각 테이블 체크섬은 그대로 유효합니다. 파일 전체 체크섬(<code>head.checkSumAdjustment</code>)은 갱신하지 않았지만 아래 검증에서 문제는 없었습니다. 폰트를 바꾸면 공백의 글리프 번호가 달라질 수 있어서, 공백이 들어간 문자열로 테스트를 걸어 두었습니다.</p>
<pre><code>it('HarfBuzz 서브셋 폰트의 마지막 빈 글리프도 fontkit 이 읽을 수 있게 된다', async () =&gt; {
  const src = readFileSync(path.join(process.cwd(), 'assets/fonts/NanumMyeongjo-Regular.ttf'));
  const sub = await subsetFont(src, '통화 녹음 1분 ', { targetFormat: 'sfnt', dropTables: ['GSUB', 'GPOS', 'gasp'], keepFeatures: [] });
  const padded = padGlyfTable(new Uint8Array(sub));
  expect(padded.byteLength).toBeGreaterThan(sub.byteLength);
  const font = fontkit.create(padded as unknown as Buffer);
  const run = font.layout('통화 녹음 1분 ');
  expect(run.glyphs.length).toBe(9);
  for (const g of run.glyphs) expect(() =&gt; g.cbox).not.toThrow();
});</code></pre>
<h2>Next.js에서 돌리기: serverExternalPackages</h2>
<p>로컬 스크립트에서 돌던 코드가 Next.js 라우트 핸들러에서는 한 번 더 막힙니다. subset-font는 wasm을 <code>readFile(require.resolve('harfbuzzjs/hb-subset.wasm'))</code>로 읽는데, Next.js는 라우트 핸들러의 의존성을 기본적으로 번들에 묶고 16부터는 기본 번들러가 Turbopack입니다. 번들 안에서는 이 경로가 실제 wasm 파일로 제대로 풀리지 않았습니다. 해당 패키지를 번들에서 빼고 Node의 <code>require</code>로 직접 불러오게 하는 설정이 <a href="https://nextjs.org/docs/app/api-reference/config/next-config-js/serverExternalPackages" target="_blank" rel="noopener">serverExternalPackages</a>입니다. 또 배포 번들에는 파일 추적으로 찾은 파일만 들어가는데, 폰트는 런타임에 조립한 경로로 읽으므로 <a href="https://nextjs.org/docs/app/api-reference/config/next-config-js/output" target="_blank" rel="noopener">outputFileTracingIncludes</a>로 폰트와 wasm을 명시했습니다.</p>
<pre><code>// next.config.ts (발췌)
const nextConfig: NextConfig = {
  // HarfBuzz(subset-font)는 런타임에 require.resolve 로 wasm 을 찾으므로 번들하지 않고 Node 가 직접 로드하게 둔다
  serverExternalPackages: ['subset-font', 'harfbuzzjs', 'fontverter'],
  // PDF 생성 함수가 폰트 파일과 HarfBuzz wasm 을 배포 번들에 포함하도록 (Vercel 파일 추적)
  outputFileTracingIncludes: {
    '/api/transcripts/[id]/pdf': ['./assets/fonts/**', './node_modules/harfbuzzjs/hb-subset.wasm'],
  },
};
// app/api/transcripts/[id]/pdf/route.ts
export const runtime = 'nodejs';</code></pre>
<ul>
<li>Edge 런타임에서는 Node 파일 시스템 API를 쓸 수 없고 <code>outputFileTracingIncludes</code>도 적용되지 않으므로 Node 런타임으로 고정합니다.</li>
<li>폰트 모듈에 <code>import 'server-only'</code>를 두어, 1.9MB짜리 원본 폰트를 읽는 코드가 클라이언트 쪽에서 import되면 빌드가 실패하게 했습니다.</li>
<li>subset-font는 wasm을 프로세스당 한 번만 초기화하고 서브셋 호출을 한 번에 하나씩(<code>p-limit(1)</code>) 처리하므로, Regular와 Bold를 <code>Promise.all</code>로 묶어도 실제로는 차례로 돕니다.</li>
</ul>
<h2>검증</h2>
<p>같은 예시 문서로 세 방식을 비교했습니다. 손상 개수는 본문 폰트 기준입니다.</p>
<table>
<thead><tr><th>방식</th><th>PDF 크기</th><th>결과</th></tr></thead>
<tbody>
<tr><td>원본 폰트 통째 (<code>subset: false</code>)</td><td>1,432,236바이트</td><td>정상</td></tr>
<tr><td>pdf-lib 내장 서브셋 (<code>subset: true</code>)</td><td>21,751바이트</td><td>글리프 139개 중 62개 손상</td></tr>
<tr><td>HarfBuzz 서브셋 + glyf 패딩</td><td>24,392바이트</td><td>138자 모두 원본과 일치</td></tr>
</tbody>
</table>
<p>"일치"는 서브셋 폰트를 fontkit으로 다시 읽어 글자마다 외곽선과 글자 폭을 원본과 비교한 결과이고, macOS 렌더러로 뽑은 이미지와 앱에서 만든 2쪽짜리 PDF로 눈으로도 확인했습니다. 내장 서브셋보다 2.6KB 크지만 원본을 통째로 넣을 때의 약 59분의 1입니다.</p>
<h2>같은 문제를 피하는 체크리스트</h2>
<ul>
<li>pdf-lib과 <code>@pdf-lib/fontkit</code>으로 TrueType 폰트를 <code>subset: true</code>로 넣는다면 <code>fontkit.create(buf).head.indexToLocFormat</code>부터 봅니다. 1이면 이 버그의 조건을 갖춘 것입니다.</li>
<li>테스트 문서는 <strong>짧게</strong>, <strong>공백을 넣어서</strong> 만듭니다. 긴 문서는 첫 번째 버그를, 공백 없는 문자열은 두 번째 버그를 가립니다.</li>
<li>눈으로 판정하지 말고 넣은 폰트를 다시 파싱해 원본 글리프와 비교합니다. 서브셋 손상, 입력 누락, NFD가 구분됩니다.</li>
<li>pdf-lib에는 미리 서브셋한 폰트를 <code>subset: false</code>로 넣고, glyf 끝에 여백을 둡니다. 폰트를 바꾸면 테스트부터 다시 돌립니다.</li>
<li>Next.js에서는 <code>serverExternalPackages</code>, <code>outputFileTracingIncludes</code>, Node 런타임을 함께 챙깁니다.</li>
</ul>
<p>가장 큰 교훈은 포크에 관한 것입니다. 2019년에 상위에서 고쳐진 버그가 2020년에 배포된 포크에는 없었습니다. 패키지 이름에 상위 프로젝트 이름이 들어 있어도 상위의 수정까지 따라온다는 보장은 없고, 용량을 줄이는 옵션도 결과가 맞는지 검증해야 할 대상입니다.</p>
<div class="tip"><strong>녹취록AI</strong> — 통화 녹음을 올리면 화자 분리와 타임스탬프를 거쳐 법원 제출 서식의 녹취록으로 정리하고, PDF와 Word로 내보낼 수 있습니다. <a href="https://law-transcript.lightonpluslab.com" target="_blank" rel="noopener">웹에서 열기</a></div>
"""
},
]

FALLBACK_OGIMG = "https://lightonpluslab.com/hero-apps.jpg"
HOME_CARD_COUNT = 3

def _newest_first(articles):
    # Sort by date desc; for same-day posts the one declared later in ARTICLES wins,
    # so appending a new entry always puts it on top.
    return [a for _, a in sorted(enumerate(articles), key=lambda t: (t[1]["date"], t[0]), reverse=True)]

LIST_HEAD = HEAD.format(
    title="블로그", slug="blog",
    desc="LightOn Plus Lab 블로그 — 앱 개발 노트, 제품 가이드, 1인 스튜디오 운영기",
    ogimg=FALLBACK_OGIMG
)

def article_jsonld(a, ogimg):
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": a["title"],
        "description": a["desc"],
        "image": ogimg,
        "datePublished": a["date"],
        "dateModified": a["date"],
        "inLanguage": "ko",
        "mainEntityOfPage": f"https://lightonpluslab.com/{a['slug']}.html",
        "author": {"@type": "Organization", "name": "LightOn Plus Lab",
                   "url": "https://lightonpluslab.com/"},
        "publisher": {"@type": "Organization", "name": "LightOn Plus Lab",
                      "logo": {"@type": "ImageObject",
                               "url": "https://lightonpluslab.com/img/logo-mark.png"}},
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=1)
            + "\n</script>\n")

def article_html(a):
    ogimg = f"https://lightonpluslab.com/{a['img']}" if a.get("img") else FALLBACK_OGIMG
    head = HEAD.format(title=a["title"], slug=a["slug"], desc=a["desc"], ogimg=ogimg)
    head = head.replace("</head>", article_jsonld(a, ogimg) + "</head>", 1)
    fig = (f'<figure class="post-hero"><img src="{a["img"]}" alt="{a["img_alt"]}" '
           f'width="840" height="627" loading="lazy"></figure>\n') if a.get("img") else ""
    hero = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow reveal">{a["eyebrow"]}</span>
    <h1 class="reveal">{a["title"]}</h1>
    <div class="article-meta">{a["date"]} · LightOn Plus Lab</div>
  </div>
</section>
<section>
  <div class="wrap">
    <article class="prose">
{fig}{a["body"]}
    <a class="back-link" href="blog.html">← 블로그 목록으로</a>
    </article>
  </div>
</section>
"""
    return head + hero + FOOTER

def list_html():
    cards = "\n".join(
        f'''<a class="post-card" href="{a["slug"]}.html">
  <h2>{a["title"]}</h2>
  <p>{a["desc"]}</p>
  <div class="pc-meta">{a["eyebrow"]} · {a["date"]}</div>
</a>''' for a in _newest_first(ARTICLES))
    hero = f"""
<section class="page-hero">
  <div class="wrap">
    <span class="eyebrow reveal">Blog</span>
    <h1 class="reveal">만들며 배운 것을 <em>기록</em>합니다</h1>
    <p class="reveal">앱 개발 노트, 제품 사용 가이드, 1인 스튜디오 운영기. 직접 만들고 운영하며 검증된 내용만 씁니다.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="post-list">
{cards}
    </div>
  </div>
</section>
"""
    return LIST_HEAD + hero + FOOTER

def update_index_cards(path="index.html"):
    """index.html의 #writing 카드를 ARTICLES에서 다시 만든다.

    index.html은 손으로 쓰는 파일이라 마커 사이만 생성한다.
    마커가 없으면 조용히 넘어가지 않고 즉시 실패시킨다 — 조용히 건너뛰면
    홈 카드가 블로그와 다시 어긋나고, 그게 이 코드가 없애려는 버그다.
    """
    start = "<!-- writing:start"
    end = "<!-- writing:end -->"
    with io.open(path, encoding="utf-8") as f:
        html = f.read()
    if start not in html or end not in html:
        raise SystemExit(
            f"{path}: writing:start / writing:end 마커를 찾지 못했습니다. "
            "#writing 섹션의 카드 블록을 두 마커로 감싸주세요."
        )
    head, _, rest = html.partition(start)
    marker_line, _, rest = rest.partition("\n")
    _, _, tail = rest.partition(end)

    cards = []
    for i, a in enumerate(_newest_first(ARTICLES)[:HOME_CARD_COUNT]):
        cls = "post-card reveal" if i == 0 else f"post-card reveal reveal-d{i}"
        cards.append(
            f'      <a class="{cls}" href="{a["slug"]}.html">\n'
            f'        <h3>{a["title"]}</h3>\n'
            f'        <p>{a["desc"]}</p>\n'
            f'        <div class="pc-meta">{a["eyebrow"]} · {a["date"]}</div>\n'
            f'      </a>'
        )

    block = start + marker_line + "\n" + "\n".join(cards) + "\n      " + end
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(head + block + tail)
    print(path)

def stamp_asset_versions():
    """styles.css / app.js 링크에 내용 해시를 찍는다.

    빌드 단계가 없는 정적 사이트라 캐시 무효화 수단이 이것뿐이다. 날짜로 찍으면
    CSS를 고치고 스탬프를 안 올리는 순간 재방문자가 새 HTML에 옛 CSS를 물어
    페이지가 깨진다. 해시는 파일이 바뀔 때만 달라지므로 어긋날 수가 없다.
    """
    import hashlib, glob, re as _re

    ver = {}
    for asset in ("styles.css", "app.js"):
        with io.open(asset, "rb") as f:
            ver[asset] = hashlib.sha1(f.read()).hexdigest()[:8]

    touched = 0
    targets = sorted(glob.glob("*.html"))
    for d in ("en", "ja", "zh"):
        targets += sorted(glob.glob(d + "/*.html"))
    for path in targets:
        with io.open(path, encoding="utf-8") as f:
            src = f.read()
        out = src
        for asset, h in ver.items():
            attr = "href" if asset.endswith(".css") else "src"
            out = _re.sub(
                r'%s="%s(\?v=[^"]*)?"' % (attr, _re.escape(asset)),
                '%s="%s?v=%s"' % (attr, asset, h),
                out,
            )
        if out != src:
            with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(out)
            touched += 1
    print("asset stamp %s (%d files)" % (ver, touched))


with io.open("blog.html", "w", encoding="utf-8") as f:
    f.write(list_html())
print("blog.html")
update_index_cards("_src/index.html")
for a in ARTICLES:
    with io.open(a["slug"] + ".html", "w", encoding="utf-8") as f:
        f.write(article_html(a))
    print(a["slug"] + ".html")

# sitemap
PAGE_LASTMOD = {
    "": "2026-10-16",
    "about.html": "2026-08-13",
    "services.html": "2026-08-13",
    "products.html": "2026-08-13",
    "korean-pronunciation-rules.html": "2026-11-07",
    "lens.html": "2026-10-22",
    "lens-docs.html": "2026-10-30",
    "momoi.html": "2026-08-13",
    "lighton-ai-note.html": "2026-08-13",
    "blog.html": "2026-08-13",
    "contact.html": "2026-07-05",
    "privacy.html": "2026-08-08",
    "privacy-en.html": "2026-08-08",
    "terms.html": "2026-07-05",
    "games/core-siege/": "2026-08-15",
    "games/hole/": "2026-08-15",
    "privacy-stone-arena.html": "2026-09-04",
}
LEGAL_PAGES = {"privacy.html", "privacy-en.html", "terms.html",
               "privacy-stone-arena.html"}

# 아직 공개하지 않을 페이지. **여기에만 적으면 된다** —
# sitemap 제외·noindex 삽입·링크 검사가 자동으로 따라온다.
#
# 왜 필요한가: "Beta"/"Soon" 배지는 공개를 막지 못한다. 2026-10-16에 아래 세
# 페이지가 배지를 단 채 7월부터 sitemap에 올라가 구글에 색인되고 있었고, 앱
# 목록에서 누구나 눌러 들어갈 수 있었다. 배지는 안내지 접근 제어가 아니다.
UNPUBLISHED = {
    "focusguard.html": "미완성",
    "teams-translator.html": "미완성",
    "vibe-studio.html": "미완성",
    # 페이지는 남긴다 — Play 등록정보가 접근 가능한 방침 URL을 요구한다.
    "score-studio-privacy.html": "SCORE STUDIO 미출시",
    # Chrome 웹 스토어 등록 양식이 방침·판매 조건 URL을 요구한다. 판매 시작 시 PAGE_LASTMOD로 옮긴다.
    "sidekey-privacy.html": "Sidekey 크롬판 미출시",
    "sidekey-terms.html": "Sidekey 크롬판 미출시",
}

NOINDEX = '<meta name="robots" content="noindex, nofollow" />'


def enforce_unpublished():
    """미공개 페이지에 noindex 를 보장하고, 어디서도 링크되지 않는지 확인한다.

    sitemap 에서 빼는 것만으로는 부족하다. 목록에 링크가 살아 있으면 방문자는
    그대로 들어가고, 구글도 링크를 타고 들어온다. 그래서 링크가 하나라도 남아
    있으면 빌드를 세운다 — 조용히 넘어가면 또 같은 일이 난다.
    """
    import glob, os, re as _re

    if "" in UNPUBLISHED:
        raise SystemExit("미공개: 홈은 내릴 수 없다")

    added = []
    for page in sorted(UNPUBLISHED):
        if not os.path.exists(page):
            raise SystemExit("미공개: %s 가 없다 (목록에서 빼거나 파일을 되살릴 것)" % page)
        with io.open(page, encoding="utf-8") as f:
            body = f.read()
        tag = _re.search(r'<meta name="robots"[^>]*>', body)
        if tag:
            if "noindex" not in tag.group(0):
                raise SystemExit("미공개: %s 의 robots 메타에 noindex 가 없다 — %s"
                                 % (page, tag.group(0)))
            continue
        vp = _re.search(r'<meta name="viewport"[^>]*>', body)
        if not vp:
            raise SystemExit("미공개: %s 에 viewport 메타가 없어 noindex 를 넣을 자리가 없다" % page)
        body = body.replace(vp.group(0), vp.group(0) + "\n" + NOINDEX, 1)
        with io.open(page, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        added.append(page)

    linked = []
    for path in sorted(glob.glob("*.html")) + sorted(glob.glob("_src/*.html")):
        if path in UNPUBLISHED:
            continue
        with io.open(path, encoding="utf-8") as f:
            body = f.read()
        for page in UNPUBLISHED:
            if 'href="%s"' % page in body:
                linked.append("%s → %s" % (path, page))
    if linked:
        raise SystemExit("미공개 페이지로 가는 링크가 남아 있다:\n  " + "\n  ".join(linked))

    print("미공개 %d개 확인%s" % (len(UNPUBLISHED),
                                 (" (noindex 추가: " + ", ".join(added) + ")") if added else ""))
LASTMOD_STATE = "_lastmod.json"


def resolve_lastmod(seed):
    """내용이 실제로 바뀐 날을 lastmod 로 쓴다.

    손으로 적은 표는 썩는다(홈을 고치고도 두 달 전 날짜가 남아 있었다). 그렇다고
    git 커밋일을 쓰면 애셋 스탬프만 바뀐 날에도 26개 전부가 "오늘 바뀜"이 되어
    lastmod 를 믿을 수 없게 만든다. 그래서 스탬프를 지운 내용의 해시를 기록해
    두고, 해시가 달라진 페이지만 날짜를 올린다. seed 는 상태 파일이 없을 때의
    최초 기준값이다.
    """
    import hashlib, os, re as _re

    try:
        with io.open(LASTMOD_STATE, encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, ValueError):
        state = {}

    today = datetime.date.today().isoformat()
    out = {}
    for page, fallback in seed:
        path = "index.html" if page == "" else page
        if page.endswith("/"):          # 게임은 폴더 — 날짜를 그대로 둔다
            out[page] = state.get(page, {}).get("date", fallback)
            state[page] = {"hash": "", "date": out[page]}
            continue
        if not os.path.exists(path):
            raise SystemExit("sitemap: %s 가 없다" % path)
        with io.open(path, encoding="utf-8") as f:
            body = _re.sub(r"\?v=[0-9a-f]+", "", f.read())
        digest = hashlib.sha1(body.encode("utf-8")).hexdigest()
        prev = state.get(page)
        if prev is None:
            out[page] = fallback          # 최초 1회 — 알고 있는 날짜를 심는다
        elif prev.get("hash") == digest:
            out[page] = prev["date"]
        else:
            out[page] = today
        state[page] = {"hash": digest, "date": out[page]}

    for gone in [k for k in state if k in UNPUBLISHED]:
        state.pop(gone)          # 내린 페이지는 상태도 들고 있지 않는다
    with io.open(LASTMOD_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    return out


def write_sitemap():
    seed = [(p, d) for p, d in list(PAGE_LASTMOD.items())
            + [(a["slug"] + ".html", a["date"]) for a in ARTICLES]
            if p not in UNPUBLISHED]
    dates = resolve_lastmod(seed)
    moved = [p for p, _ in seed if dates[p] == datetime.date.today().isoformat()]
    from i18n_home import LANG_META
    from build_i18n import PAGES as I18N_PAGES, ORDER as I18N_ORDER, DEFAULT as I18N_DEFAULT

    def url_of(page, code):
        d = LANG_META[code]["dir"]
        return "https://lightonpluslab.com/" + (d if page == "index.html" else d + page)

    def alts_of(page):
        rows = ['    <xhtml:link rel="alternate" hreflang="%s" href="%s" />'
                % (LANG_META[c]["hreflang"], url_of(page, c)) for c in I18N_ORDER]
        rows.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s" />'
                    % url_of(page, I18N_DEFAULT))
        return "\n".join(rows)

    # sitemap 의 빈 경로("")는 index.html 을 뜻한다
    def as_page(p):
        return "index.html" if p == "" else p

    rows = []
    for p, _ in seed:
        extra = "\n" + alts_of(as_page(p)) if as_page(p) in I18N_PAGES else ""
        rows.append(f"""  <url>
    <loc>https://lightonpluslab.com/{p}</loc>{extra}
    <lastmod>{dates[p]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if p == '' else '0.3' if p in LEGAL_PAGES else '0.7'}</priority>
  </url>""")
    trans = 0
    for page in I18N_PAGES:
        root_key = "" if page == "index.html" else page
        for c in I18N_ORDER:
            if c == I18N_DEFAULT:
                continue            # 기본 언어는 위의 seed 에 이미 들어 있다
            trans += 1
            rows.append(f"""  <url>
    <loc>{url_of(page, c)}</loc>
{alts_of(page)}
    <lastmod>{dates[root_key]}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'0.9' if page == 'index.html' else '0.6'}</priority>
  </url>""")
    urls = "\n".join(rows)
    with io.open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{urls}
</urlset>
""")
    print("sitemap.xml (%d URL · 번역판 %d, 오늘 갱신 %d개%s)"
          % (len(seed) + trans, trans, len(moved),
             (": " + ", ".join(p or "/" for p in moved)) if moved else ""))

# RSS feed
def _xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _rfc822(d):
    return datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 09:00:00 +0900")

rss_items = "\n".join(
    f"""  <item>
    <title>{_xml_escape(a["title"])}</title>
    <link>https://lightonpluslab.com/{a["slug"]}.html</link>
    <guid isPermaLink="true">https://lightonpluslab.com/{a["slug"]}.html</guid>
    <pubDate>{_rfc822(a["date"])}</pubDate>
    <description>{_xml_escape(a["desc"])}</description>
  </item>""" for a in _newest_first(ARTICLES))
with io.open("feed.xml", "w", encoding="utf-8") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>LightOn Plus Lab Blog</title>
  <link>https://lightonpluslab.com/blog.html</link>
  <atom:link href="https://lightonpluslab.com/feed.xml" rel="self" type="application/rss+xml" />
  <description>앱 개발 노트, 제품 가이드, 1인 스튜디오 운영기</description>
  <language>ko</language>
{rss_items}
</channel>
</rss>
""")
print("feed.xml")

enforce_unpublished()
import build_i18n; build_i18n.build()
stamp_asset_versions()
write_sitemap()
