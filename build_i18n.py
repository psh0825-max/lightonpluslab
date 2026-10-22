# -*- coding: utf-8 -*-
"""한국어 페이지에서 /en/ /ja/ /zh/ 를 찍어낸다.

치환은 **텍스트 노드 전체 일치**로만 한다. 부분 문자열로 바꾸면 '개'가
'개인정보처리방침' 안에서도 바뀌고, '무료'가 '무료 크레딧' 안에서도 바뀐다.
끝에 번역본에 한글이 남아 있으면 빌드를 세운다 — 조용히 반쪽짜리 페이지가
나가는 것보다 낫다.
"""
import io, os, re

from i18n_home import T as T_HOME, LD, BLOCKS as B_HOME, LANGS, LANG_META
from i18n_pages import T2, BLOCKS2

SITE = "https://lightonpluslab.com"
IDX = {"en": 0, "ja": 1, "zh": 2}

# 번역하는 페이지. 여기 있는 페이지끼리는 링크도 같은 언어판으로 이어 준다.
PAGES = ["index.html", "products.html", "lens.html"]

T = dict(T_HOME)
T.update(T2)
BLOCKS = dict(B_HOME)
BLOCKS.update(BLOCKS2)

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
    for code in ["ko"] + LANGS:
        m = LANG_META[code]
        a = ' aria-current="true"' if code == cur else ""
        label = m["label"] if mobile else m["short"]
        out.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>'
                   % (_page_url(page, code), m["hreflang"], m["html"], a, label))
    out.append("</div>")
    return "".join(out)


def _alternates(page):
    out = []
    for code in ["ko"] + LANGS:
        out.append('<link rel="alternate" hreflang="%s" href="%s%s" />'
                   % (LANG_META[code]["hreflang"], SITE, _page_url(page, code)))
    out.append('<link rel="alternate" hreflang="x-default" href="%s%s" />'
               % (SITE, _page_url(page, "ko")))
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


def _inject_shell(html, page, lang):
    m = LANG_META[lang]
    url = SITE + _page_url(page, lang)

    html = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % m["html"], html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*" />',
                  '<link rel="canonical" href="%s" />' % url, html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*" />',
                  '<meta property="og:url" content="%s" />' % url, html, count=1)
    html = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*" />', "", html)
    html = html.replace('<link rel="canonical"', _alternates(page) + '\n<link rel="canonical"', 1)

    if lang != "ko":
        html = REL_RE.sub(lambda mm: '%s="/%s"' % (mm.group(1), mm.group(2)), html)
        # 번역이 있는 페이지끼리는 같은 언어판으로 잇는다
        for p in PAGES:
            tgt = "/" + m["dir"] if p == "index.html" else "/" + m["dir"] + p
            html = html.replace('href="/%s"' % p, 'href="%s"' % tgt)
            html = html.replace('href="/%s#' % p, 'href="%s#' % tgt)

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
        src = io.open(page, encoding="utf-8").read()
        io.open(page, "w", encoding="utf-8", newline="").write(_inject_shell(src, page, "ko"))

        for lang in LANGS:
            i = IDX[lang]
            out = src
            for koText, tr in BLOCKS.items():
                if koText in out:
                    out = out.replace(koText, tr[lang])
            out = _translate_ld(out, i)
            out = _translate_text(out, i)
            out = _inject_shell(out, page, lang)
            out = re.sub(r"\n?<!--(?!\[if).*?-->", "", out, flags=re.S)
            _check(out, lang, page)

            d = LANG_META[lang]["dir"].rstrip("/")
            if not os.path.isdir(d):
                os.makedirs(d)
            io.open(os.path.join(d, page), "w", encoding="utf-8", newline="").write(out)
        made.append(page)
    print("i18n  %d페이지 × %d언어 (%s)" % (len(made), len(LANGS), ", ".join(made)))
