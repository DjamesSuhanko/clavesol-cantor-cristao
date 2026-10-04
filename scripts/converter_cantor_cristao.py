#!/usr/bin/env python3
"""Converte XML em sequência, sem PDF, commit, push ou acompanhamento remoto."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path.home()/'Documents/ClaveSol/CantorCristao'
STATE=Path.home()/'Documents/ClaveSol/lab/cantor-cristao-conversao'
MUSESCORE=Path.home()/'bin/musescore'
sys.path.insert(0,str(ROOT))

def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2));temp.replace(path)

def identity(source):
    match=re.search(r'(\d+)([a-zA-Z]*)(?=$|[-_ ])',source.stem)
    if not match:raise ValueError('Nome de arquivo sem número de hino.')
    number=int(match.group(1))
    version=match.group(2).lower()
    return number,f'hino-{number:03d}{version}'

def worker(source):
    from criar_licao import prepare,one_line
    number,slug=identity(source)
    xml=ET.parse(source).getroot()
    title=one_line(xml.findtext('work/work-title') or xml.findtext('movement-title') or '')
    if title.casefold() in ('title','untitled','sem título'):title=''
    version=slug.removeprefix(f'hino-{number:03d}')
    heading=f'Hino {number}{version.upper()}'+(' — '+title if title else '')
    with tempfile.TemporaryDirectory(prefix='cantor-cristao-') as directory:
        mscz=Path(directory)/(slug+'.mscz')
        subprocess.run([str(MUSESCORE),'-o',str(mscz),str(source)],check=True,timeout=180,
                       env={**os.environ,'QT_QPA_PLATFORM':'offscreen'})
        prepare(mscz,hinos=True,hinario='cantor-cristao',root=ROOT,slug=slug,title=heading,
                lesson=number,executable=str(MUSESCORE),update=True,pdf=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=SOURCE)
    parser.add_argument('--state',type=Path,default=STATE)
    parser.add_argument('--one',type=Path,help=argparse.SUPPRESS)
    args=parser.parse_args()
    if args.one:worker(args.one.resolve());return
    state=args.state.resolve();state.mkdir(parents=True,exist_ok=True)
    with (state/'process.lock').open('w') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:raise SystemExit('Já há uma conversão em execução.')
        sources=sorted(p for p in args.source.resolve().iterdir() if p.suffix.lower() in ('.xml','.musicxml'))
        if not sources:raise SystemExit('Nenhum XML encontrado.')
        slugs=[identity(p)[1] for p in sources]
        if len(set(slugs))!=len(slugs):
            duplicates={slug:[p.name for p,s in zip(sources,slugs) if s==slug] for slug in set(slugs) if slugs.count(slug)>1}
            raise SystemExit('Identificadores duplicados: '+json.dumps(duplicates,ensure_ascii=False))
        if not MUSESCORE.is_file():raise SystemExit('MuseScore não encontrado.')
        report={'state':'running','total':len(sources),'success':0,'skipped':0,'failed':0,'started':time.strftime('%Y-%m-%d %H:%M:%S'),'items':[]}
        def save():write_json(state/'status.json',report)
        save()
        for source in sources:
            _,slug=identity(source);digest=hashlib.sha256(source.read_bytes()).hexdigest()
            marker=state/'completed'/f'{slug}.json'
            previous=json.loads(marker.read_text()) if marker.exists() else {}
            if previous.get('source_sha256')==digest and previous.get('files') and all((ROOT/name).is_file() and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha for name,sha in previous['files'].items()):
                report['skipped']+=1;report['items'].append({'source':source.name,'status':'skipped'});save();continue
            log=state/'logs'/f'{slug}.log';log.parent.mkdir(exist_ok=True)
            report['current']=source.name;save()
            print(f'Convertendo {source.name}',flush=True)
            with log.open('w') as output:
                process=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'--one',str(source)],cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
                try:code=process.wait(timeout=900)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL);process.wait();code=124
                    output.write('\nTempo limite de 900 segundos excedido.\n')
            if code==0:
                folder=ROOT/'assets/music/hinos/cantor-cristao'/slug
                files=[p for p in folder.rglob('*') if p.is_file()]+[ROOT/'partituras/hinos/cantor-cristao'/f'{slug}.md']
                write_json(marker,{'source_sha256':digest,'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
                report['success']+=1
            else:report['failed']+=1
            report['items'].append({'source':source.name,'status':'success' if code==0 else 'failed','log':str(log),'exit_code':code});save()
        report['current']=None;report['state']='validating';save()
        with (state/'build.log').open('w') as output:
            env={**os.environ,'BASE_PATH':''}
            build=subprocess.run([sys.executable,'build.py'],cwd=ROOT,env=env,stdout=output,stderr=subprocess.STDOUT)
            links=subprocess.run([sys.executable,'scripts/check_links.py'],cwd=ROOT,env=env,stdout=output,stderr=subprocess.STDOUT) if build.returncode==0 else None
        report['state']='completed' if build.returncode==0 and links.returncode==0 else 'validation_failed'
        report['finished']=time.strftime('%Y-%m-%d %H:%M:%S');save()
        print('Conversão encerrada. Consulte status.json e os logs. Sem publicação automática.',flush=True)

if __name__=='__main__':main()
