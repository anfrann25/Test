#!/usr/bin/env python3
"""Create safe local workspaces for HackTheBasics practical labs."""
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'practice'/'catalog.json'
DEFAULT_BASE=Path.home()/'HackTheBasics-Labs'

def load_labs():
    return json.loads(CATALOG.read_text(encoding='utf-8'))['labs']

def find_lab(lab_id):
    return next((x for x in load_labs() if x['id']==lab_id),None)

def sample_files(lab):
    module=lab['module']; lid=lab['id']
    common={'source/NOTICE.txt':f'Harmless local training data for {lid}.\nDo not replace this folder with private or production evidence.\n'}
    if module=='networking-practical':
        common['source/network-observations.csv']='time,protocol,source,destination,detail\n09:00,DNS,device,resolver,example.test A\n09:00,TCP,device,server,443 SYN\n09:01,HTTPS,device,server,200 response\n'
    elif module=='monitoring':
        common['source/auth.log']='2026-01-12T09:00:00Z INFO login_ok user=student source=lab\n2026-01-12T09:03:02Z WARN login_failed user=analyst source=test-a\n2026-01-12T09:03:14Z WARN login_failed user=analyst source=test-a\n2026-01-12T09:08:00Z INFO login_ok user=analyst source=test-a\n'
        common['source/file-events.csv']='time,path,event\n2026-01-12T09:02:00Z,config/app.ini,modified\n2026-01-12T09:05:00Z,temp/report.txt,created\n'
    elif module=='python-automation':
        common['source/events.log']='2026-01-12 09:00 INFO service started\ninvalid record\n2026-01-12 09:04 WARN repeated failure\n2026-01-12 09:06 INFO service recovered\n'
        common['source/findings.json']='[{"id":"F-001","severity":"medium","title":"Example finding","evidence":"local sample"}]\n'
    elif module=='web-defence':
        common['source/request.txt']='POST /profile HTTP/1.1\nHost: local.test\nContent-Type: application/x-www-form-urlencoded\n\nname=Student&bio=Training+sample\n'
        common['source/response-headers.txt']='HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\nCache-Control: no-store\n'
    elif module=='hardening':
        common['source/device-services.csv']='service,purpose,startup,exposure\nacademy-demo,training,manual,loopback\nfile-share,example,disabled,none\n'
    elif module=='device-defense':
        common['source/device-state.csv']='item,category,state,owner\ntraining-browser,application,enabled,student\ndemo-updater,startup,manual,student\n'
    elif module=='network-diagnostics':
        common['source/network-checks.csv']='time,test,target,result\n09:00,dns,example.test,192.0.2.10\n09:01,latency,192.0.2.10,24ms\n'
    elif module=='secure-development':
        common['source/app.py']='from pathlib import Path\nBASE=Path("workspace").resolve()\nprint("training sample")\n'
        common['source/settings.json']='{"mode":"training","output":"reports/result.txt"}\n'
    elif module=='incident-response':
        common['source/alert.json']='{"time":"2026-02-01T10:12:00Z","type":"training-alert","severity":"medium","source":"sample"}\n'
        common['source/incident-files.csv']='time,path,event,hash_state\n10:05,docs/plan.md,modified,changed\n10:14,config/demo.ini,modified,unknown\n'
    elif module=='privacy':
        common['source/sample-contacts.csv']='name,email,purpose\nExample User,example@example.test,training\n'
        common['source/sample-metadata.txt']='file=training-photo.jpg\nauthor=Example User\nlocation=removed-in-sanitized-copy\n'
    elif module=='account-security':
        common['source/account-sessions.csv']='device,location,last_seen,status\nTraining Phone,Local,2026-02-01T10:00Z,known\nExample Browser,Unknown,2026-01-30T08:12Z,review\n'
        common['source/recovery-options.csv']='method,state,last_verified\nemail,active,2026-01-10\nbackup-code,active,2025-12-01\nold-phone,obsolete,2024-04-02\n'
    elif module=='email-security':
        common['source/message-headers.txt']='From: Support <support@example.test>\nReply-To: review@examp1e.test\nAuthentication-Results: spf=fail dkim=none dmarc=fail\nReceived: from training.local by mailbox.test\n'
        common['source/mailbox-rules.csv']='name,action,target,state\nArchive receipts,move,Receipts,enabled\nForward copy,forward,external@example.test,review\n'
    elif module=='data-forensics':
        common['source/events-a.csv']='time,source,event\n2026-02-01T10:00:00Z,login,success\n2026-02-01T10:04:00Z,file,modified\n'
        common['source/events-b.csv']='time,source,event\n2026-02-01T12:03:00+02:00,network,connected\n'
        common['source/file-list.csv']='name,extension,claimed_type\nphoto.jpg,.jpg,image\nreport.txt,.txt,text\narchive.zip,.zip,archive\n'
    elif module=='web-operations':
        common['source/response-headers.txt']='HTTP/1.1 200 OK\nSet-Cookie: session=training; Path=/; HttpOnly\nCache-Control: public, max-age=3600\nContent-Security-Policy: default-src *\nLocation: https://docs.example.test/final\n'
        common['source/published-files.txt']='index.html\nassets/app.js\nbackup/config.old\n.env.example\n'
    elif module=='resilience':
        common['source/asset-priority.csv']='asset,priority,recovery_target\nnotes,high,1h\ntraining-data,medium,4h\ncache,low,24h\n'
        common['source/outage-scenario.txt']='Synthetic outage: the primary documentation service is unavailable. No production system is involved.\n'
    elif module=='reporting':
        common['source/findings.csv']='id,title,impact,likelihood,status\nF-01,Weak test setting,medium,high,open\nF-02,Missing backup check,high,medium,open\n'
        common['source/evidence-note.txt']='Synthetic evidence only. The sample setting allows unnecessary access in the local training app.\n'
    elif module=='capstone':
        common['source/capstone-auth.log']='2026-02-01T10:00:00Z login_ok account=owner source=console\n2026-02-01T10:12:00Z login_failed account=owner source=remote-test\n'
        common['source/capstone-network.csv']='time,protocol,destination,result\n10:00,DNS,updates.example.test,allowed\n10:13,HTTPS,docs.example.test,allowed\n'
        common['source/capstone-files.csv']='time,path,event\n10:05,docs/plan.md,modified\n10:14,config/demo.ini,modified\n'
    else:
        common['source/sample-a.txt']='alpha\nbeta\nwarning: training marker\ngamma\n'
        common['source/sample-b.txt']='one,two,three\n4,5,6\n'
    return common

def prepare(lab_id,base,language='en',force=False):
    lab=find_lab(lab_id)
    if not lab: raise SystemExit(f'Unknown lab: {lab_id}')
    folder=base/lab_id
    if folder.exists() and any(folder.iterdir()) and not force:
        raise SystemExit(f'{folder} already contains files. Use --force only after making a backup.')
    folder.mkdir(parents=True,exist_ok=True)
    data=lab['el' if language=='el' else 'en']
    for rel,text in sample_files(lab).items():
        p=folder/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    tasks='\n'.join(f'- [ ] {t}' for t in data['tasks'][:3])
    readme=f"# {data['title']}\n\n{lab['hours']}h active practice\n\n{tasks}\n\nEvidence: {data['deliverable']}\n\nUse supplied samples or systems you own.\n"
    (folder/'README.md').write_text(readme,encoding='utf-8')
    (folder/'notes.md').write_text('# Notes\n\n## Observations\n\n## Assumptions\n\n## Commands and results\n\n## Limitations\n',encoding='utf-8')
    (folder/'evidence.md').write_text('# Evidence\n\nScope:\nDate:\nDevice:\n\n## Result\n\n## Verification\n\n## Limitations\n',encoding='utf-8')
    manifest=[]
    for p in sorted((folder/'source').rglob('*')):
        if p.is_file(): manifest.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(folder).as_posix()}")
    (folder/'source-sha256.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
    print(folder)

def check(lab_id,base):
    folder=base/lab_id
    required=['README.md','notes.md','evidence.md','source-sha256.txt']
    missing=[x for x in required if not (folder/x).exists()]
    if missing: print('Missing: '+', '.join(missing));return 1
    evidence=(folder/'evidence.md').read_text(encoding='utf-8')
    if len(evidence.strip())<90: print('Evidence file still looks empty.');return 1
    print(f'Workspace structure is ready: {folder}');return 0

def main():
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['prepare','check','list']);ap.add_argument('lab_id',nargs='?');ap.add_argument('--base',type=Path,default=DEFAULT_BASE);ap.add_argument('--language',choices=['en','el'],default='en');ap.add_argument('--force',action='store_true');a=ap.parse_args()
    if a.command=='list':
        for x in load_labs(): print(f"{x['id']:<26} {x['hours']}h  {x['en']['title']}")
    elif not a.lab_id: ap.error('lab_id is required')
    elif a.command=='prepare': prepare(a.lab_id,a.base,a.language,a.force)
    else: raise SystemExit(check(a.lab_id,a.base))
if __name__=='__main__': main()
