#!/usr/bin/env python3
"""Generate real MP3 files from the site's lesson JSON with gTTS (requires internet).

Run: pip install -r scripts/audio-requirements.txt && python scripts/generate_audio.py
All audio comes from the exact same structured lesson JSON, not a re-authored script.
"""
import hashlib
import json
import re
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET
from gtts import gTTS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audio'
OUT.mkdir(exist_ok=True)
DB = json.loads((ROOT / 'data/lessons.json').read_text(encoding='utf-8'))

def plain(html):
    # Ruby annotations are for display only, not spoken twice.
    html = re.sub(r'<rt>.*?</rt>', '', html, flags=re.S)
    return unescape(re.sub(r'<[^>]+>', '', html)).strip()

def texts():
    for lesson in DB['lessons']:
        for article in lesson.get('articles', []):
            lines = [plain(s['html']) for s in article.get('sentences', [])]
            for line in lines:
                if line: yield line
            if lines: yield '\n'.join(lines)
        for w in lesson.get('words', []):
            yield w.get('reading') or w['jp']
        for w in lesson.get('series', {}).get('words', []):
            yield w.get('reading') or w['jp']
    for row in ('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん',
                'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'):
        yield from row

mapping = {}
failed = []
for i, text in enumerate(dict.fromkeys(t.strip() for t in texts() if t and t.strip()), 1):
    key = hashlib.sha256(text.encode('utf-8')).hexdigest()[:24]
    path = OUT / (key + '.mp3')
    if not path.exists() or path.stat().st_size < 100:
        try:
            gTTS(text=text, lang='ja', slow=False).save(str(path))
        except Exception as exc:
            failed.append((text[:40], str(exc)))
            continue
    mapping[text] = 'audio/' + path.name
    print(f'{i}: {text[:24]}', flush=True)
(OUT / 'index.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Available MP3: {len(mapping)}; failures: {len(failed)}')
if failed:
    for t, err in failed[:5]: print('ERROR:', t, err)
    raise SystemExit(1)
