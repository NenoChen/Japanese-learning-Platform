#!/usr/bin/env python3
"""Prepare verifiable upload bundle from a PDF and its SAME-RUN lesson JSON."""
import argparse, hashlib, json, pathlib, shutil
p=argparse.ArgumentParser()
p.add_argument('--pdf',type=pathlib.Path,required=True)
p.add_argument('--json',type=pathlib.Path,required=True)
p.add_argument('--output',type=pathlib.Path,default=pathlib.Path('incoming'))
a=p.parse_args()
lesson=json.loads(a.json.read_text(encoding='utf-8'))
from import_bundle import validate
validate(lesson)
out=a.output/lesson['date'];out.mkdir(parents=True,exist_ok=True)
shutil.copyfile(a.pdf,out/'lesson.pdf')
shutil.copyfile(a.json,out/'lesson.json')
meta={'date':lesson['date'],'pdf_sha256':hashlib.sha256((out/'lesson.pdf').read_bytes()).hexdigest(),'lesson_sha256':hashlib.sha256((out/'lesson.json').read_bytes()).hexdigest(),'producer':'same-run-pdf-and-json'}
(out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
print(out)
