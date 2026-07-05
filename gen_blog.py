# -*- coding: utf-8 -*-
# Generate blog pages (list + articles) reusing the site shell.
import io, datetime, json

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title} — LightOn Plus Lab</title>
<meta name="description" content="{desc}" />
<meta property="og:title" content="{title} — LightOn Plus Lab" />
<meta property="og:type" content="article" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="https://lightonpluslab.com/{slug}.html" />
<meta property="og:image" content="{ogimg}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#050814" />
<link rel="icon" href="logo-new.png" />
<link rel="canonical" href="https://lightonpluslab.com/{slug}.html" />
<link rel="alternate" type="application/rss+xml" title="LightOn Plus Lab Blog" href="https://lightonpluslab.com/feed.xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="styles.css" />
<script async src="https://www.googletagmanager.com/gtag/js?id=G-D9LHH5465Q"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-D9LHH5465Q');</script>
<style>
.page-hero{{padding:72px 0 24px;text-align:center}}
.page-hero .eyebrow{{margin-bottom:20px}}
.page-hero h1{{font-size:clamp(30px,4.2vw,52px);font-weight:700;letter-spacing:-.03em;line-height:1.12;margin-bottom:16px}}
.page-hero h1 em{{font-style:normal;background:linear-gradient(135deg,var(--cyan),var(--mint));-webkit-background-clip:text;background-clip:text;color:transparent}}
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
<canvas id="starfield" aria-hidden="true"></canvas>
<div class="page-glow" aria-hidden="true"></div>

<header class="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="index.html">
      <img class="brand-img" src="logo-new.png" alt="LightOn Plus Lab" width="36" height="36" />
            <span class="brand-text"><span class="brand-name">LightOn<span class="plus">+</span>Lab</span><span class="brand-sub">AI Apps · Innovation</span></span>
    </a>
    <nav class="nav-links" aria-label="메뉴">
      <a href="services.html">Services</a>
      <a href="products.html">Work</a>
      <a href="blog.html">Blog</a>
      <a href="momoi.html">Momoi</a>
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
<nav class="mobile-menu" id="mobileMenu">
  <a href="services.html">Services</a>
  <a href="products.html">Work</a>
  <a href="blog.html">Blog</a>
  <a href="momoi.html">Momoi</a>
  <a href="about.html">Studio</a>
  <a href="contact.html">Contact</a>
  <a href="contact.html" style="color:var(--purple);font-weight:600">Launch Lab →</a>
</nav>

<main>
"""

FOOTER = """
</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-brand">
          <a class="brand" href="index.html">
            <img class="brand-img" src="logo-new.png" alt="LightOn Plus Lab" width="36" height="36" />
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
        <a href="momoi.html">Momoi</a>
      </div>
      <div class="footer-col">
        <h5>Work</h5>
        <a href="products.html">Products</a>
        <a href="contact.html">New project</a>
      </div>
      <div class="footer-col">
        <h5>Reach out</h5>
        <a href="mailto:support@lightonpluslab.com">support@lightonpluslab.com</a>
        <a href="https://open.kakao.com/o/lightonpluslab" target="_blank" rel="noopener">KakaoTalk</a>
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

<script src="app.js"></script>
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
]

FALLBACK_OGIMG = "https://lightonpluslab.com/hero-apps.jpg"

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
                               "url": "https://lightonpluslab.com/logo-new.png"}},
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
</a>''' for a in ARTICLES)
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

with io.open("blog.html", "w", encoding="utf-8") as f:
    f.write(list_html())
print("blog.html")
for a in ARTICLES:
    with io.open(a["slug"] + ".html", "w", encoding="utf-8") as f:
        f.write(article_html(a))
    print(a["slug"] + ".html")

# sitemap
pages = ["", "about.html", "services.html", "products.html", "momoi.html",
         "teams-translator.html", "focusguard.html", "vibe-studio.html", "contact.html",
         "privacy.html", "terms.html", "blog.html"] + [a["slug"] + ".html" for a in ARTICLES]
today = "2026-07-05"
urls = "\n".join(
    f"""  <url>
    <loc>https://lightonpluslab.com/{p}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if p == '' else '0.7'}</priority>
  </url>""" for p in pages)
with io.open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
print("sitemap.xml")

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
  </item>""" for a in sorted(ARTICLES, key=lambda a: a["date"], reverse=True))
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

# ads.txt (apex — AdSense site is registered on lightonpluslab.com)
with io.open("ads.txt", "w", encoding="utf-8") as f:
    f.write("google.com, pub-7180935400084577, DIRECT, f08c47fec0942fa0\n")
print("ads.txt")
