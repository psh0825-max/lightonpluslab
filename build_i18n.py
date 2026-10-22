# -*- coding: utf-8 -*-
"""index.html 을 /en/ /ja/ /zh/ 로 찍어낸다.

치환은 **텍스트 노드 전체 일치**로만 한다. 부분 문자열로 바꾸면 '개'가
'개인정보처리방침' 안에서도 바뀌고, '앱'이 '앱스토어' 안에서도 바뀐다.
끝에 번역본에 한글이 남아 있으면 빌드를 세운다 — 조용히 반쪽짜리 페이지가
나가는 것보다 낫다.
"""
import io, os, re

from i18n_home import T, LD, BLOCKS, LANGS, LANG_META

SITE = "https://lightonpluslab.com"
IDX = {"en": 0, "ja": 1, "zh": 2}

# 번역본에 남아도 되는 한글 — 언어 이름은 제 글자로 적는 게 맞다
HANGUL_OK = ["한국어"]

TAG_RE = re.compile(r"(<[^>]+>)")
ATTR_RE = re.compile(r'\b(alt|aria-label|content|title|placeholder)="([^"]*)"')
# 상대 경로 → 절대 경로. /en/ 아래에서도 같은 자산을 가리켜야 한다.
REL_RE = re.compile(r'\b(href|src)="(?!https?:|//|/|#|mailto:|tel:|data:)([^"]+)"')


def _translate_attrs(tag, i):
    def sub(m):
        key, val = m.group(1), m.group(2)
        if val.strip() in T:
            return '%s="%s"' % (key, T[val.strip()][i])
        return m.group(0)
    return ATTR_RE.sub(sub, tag)


def _translate_text(html, i):
    """태그 밖 텍스트만, 그것도 통째로 일치할 때만 바꾼다."""
    parts = TAG_RE.split(html)
    skip = False
    for n, part in enumerate(parts):
        if n % 2:  # 태그
            low = part.lower()
            if low.startswith("<script") or low.startswith("<style"):
                skip = True
            elif low.startswith("</script") or low.startswith("</style"):
                skip = False
            parts[n] = _translate_attrs(part, i)
        else:      # 텍스트 노드
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
        return '<script type="application/ld+json">%s</script>' % body
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', one, html, flags=re.S)


def _switcher(cur, mobile=False):
    cls = "langsw langsw-m" if mobile else "langsw"
    out = ['<div class="%s" role="group" aria-label="Language">' % cls]
    for code in ["ko"] + LANGS:
        m = LANG_META[code]
        href = "/" + m["dir"]
        a = ' aria-current="true"' if code == cur else ""
        label = m["label"] if mobile else m["short"]
        out.append('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (href, m["hreflang"], m["html"], a, label))
    out.append("</div>")
    return "".join(out)


def _alternates(path_suffix=""):
    out = []
    for code in ["ko"] + LANGS:
        m = LANG_META[code]
        out.append('<link rel="alternate" hreflang="%s" href="%s/%s%s" />'
                   % (m["hreflang"], SITE, m["dir"], path_suffix))
    out.append('<link rel="alternate" hreflang="x-default" href="%s/%s" />' % (SITE, path_suffix))
    return "\n".join(out)


def _check(html, lang):
    # style/script 안의 한글은 설계 주석이라 화면에 안 나온다. 검사 대상은
    # 사용자가 읽는 텍스트와 속성값뿐이다.
    stripped = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
    for ok in HANGUL_OK:
        stripped = stripped.replace(ok, "")
    left = re.findall(r"[^<>]*[가-힣][^<>]*", stripped)
    left = [s.strip() for s in left if s.strip()]
    if left:
        raise SystemExit("i18n(%s): 한글이 %d곳 남았다\n  %s"
                         % (lang, len(left), "\n  ".join(left[:8])))


def build():
    src = io.open("index.html", encoding="utf-8").read()

    # 한국어 원본에도 스위처와 hreflang 을 넣는다 — 한국어 방문자도 바꿀 수 있어야 한다
    ko = _inject_shell(src, "ko")
    io.open("index.html", "w", encoding="utf-8", newline="").write(ko)

    made = []
    for lang in LANGS:
        i = IDX[lang]
        out = src
        for koText, tr in BLOCKS.items():
            if koText not in out:
                raise SystemExit("i18n: BLOCKS 원문을 찾지 못했다 — %s" % koText[:50])
            out = out.replace(koText, tr[lang])
        out = _translate_ld(out, i)
        out = _translate_text(out, i)
        out = _inject_shell(out, lang)
        # 빌드용 한글 주석은 번역본에 남길 이유가 없다
        out = re.sub(r"\n?<!--(?!\[if).*?-->", "", out, flags=re.S)
        _check(out, lang)

        d = LANG_META[lang]["dir"].rstrip("/")
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="").write(out)
        made.append("%s/ %dKB" % (lang, len(out) // 1024))
    print("i18n  " + " · ".join(made))


def _inject_shell(html, lang):
    """lang 속성·canonical·hreflang·절대경로·언어 스위처."""
    m = LANG_META[lang]

    html = re.sub(r'<html lang="[^"]*"', '<html lang="%s"' % m["html"], html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*" />',
                  '<link rel="canonical" href="%s/%s" />' % (SITE, m["dir"]), html, count=1)
    html = re.sub(r'<meta property="og:url" content="[^"]*" />',
                  '<meta property="og:url" content="%s/%s" />' % (SITE, m["dir"]), html, count=1)
    # 이전 실행이 남긴 alternate 를 걷어내고 새로 넣는다
    html = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*" />', "", html)
    html = html.replace('<link rel="canonical"', _alternates() + '\n<link rel="canonical"', 1)

    if lang != "ko":
        html = REL_RE.sub(lambda mm: '%s="/%s"' % (mm.group(1), mm.group(2)), html)
        html = html.replace('href="/index.html#lens"', 'href="#lens"')

    # 스위처 — 데스크톱 헤더와 모바일 서랍 양쪽에.
    # 들여쓰기까지 같이 걷어내야 한다. 남기면 돌릴 때마다 공백 줄이 한 줄씩 쌓인다.
    html = re.sub(r'[ \t]*<div class="langsw[^"]*"[^>]*>.*?</div>\n?', "", html, flags=re.S)
    html = html.replace('    <a class="nav-cta"', "    " + _switcher(lang) + '\n    <a class="nav-cta"', 1)
    html = html.replace('<a href="/contact.html" style="color:var(--purple)' if lang != "ko"
                        else '<a href="contact.html" style="color:var(--purple)',
                        _switcher(lang, mobile=True) + "\n" +
                        ('<a href="/contact.html" style="color:var(--purple)' if lang != "ko"
                         else '<a href="contact.html" style="color:var(--purple)'), 1)
    return html
