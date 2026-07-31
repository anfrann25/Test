#!/usr/bin/env python3
"""Local companion for the HackTheBasics educational website."""
from __future__ import annotations
import argparse,json,os,platform,subprocess,sys,webbrowser
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CATALOG=ROOT/'academy_catalog.json'
STATE_DIR=Path.home()/'.hackthebasics'
STATE_FILE=STATE_DIR/'progress.json'

def device():
    prefix=os.environ.get('PREFIX','').lower()
    if os.name=='nt': return 'Windows','py'
    if 'com.termux' in prefix or os.environ.get('TERMUX_VERSION') or os.environ.get('ANDROID_ROOT'): return 'Android + Termux','python'
    return f'Linux {platform.machine()}','python3'

def catalog(): return json.loads(CATALOG.read_text(encoding='utf-8'))['lessons']
def state():
    try: data=json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except (FileNotFoundError,json.JSONDecodeError,OSError): data={}
    return {'version':2,'language':data.get('language','en'),'completed':list(dict.fromkeys(data.get('completed',[])))}
def save(s):
    STATE_DIR.mkdir(parents=True,exist_ok=True);tmp=STATE_FILE.with_suffix('.tmp');tmp.write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(STATE_FILE)
def find(query):
    q=query.strip().lower(); items=catalog(); exact=next((x for x in items if x['id'].lower()==q),None)
    if exact:return exact
    hits=[x for x in items if q in x['en']['title'].lower() or q in x['el']['title'].lower()]
    return hits[0] if len(hits)==1 else None

def cmd_list(args):
    s=state();lang=s['language'];done=set(s['completed'])
    for x in catalog():
        if args.practical and x.get('kind')!='practical':continue
        mark='✓' if x['id'] in done else '·';hours=f" {x.get('hours',0)}h" if x.get('hours') else ''
        print(f"{mark} {x['id']:<28} {x[lang]['title']}{hours}")
def cmd_status(_):
    s=state(); practical=[x for x in catalog() if x.get('kind')=='practical'];done={x for x in s['completed']};dh=sum(x.get('hours',0) for x in practical if x['id'] in done)
    total=sum(x.get('hours',0) for x in practical)
    print(f'Device: {device()[0]}');print(f'Progress file: {STATE_FILE}');print(f'Practical labs: {sum(x["id"] in done for x in practical)}/{len(practical)}');print(f'Estimated practical hours completed: {dh}/{total}')
def cmd_complete(args):
    x=find(args.lesson)
    if not x: raise SystemExit('Lesson or lab not found. Use: academy.py list')
    s=state()
    if x['id'] not in s['completed']:s['completed'].append(x['id']);save(s)
    print(f"Completed: {x[s['language']]['title']}")
def cmd_uncomplete(args):
    x=find(args.lesson)
    if not x: raise SystemExit('Lesson or lab not found.')
    s=state();s['completed']=[i for i in s['completed'] if i!=x['id']];save(s);print(f"Removed: {x[s['language']]['title']}")
def cmd_language(args):
    s=state();s['language']=args.language;save(s);print(args.language)
def cmd_prepare(args):
    x=find(args.lab)
    if not x or x.get('kind')!='practical':raise SystemExit('Practical lab not found. Use: academy.py list --practical')
    script=ROOT/'practice'/'labkit.py';s=state();command=[sys.executable,str(script),'prepare',x['id'],'--language',s['language']]
    if args.force:command.append('--force')
    raise SystemExit(subprocess.call(command))
def cmd_check(args):
    x=find(args.lab)
    if not x or x.get('kind')!='practical':raise SystemExit('Practical lab not found.')
    raise SystemExit(subprocess.call([sys.executable,str(ROOT/'practice'/'labkit.py'),'check',x['id']]))
def cmd_open(args):
    x=find(args.lesson) if args.lesson else None
    target=ROOT/(x[state()['language']]['path'] if x else 'home.html')
    if not target.exists():raise SystemExit(f'Missing page: {target}')
    webbrowser.open(target.as_uri());print(target)
def cmd_serve(args):
    os.chdir(ROOT);server=ThreadingHTTPServer((args.host,args.port),SimpleHTTPRequestHandler);url=f'http://{args.host if args.host!="0.0.0.0" else "127.0.0.1"}:{args.port}/home.html';print(url)
    if not args.no_browser:webbrowser.open(url)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

def main():
    ap=argparse.ArgumentParser(description='HackTheBasics local academy companion');sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('list');p.add_argument('--practical',action='store_true');p.set_defaults(func=cmd_list)
    p=sub.add_parser('status');p.set_defaults(func=cmd_status)
    p=sub.add_parser('complete');p.add_argument('lesson');p.set_defaults(func=cmd_complete)
    p=sub.add_parser('uncomplete');p.add_argument('lesson');p.set_defaults(func=cmd_uncomplete)
    p=sub.add_parser('language');p.add_argument('language',choices=['en','el']);p.set_defaults(func=cmd_language)
    p=sub.add_parser('prepare');p.add_argument('lab');p.add_argument('--force',action='store_true');p.set_defaults(func=cmd_prepare)
    p=sub.add_parser('check');p.add_argument('lab');p.set_defaults(func=cmd_check)
    p=sub.add_parser('open');p.add_argument('lesson',nargs='?');p.set_defaults(func=cmd_open)
    p=sub.add_parser('serve');p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8000);p.add_argument('--no-browser',action='store_true');p.set_defaults(func=cmd_serve)
    a=ap.parse_args();a.func(a)
if __name__=='__main__':main()
