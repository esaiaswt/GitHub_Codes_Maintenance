import os
import subprocess
import re
import streamlit as st
from deprecation_fetchers import get_all_deprecated_patterns
import time
import keyboard
import psutil

# List of deprecated libraries and their suggested replacements
DEPRECATED_LIBRARIES = {
    'tensorflow': {
        'deprecated_versions': ['1.x'],
        'replacement': 'tensorflow>=2.0',
        'note': 'Upgrade to TensorFlow 2.x for better support and features.'
    },
    'pandas': {
        'deprecated_versions': ['0.x'],
        'replacement': 'pandas>=1.0',
        'note': 'Upgrade to pandas 1.x or newer.'
    },
    'scikit-learn': {
        'deprecated_versions': ['0.19', '0.20'],
        'replacement': 'scikit-learn>=1.0',
        'note': 'Upgrade to scikit-learn 1.x or newer.'
    },
    'torch': {
        'deprecated_versions': ['0.x', '1.0', '1.1'],
        'replacement': 'torch>=1.10',
        'note': 'Upgrade to PyTorch 1.10 or newer.'
    },
    'cv2': {
        'deprecated_versions': ['3.x'],
        'replacement': 'opencv-python>=4.0',
        'note': 'Upgrade to OpenCV 4.x or newer.'
    },
    # Add more as needed
}

def clone_github_repo(repo_url, clone_dir="cloned_repo"):
    """
    Clone the GitHub repository to a local directory.
    """
    if os.path.exists(clone_dir):
        print(f"Directory '{clone_dir}' already exists. Removing it...")
        subprocess.run(["rm", "-rf", clone_dir], shell=True)
    print(f"Cloning {repo_url} into {clone_dir}...")
    result = subprocess.run(["git", "clone", repo_url, clone_dir], capture_output=True, text=True)
    if result.returncode == 0:
        print("Repository cloned successfully.")
    else:
        print(f"Error cloning repository: {result.stderr}")

def scan_imports_in_repo(repo_dir):
    """
    Scan all Python files in the repo for import statements and collect libraries used.
    """
    imports = set()
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        # Match 'import x' or 'from x import y'
                        match = re.match(r'\s*(import|from)\s+([\w\.]+)', line)
                        if match:
                            imports.add(match.group(2).split('.')[0])
    return sorted(imports)

def check_deprecated_libraries(imports):
    """
    Check for deprecated libraries and suggest replacements.
    """
    deprecated_found = []
    for lib in imports:
        if lib in DEPRECATED_LIBRARIES:
            deprecated_found.append({
                'library': lib,
                'replacement': DEPRECATED_LIBRARIES[lib]['replacement'],
                'note': DEPRECATED_LIBRARIES[lib]['note']
            })
    return deprecated_found

def write_import_report(imports, report_path="import_report.txt"):
    """
    Write the list of imports and deprecated libraries to a report file.
    """
    with open(report_path, 'w') as f:
        f.write("Imported libraries found in the repository:\n")
        for lib in imports:
            f.write(f"- {lib}\n")
        f.write("\n---\n")
        deprecated = check_deprecated_libraries(imports)
        if deprecated:
            f.write("Deprecated libraries detected and suggestions:\n")
            for item in deprecated:
                f.write(f"- {item['library']}: {item['note']}\n  Suggested replacement: {item['replacement']}\n")
        else:
            f.write("No deprecated libraries detected.\n")
    print(f"Import report written to {report_path}")

def scan_deprecated_code(repo_dir):
    """
    Scan all Python files for known deprecated code patterns and suggest replacements.
    Patterns are fetched dynamically from official library repos.
    """
    deprecated_patterns = get_all_deprecated_patterns()
    findings = []
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        for pattern, suggestion, note in deprecated_patterns:
                            if re.search(pattern, line):
                                findings.append({
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'note': note,
                                    'suggestion': suggestion
                                })
    return findings

def write_deprecation_report(findings, report_path="deprecation_report.txt"):
    """
    Write a detailed report of deprecated code findings and suggestions, including context for VS Code agent updates.
    """
    with open(report_path, 'w', encoding='utf-8') as f:
        if not findings:
            f.write("No deprecated code patterns found.\n")
        else:
            f.write("Deprecated code patterns detected and suggestions:\n\n")
            for item in findings:
                f.write(f"File: {item['file']} (Line {item['line']})\n")
                f.write(f"  Code: {item['code']}\n")
                f.write(f"  Note: {item['note']}\n")
                f.write(f"  Suggestion: {item['suggestion']}\n")
                f.write(f"  --- VS Code Agent Instructions ---\n")
                f.write(f"  - Locate the above code in the specified file and line.\n")
                f.write(f"  - Review the context and the deprecation note.\n")
                f.write(f"  - Apply the suggested replacement or follow the suggestion to update the code.\n")
                f.write(f"  - Test the updated code to ensure it works as expected.\n")
                f.write(f"  - If the suggestion is unclear, refer to the official documentation for the library.\n\n")
    print(f"Deprecation report written to {report_path}")

def main():
    st.title("GitHub Codes Maintenance Tool")
    st.markdown("""
    **Usage Instructions:**
    1. Enter a public GitHub repository URL below and click **Clone Repository**.
    2. Once cloned, click **Scan Repository for Deprecations** to analyze the code.
    3. View the generated import and deprecation reports directly in the app.
    4. Use **🔄 Rerun App** to refresh, or **🛑 Shutdown App** to close the app and browser tab.
    """)
    repo_dir = "cloned_repo"
    rerun = st.button("🔄 Rerun App")
    if rerun:
        st.rerun()
    # Section: Clone or reuse repo
    if not os.path.exists(repo_dir) or not os.path.isdir(repo_dir) or not os.listdir(repo_dir):
        repo_url = st.text_input("Enter the GitHub repository URL:")
        if st.button("Clone Repository") and repo_url:
            with st.spinner("Cloning repository..."):
                clone_github_repo(repo_url)
            st.success("Repository cloned successfully.")
    else:
        st.info(f"Repository already cloned in '{repo_dir}'.")
        if st.button("Delete and Clone New Repository"):
            subprocess.run(["rmdir", "/s", "/q", repo_dir], shell=True)
            st.success(f"Deleted '{repo_dir}'. Please enter a new GitHub repository URL and clone again.")
            st.stop()
    # Section: Scan and report
    if os.path.exists(repo_dir) and os.path.isdir(repo_dir) and os.listdir(repo_dir):
        if st.button("Scan Repository for Deprecations"):
            with st.spinner("Scanning for imports and deprecated code..."):
                imports = scan_imports_in_repo(repo_dir)
                write_import_report(imports)
                findings = scan_deprecated_code(repo_dir)
                write_deprecation_report(findings)
            st.success("Scan complete. Reports generated.")
            # Display import report
            st.subheader("Import Report")
            with open("import_report.txt", "r", encoding="utf-8") as f:
                st.text(f.read())
            # Display deprecation report
            st.subheader("Deprecation Report")
            with open("deprecation_report.txt", "r", encoding="utf-8") as f:
                st.text(f.read())
    # Shutdown button at the bottom
    st.markdown("---")
    shutdown = st.button("🛑 Shutdown App")
    if shutdown:
        st.success("Shutting down the app. The browser tab will close automatically.")
        st.markdown("""
            <script>
                window.open('','_self').close();
            </script>
        """, unsafe_allow_html=True)
        # Give a bit of delay for user experience
        time.sleep(0.5)
        # Close streamlit browser tab
        keyboard.press_and_release('ctrl+w')
        # Terminate streamlit python process
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()
        st.stop()

if __name__ == "__main__":
    main()
