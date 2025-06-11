import requests
import re

def fetch_tensorflow_deprecations():
    # Example: Fetch TensorFlow 2.x release notes for deprecations
    url = "https://raw.githubusercontent.com/tensorflow/tensorflow/master/RELEASE.md"
    resp = requests.get(url)
    patterns = []
    if resp.status_code == 200:
        for line in resp.text.splitlines():
            if "deprecated" in line.lower():
                # Try to extract function/class/module names
                match = re.findall(r'`([^`]+)`', line)
                for m in match:
                    patterns.append((re.escape(m), f"Check TensorFlow docs for replacement of {m}.", "TensorFlow deprecation notice."))
    return patterns

def fetch_pandas_deprecations():
    url = "https://raw.githubusercontent.com/pandas-dev/pandas/main/RELEASE.md"
    resp = requests.get(url)
    patterns = []
    if resp.status_code == 200:
        for line in resp.text.splitlines():
            if "deprecated" in line.lower():
                match = re.findall(r'`([^`]+)`', line)
                for m in match:
                    patterns.append((re.escape(m), f"Check pandas docs for replacement of {m}.", "pandas deprecation notice."))
    return patterns

def fetch_sklearn_deprecations():
    url = "https://raw.githubusercontent.com/scikit-learn/scikit-learn/main/doc/whats_new/v1.4.rst"
    resp = requests.get(url)
    patterns = []
    if resp.status_code == 200:
        for line in resp.text.splitlines():
            if "deprecated" in line.lower():
                match = re.findall(r'`([^`]+)`', line)
                for m in match:
                    patterns.append((re.escape(m), f"Check scikit-learn docs for replacement of {m}.", "scikit-learn deprecation notice."))
    return patterns

def fetch_torch_deprecations():
    url = "https://raw.githubusercontent.com/pytorch/pytorch/main/RELEASE.md"
    resp = requests.get(url)
    patterns = []
    if resp.status_code == 200:
        for line in resp.text.splitlines():
            if "deprecated" in line.lower():
                match = re.findall(r'`([^`]+)`', line)
                for m in match:
                    patterns.append((re.escape(m), f"Check PyTorch docs for replacement of {m}.", "PyTorch deprecation notice."))
    return patterns

def fetch_opencv_deprecations():
    url = "https://raw.githubusercontent.com/opencv/opencv/master/doc/ChangeLog.md"
    resp = requests.get(url)
    patterns = []
    if resp.status_code == 200:
        for line in resp.text.splitlines():
            if "deprecated" in line.lower():
                match = re.findall(r'`([^`]+)`', line)
                for m in match:
                    patterns.append((re.escape(m), f"Check OpenCV docs for replacement of {m}.", "OpenCV deprecation notice."))
    return patterns

def get_all_deprecated_patterns():
    patterns = []
    patterns += fetch_tensorflow_deprecations()
    patterns += fetch_pandas_deprecations()
    patterns += fetch_sklearn_deprecations()
    patterns += fetch_torch_deprecations()
    patterns += fetch_opencv_deprecations()
    return patterns
