#!/usr/bin/env python3
import os, re, glob

# ──────────────────────────────────────────────
# 1. CSS replacements
# ──────────────────────────────────────────────

# Old hamburger CSS (single-line variant used in sub-pages)
OLD_HAMBURGER_CSS_ONELINE = (
    '    .nav-hamburger { display: none; flex-direction: column; gap: 5px; cursor: pointer; '
    'padding: 8px; background: none; border: none; margin-left: 12px; }\n'
    '    .nav-hamburger span { width: 22px; height: 2px; background: var(--black); border-radius: 2px; transition: 0.3s; display: block; }\n'
    '    .nav-hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); } '
    '.nav-hamburger.open span:nth-child(2) { opacity: 0; } '
    '.nav-hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }\n'
)

# Old mobile-menu CSS (sub-pages)
OLD_MOBILE_CSS_ONELINE = (
    '    .nav-mobile { background: var(--white); border-top: 1px solid var(--border); '
    'max-height: 0; overflow: hidden; transition: max-height 0.4s ease; }\n'
    '    .nav-mobile.open { max-height: 1200px; }\n'
)

# Old mobile-item CSS (sub-pages)
OLD_MOBILE_ITEM_CSS_ONELINE = (
    '    .mobile-item { border-bottom: 1px solid var(--border); padding-bottom: 8px; } '
    '.mobile-item:last-of-type { border-bottom: none; }\n'
    '    .mobile-section-label { padding: 16px 24px 8px; font-size: 11px; font-weight: 700; '
    'color: var(--red); letter-spacing: 2px; text-transform: uppercase; display: block; }\n'
    '    .mobile-sub a { display: flex; align-items: center; gap: 10px; padding: 11px 28px; '
    'font-size: 15px; color: var(--gray-dark); text-decoration: none; '
    'transition: color 0.15s, background 0.15s, padding-left 0.15s; }\n'
    '    .mobile-sub a::before { content: \'\'; width: 4px; height: 4px; border-radius: 50%; '
    'background: var(--border); flex-shrink: 0; transition: background 0.15s; }\n'
    '    .mobile-sub a:hover { color: var(--red); background: var(--red-light); padding-left: 36px; } '
    '.mobile-sub a:hover::before { background: var(--red); }\n'
    '    .mobile-sns { display: flex; align-items: center; gap: 10px; padding: 16px 24px; '
    'border-top: 1px solid var(--border); margin-top: 8px; }\n'
)

# Old media query (sub-pages, single line)
OLD_MEDIA_1100_ONELINE = (
    '    @media (max-width: 1100px) { .nav-menus { display: none; } .nav-sns { display: none; } '
    '.nav-hamburger { display: flex; } .nav-right { margin-left: auto; } '
    '.nav-container { padding: 0 20px; } }\n'
)
OLD_MEDIA_480_ONELINE = (
    '    @media (max-width: 480px) { .nav-logo img { height: 40px; } '
    '.nav-cta { padding: 8px 14px; font-size: 13px; } }\n'
)

# New CSS to inject (replaces old hamburger + mobile CSS + old media queries)
NEW_NAV_CSS = '''\
    /* Hamburger – always visible */
    .nav-hamburger { display: flex; flex-direction: column; gap: 5px; cursor: pointer; padding: 8px; background: none; border: none; margin-left: 16px; z-index: 10002; flex-shrink: 0; }
    .nav-hamburger span { width: 24px; height: 2px; background: var(--black); border-radius: 2px; transition: 0.3s; display: block; }

    /* Fullscreen overlay */
    .fs-overlay { position: fixed; inset: 0; background: #0f0f0f; z-index: 10001; display: flex; flex-direction: column; opacity: 0; pointer-events: none; transition: opacity 0.28s ease; overflow-y: auto; }
    .fs-overlay.open { opacity: 1; pointer-events: auto; }
    .fs-nav-bar { display: flex; align-items: center; justify-content: space-between; padding: 0 40px; height: var(--nav-h); flex-shrink: 0; border-bottom: 1px solid rgba(255,255,255,0.07); }
    .fs-logo { text-decoration: none; display: flex; align-items: center; }
    .fs-logo img { height: 48px; width: auto; filter: brightness(0) invert(1); }
    .fs-close { background: none; border: 1px solid rgba(255,255,255,0.22); border-radius: 8px; width: 40px; height: 40px; color: #fff; font-size: 22px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s; line-height: 1; }
    .fs-close:hover { background: rgba(255,255,255,0.1); }
    .fs-body { flex: 1; display: grid; grid-template-columns: repeat(5, 1fr); padding: 56px 40px 40px; max-width: 1200px; margin: 0 auto; width: 100%; }
    .fs-col { padding: 0 28px; border-right: 1px solid rgba(255,255,255,0.06); }
    .fs-col:first-child { padding-left: 0; }
    .fs-col:last-child { border-right: none; padding-right: 0; }
    .fs-cat { font-size: 11px; font-weight: 700; color: var(--red); letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .fs-links { display: flex; flex-direction: column; gap: 2px; }
    .fs-links a { font-size: 16px; color: rgba(255,255,255,0.65); text-decoration: none; padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.04); transition: color 0.18s, padding-left 0.18s; }
    .fs-links a:last-child { border-bottom: none; }
    .fs-links a:hover { color: #fff; padding-left: 8px; }
    .fs-footer { padding: 24px 40px 40px; border-top: 1px solid rgba(255,255,255,0.07); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; max-width: 1200px; margin: 0 auto; width: 100%; }
    .fs-footer-sns { display: flex; gap: 10px; }
    .fs-cta { background: var(--red); color: #fff; padding: 12px 28px; border-radius: 8px; font-size: 14px; font-weight: 600; text-decoration: none; transition: background 0.2s; white-space: nowrap; }
    .fs-cta:hover { background: var(--red-dark); }

    @media (max-width: 1100px) {
      .nav-menus { display: none; }
      .nav-sns { display: none; }
      .nav-right { margin-left: auto; }
      .nav-container { padding: 0 20px; }
      .fs-body { grid-template-columns: 1fr 1fr; padding: 32px 24px 24px; }
      .fs-col { border-right: none; border-bottom: 1px solid rgba(255,255,255,0.06); padding: 20px 0; }
      .fs-col:last-child { border-bottom: none; }
      .fs-nav-bar { padding: 0 20px; }
      .fs-footer { padding: 20px 24px 32px; }
    }
    @media (max-width: 600px) { .fs-body { grid-template-columns: 1fr; } .fs-links a { font-size: 15px; } }
    @media (max-width: 480px) { .nav-logo img { height: 40px; } .nav-cta { padding: 8px 14px; font-size: 13px; } }
'''

# ──────────────────────────────────────────────
# 2. HTML: fullscreen overlay block (inserted after </nav>)
# ──────────────────────────────────────────────
FS_OVERLAY_HTML = '''\
<div class="fs-overlay" id="fsOverlay">
  <div class="fs-nav-bar">
    <a href="index.html" class="fs-logo"><img src="삼신로고2.png" alt="삼년의 신화 국어논술학원"></a>
    <button class="fs-close" id="fsClose" aria-label="메뉴 닫기">&#x2715;</button>
  </div>
  <div class="fs-body">
    <div class="fs-col">
      <div class="fs-cat">학원 소개</div>
      <div class="fs-links">
        <a href="about-greeting.html">인사말</a>
        <a href="about-features.html">학원 특징</a>
        <a href="about-history.html">연혁</a>
        <a href="about-branches.html">지점 안내 및 오시는 길</a>
      </div>
    </div>
    <div class="fs-col">
      <div class="fs-cat">강사 소개</div>
      <div class="fs-links">
        <a href="teachers-gojan.html">고잔점</a>
        <a href="teachers-zai.html">자이점</a>
        <a href="teachers-hyper.html">하이퍼관</a>
      </div>
    </div>
    <div class="fs-col">
      <div class="fs-cat">커리큘럼</div>
      <div class="fs-links">
        <a href="curriculum.html#elem">초등 과정</a>
        <a href="curriculum.html#middle">중등 과정</a>
        <a href="curriculum.html#high">고등 과정</a>
      </div>
    </div>
    <div class="fs-col">
      <div class="fs-cat">학원 소식</div>
      <div class="fs-links">
        <a href="news-notice.html">공지사항</a>
        <a href="news-seminar.html">설명회 신청</a>
        <a href="news-schedule.html">학원 일정</a>
        <a href="news-timetable.html">학원 시간표</a>
      </div>
    </div>
    <div class="fs-col">
      <div class="fs-cat">생생 후기</div>
      <div class="fs-links">
        <a href="about-results.html">명예의 전당</a>
        <a href="reviews-list.html">수강 후기</a>
      </div>
    </div>
  </div>
  <div class="fs-footer">
    <div class="fs-footer-sns">
      <a href="http://pf.kakao.com/_icyxgn" class="sns-btn sns-kakao" target="_blank" rel="noopener">K</a>
      <a href="#" class="sns-btn sns-insta"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="5"/><circle cx="17.5" cy="6.5" r="1.2" fill="white" stroke="none"/></svg></a>
      <a href="#" class="sns-btn sns-youtube"><svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M21.8 8s-.2-1.4-.8-2c-.7-.8-1.5-.8-1.9-.8C16.6 5 12 5 12 5s-4.6 0-7.1.2c-.4 0-1.2.1-1.9.8-.6.6-.8 2-.8 2S2 9.6 2 11.2v1.5C2 14.4 2.2 16 2.2 16s.2 1.4.8 2c.7.8 1.7.7 2.2.8C6.7 19 12 19 12 19s4.6 0 7.1-.2c.4 0 1.2-.1 1.9-.8.6-.6.8-2 .8-2S22 14.4 22 12.7v-1.5C22 9.6 21.8 8 21.8 8zM9.8 14.5V9.5l5.4 2.5-5.4 2.5z"/></svg></a>
      <a href="#" class="sns-btn sns-blog">N</a>
    </div>
    <a href="consulting.html" class="fs-cta">상담 신청 →</a>
  </div>
</div>
'''

# ──────────────────────────────────────────────
# 3. JS: new overlay logic
# ──────────────────────────────────────────────
NEW_JS_BLOCK = (
    '  const hamburger = document.getElementById(\'hamburger\');\n'
    '  const fsOverlay = document.getElementById(\'fsOverlay\');\n'
    '  const fsClose   = document.getElementById(\'fsClose\');\n'
    '  function openFsMenu()  { fsOverlay.classList.add(\'open\');    document.body.style.overflow = \'hidden\'; }\n'
    '  function closeFsMenu() { fsOverlay.classList.remove(\'open\'); document.body.style.overflow = \'\'; }\n'
    '  hamburger.addEventListener(\'click\', openFsMenu);\n'
    '  fsClose.addEventListener(\'click\', closeFsMenu);\n'
    '  document.addEventListener(\'keydown\', e => { if (e.key === \'Escape\') closeFsMenu(); });\n'
)

# ──────────────────────────────────────────────
# Regex patterns for old mobile nav block in HTML
# ──────────────────────────────────────────────
# Matches the entire <div class="nav-mobile" ...>...</div> block (multi-line)
RE_MOBILE_BLOCK = re.compile(
    r'\n  <!-- .*?-->\n  <div class="nav-mobile"[^>]*>.*?</div>\n</nav>',
    re.DOTALL
)
# Also handle without the comment line
RE_MOBILE_BLOCK2 = re.compile(
    r'\n  <div class="nav-mobile"[^>]*>.*?</div>\n</nav>',
    re.DOTALL
)

# ──────────────────────────────────────────────
# Regex patterns for old JS hamburger block
# ──────────────────────────────────────────────
# Multi-line variant (index.html style)
RE_JS_HAMBURGER_MULTI = re.compile(
    r"  const hamburger = document\.getElementById\('hamburger'\);\n"
    r"  const mobileMenu = document\.getElementById\('mobileMenu'\);\n"
    r"  hamburger\.addEventListener\('click', \(\) => \{[^}]+\}\);\n"
    r"  function closeMobileMenu\(\) \{[^}]+\}\n",
    re.DOTALL
)
# Single-line variant (sub-page style)
RE_JS_HAMBURGER_SINGLE = re.compile(
    r"  const hamburger = document\.getElementById\('hamburger'\);\n"
    r"  const mobileMenu = document\.getElementById\('mobileMenu'\);\n"
    r"  hamburger\.addEventListener\('click', \(\) => \{ hamburger\.classList\.toggle\('open'\); mobileMenu\.classList\.toggle\('open'\); \}\);\n"
    r"  function closeMobileMenu\(\) \{ hamburger\.classList\.remove\('open'\); mobileMenu\.classList\.remove\('open'\); \}\n"
)

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── Step 1: CSS replacements ──
    # Remove old hamburger CSS (multi-line index.html style)
    content = re.sub(
        r'    /\* Mobile hamburger \*/\n'
        r'    \.nav-hamburger \{[^}]+\}\n'
        r'    \.nav-hamburger span \{[^}]+\}\n'
        r'    \.nav-hamburger\.open span:nth-child\(1\) \{[^}]+\} '
        r'\.nav-hamburger\.open span:nth-child\(2\) \{[^}]+\} '
        r'\.nav-hamburger\.open span:nth-child\(3\) \{[^}]+\}\n'
        r'\n'
        r'    /\* Mobile menu \*/\n'
        r'    \.nav-mobile \{[^}]+\}\n'
        r'    \.nav-mobile\.open \{[^}]+\}\n'
        r'    \.mobile-item \{[^}]+\}\n'
        r'    \.mobile-item:last-of-type \{[^}]+\}\n'
        r'    \.mobile-section-label \{[^}]+\}\n'
        r'    \.mobile-sub a \{[^}]+\}\n'
        r'    \.mobile-sub a::before \{[^}]+\}\n'
        r'    \.mobile-sub a:hover \{[^}]+\} \.mobile-sub a:hover::before \{[^}]+\}\n'
        r'    \.mobile-sns \{[^}]+\}\n',
        '',
        content,
        flags=re.DOTALL
    )
    # Remove old media queries for nav (various single-line patterns in sub-pages)
    content = content.replace(OLD_HAMBURGER_CSS_ONELINE, '')
    content = content.replace(OLD_MOBILE_CSS_ONELINE, '')
    content = content.replace(OLD_MOBILE_ITEM_CSS_ONELINE, '')
    content = content.replace(OLD_MEDIA_1100_ONELINE, '')
    content = content.replace(OLD_MEDIA_480_ONELINE, '')

    # Remove multi-line media queries for nav
    content = re.sub(
        r'    @media \(max-width: 1100px\) \{\n'
        r'      \.nav-menus \{ display: none; \}[^\}]*\n'
        r'      \.nav-sns \{ display: none; \}[^\}]*\n'
        r'      \.nav-hamburger \{ display: flex; \}[^\}]*\n'
        r'      \.nav-right \{ margin-left: auto; \}[^\}]*\n'
        r'      \.nav-container \{ padding: 0 20px; \}[^\}]*\n'
        r'    \}\n'
        r'    @media \(max-width: 480px\) \{\n'
        r'      \.nav-logo img \{ height: 40px; \}[^\}]*\n'
        r'      \.nav-cta \{ padding: 8px 14px; font-size: 13px; \}[^\}]*\n'
        r'    \}\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Inject new CSS just before closing </style>
    if NEW_NAV_CSS not in content:
        content = content.replace('  </style>\n', NEW_NAV_CSS + '  </style>\n', 1)

    # ── Step 2: Remove old mobile HTML block, add FS overlay after </nav> ──
    # Try multi-line with comment
    m = RE_MOBILE_BLOCK.search(content)
    if m:
        content = content[:m.start()] + '\n</nav>\n' + FS_OVERLAY_HTML + content[m.end():]
    else:
        # Try without comment line
        m2 = RE_MOBILE_BLOCK2.search(content)
        if m2:
            content = content[:m2.start()] + '\n</nav>\n' + FS_OVERLAY_HTML + content[m2.end():]

    # ── Step 3: Replace JS hamburger logic ──
    # Try multi-line first
    m3 = RE_JS_HAMBURGER_MULTI.search(content)
    if m3:
        content = content[:m3.start()] + NEW_JS_BLOCK + content[m3.end():]
    else:
        m4 = RE_JS_HAMBURGER_SINGLE.search(content)
        if m4:
            content = content[:m4.start()] + NEW_JS_BLOCK + content[m4.end():]

    # ── Step 4: Remove any remaining closeMobileMenu() references ──
    content = content.replace(' onclick="closeMobileMenu()"', '')

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

html_files = sorted(glob.glob('/Users/gimseong-eon/Desktop/samnyun-website/*.html'))
changed, skipped = [], []
for p in html_files:
    if process_file(p):
        changed.append(os.path.basename(p))
    else:
        skipped.append(os.path.basename(p))

print(f"Changed ({len(changed)}): {changed}")
print(f"Skipped ({len(skipped)}): {skipped}")
