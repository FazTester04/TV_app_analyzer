# TV App Test & Log Analyzer — Full Project (with GUI, Flow Builder & Packaging)

## 🚀 Quick Start

1. Create and activate a virtual environment (recommended)
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Start the dashboard:

   ```bash
   python dashboard/dashboard.py
   ```
4. Use the dashboard to:

   * Start or stop the mock TV server
   * Build JSON test flows via Flow Builder
   * Run test flows and view logs
   * Analyze logs and generate visual reports
   * Package the project into a ZIP file

---

##  Project Structure

```
tv-test-analyzer/
│
├── dashboard/            # GUI dashboard (main control panel)
│   └── dashboard.py
│
├── tools/                # Tools and utilities
│   └── flow_builder.py   # Interactive JSON flow builder
│
├── runner/               # Test execution engine
│   ├── test_runner.py    # Executes flow JSON files and logs results
│   └── test_log.txt      # Test log output
│
├── mock_tv/              # Mock TV API (Flask server)
│   └── server.py
│
├── analyzer/             # Log and report analyzers
│   └── log_analyzer.py
│
├── reports/              # Charts and generated summaries
│   └── report_generator.py
│
├── examples/             # Sample test flows
│   └── sample_flow.json
│
└── README.md
```

---

## Flow Builder

The **Flow Builder** allows you to create and customize test flows interactively — without editing JSON manually.

### 🔹 Launch Flow Builder

* From the dashboard: click **“Build Test Flow (JSON)”**
* Or manually from terminal:

  ```bash
  python tools/flow_builder.py
  ```

### 🔹 Flow Builder Features

* Add steps such as `power_on`, `launch_app`, `play`, `wait`, or `check_status`
* Enter parameters (e.g., app name or wait time)
* Save your flow as a `.json` file under `/flows` or `/examples`

Example flow JSON:

```json
{
  "steps": [
    {"action": "power_on"},
    {"action": "launch_app", "app": "YouTube"},
    {"action": "play", "title": "Sony Demo Clip"},
    {"action": "check_status", "expect": "Playing"},
    {"action": "power_off"}
  ]
}
```

---

## Running Test Flows

### From the Dashboard

1. Click **“Run Test Flow”**
2. Select a JSON flow file from `examples/` or `flows/`
3. View logs directly inside the dashboard after execution

### From the Command Line

```bash
python runner/test_runner.py examples/sample_flow.json
```

If you run without arguments, the script will prompt you to select or use the default flow.

---

---

##  Reports and Log Analysis

1. After tests, logs are written to:

   ```
   runner/test_log.txt
   ```
2. Click **“Analyze Logs & Generate Report”** in the dashboard or run manually:

   ```bash
   python analyzer/log_analyzer.py runner/test_log.txt
   python reports/report_generator.py runner/test_log.txt
   ```
3. Charts are saved to `/reports/pass_fail.png` and opened automatically.

---

---

## System Flow Overview

```
Flow Builder  →  JSON Flow File  →  Test Runner  →  Flask Mock TV  →  Log + Report  →  Dashboard Display
```

---

##  Requirements

* Python 3.9+
* Flask
* requests
* tkinter

---

**Author:** Fazni Alif — Sony TV R&D Technical Demo

**Purpose:** Demonstrate an end-to-end TV test automation system using Python (Flask + Tkinter + JSON).
