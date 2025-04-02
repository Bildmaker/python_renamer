########################################
# File: file_renamer_qt6_preview.py
# Author: Sebastian
# Updated: 2025-04-02
########################################
#
# This script provides a graphical user interface (GUI) for renaming files,
# now updated with a live preview feature and a modernized PyQt6 interface.
#
# Features:
# - Modern PyQt6-based GUI with dark mode styling.
# - Allows users to specify a search pattern and replacement text.
# - Supports drag and drop for selecting files from the file system.
# - Displays the list of selected files.
# - Shows a file count of the selected files.
# - Live preview of the renamed filenames based on user input.
# - Logs the renaming process in a text output window.
# - Includes buttons to process renaming and cancel the operation.
# - Dynamically updates preview when input or file list changes.
#
# How It Works:
# 1. Enter a search pattern and replacement text.
# 2. Drag and drop files into the drop zone.
# 3. Preview updated file names live in the preview window below.
# 4. Click "Process" to rename files based on the pattern.
# 5. The log window will display the renaming result.
# 6. Click "Cancel" to clear the file list and preview.
#
# ----------------------------------------
# Requirements:
# - Python 3.10 or higher
# - PyQt6 >= 6.5
#
# Installation (via pip):
#   pip install PyQt6
#
# Optional (for GUI design tools):
#   pip install pyqt6-tools
#
########################################

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel, QHBoxLayout, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class DropListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(False)
        self.setDragDropMode(QListWidget.DragDropMode.DropOnly)
        self.files = []

        self.setStyleSheet("background-color: #444; border: 2px dashed #888; color: white;")
        self.setMinimumHeight(300)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            changed = False
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and file_path not in self.files:
                    self.files.append(file_path)
                    self.addItem(file_path)
                    changed = True
            self.parent().update_file_count()
            if changed:
                self.parent().update_preview()
            event.acceptProposedAction()
        else:
            event.ignore()


class FileRenamerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 1024, 1024)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Rename files", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        layout.addWidget(QLabel("Search for pattern in filename(s):", self))
        self.pattern_input = QLineEdit(self)
        self.pattern_input.setPlaceholderText("Enter pattern to find:")
        self.pattern_input.textChanged.connect(self.update_preview)
        layout.addWidget(self.pattern_input)

        layout.addWidget(QLabel("Replace with:", self))
        self.replace_input = QLineEdit(self)
        self.replace_input.setPlaceholderText("Enter replacement text")
        self.replace_input.textChanged.connect(self.update_preview)
        layout.addWidget(self.replace_input)

        drop_label = QLabel("Please drag your files here...", self)
        drop_label.setStyleSheet("font-size: 16px; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(drop_label)

        self.drop_area = DropListWidget(self)
        layout.addWidget(self.drop_area)

        self.file_count_label = QLabel("Files to rename: 0", self)
        layout.addWidget(self.file_count_label)

        # Vorschau unterhalb Dropbereich
        layout.addWidget(QLabel("Live Preview (renamed filenames):", self))
        self.preview_area = QTextEdit(self)
        self.preview_area.setReadOnly(True)
        self.preview_area.setStyleSheet("background-color: #222; color: lightgreen;")
        layout.addWidget(self.preview_area)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.clear_files)
        button_layout.addWidget(self.cancel_button)

        self.process_button = QPushButton("Process", self)
        self.process_button.clicked.connect(self.rename_files)
        button_layout.addWidget(self.process_button)

        layout.addLayout(button_layout)

        layout.addWidget(QLabel("Log output:", self))
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def update_file_count(self):
        count = len(self.drop_area.files)
        self.file_count_label.setText(f"Files to rename: {count}")

    def update_preview(self):
        files = self.drop_area.files
        pattern = self.pattern_input.text()
        replace = self.replace_input.text()
        preview = []

        for file_path in files:
            filename = os.path.basename(file_path)
            if pattern in filename:
                new_name = filename.replace(pattern, replace)
                preview.append(f"{filename}  ➔  {new_name}")
            else:
                preview.append(f"{filename}  (no change)")

        self.preview_area.setPlainText("\n".join(preview))

    def rename_files(self):
        files = self.drop_area.files
        if not files:
            self.log_output.append("No files to rename.")
            return

        pattern = self.pattern_input.text().strip()
        replace = self.replace_input.text().strip()

        if not pattern:
            self.log_output.append("Pattern cannot be empty.")
            return

        renamed_count = 0
        for file_path in files:
            folder = os.path.dirname(file_path)
            filename = os.path.basename(file_path)

            if pattern in filename:
                new_filename = filename.replace(pattern, replace)
                new_file_path = os.path.join(folder, new_filename)

                try:
                    os.rename(file_path, new_file_path)
                    self.log_output.append(f"Renamed: {filename} ➔ {new_filename}")
                    renamed_count += 1
                except Exception as e:
                    self.log_output.append(f"Failed to rename {filename}: {e}")

        self.log_output.append(f"{renamed_count} file(s) renamed.")
        self.clear_files()

    def clear_files(self):
        self.drop_area.files.clear()
        self.drop_area.clear()
        self.update_file_count()
        self.update_preview()


def set_dark_mode(app: QApplication):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(60, 60, 60))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)
    app.setStyleSheet("QWidget { font-family: Arial; font-size: 12pt; }")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_dark_mode(app)
    window = FileRenamerApp()
    window.show()
    sys.exit(app.exec())
