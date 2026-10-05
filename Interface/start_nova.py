import os
import subprocess


PROJECT_ROOT = r"C:\Nova"

PYTHONW = os.path.join(
    PROJECT_ROOT,
    ".venv1",
    "Scripts",
    "pythonw.exe"
)

UI_FILE = os.path.join(
    PROJECT_ROOT,
    "Interface",
    "nova_ui_pyqt.py"
)


if __name__ == "__main__":

    subprocess.Popen(
        [PYTHONW, UI_FILE],
        cwd=PROJECT_ROOT,
        creationflags=subprocess.CREATE_NO_WINDOW
    )