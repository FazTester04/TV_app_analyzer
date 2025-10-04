import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Usage: python reports/report_generator.py path/to/test_log.txt")
        sys.exit(1)

    csv_path = os.path.join("runner", "log_summary.csv")

    if not os.path.exists(csv_path):
        print(f"[ERROR] Missing file: {csv_path}")
        print("Please run log_analyzer.py first to generate it.")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            print("[ERROR] log_summary.csv is empty — no data to plot.")
            sys.exit(1)
        summary = df['status'].value_counts()
        print(summary)
        colors = []
        for status in summary.index:
            if status.upper() == "PASS":
                colors.append("green")
            elif status.upper() == "FAIL":
                colors.append("red")
            else:
                colors.append("gray")

        fig, ax = plt.subplots(figsize=(6, 4))
        summary.plot(kind="bar", color=colors, ax=ax)

        for i, count in enumerate(summary.values):
            ax.text(i, count + 0.1, str(count), ha='center', va='bottom', fontweight='bold')

        plt.title("Test Results (PASS vs FAIL)")
        plt.xlabel("Status")
        plt.ylabel("Count")
        plt.tight_layout()

        # Save bar chart
        out_img_bar = os.path.join("reports", "pass_fail.png")
        plt.savefig(out_img_bar)
        print(f"[OK] Saved bar chart to {out_img_bar}")

    except Exception as e:
        print(f"[ERROR] Failed to generate report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
