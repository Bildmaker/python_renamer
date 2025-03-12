########################################
# File: file_renamer.py
# Author: Sebastian
# Date: 2025-03-12
########################################
#
# This script provides a graphical user interface (GUI) for renaming files.
#
# Features:
# - Allows users to specify a search pattern and replacement text.
# - Supports drag and drop for selecting files.
# - Displays the list of selected files.
# - Shows a file count of the selected files.
# - Logs the renaming process in a text output window.
# - Includes buttons to process renaming and cancel the operation.
#
# How It Works:
# 1. Enter a search pattern and replacement text.
# 2. Drag and drop files into the drop zone.
# 3. Click "Process" to rename files.
# 4. The log window will display the renaming result.
# 5. Click "Cancel" to clear the file list.
#
########################################

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QListWidget, QHBoxLayout
from PyQt5.QtCore import Qt


class FileRenamerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 1024, 1024)  # Set default window size to 1024x1024

        self.files = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Rename files", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Pattern and Replace input fields with labels
        pattern_label = QLabel("Search for pattern in filename(s):", self)
        layout.addWidget(pattern_label)

        self.pattern_input = QLineEdit(self)
        self.pattern_input.setPlaceholderText("Enter pattern to find:")
        layout.addWidget(self.pattern_input)

        replace_label = QLabel("Replace with:", self)
        layout.addWidget(replace_label)

        self.replace_input = QLineEdit(self)
        self.replace_input.setPlaceholderText("Enter replacement text")
        layout.addWidget(self.replace_input)

        # Drop area label
        drop_label = QLabel("Please drag your files here...", self)
        drop_label.setStyleSheet("font-size: 16px; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(drop_label)

        # Drop area for files
        self.drop_area = QListWidget(self)
        self.drop_area.setAcceptDrops(True)
        self.drop_area.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #ccc;")
        self.drop_area.setMinimumHeight(300)
        self.drop_area.setDragDropMode(QListWidget.InternalMove)
        self.drop_area.setDefaultDropAction(Qt.MoveAction)
        self.drop_area.dragEnterEvent = self.dragEnterEvent
        self.drop_area.dropEvent = self.dropEvent
        layout.addWidget(self.drop_area)

        # File counter label
        self.file_count_label = QLabel("Files to rename: 0", self)
        self.file_count_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(self.file_count_label)

        # Process and Cancel buttons
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.clear_files)
        button_layout.addWidget(self.cancel_button)

        self.process_button = QPushButton("Process", self)
        self.process_button.clicked.connect(self.rename_files)
        button_layout.addWidget(self.process_button)

        layout.addLayout(button_layout)

        # Log output for renaming process
        log_label = QLabel("Log output:", self)
        layout.addWidget(log_label)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Log output will appear here...")
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        # Accept the drag event if it contains file URLs
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Handle the file drop event
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                self.drop_area.addItem(file_path)

        self.update_file_count()

    def update_file_count(self):
        # Update the file count label
        self.file_count_label.setText(f"Files to rename: {len(self.files)}")

    def rename_files(self):
        if not self.files:
            self.log_output.append("No files to rename.")
            return

        pattern = self.pattern_input.text().strip()
        replace = self.replace_input.text().strip()

        if not pattern:
            self.log_output.append("Pattern cannot be empty.")
            return

        renamed_count = 0
        for file_path in self.files:
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
        # Clear file list and reset UI
        self.files.clear()
        self.drop_area.clear()
        self.update_file_count()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileRenamerApp()
    window.show()
    sys.exit(app.exec_())
