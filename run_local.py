"""Runs 4 standalone services in subprocesses, SQLite development mode (no Docker)."""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parent
HOST=os.environ.get('APP_HOST','127.0.0.1')
SERVICES=[('catalog',3001),('orders',3002),('delivery',3003),('gateway',int(os.environ.get('GATEWAY_PORT','8080')))]

def environment(name):
    env=os.environ.copy()
    env.update({'CATALOG_URL':f'http://{HOST}:3001','ORDERS_URL':f'http://{HOST}:3002',
                'DELIVERY_URL':f'http://{HOST}:3003'})
    if name in ('orders','delivery'):
        dbfile=ROOT/'data'/f'{name}.db'
        dbfile.parent.mkdir(exist_ok=True)
        env['DATABASE_URL']='sqlite:///'+dbfile.as_posix()
    return env

def ready(name,port,proc):
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        if proc.poll() is not None:
            raise RuntimeError(f'{name} exited unexpectedly with code {proc.returncode}')
        try:
            with urlopen(f'http://{HOST}:{port}/health',timeout=1) as response:
                if response.status==200:
                    print(f'[READY] {name}: http://{HOST}:{port}',flush=True)
                    return
        except (OSError,URLError):pass
        time.sleep(.3)
    raise TimeoutError(f'{name} was not healthy after 60 seconds')

def stop(processes):
    for p in reversed(processes):
        if p.poll() is None:p.terminate()
    for p in reversed(processes):
        try:p.wait(timeout=5)
        except subprocess.TimeoutExpired:p.kill();p.wait()

def main():
    processes=[]
    try:
        for name,port in SERVICES:
            cmd=[sys.executable,'-m','uvicorn','main:app','--host',HOST,'--port',str(port)]
            print(f'Starting {name} on port {port}...',flush=True)
            p=subprocess.Popen(cmd,cwd=ROOT/'services'/name,env=environment(name))
            processes.append(p)
            ready(name,port,p)
        print(f'\nQuickBite: http://{HOST}:{SERVICES[-1][1]}\nSwagger: http://{HOST}:{SERVICES[-1][1]}/docs\nPress Ctrl+C to stop.\n',flush=True)
        while True:
            if any(p.poll() is not None for p in processes):
                raise RuntimeError('One or more services exited unexpectedly')
            time.sleep(.5)
    except KeyboardInterrupt:
        print('\nStopping services...',flush=True)
    finally:stop(processes)

if __name__=='__main__':main()
