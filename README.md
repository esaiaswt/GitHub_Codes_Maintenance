# GitHub Codes Maintenance Tool

This Streamlit-based Python application helps you maintain GitHub repositories by:
- Scanning for deprecated libraries and code patterns (especially for Colab and ML projects)
- Dynamically fetching deprecation patterns from official library repositories (TensorFlow, pandas, scikit-learn, PyTorch, OpenCV)
- Generating reports of imports and code deprecations
- Suggesting and optionally automating code replacements (with user permission via UI)
- Logging all automated code changes for traceability

## Features
- **Clone any public GitHub repository**
- **Detect deprecated imports and code patterns**
- **Generate `import_report.txt` and `deprecation_report.txt`**
- **Automate code replacement with user approval (via Streamlit UI)**
- **Log all changes in `code_change_log.txt`**
- **Rerun and shutdown the app from the UI**

## How It Works
1. **Clone a Repository:**
   - Enter a GitHub repository URL in the UI and click "Clone Repository" (unless a repo is already cloned).
   - If a repository is already cloned, you can choose to delete it and clone a new one.
2. **Scan for Deprecations:**
   - Click "Scan Repository for Deprecations" to scan all Python files for deprecated imports and code patterns.
   - The tool fetches deprecation patterns dynamically from official library repos.
   - It generates `import_report.txt` (all imports and deprecated libraries) and `deprecation_report.txt` (all deprecated code patterns found).
3. **Automated Code Replacement:**
   - If deprecated code is found, you will be prompted to approve automated replacements via the UI.
   - Deprecated lines are commented out and suggestions are inserted above them.
   - All changes are logged in `code_change_log.txt`.
4. **Rerun or Shutdown:**
   - Use the "🔄 Rerun App" button to refresh the app, or the "🛑 Shutdown App" button at the bottom to close the app and browser tab.

## Usage
1. Make sure you have Python 3.7+ and Git installed.
2. Install requirements:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the app:
   ```powershell
   streamlit run github_maintenance.py
   ```
4. Follow the prompts in the browser UI.

## Example Output
```
Imported libraries found in the repository:
- tensorflow
- pandas
...
Deprecated libraries detected and suggestions:
- tensorflow: Upgrade to TensorFlow 2.x for better support and features.
  Suggested replacement: tensorflow>=2.0
...
The following deprecated code patterns were found:
1. cloned_repo/example.py (Line 10): tf.Session(...)
   Suggestion: Remove tf.Session and use eager execution (TensorFlow 2.x).
```

## Output Files
- `import_report.txt`: List of all imports and deprecated libraries found.
- `deprecation_report.txt`: List of all deprecated code patterns and suggestions (dynamically fetched).
- `code_change_log.txt`: Log of all automated code changes (file, line, old/new code).

## License
MIT
