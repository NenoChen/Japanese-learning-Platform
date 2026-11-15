#!/usr/bin/env python3
"""Prepare reviewable text from PDFs uploaded to pdf-inbox/; never invent ruby/answers."""
import pathlib, re, sys, json
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[1]
INBOX=ROOT/'pdf-inbox'
OUT=ROOT/'pdf-review'
DATE=re.compile(r'^\d{4}-\d{2}-\d{2}\.pdf$')

def inspect(path):
    if not DATE.fullmatch(path.name):
        raise ValueError(f'PDF filename must be YYYY-MM-DD.pdf: {path.name}')
    if path.stat().st_size > 20_000_000 or path.read_bytes()[:5] != b'%PDF-':
        raise ValueError(f'Not a supported PDF: {path.name}')
    doc=fitz.open(path)
    if doc.is_encrypted or len(doc)==0:
        raise ValueError(f'Encrypted or empty PDF: {path.name}')
    pages=[page.get_text('text',sort=True) for page in doc]
    if not ''.join(pages).strip():
        raise ValueError(f'No extractable text (scanned PDF?): {path.name}')
    date=path.stem
    folder=OUT/date
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'extracted.txt').write_text('\n\n'.join(f'--- Page {i+1} ---\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
    (folder/'status.json').write_text(json.dumps({'date':date,'pages':len(doc),'status':'NEEDS_REVIEW','note':'PDF extraction is not verified lesson JSON. Ruby/answers/word metadata require review.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{date}: {len(doc)} pages; review needed')

if __name__=='__main__':
    files=sorted(INBOX.glob('*.pdf')) if INBOX.exists() else []
    if not files:
        print('No PDF files in pdf-inbox/')
        sys.exit(0)
    try:
        for f in files: inspect(f)
    except (ValueError,RuntimeError) as e:
        print('PDF REVIEW ERROR:',e,file=sys.stderr)
        sys.exit(1)
