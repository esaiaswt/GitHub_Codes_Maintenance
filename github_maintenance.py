import os
import subprocess
import re

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
    """
    # Example patterns: (pattern, suggestion, note)
    deprecated_patterns = [
        (r'tf\.Session\(', 'Remove tf.Session and use eager execution (TensorFlow 2.x).', 'TensorFlow 1.x session-based code is deprecated.'),
        (r'tf\.placeholder\(', 'Use tf.Variable or tf.Tensor (TensorFlow 2.x).', 'tf.placeholder is deprecated in TensorFlow 2.x.'),
        (r'tf\.contrib', 'Find alternative in tf.* or external packages.', 'tf.contrib module is removed in TensorFlow 2.x.'),
        (r'pandas\.Panel', 'Use MultiIndex DataFrames or xarray.', 'pandas.Panel is deprecated.'),
        (r'sklearn\.cross_validation', 'Use sklearn.model_selection.', 'sklearn.cross_validation is deprecated.'),
        (r'torch\.autograd\.Variable', 'Use plain tensors with requires_grad=True.', 'torch.autograd.Variable is deprecated.'),
        (r'cv2\.findContours\([^,]+,[^,]+,[^,]+\)', 'Check OpenCV 4.x API for findContours return values.', 'cv2.findContours return signature changed in OpenCV 4.x.'),
        # Add more patterns as needed
    ]
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
    Write a report of deprecated code findings and suggestions.
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
                f.write(f"  Suggestion: {item['suggestion']}\n\n")
    print(f"Deprecation report written to {report_path}")

def auto_replace_deprecated_code(repo_dir, findings, log_path="code_change_log.txt"):
    """
    With user permission, automatically replace deprecated code patterns with suggestions.
    Log all changes to a log file.
    """
    if not findings:
        print("No deprecated code patterns to replace.")
        return
    print("\nThe following deprecated code patterns were found:")
    for idx, item in enumerate(findings, 1):
        print(f"{idx}. {item['file']} (Line {item['line']}): {item['code']}")
        print(f"   Suggestion: {item['suggestion']}")
    user_choice = input("\nDo you want to automatically replace all deprecated code with the suggested replacements? (y/n): ").strip().lower()
    if user_choice != 'y':
        print("No changes made.")
        return
    from collections import defaultdict
    file_changes = defaultdict(list)
    for item in findings:
        file_changes[item['file']].append(item)
    log_entries = []
    for file_path, changes in file_changes.items():
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        for item in changes:
            line_idx = item['line'] - 1
            old_line = lines[line_idx].rstrip('\n')
            new_lines = [f"# DEPRECATED: {item['code']}\n", f"# SUGGESTION: {item['suggestion']}\n"]
            lines[line_idx] = ''.join(new_lines)
            log_entries.append(f"File: {file_path}\nLine: {item['line']}\nOld: {old_line}\nNew: {''.join(new_lines).rstrip()}\n---\n")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Updated deprecated code in {file_path}.")
    # Write log
    with open(log_path, 'w', encoding='utf-8') as logf:
        logf.writelines(log_entries)
    print(f"Code change log written to {log_path}")

def main():
    repo_dir = "cloned_repo"
    if not os.path.exists(repo_dir) or not os.path.isdir(repo_dir) or not os.listdir(repo_dir):
        repo_url = input("Enter the GitHub repository URL: ")
        clone_github_repo(repo_url)
    else:
        print(f"Repository already cloned in '{repo_dir}'.")
        user_choice = input("Do you want to delete the existing cloned repository and clone a new one? (y/n): ").strip().lower()
        if user_choice == 'y':
            subprocess.run(["rmdir", "/s", "/q", repo_dir], shell=True)
            print(f"Deleted '{repo_dir}'.")
            repo_url = input("Enter the GitHub repository URL: ")
            clone_github_repo(repo_url)
        else:
            print("Skipping clone. Using the existing cloned repository.")
    imports = scan_imports_in_repo(repo_dir)
    write_import_report(imports)
    findings = scan_deprecated_code(repo_dir)
    write_deprecation_report(findings)
    auto_replace_deprecated_code(repo_dir, findings)

if __name__ == "__main__":
    main()
