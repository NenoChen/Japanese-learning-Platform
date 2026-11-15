#!/usr/bin/env python3
"""Import verified same-run PDF+JSON lesson bundles from incoming/YYYY-MM-DD/.

Never infer structured quiz, furigana, or translations from PDF text: those
must be generated alongside the PDF and approved by the producer.
"""
import datetime, hashlib, json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'lessons.json'
INCOMING=ROOT/'incoming'
MATERIALS=ROOT/'materials'
TAG=re.compile(r'</?(?:ruby|rt)>')
DATE=re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate(lesson):
    for key in ('id','date','day','title','articles','words','grammar','quiz'):
        if key not in lesson: raise ValueError('Missing lesson field '+key)
    if not DATE.fullmatch(lesson['date']) or lesson['id']!=lesson['date']:
        raise ValueError('Lesson id must equal ISO date')
    datetime.date.fromisoformat(lesson['date'])
    if not isinstance(lesson['day'],int) or lesson['day']<1: raise ValueError('Invalid day')
    for key in ('articles','words','grammar','quiz'):
        if not isinstance(lesson[key],list): raise ValueError('Invalid '+key)
    for article in lesson['articles']:
        if not isinstance(article.get('sentences'),list): raise ValueError('Missing sentences')
        for s in article['sentences']:
            h=s.get('html','')
            if '<' in TAG.sub('',h) or '>' in TAG.sub('',h):
                raise ValueError('Unsafe lesson markup')
            if not isinstance(s.get('zh'),str): raise ValueError('Missing translation')
    for q in lesson['quiz']:
        if not isinstance(q.get('options'),list) or not isinstance(q.get('answer'),int) or not 0<=q['answer']<len(q['options']):
            raise ValueError('Invalid quiz')

def main():
    db=json.loads(DATA.read_text(encoding='utf-8'))
    current={l['id']:l for l in db['lessons']}
    count=0
    for folder in sorted(INCOMING.iterdir() if INCOMING.exists() else []):
        if not folder.is_dir() or not DATE.fullmatch(folder.name): continue
        pdf=folder/'lesson.pdf'; lessonfile=folder/'lesson.json'; manifest=folder/'manifest.json'
        if not (pdf.exists() and lessonfile.exists() and manifest.exists()):
            raise ValueError(f'Incomplete bundle: {folder.name}')
        meta=json.loads(manifest.read_text(encoding='utf-8'))
        lesson=json.loads(lessonfile.read_text(encoding='utf-8'))
        validate(lesson)
        digest=hashlib.sha256(pdf.read_bytes()).hexdigest()
        if pdf.stat().st_size>20_000_000 or not pdf.read_bytes().startswith(b'%PDF-'):
            raise ValueError('Invalid or oversized PDF')
        if meta.get('pdf_sha256')!=digest or meta.get('date')!=folder.name or lesson['date']!=folder.name:
            raise ValueError('PDF/JSON manifest mismatch: '+folder.name)
        if meta.get('lesson_sha256')!=hashlib.sha256(lessonfile.read_bytes()).hexdigest():
            raise ValueError('JSON manifest mismatch: '+folder.name)
        dest=MATERIALS/f'Day{lesson["day"]:02d}.pdf'
        if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Existing Day {lesson["day"]} PDF differs; refusing overwrite')
        dest.parent.mkdir(exist_ok=True)
        dest.write_bytes(pdf.read_bytes())
        # Preserve existing lessons; only permit replacing identical content for repeat runs.
        if lesson['id'] in current and current[lesson['id']]!=lesson:
            raise ValueError('Existing lesson differs; manual review required: '+lesson['id'])
        current[lesson['id']]=lesson
        count+=1
    db['lessons']=sorted(current.values(),key=lambda l:l['date'])
    DATA.write_text(json.dumps(db,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Validated {count} bundle(s); total {len(current)} lessons')

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,json.JSONDecodeError) as e:
        print('IMPORT ERROR:',e,file=sys.stderr);sys.exit(1)
