# TV App Test & Log Analyzer — Full Project (with GUI & Packaging)

## Quick start

1. Create and activate a virtualenv (recommended).
2. Install requirements: `pip install -r requirements.txt`.
3. Start the GUI: `python gui/dashboard.py`.
4. Use the GUI to start the mock server, run tests, analyze logs, and package the project.

## Manual CLI usage

1. Start mock TV server:
   `python mock_tv/server.py`
2. Run a test flow:
   `python runner/test_runner.py examples/sample_flow.json`
3. Analyze logs and generate CSV:
   `python analyzer/log_analyzer.py runner/test_log.txt`
4. Generate chart:
   `python reports/report_generator.py runner/test_log.txt`
5. Package project:
   `python make_package.py`

## GUI Dashboard

- The dashboard can start/stop the mock server, run the test runner, analyze logs,
  view the latest log content, open the generated chart, and create a ZIP package.

Notes:
- Keep the terminal open if you want to see Flask console output when starting the mock server.
- On Windows the GUI uses os.startfile to open the generated chart; on Linux it will try xdg-open.

