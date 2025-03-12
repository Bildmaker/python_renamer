import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QListWidget
from PyQt5.QtCore import Qt


class FileRenamerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 600, 400)
        
        self.files = []
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        # Pattern and Replace input fields
        self.pattern_input = QLineEdit(self)
        self.pattern_input.setPlaceholderText("Pattern in filename")
        layout.addWidget(self.pattern_input)

        self.replace_input = QLineEdit(self)
        self.replace_input.setPlaceholderText("Replace with")
        layout.addWidget(self.replace_input)

        # Drop area for files
        self.drop_area = QListWidget(self)
        self.drop_area.setAcceptDrops(True)
        self.drop_area.setStyleSheet("background-color: #f0f0f0; border: 2px dashed #ccc;")
        self.drop_area.setMinimumHeight(150)
        self.drop_area.setDragDropMode(QListWidget.InternalMove)
        self.drop_area.setDefaultDropAction(Qt.MoveAction)
        self.drop_area.dragEnterEvent = self.dragEnterEvent
        self.drop_area.dropEvent = self.dropEvent
        layout.addWidget(self.drop_area)

        # File counter label
        self.file_count_label = QLabel("Files to rename: 0", self)
        layout.addWidget(self.file_count_label)

        # Process and Cancel buttons
        self.process_button = QPushButton("Process", self)
        self.process_button.clicked.connect(self.rename_files)
        layout.addWidget(self.process_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.clear_files)
        layout.addWidget(self.cancel_button)

        # Log output
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Log output will appear here...")
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path not in self.files:
                self.files.append(file_path)
                self.drop_area.addItem(file_path)
        
        self.update_file_count()

    def update_file_count(self):
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
        self.files.clear()
        self.drop_area.clear()
        self.update_file_count()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileRenamerApp()
    window.show()
    sys.exit(app.exec_())
