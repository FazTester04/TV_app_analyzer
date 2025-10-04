import sys
import re
import pandas as pd
from collections import Counter

LOG_PATTERN = re.compile(r"^(?P<ts>[^|]+) \| (?P<level>[^|]+) \| (?P<msg>.*)$")

def parse_log(path):
    entries = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = LOG_PATTERN.match(line)
            if not m:
                continue
            ts = m.group('ts').strip()
            level = m.group('level').strip()
            msg = m.group('msg').strip()
            status = None
            action = None
            error = None
            if msg.startswith('[PASS]'):
                status = 'PASS'
                action = msg[len('[PASS]'):].strip()
            elif msg.startswith('[FAIL]'):
                status = 'FAIL'
                action = msg[len('[FAIL]'):].strip()
            elif msg.startswith('[INFO]'):
                status = 'INFO'
                action = msg[len('[INFO]'):].strip()
            else:
                action = msg
            err_match = re.search(r'\\{.*\\}|code\\": \\"(?P<code>[A-Za-z0-9_]+)\\"', msg)
            if err_match:
                error = err_match.groupdict().get('code')
            entries.append({'timestamp': ts, 'level': level, 'status': status, 'action': action, 'error': error})
    return pd.DataFrame(entries)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python analyzer/log_analyzer.py path/to/test_log.txt')
        sys.exit(1)
    path = sys.argv[1]
    df = parse_log(path)
    if df.empty:
        print('No log entries parsed')
        sys.exit(0)
    total = len(df[df['status'].isin(['PASS','FAIL'])])
    passes = len(df[df['status'] == 'PASS'])
    fails = len(df[df['status'] == 'FAIL'])
    print(f'Total assertions: {total}  PASS: {passes}  FAIL: {fails}')

    common = df[df['status']=='FAIL']['action'].value_counts().head(10)
    print('\nTop failures:')
    print(common)

    out_csv = 'runner/log_summary.csv'
    df.to_csv(out_csv, index=False)
    print('Saved summary to', out_csv)
