"""
============================================================
NOVA QT HELPERS
============================================================
"""

from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve
)

from PyQt5.QtGui import (
    QFont
)

from PyQt5.QtWidgets import (
    QLabel
)


# ============================================================
# LABEL CREATOR
# ============================================================

def create_label(
    text="",
    font_size=16,
    bold=False,
    alignment=Qt.AlignCenter
):

    label = QLabel(text)

    font = QFont(
        "Segoe UI",
        font_size
    )

    font.setBold(bold)

    label.setFont(font)

    label.setAlignment(alignment)

    return label


# ============================================================
# FADE ANIMATION
# ============================================================

def fade_widget(
    widget,
    start=0.0,
    end=1.0,
    duration=300
):

    animation = QPropertyAnimation(
        widget,
        b"windowOpacity"
    )

    animation.setDuration(duration)

    animation.setStartValue(start)

    animation.setEndValue(end)

    animation.setEasingCurve(
        QEasingCurve.InOutQuad
    )

    animation.start()

    return animation