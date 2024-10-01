




import sys
import os
import subprocess
from supabase import create_client, Client
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QSizePolicy,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation

# Replace with your Supabase project URL and API key
SUPABASE_URL = "https://jdisuejxelaxgsjsctvm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpkaXN1ZWp4ZWxheGdzanNjdHZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc2NDIzOTEsImV4cCI6MjA0MzIxODM5MX0.V07FjL6CLUO7_Hz2LoK4w3L75iIm4dbpCaWEu32mRo0"


class DownloadThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, supabase: Client):
        super().__init__()
        self.supabase = supabase

    def run(self):
        try:
            # Fetch the newest file info from the database
            response = (
                self.supabase.table("bat_files")
                .select("*")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            if not response.data:
                self.finished.emit(False, "No files found in the database.")
                return

            newest_file = response.data[0]
            file_path = newest_file["file_path"]

            # Download the file from storage
            file_content = self.supabase.storage.from_("game-updates").download(
                file_path
            )

            # Save the content to a local file
            with open("latest_update.bat", "wb") as f:
                f.write(file_content)

            self.finished.emit(True, "Download complete!")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGraphicsEffect(QGraphicsOpacityEffect())
        self.anim = QPropertyAnimation(self.graphicsEffect(), b"opacity")
        self.anim.setDuration(300)

    def enterEvent(self, event):
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.7)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.setStartValue(0.7)
        self.anim.setEndValue(1.0)
        self.anim.start()
        super().leaveEvent(event)


class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Launcher")
        self.setGeometry(100, 100, 600, 400)  # Increased size for modern feel
        self.setStyleSheet(self.window_style())

        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Set margins for modern spacing
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center layout

        self.status_label = QLabel("Welcome to the Game Launcher!")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            "color: white; font-size: 22px; font-weight: bold;"
        )
        layout.addWidget(self.status_label)

        self.download_button = AnimatedButton("Download Latest Update")
        self.download_button.clicked.connect(self.download_file)
        self.download_button.setStyleSheet(self.button_style())
        layout.addWidget(self.download_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.run_button = AnimatedButton("Run Batch File")
        self.run_button.clicked.connect(self.run_batch_file)
        self.run_button.setEnabled(False)
        self.run_button.setStyleSheet(self.button_style(disabled=True))
        layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet(self.container_style())
        self.setCentralWidget(container)

    def button_style(self, disabled=False):
        base_style = """
            QPushButton {
                background-color: #0078D7;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                padding-left: 20px; /* Add horizontal padding */
                padding-right: 20px; /* Add horizontal padding */
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """
        if disabled:
            base_style += """
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #3B3B3B;
            }
            """
        return base_style

    def container_style(self):
        return """
            QWidget {
                background-color: #2C2C2C;
                border-radius: 12px;
                padding: 20px;
            }
        """

    def window_style(self):
        return """
            QMainWindow {
                background-color: #1E1E1E;
                border: 1px solid #3C3C3C;
            }
        """

    def download_file(self):
        self.status_label.setText("Downloading latest update...")
        self.download_button.setEnabled(False)
        self.run_button.setEnabled(False)

        self.download_thread = DownloadThread(self.supabase)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def download_finished(self, success, message):
        self.status_label.setText(message)
        self.download_button.setEnabled(True)
        if success:
            self.run_button.setEnabled(True)

    def run_batch_file(self):
        batch_file = "latest_update.bat"
        if os.path.exists(batch_file):
            try:
                subprocess.Popen(f"start cmd /k {batch_file}", shell=True)
                self.status_label.setText("Batch file executed in a new window.")
            except Exception as e:
                self.status_label.setText(f"Error running batch file: {str(e)}")
        else:
            self.status_label.setText("Batch file not found. Please download first.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())
