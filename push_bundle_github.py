#!/usr/bin/env python3
"""Push verified bundle files to GitHub via Contents API.
Requires GH_TOKEN environment variable (fine-grained Contents: Read and write).
Only run this from a trusted machine/service, never client-side PWA.
"""
import argparse, base64, json, os, pathlib, urllib.request, urllib.error
p=argparse.ArgumentParser();p.add_argument('--folder',type=pathlib.Path,required=True)
p.add_argument('--repo',default='NenoChen/Japanese-learning-Platform');a=p.parse_args()
token=os.environ.get('GH_TOKEN')
if not token: raise SystemExit('Set GH_TOKEN in trusted environment')
for name in ('lesson.pdf','lesson.json','manifest.json'):
    src=a.folder/name
    if not src.is_file(): raise SystemExit('Missing '+str(src))
    path=f'incoming/{a.folder.name}/{name}'
    url=f'https://api.github.com/repos/{a.repo}/contents/{path}'
    headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'HibiLessonUploader'}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:
            existing=json.load(r)
        sha=existing['sha']
    except urllib.error.HTTPError as e:
        if e.code!=404: raise
        sha=None
    payload={'message':f'Upload {a.folder.name} {name}','content':base64.b64encode(src.read_bytes()).decode(),'branch':'main'}
    if sha: payload['sha']=sha
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={**headers,'Content-Type':'application/json'},method='PUT')
    with urllib.request.urlopen(req,timeout=120) as r: print(name,r.status)
print('GitHub workflow will verify the bundle and update the site.')
