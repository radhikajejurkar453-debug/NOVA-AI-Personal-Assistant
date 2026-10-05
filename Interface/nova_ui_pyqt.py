
import sys
import math
import os
import subprocess
import multiprocessing

from pathlib import Path

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPoint,
    QRect,
    QObject,
    pyqtSignal,
    QPropertyAnimation,
    QEasingCurve
)

from PyQt5.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
    QRadialGradient
)

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsOpacityEffect,
    QPushButton,
    QScrollArea,
    QSplitter
)


# ============================================================
# PATHS
# ============================================================

NOVA_ROOT = Path(
    r"C:\Nova"
)

NOVA_UI_FILE = (
    NOVA_ROOT
    / "Interface"
    / "nova_ui_pyqt.py"
)

VENV_PYTHON = (
    NOVA_ROOT
    / ".venv1"
    / "Scripts"
    / "python.exe"
)

VENV_PYTHONW = (
    NOVA_ROOT
    / ".venv1"
    / "Scripts"
    / "pythonw.exe"
)

STARTUP_FOLDER = (
    Path(
        os.environ.get(
            "APPDATA",
            ""
        )
    )
    / "Microsoft"
    / "Windows"
    / "Start Menu"
    / "Programs"
    / "Startup"
)

STARTUP_SHORTCUT = (
    STARTUP_FOLDER
    / "Nova_UI_Startup.lnk"
)

OLD_STARTUP_VBS = (
    STARTUP_FOLDER
    / "Nova_UI_Startup.vbs"
)


# ============================================================
# NOVA PROJECT PATH
# ============================================================

if str(NOVA_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(NOVA_ROOT)
    )

os.chdir(
    str(NOVA_ROOT)
)


# ============================================================
# WINDOWS STARTUP
# ============================================================

def setup_windows_startup():

    try:

        STARTUP_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Remove old VBS startup file
        # ----------------------------------------------------

        if OLD_STARTUP_VBS.exists():

            try:

                OLD_STARTUP_VBS.unlink()

                print(
                    "[NOVA UI] Old VBS startup file removed."
                )

            except Exception as e:

                print(
                    "[NOVA UI] Could not remove old VBS:",
                    e
                )

        # ----------------------------------------------------
        # Select Python executable
        # ----------------------------------------------------

        if VENV_PYTHONW.exists():

            python_executable = (
                VENV_PYTHONW
            )

        elif VENV_PYTHON.exists():

            python_executable = (
                VENV_PYTHON
            )

        else:

            python_executable = Path(
                sys.executable
            )

        # ----------------------------------------------------
        # Remove old shortcut
        # ----------------------------------------------------

        if STARTUP_SHORTCUT.exists():

            try:

                STARTUP_SHORTCUT.unlink()

            except Exception as e:

                print(
                    "[NOVA UI] Could not remove old shortcut:",
                    e
                )

        # ----------------------------------------------------
        # Escape PowerShell strings
        # ----------------------------------------------------

        shortcut_path = str(
            STARTUP_SHORTCUT
        ).replace(
            "'",
            "''"
        )

        target_path = str(
            python_executable
        ).replace(
            "'",
            "''"
        )

        script_path = str(
            NOVA_UI_FILE
        ).replace(
            "'",
            "''"
        )

        working_directory = str(
            NOVA_ROOT
        ).replace(
            "'",
            "''"
        )

        # ----------------------------------------------------
        # PowerShell shortcut
        # ----------------------------------------------------

        powershell_script = (
            "$WshShell = "
            "New-Object -ComObject WScript.Shell; "

            f"$Shortcut = "
            f"$WshShell.CreateShortcut('{shortcut_path}'); "

            f"$Shortcut.TargetPath = "
            f"'{target_path}'; "

            f"$Shortcut.Arguments = "
            f"'\"{script_path}\"'; "

            f"$Shortcut.WorkingDirectory = "
            f"'{working_directory}'; "

            "$Shortcut.Description = "
            "'Nova AI Assistant'; "

            "$Shortcut.WindowStyle = 1; "

            "$Shortcut.Save();"
        )

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                powershell_script
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False
        )

        # ----------------------------------------------------
        # Verify
        # ----------------------------------------------------

        if STARTUP_SHORTCUT.exists():

            print(
                "[NOVA UI] Windows startup enabled."
            )

            print(
                "[NOVA UI] Startup shortcut:",
                STARTUP_SHORTCUT
            )

            print(
                "[NOVA UI] Startup executable:",
                python_executable
            )

        else:

            print(
                "[NOVA UI] Startup shortcut could not be created."
            )

            if result.stderr:

                print(
                    "[NOVA UI] PowerShell error:",
                    result.stderr.strip()
                )

    except Exception as e:

        print(
            "[NOVA UI] Startup setup error:",
            e
        )


# ============================================================
# BACKEND PROCESS
# ============================================================

def run_nova_backend(
    event_queue
):

    try:

        nova_root = str(
            NOVA_ROOT
        )

        if nova_root not in sys.path:

            sys.path.insert(
                0,
                nova_root
            )

        os.chdir(
            nova_root
        )

        # ----------------------------------------------------
        # UI bridge
        # ----------------------------------------------------

        from Interface.nova_ui_bridge import (
            set_event_queue
        )

        set_event_queue(
            event_queue
        )

        # ----------------------------------------------------
        # Nova backend
        # ----------------------------------------------------

        from Main.main import nova

        nova()

    except Exception as e:

        import traceback

        error_text = (
            traceback.format_exc()
        )

        print(
            "[NOVA BACKEND ERROR]"
        )

        print(
            error_text
        )

        # ----------------------------------------------------
        # Save backend error
        # ----------------------------------------------------

        try:

            error_file = (
                NOVA_ROOT
                / "Nova_Data"
                / "nova_backend_error.txt"
            )

            error_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            error_file.write_text(
                error_text,
                encoding="utf-8"
            )

        except Exception:

            pass

        # ----------------------------------------------------
        # Send error to UI
        # ----------------------------------------------------

        try:

            event_queue.put(
                (
                    "error",
                    error_text
                ),
                block=False
            )

        except Exception:

            pass


# ============================================================
# COLORS
# ============================================================

COLORS = {

    "SLEEPING": QColor(
        160,
        75,
        255
    ),

    "STARTING": QColor(
        255,
        190,
        45
    ),

    "ACTIVE": QColor(
        255,
        190,
        45
    ),

    "LISTENING": QColor(
        0,
        190,
        255
    ),

    "THINKING": QColor(
        175,
        75,
        255
    ),

    "SPEAKING": QColor(
        0,
        235,
        155
    ),

    "ERROR": QColor(
        255,
        70,
        85
    )
}


# ============================================================
# NETWORK COLORS
# ============================================================

NETWORK_ONLINE_COLOR = QColor(
    83,
    231,
    165
)

NETWORK_OFFLINE_COLOR = QColor(
    255,
    85,
    100
)

NETWORK_UNKNOWN_COLOR = QColor(
    160,
    170,
    195
)


# ============================================================
# NOVA ORB
# ============================================================

class NovaOrb(QWidget):

    double_clicked = pyqtSignal()

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        # ----------------------------------------------------
        # NEVER CHANGE ORB SIZE
        # ----------------------------------------------------

        self.setFixedSize(
            370,
            340
        )

        self.state = "SLEEPING"

        self.angle = 0

        self.pulse = 0

        self.pulse_direction = 1

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(
            28
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

    # ========================================================

    def set_state(
        self,
        state
    ):

        if state not in COLORS:

            state = "SLEEPING"

        self.state = state

        self.update()

    # ========================================================

    def animate(
        self
    ):

        speeds = {

            "SLEEPING": 0.30,
            "STARTING": 1.10,
            "ACTIVE": 0.85,
            "LISTENING": 1.90,
            "THINKING": 3.00,
            "SPEAKING": 2.35,
            "ERROR": 0.60
        }

        self.angle += speeds.get(
            self.state,
            1.0
        )

        pulse_speed = {

            "SLEEPING": 0.45,
            "STARTING": 1.20,
            "ACTIVE": 0.90,
            "LISTENING": 1.80,
            "THINKING": 2.20,
            "SPEAKING": 2.80,
            "ERROR": 1.00

        }.get(
            self.state,
            1.0
        )

        self.pulse += (
            self.pulse_direction
            * pulse_speed
        )

        if self.pulse >= 30:

            self.pulse_direction = -1

        if self.pulse <= 0:

            self.pulse_direction = 1

        self.update()

    # ========================================================

    def mouseDoubleClickEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.double_clicked.emit()

        super().mouseDoubleClickEvent(
            event
        )

    # ========================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        center = QPoint(
            self.width() // 2,
            170
        )

        color = QColor(
            COLORS.get(
                self.state,
                COLORS["SLEEPING"]
            )
        )

        # ====================================================
        # LARGE BACK GLOW
        # ====================================================

        for radius, alpha in [

            (185, 6),
            (170, 8),
            (155, 11),
            (140, 14),
            (125, 19),
            (110, 27)

        ]:

            gradient = QRadialGradient(
                center,
                radius
            )

            glow = QColor(
                color
            )

            glow.setAlpha(
                alpha
            )

            gradient.setColorAt(
                0,
                glow
            )

            gradient.setColorAt(
                1,
                QColor(
                    0,
                    0,
                    0,
                    0
                )
            )

            painter.setBrush(
                QBrush(
                    gradient
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                center,
                radius,
                radius
            )

        # ====================================================
        # ORBIT RINGS
        # ====================================================

        painter.setBrush(
            Qt.NoBrush
        )

        ring_data = [

            (78, 120),
            (92, 105),
            (106, 92),
            (120, 78),
            (134, 62),
            (148, 48),
            (162, 34)

        ]

        for radius, alpha in ring_data:

            ring = QColor(
                color
            )

            ring.setAlpha(
                alpha
            )

            painter.setPen(
                QPen(
                    ring,
                    1.15
                )
            )

            painter.drawEllipse(
                center,
                radius,
                radius
            )

        # ====================================================
        # ROTATING ORBIT ARCS
        # ====================================================

        painter.setBrush(
            Qt.NoBrush
        )

        for i, radius in enumerate(
            [106, 134, 162]
        ):

            arc = QColor(
                color
            )

            arc.setAlpha(
                125
            )

            painter.setPen(
                QPen(
                    arc,
                    2
                )
            )

            start = int(
                (
                    self.angle
                    * (
                        1
                        if i % 2 == 0
                        else -1
                    )
                    + i * 75
                )
                * 16
            )

            span = int(
                (
                    55
                    + i * 12
                )
                * 16
            )

            painter.drawArc(
                QRect(
                    center.x() - radius,
                    center.y() - radius,
                    radius * 2,
                    radius * 2
                ),
                start,
                span
            )

        # ====================================================
        # PARTICLES
        # ====================================================

        particle_count = 42

        for i in range(
            particle_count
        ):

            angle = (
                self.angle
                * (
                    1
                    if i % 2 == 0
                    else -0.65
                )
                + i * 17
            )

            radians = math.radians(
                angle
            )

            radius = (
                92
                + (i % 5) * 15
            )

            x = (
                center.x()
                + math.cos(
                    radians
                ) * radius
            )

            y = (
                center.y()
                + math.sin(
                    radians
                ) * radius
            )

            particle = QColor(
                color
            )

            particle.setAlpha(
                65
                + (i % 6) * 28
            )

            painter.setBrush(
                QBrush(
                    particle
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            size = (
                1
                + (i % 4)
            )

            painter.drawEllipse(
                QPoint(
                    int(x),
                    int(y)
                ),
                size,
                size
            )

        # ====================================================
        # MAIN ORB
        # ====================================================

        orb_radius = (
            60
            + int(
                self.pulse / 6
            )
        )

        orb_gradient = QRadialGradient(
            center,
            orb_radius
        )

        orb_gradient.setColorAt(
            0.0,
            QColor(
                255,
                255,
                255,
                245
            )
        )

        bright = QColor(
            color
        )

        bright.setAlpha(
            255
        )

        orb_gradient.setColorAt(
            0.13,
            bright
        )

        mid = QColor(
            color
        )

        mid.setAlpha(
            195
        )

        orb_gradient.setColorAt(
            0.55,
            mid
        )

        orb_gradient.setColorAt(
            1.0,
            QColor(
                2,
                8,
                30,
                255
            )
        )

        painter.setBrush(
            QBrush(
                orb_gradient
            )
        )

        painter.setPen(
            QPen(
                color,
                2
            )
        )

        painter.drawEllipse(
            center,
            orb_radius,
            orb_radius
        )

        # ====================================================
        # INNER LIGHT
        # ====================================================

        inner = QRadialGradient(
            center,
            58
        )

        inner.setColorAt(
            0,
            QColor(
                255,
                255,
                255,
                235
            )
        )

        inner.setColorAt(
            0.20,
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                225
            )
        )

        inner.setColorAt(
            0.62,
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                80
            )
        )

        inner.setColorAt(
            1,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(
            QBrush(
                inner
            )
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawEllipse(
            center,
            58,
            58
        )

        # ====================================================
        # NOVA TEXT
        # ====================================================

        painter.setPen(
            QColor(
                255,
                255,
                255
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                24,
                QFont.Bold
            )
        )

        painter.drawText(
            QRect(
                center.x() - 90,
                center.y() - 28,
                180,
                56
            ),
            Qt.AlignCenter,
            "NOVA"
        )


# ============================================================
# WAVEFORM
# ============================================================

class Waveform(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setFixedSize(
            380,
            62
        )

        self.state = "SLEEPING"

        self.phase = 0

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(
            35
        )

    # ========================================================

    def set_state(
        self,
        state
    ):

        self.state = state

        self.update()

    # ========================================================

    def animate(
        self
    ):

        self.phase += 1

        self.update()

    # ========================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        if self.state == "SPEAKING":

            color = QColor(
                0,
                235,
                155
            )

        elif self.state == "THINKING":

            color = QColor(
                175,
                75,
                255
            )

        elif self.state in [
            "LISTENING",
            "ACTIVE"
        ]:

            color = QColor(
                0,
                190,
                255
            )

        elif self.state == "STARTING":

            color = QColor(
                255,
                190,
                45
            )

        else:

            color = QColor(
                100,
                110,
                150
            )

        center_y = (
            self.height()
            // 2
        )

        bars = 45

        for i in range(
            bars
        ):

            normalized = (
                i
                / (
                    bars - 1
                )
            )

            distance = abs(
                normalized - 0.5
            )

            if self.state in [

                "LISTENING",
                "THINKING",
                "SPEAKING",
                "ACTIVE"

            ]:

                wave_1 = abs(
                    math.sin(
                        self.phase * 0.17
                        + i * 0.43
                    )
                )

                wave_2 = abs(
                    math.sin(
                        self.phase * 0.08
                        + i * 0.21
                    )
                )

                height = (
                    5
                    + (
                        wave_1 * 26
                        + wave_2 * 15
                    )
                    * (
                        1.0
                        - distance * 0.55
                    )
                )

            elif self.state == "STARTING":

                height = (
                    7
                    + abs(
                        math.sin(
                            self.phase * 0.13
                            + i * 0.25
                        )
                    ) * 16
                )

            else:

                height = 3

            x = (
                8
                + i * (
                    (
                        self.width()
                        - 16
                    )
                    / (
                        bars - 1
                    )
                )
            )

            painter.setPen(
                QPen(
                    color,
                    2
                )
            )

            painter.drawLine(
                int(x),
                int(
                    center_y - height
                ),
                int(x),
                int(
                    center_y + height
                )
            )


# ============================================================
# CHAT MESSAGE
# ============================================================

class ChatMessage(QFrame):

    def __init__(
        self,
        title,
        text,
        is_user,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.is_user = is_user

        self.setObjectName(
            "UserMessage"
            if is_user
            else "NovaMessage"
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            14,
            10,
            14,
            11
        )

        layout.setSpacing(
            4
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.title_label = QLabel(
            title
        )

        if is_user:

            self.title_label.setStyleSheet(
                """
                color: #39c7ff;
                font-size: 8px;
                font-weight: bold;
                letter-spacing: 2px;
                """
            )

        else:

            self.title_label.setStyleSheet(
                """
                color: #bd72ff;
                font-size: 8px;
                font-weight: bold;
                letter-spacing: 2px;
                """
            )

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        self.message_label = QLabel(
            str(text)
        )

        self.message_label.setWordWrap(
            True
        )

        self.message_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.message_label.setStyleSheet(
            """
            color: #edf3ff;
            font-size: 12px;
            font-weight: 500;
            """
        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.message_label
        )

        self.setMinimumHeight(
            58
        )

    # ========================================================

    def set_message(
        self,
        text
    ):

        self.message_label.setText(
            str(text)
        )


# ============================================================
# WINDOW DRAG FILTER
# ============================================================

class WindowDragFilter(QObject):

    def __init__(
        self,
        window,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.window = window

    # ========================================================

    def eventFilter(
        self,
        watched,
        event
    ):

        if event.type() == event.MouseButtonPress:

            if event.button() == Qt.LeftButton:

                if isinstance(
                    watched,
                    QPushButton
                ):

                    return False

                window_handle = (
                    self.window.windowHandle()
                )

                if (
                    window_handle is not None
                    and hasattr(
                        window_handle,
                        "startSystemMove"
                    )
                ):

                    try:

                        started = (
                            window_handle.startSystemMove()
                        )

                        if started:

                            return True

                    except Exception:

                        pass

        return False


# ============================================================
# MAIN WINDOW
# ============================================================

class NovaWindow(QWidget):

    def __init__(
        self
    ):

        super().__init__()

        # ====================================================
        # BACKEND
        # ====================================================

        self.backend_process = None

        self.queue = None

        self.shutdown_requested = False

        self.current_state = "SLEEPING"

        # ====================================================
        # NETWORK
        # ====================================================

        self.network_status = "UNKNOWN"

        # ====================================================
        # FRONT CURRENT EXCHANGE
        # ====================================================

        self.current_user_message = None

        self.current_nova_message = None

        # ====================================================
        # SIDEBAR CURRENT EXCHANGE
        # ====================================================

        self.sidebar_current_user = None

        self.sidebar_current_nova = None

        # ====================================================
        # SIDEBAR
        # ====================================================

        self.sidebar_open = False

        # ----------------------------------------------------
        # Original Nova window remains 760px.
        # ----------------------------------------------------

        self.collapsed_width = 800

        self.window_height = 800

        # ----------------------------------------------------
        # Minimum right Nova area.
        # ----------------------------------------------------

        self.minimum_nova_width = 430

        # ----------------------------------------------------
        # Initial sidebar width.
        #
        # This is INSIDE the 760px window.
        # ----------------------------------------------------

        self.initial_sidebar_width = 320

        # ====================================================
        # WINDOW SETTINGS
        # ====================================================

        self.setWindowTitle(
            "Nova"
        )

        self.setMinimumSize(
            self.collapsed_width,
            self.window_height
        )

        self.setMaximumSize(
            self.collapsed_width,
            self.window_height
        )

        self.resize(
            self.collapsed_width,
            self.window_height
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Window
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # ====================================================
        # BUILD UI
        # ====================================================

        self.build_ui()

        # ====================================================
        # EVENT QUEUE
        # ====================================================

        self.queue = multiprocessing.Queue()

        self.queue_timer = QTimer(
            self
        )

        self.queue_timer.timeout.connect(
            self.check_backend_events
        )

        self.queue_timer.start(
            50
        )

        # ====================================================
        # PROCESS CHECK
        # ====================================================

        self.process_timer = QTimer(
            self
        )

        self.process_timer.timeout.connect(
            self.check_backend_process
        )

        self.process_timer.start(
            500
        )

        # ====================================================
        # INITIAL STATE
        # ====================================================

        self.set_state(
            "SLEEPING"
        )

        self.set_network_status(
            "UNKNOWN"
        )


    # ============================================================
    # BUILD UI
    # ============================================================

    def build_ui(
        self
    ):

        self.setStyleSheet(
            """
            QWidget {
                font-family: "Segoe UI";
            }

            QFrame#MainPanel {
                background-color: rgba(2, 6, 24, 250);
                border: 1px solid rgba(80, 135, 235, 150);
                border-radius: 24px;
            }

            QFrame#TopLine {
                background: transparent;
                border-bottom: 1px solid rgba(80, 125, 205, 85);
            }

            QFrame#Sidebar {
                background-color: rgba(7, 13, 34, 235);
                border: 1px solid rgba(95, 130, 205, 100);
                border-radius: 17px;
            }

            QFrame#ContentPanel {
                background: transparent;
                border: none;
            }

            QFrame#UserMessage {
                background-color: rgba(8, 37, 76, 205);
                border: 1px solid rgba(35, 196, 255, 120);
                border-radius: 12px;
            }

            QFrame#UserMessage:hover {
                background-color: rgba(10, 46, 92, 225);
            }

            QFrame#NovaMessage {
                background-color: rgba(40, 14, 76, 205);
                border: 1px solid rgba(193, 91, 255, 125);
                border-radius: 12px;
            }

            QFrame#NovaMessage:hover {
                background-color: rgba(49, 17, 91, 225);
            }

            QPushButton#MenuButton {
                color: #e8f2ff;
                background-color: rgba(30, 48, 82, 205);
                border: 1px solid rgba(100, 145, 215, 110);
                border-radius: 9px;
                font-size: 17px;
                font-weight: bold;
            }

            QPushButton#MenuButton:hover {
                color: white;
                background-color: rgba(38, 75, 120, 230);
                border: 1px solid rgba(65, 205, 255, 160);
            }

            QPushButton#MenuButton:pressed {
                background-color: rgba(70, 45, 125, 235);
            }

            QSplitter::handle {
                background-color: rgba(85, 130, 205, 150);
                width: 5px;
                margin: 8px 0px;
                border-radius: 2px;
            }

            QSplitter::handle:hover {
                background-color: rgba(75, 205, 255, 220);
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: rgba(10, 18, 42, 180);
                width: 8px;
                margin: 2px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: rgba(105, 135, 205, 160);
                min-height: 35px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(75, 200, 255, 200);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }

            QLabel {
                background: transparent;
            }
            """
        )

        # ========================================================
        # OUTER
        # ========================================================

        outer = QVBoxLayout(
            self
        )

        outer.setContentsMargins(
            0,
            0,
            0,
            0
        )

        panel = QFrame()

        panel.setObjectName(
            "MainPanel"
        )

        outer.addWidget(
            panel
        )

        main_layout = QVBoxLayout(
            panel
        )

        main_layout.setContentsMargins(
            18,
            12,
            18,
            12
        )

        main_layout.setSpacing(
            0
        )

        # ========================================================
        # HEADER
        # ========================================================

        top = QFrame()

        top.setObjectName(
            "TopLine"
        )

        top_layout = QHBoxLayout(
            top
        )

        top_layout.setContentsMargins(
            3,
            0,
            3,
            10
        )

        # --------------------------------------------------------
        # MENU
        # --------------------------------------------------------

        self.menu_button = QPushButton(
            "☰"
        )

        self.menu_button.setObjectName(
            "MenuButton"
        )

        self.menu_button.setFixedSize(
            32,
            28
        )

        self.menu_button.setCursor(
            Qt.PointingHandCursor
        )

        self.menu_button.setToolTip(
            "Show conversation history"
        )

        self.menu_button.clicked.connect(
            self.toggle_sidebar
        )

        top_layout.addWidget(
            self.menu_button
        )

        top_layout.addSpacing(
            10
        )

        # --------------------------------------------------------
        # LOGO
        # --------------------------------------------------------

        logo = QLabel(
            "N  O  V  A"
        )

        logo.setToolTip(
            "Nova Intelligent Personal Assistant"
        )

        logo.setStyleSheet(
            """
            color: #f7f9ff;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 5px;
            """
        )

        top_layout.addWidget(
            logo
        )

        top_layout.addStretch()

        # --------------------------------------------------------
        # NETWORK
        # --------------------------------------------------------

        self.system_label = QLabel(
            "● NETWORK CHECKING"
        )

        top_layout.addWidget(
            self.system_label
        )

        top_layout.addSpacing(
            15
        )

        # --------------------------------------------------------
        # STATE
        # --------------------------------------------------------

        self.state_label = QLabel(
            "● SLEEPING"
        )

        top_layout.addWidget(
            self.state_label
        )

        top_layout.addSpacing(
            20
        )

        # --------------------------------------------------------
        # MINIMIZE
        # --------------------------------------------------------

        minimize = QLabel(
            "−"
        )

        minimize.setAlignment(
            Qt.AlignCenter
        )

        minimize.setFixedSize(
            25,
            25
        )

        minimize.setStyleSheet(
            """
            QLabel {
                color: #aeb9d8;
                background-color: rgba(35, 45, 75, 180);
                border-radius: 6px;
                font-size: 16px;
            }

            QLabel:hover {
                background-color: rgba(60, 75, 110, 220);
            }
            """
        )

        minimize.setCursor(
            Qt.PointingHandCursor
        )

        minimize.mousePressEvent = (
            lambda event:
            self.showMinimized()
        )

        top_layout.addWidget(
            minimize
        )

        top_layout.addSpacing(
            5
        )

        # --------------------------------------------------------
        # CLOSE
        # --------------------------------------------------------

        close_button = QLabel(
            "×"
        )

        close_button.setAlignment(
            Qt.AlignCenter
        )

        close_button.setFixedSize(
            25,
            25
        )

        close_button.setStyleSheet(
            """
            QLabel {
                color: #aeb9d8;
                background-color: rgba(35, 45, 75, 180);
                border-radius: 6px;
                font-size: 18px;
            }

            QLabel:hover {
                color: white;
                background-color: rgba(150, 45, 70, 190);
            }
            """
        )

        close_button.setCursor(
            Qt.PointingHandCursor
        )

        close_button.mousePressEvent = (
            lambda event:
            self.close()
        )

        top_layout.addWidget(
            close_button
        )

        main_layout.addWidget(
            top
        )

        # ========================================================
        # NATIVE WINDOW DRAG
        # ========================================================

        self.drag_filter = WindowDragFilter(
            self
        )

        top.installEventFilter(
            self.drag_filter
        )

        logo.installEventFilter(
            self.drag_filter
        )

        self.system_label.installEventFilter(
            self.drag_filter
        )

        self.state_label.installEventFilter(
            self.drag_filter
        )

        # ========================================================
        # MAIN CONTENT
        # ========================================================

        content_container = QFrame()

        content_container.setObjectName(
            "ContentPanel"
        )

        content_layout = QVBoxLayout(
            content_container
        )

        content_layout.setContentsMargins(
            0,
            10,
            0,
            0
        )

        content_layout.setSpacing(
            0
        )

        # ========================================================
        # SPLITTER
        # ========================================================

        self.splitter = QSplitter(
            Qt.Horizontal
        )

        self.splitter.setChildrenCollapsible(
            False
        )

        self.splitter.setHandleWidth(
            5
        )

        # ========================================================
        # SIDEBAR
        # ========================================================

        self.sidebar = QFrame()

        self.sidebar.setObjectName(
            "Sidebar"
        )

        # --------------------------------------------------------
        # Sidebar can be resized inside the 760px window.
        # --------------------------------------------------------

        self.sidebar.setMinimumWidth(
            180
        )

        sidebar_layout = QVBoxLayout(
            self.sidebar
        )

        sidebar_layout.setContentsMargins(
            10,
            12,
            10,
            10
        )

        sidebar_layout.setSpacing(
            8
        )

        # --------------------------------------------------------
        # TITLE
        # --------------------------------------------------------

        sidebar_title = QLabel(
            "NOVA MEMORY"
        )

        sidebar_title.setStyleSheet(
            """
            color: #b979ff;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            padding-left: 3px;
            """
        )

        sidebar_layout.addWidget(
            sidebar_title
        )

        # ========================================================
        # SIDEBAR SCROLL
        # ========================================================

        self.sidebar_scroll = QScrollArea()

        self.sidebar_scroll.setWidgetResizable(
            True
        )

        self.sidebar_scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.sidebar_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.sidebar_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # --------------------------------------------------------
        # Sidebar history widget
        # --------------------------------------------------------

        self.sidebar_history_widget = QWidget()

        self.sidebar_history_widget.setStyleSheet(
            "background: transparent;"
        )

        self.sidebar_history_layout = QVBoxLayout(
            self.sidebar_history_widget
        )

        self.sidebar_history_layout.setContentsMargins(
            2,
            2,
            2,
            10
        )

        self.sidebar_history_layout.setSpacing(
            9
        )

        self.sidebar_history_layout.setAlignment(
            Qt.AlignTop
        )

        self.sidebar_scroll.setWidget(
            self.sidebar_history_widget
        )

        sidebar_layout.addWidget(
            self.sidebar_scroll,
            1
        )

        # --------------------------------------------------------
        # Footer
        # --------------------------------------------------------

        sidebar_hint = QLabel(
            "Current session only.\n"
            "History is not saved to disk."
        )

        sidebar_hint.setStyleSheet(
            """
            color: #68789f;
            font-size: 8px;
            padding-left: 3px;
            """
        )

        sidebar_layout.addWidget(
            sidebar_hint
        )

        # ========================================================
        # RIGHT NOVA PANEL
        # ========================================================

        right_panel = QFrame()

        right_panel.setObjectName(
            "ContentPanel"
        )

        # --------------------------------------------------------
        # NEVER LET RIGHT AREA SHRINK BELOW 430.
        # --------------------------------------------------------

        right_panel.setMinimumWidth(
            self.minimum_nova_width
        )

        right_layout = QVBoxLayout(
            right_panel
        )

        right_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        right_layout.setSpacing(
            0
        )

        # ========================================================
        # HERO
        # ========================================================

        self.hero_status = QLabel(
            "WAITING FOR WAKE WORD"
        )

        self.hero_status.setAlignment(
            Qt.AlignCenter
        )

        right_layout.addWidget(
            self.hero_status
        )
        # --------------------------------------------------------
        # SPACE: LISTENING... -> ORB
        # --------------------------------------------------------

        right_layout.addSpacing(
            12
        )


        # ========================================================
        # ORB
        # ========================================================

        orb_container = QHBoxLayout()

        orb_container.setAlignment(
            Qt.AlignCenter
        )

        self.orb = NovaOrb()

        self.orb.double_clicked.connect(
            self.toggle_backend
        )

        orb_container.addWidget(
            self.orb
        )

        right_layout.addLayout(
            orb_container
        )

        # --------------------------------------------------------
        # SPACE: ORB -> YOU ARE SPEAKING
        # --------------------------------------------------------

        right_layout.addSpacing(
            16
        )

        # ========================================================
        # WAVE TITLE
        # ========================================================

        self.wave_title = QLabel(
            "● STANDBY"
        )

        self.wave_title.setAlignment(
            Qt.AlignCenter
        )

        right_layout.addWidget(
            self.wave_title
        )

        # --------------------------------------------------------
        # SPACE: YOU ARE SPEAKING -> WAVEFORM
        # --------------------------------------------------------

        right_layout.addSpacing(
            7
        )

        # ========================================================
        # WAVEFORM
        # ========================================================

        waveform_layout = QHBoxLayout()

        waveform_layout.setAlignment(
            Qt.AlignCenter
        )

        self.waveform = Waveform()

        waveform_layout.addWidget(
            self.waveform
        )

        right_layout.addLayout(
            waveform_layout
        )
        # --------------------------------------------------------
        # SPACE: WAVEFORM -> LIVE INTERACTION
        # --------------------------------------------------------

        right_layout.addSpacing(
            14
        )

        # ========================================================
        # CURRENT EXCHANGE HEADER
        # ========================================================

        chat_header = QLabel(
            "LIVE INTERACTION ✨ "
        )

        chat_header.setStyleSheet(
            """
            color: #7887a8;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            padding: 4px 8px 2px 8px;
            """
        )

        right_layout.addWidget(
            chat_header
        )

        # ========================================================
        # CURRENT EXCHANGE
        # ========================================================

        self.current_exchange = QVBoxLayout()

        self.current_exchange.setContentsMargins(
            6,
            4,
            6,
            4
        )

        self.current_exchange.setSpacing(
            10
        )

        self.current_exchange.setAlignment(
            Qt.AlignTop
        )

        right_layout.addLayout(
            self.current_exchange,
            1
        )

        # ========================================================
        # FOOTER
        # ========================================================

        footer = QHBoxLayout()

        footer.setContentsMargins(
            3,
            6,
            3,
            0
        )

        self.activity_label = QLabel(
            "● DOUBLE-CLICK THE ORB TO START NOVA"
        )

        footer.addWidget(
            self.activity_label
        )

        footer.addStretch()

        self.backend_label = QLabel(
            "NOVA STANDBY"
        )

        footer.addWidget(
            self.backend_label
        )

        right_layout.addLayout(
            footer
        )

        # ========================================================
        # ADD PANELS
        # ========================================================

        self.splitter.addWidget(
            self.sidebar
        )

        self.splitter.addWidget(
            right_panel
        )

        # --------------------------------------------------------
        # Sidebar does not stretch.
        # Right side receives remaining space.
        # --------------------------------------------------------

        self.splitter.setStretchFactor(
            0,
            0
        )

        self.splitter.setStretchFactor(
            1,
            1
        )

        # --------------------------------------------------------
        # Start closed.
        # --------------------------------------------------------

        self.sidebar.setVisible(
            False
        )

        # --------------------------------------------------------
        # Divider movement.
        # --------------------------------------------------------

        self.splitter.splitterMoved.connect(
            self.sidebar_width_changed
        )

        content_layout.addWidget(
            self.splitter
        )

        main_layout.addWidget(
            content_container,
            1
        )


    # ============================================================
    # SIDEBAR WIDTH CHANGED
    # ============================================================

    def sidebar_width_changed(
        self,
        position,
        index
    ):

        if not self.sidebar_open:

            return

        sizes = self.splitter.sizes()

        if len(sizes) != 2:

            return

        sidebar_width = sizes[0]

        right_width = sizes[1]

        # --------------------------------------------------------
        # IMPORTANT:
        #
        # DO NOT RESIZE THE WINDOW HERE.
        #
        # The 760px Nova window remains fixed.
        # --------------------------------------------------------

        if right_width < self.minimum_nova_width:

            available_width = (
                self.splitter.width()
            )

            maximum_sidebar = (
                available_width
                - self.minimum_nova_width
            )

            maximum_sidebar = max(
                180,
                maximum_sidebar
            )

            corrected_sidebar = min(
                sidebar_width,
                maximum_sidebar
            )

            self.splitter.setSizes(
                [
                    corrected_sidebar,
                    available_width - corrected_sidebar
                ]
            )

            sidebar_width = corrected_sidebar

        # --------------------------------------------------------
        # Remember current sidebar width.
        # --------------------------------------------------------

        self.initial_sidebar_width = max(
            180,
            sidebar_width
        )


    # ============================================================
    # CLEAR FRONT
    # ============================================================

    def clear_front_exchange(
        self
    ):

        while self.current_exchange.count():

            item = (
                self.current_exchange.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:

                widget.hide()

                widget.setParent(
                    None
                )

                widget.deleteLater()

        self.current_user_message = None

        self.current_nova_message = None


    # ============================================================
    # CLEAR SIDEBAR
    # ============================================================

    def clear_sidebar_history(
        self
    ):

        while self.sidebar_history_layout.count():

            item = (
                self.sidebar_history_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:

                widget.hide()

                widget.setParent(
                    None
                )

                widget.deleteLater()

        self.sidebar_current_user = None

        self.sidebar_current_nova = None


    # ============================================================
    # CLEAR ALL
    # ============================================================

    def clear_current_exchange(
        self
    ):

        self.clear_front_exchange()

        self.clear_sidebar_history()


    # ============================================================
    # COMPATIBILITY
    # ============================================================

    def clear_message_areas(
        self
    ):

        self.clear_current_exchange()


    # ============================================================
    # NEW CHAT
    # ============================================================

    def new_chat(
        self
    ):

        self.clear_current_exchange()

        self.activity_label.setText(
            "● READY FOR A NEW CONVERSATION"
        )


    # ============================================================
    # USER MESSAGE
    # ============================================================

    def show_user_message(
        self,
        text
    ):

        # --------------------------------------------------------
        # FRONT:
        # Only current exchange.
        # --------------------------------------------------------

        self.clear_front_exchange()

        # --------------------------------------------------------
        # FRONT USER
        # --------------------------------------------------------

        front_bubble = ChatMessage(
            "YOU:",
            text,
            True
        )

        self.current_user_message = (
            front_bubble
        )

        self.current_exchange.addWidget(
            front_bubble
        )

        self.fade_message(
            front_bubble
        )

        # --------------------------------------------------------
        # SIDEBAR:
        # Keep all previous exchanges.
        # --------------------------------------------------------

        sidebar_user = ChatMessage(
            "YOU:",
            text,
            True
        )

        self.sidebar_current_user = (
            sidebar_user
        )

        self.sidebar_current_nova = None

        self.sidebar_history_layout.addWidget(
            sidebar_user
        )

        self.fade_message(
            sidebar_user
        )

        QTimer.singleShot(
            50,
            self.scroll_sidebar_to_bottom
        )

        self.activity_label.setText(
            "● LISTENING TO YOU"
        )


    # ============================================================
    # NOVA MESSAGE
    # ============================================================

    def show_nova_message(
        self,
        text
    ):

        # --------------------------------------------------------
        # FRONT:
        # Replace current Nova response only.
        # --------------------------------------------------------

        if self.current_nova_message is not None:

            try:

                self.current_nova_message.hide()

                self.current_nova_message.setParent(
                    None
                )

                self.current_nova_message.deleteLater()

            except Exception:

                pass

        front_bubble = ChatMessage(
            "NOVA:",
            text,
            False
        )

        self.current_nova_message = (
            front_bubble
        )

        self.current_exchange.addWidget(
            front_bubble
        )

        self.fade_message(
            front_bubble
        )

        # --------------------------------------------------------
        # SIDEBAR:
        # Update existing Nova response if necessary.
        # --------------------------------------------------------

        if self.sidebar_current_nova is not None:

            self.sidebar_current_nova.set_message(
                text
            )

        else:

            sidebar_nova = ChatMessage(
                "NOVA:",
                text,
                False
            )

            self.sidebar_current_nova = (
                sidebar_nova
            )

            self.sidebar_history_layout.addWidget(
                sidebar_nova
            )

            self.fade_message(
                sidebar_nova
            )

        QTimer.singleShot(
            50,
            self.scroll_sidebar_to_bottom
        )


    # ============================================================
    # SIDEBAR AUTO SCROLL
    # ============================================================

    def scroll_sidebar_to_bottom(
        self
    ):

        try:

            scrollbar = (
                self.sidebar_scroll
                .verticalScrollBar()
            )

            scrollbar.setValue(
                scrollbar.maximum()
            )

        except Exception:

            pass


    # ============================================================
    # SIDEBAR TOGGLE
    # ============================================================

    def toggle_sidebar(
        self
    ):

        if self.sidebar_open:

            self.close_sidebar()

        else:

            self.open_sidebar()


    # ============================================================
    # OPEN SIDEBAR
    # ============================================================

    def open_sidebar(
        self
    ):

        if self.sidebar_open:

            return

        self.sidebar_open = True

        # --------------------------------------------------------
        # Show sidebar.
        #
        # IMPORTANT:
        # Window remains 760px.
        # --------------------------------------------------------

        self.sidebar.setVisible(
            True
        )

        # --------------------------------------------------------
        # Give the sidebar a reasonable starting width.
        #
        # No window resize.
        # --------------------------------------------------------

        available_width = (
            self.splitter.width()
        )

        if available_width <= 0:

            available_width = (
                self.collapsed_width
                - 36
            )

        maximum_sidebar = (
            available_width
            - self.minimum_nova_width
        )

        sidebar_width = min(
            max(
                self.initial_sidebar_width,
                180
            ),
            maximum_sidebar
        )

        sidebar_width = max(
            180,
            sidebar_width
        )

        right_width = (
            available_width
            - sidebar_width
        )

        self.splitter.setSizes(
            [
                sidebar_width,
                right_width
            ]
        )

        self.menu_button.setToolTip(
            "Hide conversation history"
        )


    # ============================================================
    # CLOSE SIDEBAR
    # ============================================================

    def close_sidebar(
        self
    ):

        if not self.sidebar_open:

            return

        # --------------------------------------------------------
        # Remember width before closing.
        # --------------------------------------------------------

        sizes = self.splitter.sizes()

        if len(sizes) == 2:

            self.initial_sidebar_width = max(
                180,
                sizes[0]
            )

        self.sidebar_open = False

        # --------------------------------------------------------
        # Hide sidebar.
        #
        # Window stays 760px.
        # --------------------------------------------------------

        self.sidebar.setVisible(
            False
        )

        # --------------------------------------------------------
        # Give all available space back to Nova.
        # --------------------------------------------------------

        available_width = (
            self.splitter.width()
        )

        self.splitter.setSizes(
            [
                0,
                available_width
            ]
        )

        self.menu_button.setToolTip(
            "Show conversation history"
        )


    # ============================================================
    # NETWORK STATUS
    # ============================================================

    def set_network_status(
        self,
        status
    ):

        status = str(
            status
        ).upper().strip()

        if status not in [
            "ONLINE",
            "OFFLINE"
        ]:

            self.network_status = "UNKNOWN"

            self.system_label.setText(
                "● NETWORK CHECKING"
            )

            self.system_label.setStyleSheet(
                """
                color: rgb(160,170,195);
                font-size: 9px;
                font-weight: bold;
                letter-spacing: 1px;
                padding: 4px 8px;
                background: rgba(20, 30, 55, 150);
                border: 1px solid rgba(90, 125, 190, 70);
                border-radius: 7px;
                """
            )

            return

        self.network_status = status

        if status == "ONLINE":

            color = NETWORK_ONLINE_COLOR

            text = (
                "● NETWORK ONLINE"
            )

        else:

            color = NETWORK_OFFLINE_COLOR

            text = (
                "● NETWORK OFFLINE"
            )

        color_text = (
            f"rgb("
            f"{color.red()},"
            f"{color.green()},"
            f"{color.blue()}"
            f")"
        )

        self.system_label.setText(
            text
        )

        self.system_label.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 9px;
            font-weight: bold;
            letter-spacing: 1px;
            """
        )


    # ============================================================
    # SET STATE
    # ============================================================

    def set_state(
        self,
        state
    ):

        if state == "SHUTDOWN_REQUESTED":

            state = "SLEEPING"

        if state not in COLORS:

            state = "SLEEPING"

        self.current_state = state

        self.orb.set_state(
            state
        )

        self.waveform.set_state(
            state
        )

        color = COLORS[
            state
        ]

        color_text = (
            f"rgb("
            f"{color.red()},"
            f"{color.green()},"
            f"{color.blue()}"
            f")"
        )

        self.state_label.setText(
            f"● {state}"
        )

        self.state_label.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 9px;
            font-weight: bold;
            letter-spacing: 1px;
            """
        )

        hero_text = {

            "SLEEPING":
                "WAITING FOR WAKE WORD",

            "STARTING":
                "STARTING NOVA...",

            "ACTIVE":
                "NOVA ACTIVE",

            "LISTENING":
                "LISTENING...",

            "THINKING":
                "THINKING...",

            "SPEAKING":
                "SPEAKING...",

            "ERROR":
                "NOVA ERROR"
        }

        self.hero_status.setText(
            hero_text.get(
                state,
                "NOVA"
            )
        )

        self.hero_status.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 3px;
            """
        )

        wave_text = {

            "SLEEPING":
                "● STANDBY",

            "STARTING":
                "● INITIALIZING",

            "ACTIVE":
                "● NOVA ACTIVE",

            "LISTENING":
                "● YOU ARE SPEAKING",

            "THINKING":
                "● NOVA IS THINKING",

            "SPEAKING":
                "● NOVA IS SPEAKING",

            "ERROR":
                "● SYSTEM ERROR"
        }

        self.wave_title.setText(
            wave_text.get(
                state,
                "● NOVA"
            )
        )

        self.wave_title.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 8px;
            font-weight: bold;
            letter-spacing: 2px;
            """
        )

        activities = {

            "SLEEPING":
                "● WAITING FOR WAKE WORD",

            "STARTING":
                "● STARTING NOVA...",

            "ACTIVE":
                "● NOVA ACTIVE",

            "LISTENING":
                "● LISTENING TO YOU",

            "THINKING":
                "● NOVA IS THINKING",

            "SPEAKING":
                "● NOVA IS SPEAKING",

            "ERROR":
                "● NOVA ERROR"
        }

        self.activity_label.setText(
            activities.get(
                state,
                "● NOVA"
            )
        )

        self.activity_label.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 8px;
            font-weight: bold;
            letter-spacing: 1px;
            """
        )

        self.backend_label.setStyleSheet(
            f"""
            color: {color_text};
            font-size: 8px;
            font-weight: bold;
            letter-spacing: 1px;
            """
        )


    # ============================================================
    # START BACKEND
    # ============================================================

    def toggle_backend(
        self
    ):

        if (
            self.backend_process
            and self.backend_process.is_alive()
        ):

            self.activity_label.setText(
                "● NOVA IS ALREADY RUNNING"
            )

            return

        self.start_backend()


    # ============================================================

    def start_backend(
        self
    ):

        if (
            self.backend_process
            and self.backend_process.is_alive()
        ):

            return

        self.shutdown_requested = False

        # --------------------------------------------------------
        # New backend session.
        # --------------------------------------------------------

        self.prepare_new_session()

        self.set_state(
            "STARTING"
        )

        self.backend_label.setText(
            "NOVA STARTING..."
        )

        try:

            self.queue = (
                multiprocessing.Queue()
            )

            self.backend_process = (
                multiprocessing.Process(
                    target=run_nova_backend,
                    args=(
                        self.queue,
                    ),
                    daemon=True
                )
            )

            self.backend_process.start()

            self.backend_label.setText(
                "NOVA STARTED"
            )

            self.activity_label.setText(
                "● NOVA STARTED — WAITING FOR WAKE WORD"
            )

        except Exception as e:

            self.backend_process = None

            self.show_error(
                str(e)
            )

            self.set_state(
                "SLEEPING"
            )


    # ============================================================
    # BACKEND EVENTS
    # ============================================================

    def check_backend_events(
        self
    ):

        if self.queue is None:

            return

        while True:

            try:

                event_type, value = (
                    self.queue.get_nowait()
                )

            except Exception:

                break

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            if event_type == "status":

                self.handle_status(
                    value
                )

            # ------------------------------------------------
            # NETWORK
            # ------------------------------------------------

            elif event_type == "network":

                self.handle_network_status(
                    value
                )

            # ------------------------------------------------
            # USER COMMAND
            # ------------------------------------------------

            elif event_type == "command":

                self.show_user_message(
                    value
                )

            # ------------------------------------------------
            # NOVA RESPONSE
            # ------------------------------------------------

            elif event_type == "response":

                self.show_nova_message(
                    value
                )

            # ------------------------------------------------
            # ERROR
            # ------------------------------------------------

            elif event_type == "error":

                self.show_error(
                    value
                )


    # ============================================================
    # NETWORK EVENT
    # ============================================================

    def handle_network_status(
        self,
        status
    ):

        self.set_network_status(
            status
        )


    # ============================================================
    # STATUS
    # ============================================================

    def handle_status(
        self,
        status
    ):

        status = str(
            status
        ).upper().strip()

        if status == "SHUTDOWN_REQUESTED":

            self.shutdown_requested = True

            self.set_state(
                "SLEEPING"
            )

            self.backend_label.setText(
                "NOVA SHUTTING DOWN..."
            )

            self.activity_label.setText(
                "● NOVA SLEEPING"
            )

            QTimer.singleShot(
                250,
                self.reset_live_conversation
            )

            return

        if status in COLORS:

            self.set_state(
                status
            )

            if status in [

                "STARTING",
                "ACTIVE",
                "LISTENING",
                "THINKING",
                "SPEAKING",
                "SLEEPING"

            ]:

                self.backend_label.setText(

                    "NOVA ACTIVE"
                    if status != "SLEEPING"
                    else "NOVA STANDBY"

                )


    # ============================================================
    # RESET LIVE CONVERSATION
    # ============================================================

    def reset_live_conversation(
        self
    ):

        self.clear_current_exchange()

        self.activity_label.setText(
            "● READY FOR A NEW CONVERSATION"
        )


    # ============================================================
    # PREPARE NEW SESSION
    # ============================================================

    def prepare_new_session(
        self
    ):

        self.clear_current_exchange()

        self.activity_label.setText(
            "● NOVA STARTED — WAITING FOR YOU"
        )


    # ============================================================
    # MESSAGE FADE
    # ============================================================

    def fade_message(
        self,
        widget
    ):

        effect = QGraphicsOpacityEffect(
            widget
        )

        widget.setGraphicsEffect(
            effect
        )

        animation = QPropertyAnimation(
            effect,
            b"opacity"
        )

        animation.setDuration(
            280
        )

        animation.setStartValue(
            0.0
        )

        animation.setEndValue(
            1.0
        )

        animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        animation.start()

        widget._fade_animation = (
            animation
        )


    # ============================================================
    # ERROR
    # ============================================================

    def show_error(
        self,
        error
    ):

        self.backend_label.setText(
            "NOVA ERROR"
        )

        self.clear_front_exchange()

        self.show_nova_message(
            "Error: " + str(error)
        )

        self.set_state(
            "ERROR"
        )

        QTimer.singleShot(
            6000,
            self.restore_backend_label
        )


    # ============================================================

    def restore_backend_label(
        self
    ):

        if (
            self.backend_process
            and self.backend_process.is_alive()
        ):

            if self.current_state == "SLEEPING":

                self.backend_label.setText(
                    "NOVA STANDBY"
                )

            else:

                self.backend_label.setText(
                    "NOVA ACTIVE"
                )

        else:

            self.backend_label.setText(
                "NOVA STANDBY"
            )


    # ============================================================
    # BACKEND PROCESS MONITOR
    # ============================================================

    def check_backend_process(
        self
    ):

        if self.backend_process is None:

            return

        if not self.backend_process.is_alive():

            try:

                self.backend_process.join(
                    timeout=0.1
                )

            except Exception:

                pass

            self.backend_process = None

            self.set_state(
                "SLEEPING"
            )

            self.backend_label.setText(
                "NOVA STANDBY"
            )

            if self.shutdown_requested:

                self.reset_live_conversation()

                self.activity_label.setText(
                    "● NOVA SLEEPING — DOUBLE-CLICK TO START"
                )

            else:

                self.activity_label.setText(
                    "● NOVA STOPPED — DOUBLE-CLICK TO START"
                )


    # ============================================================
    # CLOSE
    # ============================================================

    def closeEvent(
        self,
        event
    ):

        # --------------------------------------------------------
        # Conversation is memory-only.
        # --------------------------------------------------------

        self.clear_current_exchange()

        if (
            self.backend_process
            and self.backend_process.is_alive()
        ):

            try:

                self.backend_process.terminate()

                self.backend_process.join(
                    timeout=2
                )

            except Exception:

                pass

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    multiprocessing.freeze_support()

    # --------------------------------------------------------
    # ENABLE WINDOWS STARTUP
    # --------------------------------------------------------

    setup_windows_startup()

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Nova"
    )

    window = NovaWindow()

    # --------------------------------------------------------
    # CENTER WINDOW
    # --------------------------------------------------------

    screen = (
        QApplication
        .primaryScreen()
        .availableGeometry()
    )

    window.move(
        screen.center()
        - window.rect().center()
    )

    # --------------------------------------------------------
    # SHOW UI
    # --------------------------------------------------------

    window.show()

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    sys.exit(
        app.exec_()
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()