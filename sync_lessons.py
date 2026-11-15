#!/usr/bin/env python3
"""Sync a trusted lesson JSON feed into data/lessons.json.
Requires LESSON_FEED_URL. Optionally LESSON_FEED_TOKEN for Bearer auth.
No AI/PDF conversion is performed here: the producer must publish valid JSON.
"""
import json, os, pathlib, urllib.request, datetime
p=pathlib.Path(__file__).resolve().parents[1]/'data'/'lessons.json'
url=os.environ.get('LESSON_FEED_URL','')
if not url.startswith('https://'):
    raise SystemExit('LESSON_FEED_URL must be an HTTPS URL')
headers={'User-Agent':'HibiJapaneseSync/1.0'}
if os.environ.get('LESSON_FEED_TOKEN'):
    headers['Authorization']='Bearer '+os.environ['LESSON_FEED_TOKEN']
with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:
    raw=response.read(3_000_001)
if len(raw)>3_000_000: raise SystemExit('Feed too large')
feed=json.loads(raw)
items=feed.get('lessons') if isinstance(feed,dict) else [feed]
if not isinstance(items,list): raise SystemExit('Invalid feed')
current=json.loads(p.read_text(encoding='utf-8'))
by_id={l['id']:l for l in current['lessons']}
for l in items:
    if not isinstance(l,dict) or not all(k in l for k in ('id','date','day','title','articles','words','grammar','quiz')):
        raise SystemExit('Invalid lesson shape')
    datetime.date.fromisoformat(l['date'])
    if not all(isinstance(l[k],list) for k in ('articles','words','grammar','quiz')):
        raise SystemExit('Invalid lesson lists')
    for a in l['articles']:
        for s in a['sentences']:
            html=s['html']
            # Strictly allow ruby markup; block scripts, attributes, event handlers and external content.
            import re
            if re.search(r'<(?!/?(?:ruby|rt)>)[^>]*>',html,re.I):
                raise SystemExit('Disallowed HTML in lesson')
    by_id[l['id']]=l
current['lessons']=sorted(by_id.values(),key=lambda l:l['date'])
p.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Synced',len(items),'lesson(s); total',len(by_id))
