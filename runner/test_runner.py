import sys
import json
import requests
import logging
import time
from datetime import datetime

LOG_FILE = 'runner/test_log.txt'
TV_BASE = 'http://127.0.0.1:5000'

# Setup logging
logger = logging.getLogger('test_runner')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Helper functions

def log_pass(msg):
    logger.info('[PASS] ' + msg)

def log_fail(msg):
    logger.error('[FAIL] ' + msg)

def do_action(action):
    t0 = time.time()
    try:
        name = action.get('action')
        if name == 'power_on':
            r = requests.post(f'{TV_BASE}/power', json={'on': True}, timeout=5)
            r.raise_for_status()
            log_pass('Power ON')
        elif name == 'power_off':
            r = requests.post(f'{TV_BASE}/power', json={'on': False}, timeout=5)
            r.raise_for_status()
            log_pass('Power OFF')
        elif name == 'open_app' or name == 'launch_app':
            app = action.get('app')
            r = requests.post(f'{TV_BASE}/app/launch', json={'app': app}, timeout=5)
            if r.status_code == 200:
                log_pass(f'Open App: {app}')
            else:
                log_fail(f'Open App: {app} -> {r.status_code} {r.text}')
        elif name == 'play':
            title = action.get('title')
            r = requests.post(f'{TV_BASE}/app/play', json={'title': title}, timeout=5)
            if r.status_code == 200:
                log_pass(f'Play: {title}')
            else:
                log_fail(f'Play: {title} -> {r.status_code} {r.text}')
        elif name == 'wait':
            secs = action.get('seconds', 1)
            time.sleep(secs)
            logger.info(f'[INFO] Waited {secs}s')
        elif name == 'check_status':
            expect = action.get('expect')
            r = requests.get(f'{TV_BASE}/status', timeout=5)
            r.raise_for_status()
            js = r.json()
            ok = False
            if expect == 'App loaded':
                ok = js.get('app') is not None
            elif expect == 'Playing':
                ok = js.get('playing') is True
            if ok:
                log_pass(f'Check: {expect}')
            else:
                log_fail(f'Check: {expect} -> state={js}')
        else:
            logger.warning('[INFO] Unknown action ' + str(name))
    except Exception as e:
        log_fail(f'Exception during action {action}: {e}')
    finally:
        duration = time.time() - t0
        logger.info(f'[INFO] Action duration: {duration:.2f}s')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python runner/test_runner.py path/to/flow.json')
        sys.exit(1)
    flow_file = sys.argv[1]
    with open(flow_file, 'r') as f:
        flow = json.load(f)

    logger.info('=== TEST RUN START ===')
    for step in flow.get('steps', []):
        do_action(step)
    logger.info('=== TEST RUN END ===')
    print('Test run complete. Log saved to', LOG_FILE)
