import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python reports/report_generator.py path/to/test_log.txt')
        sys.exit(1)
    # log_summary.csv should be created by analyzer
    df = pd.read_csv('runner/log_summary.csv')
    summary = df['status'].value_counts()
    print(summary)
    summary.plot(kind='bar')
    plt.title('Test Results (PASS vs FAIL)')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.tight_layout()
    out_img = 'reports/pass_fail.png'
    plt.savefig(out_img)
    print('Saved chart to', out_img)
