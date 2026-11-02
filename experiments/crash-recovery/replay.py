#!/usr/bin/env python3
"""NINFA S03: independently subprocess-killed local workflow. No external APIs."""
import argparse, hashlib, json, os, sqlite3, subprocess, sys, tempfile
from pathlib import Path

STEPS = ('READ', 'VALIDATE', 'TRANSFORM', 'STORE')
CRASH_AFTER = 2
CRASH_CODE = 27


def initialize(db_path):
    with sqlite3.connect(db_path) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS actions (sequence INTEGER PRIMARY KEY AUTOINCREMENT, step TEXT NOT NULL, phase INTEGER NOT NULL)')
        conn.execute('CREATE TABLE IF NOT EXISTS checkpoints (step TEXT PRIMARY KEY, completed INTEGER NOT NULL CHECK(completed=1))')


def execute_worker(db_path, mode, phase, crash):
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        completed = {row[0] for row in conn.execute('SELECT step FROM checkpoints')}
    count = 0
    for step in STEPS:
        if mode == 'checkpoint' and step in completed:
            continue
        with sqlite3.connect(db_path) as conn:
            # Local SQL writes and checkpoint are in the same SQLite transaction.
            # This DOES NOT generalize to external side effects or distributed systems.
            conn.execute('INSERT INTO actions(step,phase) VALUES (?,?)', (step, phase))
            if mode == 'checkpoint':
                conn.execute('INSERT INTO checkpoints(step,completed) VALUES (?,1)', (step,))
        count += 1
        if crash and count == CRASH_AFTER:
            os._exit(CRASH_CODE)  # Intentionally kills worker, bypasses normal Python cleanup.
    return 0


def subprocess_run(db_path, mode, phase, crash):
    cmd=[sys.executable, str(Path(__file__).resolve()), 'worker', '--db', str(db_path), '--mode', mode, '--phase', str(phase)]
    if crash: cmd.append('--crash')
    p=subprocess.run(cmd, capture_output=True,text=True,check=False,timeout=10)
    if p.returncode not in (0, CRASH_CODE):
        raise RuntimeError(f'worker error {p.returncode}: {p.stderr}')
    return p.returncode


def evaluate(out_dir):
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    results={}
    for mode in ('naive','checkpoint'):
        db=out_dir/f'{mode}.sqlite3'
        if db.exists(): db.unlink()
        first=subprocess_run(db,mode,1,True)
        second=subprocess_run(db,mode,2,False)
        with sqlite3.connect(db) as conn:
            actions=[{'step':row[0],'phase':row[1]} for row in conn.execute('SELECT step,phase FROM actions ORDER BY sequence')]
            checkpoints=[row[0] for row in conn.execute('SELECT step FROM checkpoints ORDER BY rowid')]
        results[mode]={
            'first_process_exit_code':first,'second_process_exit_code':second,
            'actions':actions,'action_count':len(actions),
            'unique_step_count':len(set(row['step'] for row in actions)),
            'repeated_action_count':len(actions)-len(set(row['step'] for row in actions)),
            'persisted_checkpoints':checkpoints
        }
    assert results['naive']['first_process_exit_code']==CRASH_CODE
    assert results['checkpoint']['first_process_exit_code']==CRASH_CODE
    assert results['naive']['action_count']==6
    assert results['checkpoint']['action_count']==4
    assert results['naive']['repeated_action_count']==2
    assert results['checkpoint']['repeated_action_count']==0
    record={
        'schema':'ninfa-local-crash-recovery-v1','experiment':'NINFA-S03',
        'test_type':'LOCAL_SUBPROCESS_CRASH_RESTART',
        'actual_worker_process_crashed':True, 'forced_exit_code':CRASH_CODE,
        'interruption_after_completed_steps':CRASH_AFTER,
        'steps':list(STEPS),'modes':results,
        'boundary':{
            'no_ai_model_tested':True,'no_external_api_or_provider':True,
            'no_network':True,'no_real_customer_data':True,
            'guarantee':'SQLite local writes and checkpoint in same transaction ONLY; does not prove external exactly-once effects, crashes between remote effects and ack, distributed queues or production reliability.'
        },
        'publish_approved':False
    }
    payload=json.dumps(record,sort_keys=True,separators=(',',':')).encode('utf-8')
    record['sha256_canonical_core']=hashlib.sha256(payload).hexdigest()
    (out_dir/'evidence.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return record


def main():
    a=argparse.ArgumentParser()
    sub=a.add_subparsers(dest='command', required=True)
    worker=sub.add_parser('worker')
    worker.add_argument('--db',required=True)
    worker.add_argument('--mode',choices=['naive','checkpoint'],required=True)
    worker.add_argument('--phase',type=int,required=True)
    worker.add_argument('--crash',action='store_true')
    run=sub.add_parser('run')
    run.add_argument('--out',required=True)
    args=a.parse_args()
    if args.command=='worker':
        raise SystemExit(execute_worker(args.db,args.mode,args.phase,args.crash))
    record=evaluate(args.out)
    print(json.dumps({'experiment':record['experiment'], 'naive_total':record['modes']['naive']['action_count'], 'guarded_total':record['modes']['checkpoint']['action_count'], 'core_sha256':record['sha256_canonical_core']},indent=2))

if __name__=='__main__':main()
