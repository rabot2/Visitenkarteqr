#!/usr/bin/env python3
"""Build a standalone HTML file with all assets base64-embedded."""
import base64, re, sys
from pathlib import Path

BASE = Path(__file__).parent

def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

def mime(path):
    p = str(path)
    if p.endswith('.ttf'):  return 'font/truetype'
    if p.endswith('.svg'):  return 'image/svg+xml'
    if p.endswith('.png'):  return 'image/png'
    if p.endswith('.jpg') or p.endswith('.jpeg'): return 'image/jpeg'
    if p.endswith('.js'):   return 'application/javascript'
    return 'application/octet-stream'

src = (BASE / 'index.html').read_text(encoding='utf-8')

# 1. Inline font @font-face url('fonts/...')
def replace_font(m):
    path = BASE / m.group(1)
    return f"url('data:{mime(path)};base64,{b64(path)}')"
src = re.sub(r"url\('(fonts/[^']+)'\)", replace_font, src)

# 2. Inline SVG img src="logos/..."
def replace_img(m):
    path = BASE / m.group(1)
    return f'src="data:{mime(path)};base64,{b64(path)}"'
src = re.sub(r'src="(logos/[^"]+)"', replace_img, src)

# 2b. Inline background-image url('backgrounds/...')
def replace_bg(m):
    path = BASE / m.group(1)
    return f"url('data:{mime(path)};base64,{b64(path)}')"
src = re.sub(r"url\('(backgrounds/[^']+)'\)", replace_bg, src)

# 2c. Inline img src="backgrounds/..."
src = re.sub(r'src="(backgrounds/[^"]+)"', replace_img, src)

# 3. Inline <script src="js/..."></script>
def replace_script(m):
    path = BASE / m.group(1)
    js = path.read_text(encoding='utf-8')
    return f'<script>{js}</script>'
src = re.sub(r'<script src="(js/[^"]+)"></script>', replace_script, src)

out = sys.argv[1] if len(sys.argv) > 1 else str(BASE / 'index_standalone.html')
Path(out).write_text(src, encoding='utf-8')
print(f"Written {len(src):,} bytes → {out}")
