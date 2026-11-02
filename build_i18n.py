# -*- coding: utf-8 -*-
"""_src/ 의 한국어 원본에서 4개 언어판을 찍어낸다.

한국어가 기본이다 — 한국어판이 루트(/)로 나가고 /en/ /ja/ /zh/ 가 따라붙는다.
루트 URL 은 건드리지 않는다. 구글이 이미 루트를 한국어로 색인해 뒀고,
AdSense 재심사가 걸려 있는 동안 기본 언어를 옮기면 심사 중에 사이트가
흔들린다. 원본을 _src/ 에 둔 이유: 루트도 생성물이라 원본과 겹칠 수 없고,
생성물을 다시 원본으로 읽으면(제자리 수정) 두 번째 빌드에서 하위 폴더로
바뀐 링크가 루트판에 섞여 들어간다. `_` 폴더는 Jekyll 이 서빙하지 않는다
(/_design/ 404).

치환은 **텍스트 노드 전체 일치**로만 한다. 부분 문자열로 바꾸면 '개'가
'개인정보처리방침' 안에서도 바뀌고, '무료'가 '무료 크레딧' 안에서도 바뀐다.
끝에 번역본에 한글이 남아 있으면 빌드를 세운다 — 조용히 반쪽짜리 페이지가
나가는 것보다 낫다.

언어 자동 전환 스크립트는 두지 않는다. 2026-10-30 에 걷어낸 그 스크립트는
크롤러(mediapartners·adsbot)만 예외로 빼고 사람만 다른 언어로 보내서, 구글이
클로킹으로 읽는 모양이었다. 언어는 방문자가 스위처로 고른다.
"""
import io, os, re

from i18n_home import T as T_HOME, LD, BLOCKS as B_HOME, LANGS, LANG_META
from i18n_pages import T2, BLOCKS2
from i18n_more import T3, BLOCKS3
from i18n_lens import T4, BLOCKS4

SITE = "https://lightonpluslab.com"
SRC = "_src"
IDX = {"en": 0, "ja": 1, "zh": 2}

# 기본 언어 — 루트로 나간다. x-default 도 이쪽을 가리킨다.
DEFAULT = "ko"
# 스위처에 찍히는 순서. 기본 언어가 먼저.
ORDER = ["ko", "en", "ja", "zh"]

# 번역하는 페이지. 여기 있는 페이지끼리는 링크도 같은 언어판으로 이어 준다.
PAGES = ["index.html", "products.html", "lens.html", "about.html", "services.html", "contact.html"]

# 번역본이 없어 모든 언어판이 공유하는 한국어 페이지. 링크에 hreflang 을 달아
# 목적지가 한국어라고 밝힌다(앵커 글자는 그 언어판 글자이므로 lang 은 달지 않는다).
KO_ONLY = ["blog.html", "momoi.html", "lighton-ai-note.html", "lens-docs.html",
           "privacy.html", "terms.html"]

T = dict(T_HOME)
T.update(T2)
T.update(T3)
T.update(T4)
BLOCKS = dict(B_HOME)
BLOCKS.update(BLOCKS2)
BLOCKS.update(BLOCKS3)
BLOCKS.update(BLOCKS4)

# 번역본에 남아도 되는 한글 — 언어 이름은 제 글자로 적는 게 맞다
HANGUL_OK = ["한국어"]

TAG_RE = re.compile(r"(<[^>]+>)")
ATTR_RE = re.compile(r'\b(alt|aria-label|content|title|placeholder)="([^"]*)"')
REL_RE = re.compile(r'\b(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:)([^"]+)"')


def _page_url(page, lang):
    d = LANG_META[lang]["dir"]
    return "/" + d if page == "index.html" else "/" + d + page


def _translate_attrs(tag, i):
    def sub(m):
        key, val = m.group(1), m.group(2)
        if val.strip() in T:
            return '%s="%s"' % (key, T[val.strip()][i])
        return m.group(0)
    return ATTR_RE.sub(sub, tag)


def _translate_text(html, i):
    parts = TAG_RE.split(html)
    skip = False
    for n, part in enumerate(parts):
        if n % 2:
            low = part.lower()
            if low.startswith("<script"):
                skip = True
            elif low.startswith("<style"):
                skip = True
            elif low.startswith("</script") or low.startswith("</style"):
                skip = False
            parts[n] = _translate_attrs(part, i)
        else:
            if skip:
                continue
            s = part.strip()
            if s and s in T:
                parts[n] = part.replace(s, T[s][i])
    return "".join(parts)


def _translate_ld(html, i):
    """JSON-LD 안의 한글. 긴 문자열부터 바꿔야 짧은 게 긴 걸 깨지 않는다."""
    def one(m):
        body = m.group(1)
        for ko in sorted(LD, key=len, reverse=True):
            body = body.replace(ko, LD[ko][i])
        for ko in sorted(T, key=len, reverse=True):
            if re.search(r"[가-힣]", ko):
                body = body.replace('"%s"' % ko, '"%s"' % T[ko][i])
        return '<script type="application/ld+json">%s</script>' % body
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', one, html, flags=re.S)


def _switcher(page, cur, mobile=False):
    cls = "langsw langsw-m" if mobile else "langsw"
    out = ['<div class="%s" role="group" aria-label="Language">' % cls]
    for code in ORDER:
        m = LANG_META[code]
        a = ' aria-current="true"' if code == cur else ""
        label = m["label"] if mobile else m["short"]
        out.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>'
                   % (_page_url(page, code), m["hreflang"], m["html"], a, label))
    out.append("</div>")
    return "".join(out)


def _alternates(page):
    out = []
    for code in ORDER:
        out.append('<link rel="alternate" hreflang="%s" href="%s%s" />'
                   % (LANG_META[code]["hreflang"], SITE, _page_url(page, code)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s" />'
               % (SITE, _page_url(page, DEFAULT)))
    return "\n".join(out)


def _check(html, lang, page):
    # style/script 안의 한글은 설계 주석이라 화면에 안 나온다.
    stripped = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
    for ok in HANGUL_OK:
        stripped = stripped.replace(ok, "")
    left = [s.strip() for s in re.findall(r"[^<>]*[가-힣][^<>]*", stripped) if s.strip()]
    if left:
        raise SystemExit("i18n(%s/%s): 한글이 %d곳 남았다\n  %s"
                         % (lang, page, len(left), "\n  ".join(left[:8])))


def _mark_ko_links(html):
    """번역본에서 한국어 전용 페이지로 가는 링크에 hreflang="ko" 를 단다.

    기본 언어판은 링크를 절대경로로 바꾸지 않으므로 `href="blog.html"` 처럼
    상대형으로 남는다. 두 형태를 다 잡아야 영어판에서도 표시가 붙는다.
    """
    for p in KO_ONLY:
        html = re.sub(r'href="(/?%s)"(?![^>]*hreflang)' % re.escape(p),
                      r'href="\1" hreflang="ko"', html)
    return html


def _inject_shell(html, page, lang):
    m = LANG_META[lang]
    url = SITE + _page_url(page, lang)

    html = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % m["html"], html, count=1)
    html = re.sub(r'\n?<script id="lpl-lang">.*?</script>', "", html, flags=re.S)
    html = re.sub(r'<link rel="canonical" href="[^"]*" />',
                  '<link rel="canonical" href="%s" />' % url, html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*" />',
                  '<meta property="og:url" content="%s" />' % url, html, count=1)
    html = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*" />', "", html)
    html = html.replace('<link rel="canonical"', _alternates(page) + '\n<link rel="canonical"', 1)

    # 하위 폴더로 나가는 언어판만 링크를 절대경로로 바꾼다. 기본 언어는 루트에
    # 그대로 놓이므로 원본의 상대 링크가 이미 맞다.
    if m["dir"]:
        html = REL_RE.sub(lambda mm: '%s="/%s"' % (mm.group(1), mm.group(2)), html)
        # 번역이 있는 페이지끼리는 같은 언어판으로 잇는다
        for p in PAGES:
            tgt = "/" + m["dir"] if p == "index.html" else "/" + m["dir"] + p
            html = html.replace('href="/%s"' % p, 'href="%s"' % tgt)
            html = html.replace('href="/%s#' % p, 'href="%s#' % tgt)
    if lang != "ko":
        html = _mark_ko_links(html)
        # Lens 앱과 그 가이드는 같은 네 언어를 갖고 있다(en·ja·zh 전부 200 확인).
        # 번역본에서 /ko 로 보내면 읽는 사람이 모르는 글자를 만난다.
        html = html.replace("lens.lightonpluslab.com/guide/ko/",
                            "lens.lightonpluslab.com/guide/%s/" % lang)
        html = html.replace('lens.lightonpluslab.com/ko"',
                            'lens.lightonpluslab.com/%s"' % lang)

    # 들여쓰기까지 같이 걷어내야 돌릴 때마다 공백 줄이 쌓이지 않는다
    html = re.sub(r'[ \t]*<div class="langsw[^"]*"[^>]*>.*?</div>\n?', "", html, flags=re.S)
    cta = '<a class="nav-cta" href='
    i = html.index(cta)
    j = html.rfind("\n", 0, i) + 1      # nav-cta 가 있는 줄의 시작
    indent = html[j:i]
    html = html[:j] + indent + _switcher(page, lang) + "\n" + html[j:]

    drawer = re.search(r'<a href="[^"]*contact\.html" style="color:var\(--purple\)', html)
    if drawer:
        html = html[:drawer.start()] + _switcher(page, lang, mobile=True) + "\n" + html[drawer.start():]
    return html


def build():
    made = []
    for page in PAGES:
        src = io.open(os.path.join(SRC, page), encoding="utf-8").read()

        for lang in ORDER:
            if lang == "ko":
                out = src                      # 원본이 한국어판이다
            else:
                i = IDX[lang]
                out = src
                for koText, tr in BLOCKS.items():
                    if koText in out:
                        out = out.replace(koText, tr[lang])
                out = _translate_ld(out, i)
                out = _translate_text(out, i)
            out = _inject_shell(out, page, lang)
            out = re.sub(r"\n?<!--(?!\[if).*?-->", "", out, flags=re.S)
            if lang != "ko":
                _check(out, lang, page)

            d = LANG_META[lang]["dir"].rstrip("/")
            if d and not os.path.isdir(d):
                os.makedirs(d)
            io.open(os.path.join(d, page) if d else page,
                    "w", encoding="utf-8", newline="").write(out)
        made.append(page)
    print("i18n  %d페이지 × %d언어 — 기본 %s(/), 나머지 %s (%s)"
          % (len(made), len(ORDER), DEFAULT,
             ", ".join("/" + LANG_META[c]["dir"] for c in ORDER if c != DEFAULT),
             ", ".join(made)))
