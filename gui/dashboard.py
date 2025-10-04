import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MOCK_CMD = ['python', os.path.join(ROOT, 'mock_tv', 'server.py')]
RUNNER_CMD = ['python', os.path.join(ROOT, 'runner', 'test_runner.py'), os.path.join(ROOT, 'examples', 'sample_flow.json')]
ANALYZER_CMD = ['python', os.path.join(ROOT, 'analyzer', 'log_analyzer.py'), os.path.join(ROOT, 'runner', 'test_log.txt')]
REPORT_CMD = ['python', os.path.join(ROOT, 'reports', 'report_generator.py'), os.path.join(ROOT, 'runner', 'test_log.txt')]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TV Test & Log Analyzer - Dashboard')
        self.geometry('900x600')

        self.create_widgets()
        self.mock_proc = None
        self.runner_proc = None

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill='both', expand=True)

        left = ttk.Frame(frm)
        left.pack(side='left', fill='y', padx=(0,10))

        ttk.Label(left, text='Controls', font=('Segoe UI', 12, 'bold')).pack(pady=(0,10))

        btn_start_mock = ttk.Button(left, text='Start Mock TV Server', command=self.start_mock)
        btn_start_mock.pack(fill='x', pady=4)

        btn_stop_mock = ttk.Button(left, text='Stop Mock TV Server', command=self.stop_mock)
        btn_stop_mock.pack(fill='x', pady=4)

        btn_run_tests = ttk.Button(left, text='Run Test Flow', command=self.run_tests)
        btn_run_tests.pack(fill='x', pady=4)

        btn_generate_report = ttk.Button(left, text='Analyze Logs & Generate Report', command=self.generate_report)
        btn_generate_report.pack(fill='x', pady=4)

        ttk.Separator(left, orient='horizontal').pack(fill='x', pady=10)
        ttk.Label(left, text='Logs', font=('Segoe UI', 12, 'bold')).pack(pady=(0,6))

        btn_refresh = ttk.Button(left, text='Refresh Log View', command=self.load_log)
        btn_refresh.pack(fill='x', pady=4)

        btn_open_report = ttk.Button(left, text='Open Generated Chart', command=self.open_chart)
        btn_open_report.pack(fill='x', pady=4)

        # Right: Text area
        right = ttk.Frame(frm)
        right.pack(side='right', fill='both', expand=True)

        self.log_text = tk.Text(right, wrap='none')
        self.log_text.pack(fill='both', expand=True)

        # initial load
        self.load_log()

    def start_mock(self):
        if self.mock_proc and self.mock_proc.poll() is None:
            messagebox.showinfo('Mock Server', 'Mock server already running')
            return
        def target():
            self.append('Starting mock TV server...\n')
            self.mock_proc = subprocess.Popen(MOCK_CMD, cwd=ROOT)
            self.append(f'Mock server started (pid={self.mock_proc.pid})\n')
        threading.Thread(target=target, daemon=True).start()

    def stop_mock(self):
        if self.mock_proc and self.mock_proc.poll() is None:
            self.append('Stopping mock server...\n')
            self.mock_proc.terminate()
            try:
                self.mock_proc.wait(timeout=3)
            except Exception:
                self.mock_proc.kill()
            self.append('Mock server stopped.\n')
            self.mock_proc = None
        else:
            messagebox.showinfo('Mock Server', 'No mock server running')

    def run_tests(self):
        def target():
            self.append('Running test flow...\n')
            try:
                self.runner_proc = subprocess.Popen(RUNNER_CMD, cwd=ROOT)
                out, err = self.runner_proc.communicate()
                self.append('Test runner finished.\n')
            except Exception as e:
                self.append(f'Error running tests: {e}\n')
            self.load_log()
        threading.Thread(target=target, daemon=True).start()

    def generate_report(self):
        def target():
            self.append('Analyzing logs and generating report...\n')
            try:
                subprocess.run(ANALYZER_CMD, cwd=ROOT, check=True)
                subprocess.run(REPORT_CMD, cwd=ROOT, check=True)
                self.append('Report generated (check runner/log_summary.csv and reports/pass_fail.png)\n')
            except subprocess.CalledProcessError as e:
                self.append(f'Error generating report: {e}\n')
            self.load_log()
        threading.Thread(target=target, daemon=True).start()

    def package_project(self):
        def target():
            self.append('Packaging project into zip...\n')
            try:
                subprocess.run(['python', os.path.join(ROOT, 'make_package.py')], cwd=ROOT, check=True)
                self.append('Packaged to tv-test-analyzer.zip in project root.\n')
            except subprocess.CalledProcessError as e:
                self.append(f'Packaging failed: {e}\n')
        threading.Thread(target=target, daemon=True).start()

    def load_log(self):
        path = os.path.join(ROOT, 'runner', 'test_log.txt')
        self.log_text.delete('1.0', tk.END)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                self.log_text.insert(tk.END, f.read())
        else:
            self.log_text.insert(tk.END, 'No test_log.txt found. Run tests first.')

    def open_chart(self):
        path = os.path.join(ROOT, 'reports', 'pass_fail.png')
        if os.path.exists(path):
            try:
                if os.name == 'nt':
                    os.startfile(path)
                else:
                    subprocess.run(['xdg-open', path])
            except Exception as e:
                messagebox.showerror('Open Chart', f'Could not open chart: {e}')
        else:
            messagebox.showinfo('Open Chart', 'Chart not found. Generate report first.')

    def append(self, text):
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)

if __name__ == '__main__':
    app = App()
    app.mainloop()
