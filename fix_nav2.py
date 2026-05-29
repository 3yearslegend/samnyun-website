#!/usr/bin/env python3
"""Fix remaining nav issues after first pass."""
import os, re, glob

NEW_JS_BLOCK = (
    'const hamburger = document.getElementById(\'hamburger\');\n'
    'const fsOverlay = document.getElementById(\'fsOverlay\');\n'
    'const fsClose   = document.getElementById(\'fsClose\');\n'
    'function openFsMenu()  { fsOverlay.classList.add(\'open\');    document.body.style.overflow = \'hidden\'; }\n'
    'function closeFsMenu() { fsOverlay.classList.remove(\'open\'); document.body.style.overflow = \'\'; }\n'
    'hamburger.addEventListener(\'click\', openFsMenu);\n'
    'fsClose.addEventListener(\'click\', closeFsMenu);\n'
    'document.addEventListener(\'keydown\', e => { if (e.key === \'Escape\') closeFsMenu(); });\n'
)

# Patterns for curriculum files (no leading 2-space indent)
RE_CURR_JS = re.compile(
    r"const mobileMenu = document\.getElementById\('mobileMenu'\);\n"
    r"function closeMobileMenu\(\) \{[^\n]+\}\n"
    r"hamburger\.addEventListener\('click', \(\) => \{[^\n]+\}\);\n"
)

# Pattern for index.html (leading 2-space, multiline)
RE_INDEX_JS = re.compile(
    r"  const hamburger = document\.getElementById\('hamburger'\);\n"
    r"  const mobileMenu = document\.getElementById\('mobileMenu'\);\n"
    r"  hamburger\.addEventListener\('click', \(\) => \{\n"
    r"    hamburger\.classList\.toggle\('open'\);\n"
    r"    mobileMenu\.classList\.toggle\('open'\);\n"
    r"  \}\);\n"
    r"\n"
    r"  function closeMobileMenu\(\) \{\n"
    r"    hamburger\.classList\.remove\('open'\);\n"
    r"    mobileMenu\.classList\.remove\('open'\);\n"
    r"  \}\n",
    re.DOTALL
)

# CSS patterns that vary across files
# Combined single-line nav-mobile + nav-mobile.open
RE_NAV_MOBILE_COMBINED = re.compile(
    r'    \.nav-mobile \{[^\}]+\} \.nav-mobile\.open \{[^\}]+\}\n'
)
# Compact: just nav-mobile { ... } \n .nav-mobile.open { ... }
RE_NAV_MOBILE_SEP = re.compile(
    r'    \.nav-mobile \{[^\}]+\}\n    \.nav-mobile\.open \{[^\}]+\}\n'
)
# Multi-line nav-mobile block (index.html style)
RE_NAV_MOBILE_MULTI = re.compile(
    r'    /\* Mobile menu \*/\n'
    r'    \.nav-mobile \{\n'
    r'[^\}]+\}\n'
    r'    \.nav-mobile\.open \{[^\}]+\}\n'
    r'    \.mobile-item \{[^\}]+\}\n'
    r'    \.mobile-item:last-of-type \{[^\}]+\}\n'
    r'    \.mobile-section-label \{\n'
    r'[^\}]+\}\n'
    r'    \.mobile-sub a \{\n'
    r'[^\}]+\}\n'
    r'    \.mobile-sub a::before \{\n'
    r'[^\}]+\}\n'
    r'    \.mobile-sub a:hover \{[^\}]+\} \.mobile-sub a:hover::before \{[^\}]+\}\n'
    r'    \.mobile-sns \{[^\}]+\}\n',
    re.DOTALL
)

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Remove remaining nav-mobile CSS variants
    content = RE_NAV_MOBILE_MULTI.sub('', content)
    content = RE_NAV_MOBILE_COMBINED.sub('', content)
    content = RE_NAV_MOBILE_SEP.sub('', content)

    # Also remove stray mobile-item / mobile-section / mobile-sub CSS if present
    content = re.sub(
        r'    \.mobile-item \{[^\}]+\}[^\n]*\n'
        r'(?:    \.mobile-item:last-of-type \{[^\}]+\}\n)?'
        r'(?:    \.mobile-section-label \{[^\}]+\}\n)?'
        r'(?:    \.mobile-sub a \{[^\}]+\}\n)?'
        r'(?:    \.mobile-sub a::before \{[^\}]+\}\n)?'
        r'(?:    \.mobile-sub a:hover \{[^\}]+\}[^\n]*\n)?'
        r'(?:    \.mobile-sns \{[^\}]+\}\n)?',
        '',
        content,
        flags=re.DOTALL
    )

    # Fix JS for curriculum-style (no indent)
    m = RE_CURR_JS.search(content)
    if m:
        content = content[:m.start()] + NEW_JS_BLOCK + content[m.end():]

    # Fix JS for index.html style (multi-line, 2-space indent)
    m2 = RE_INDEX_JS.search(content)
    if m2:
        indented = '\n'.join('  ' + line if line else '' for line in NEW_JS_BLOCK.rstrip('\n').split('\n')) + '\n'
        content = content[:m2.start()] + indented + content[m2.end():]

    # Remove any remaining closeMobileMenu function and mobileMenu const that weren't caught
    content = re.sub(r"  ?const mobileMenu = document\.getElementById\('mobileMenu'\);\n", '', content)
    content = re.sub(r"  ?function closeMobileMenu\(\) \{[^\n]+\}\n", '', content)
    content = content.replace(' onclick="closeMobileMenu()"', '')

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

html_files = sorted(glob.glob('/Users/gimseong-eon/Desktop/samnyun-website/*.html'))
changed, skipped = [], []
for p in html_files:
    if fix_file(p):
        changed.append(os.path.basename(p))
    else:
        skipped.append(os.path.basename(p))

print(f"Fixed  ({len(changed)}): {changed}")
print(f"Clean  ({len(skipped)}): {skipped}")
