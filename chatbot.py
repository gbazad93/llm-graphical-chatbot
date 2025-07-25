import os
from pathlib import Path
from dotenv import load_dotenv #use this line only when you want to read from local env file instead of system variables
import openai

from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPlainTextEdit,
    QPushButton, QFileDialog, QLineEdit, QFrame, QSizePolicy, QSplitter, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor, QColor, QPalette


# ====== Environment & API Key ======
ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env") #use this line only when you want to read from local env file instead of system variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

MODEL = "gpt-4o-mini"   # or "gpt-4o"

class DataChatBotDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Powered Data Chatbot - Demo by Bobby Azad")
        self.setMinimumSize(980, 580)
        self.setStyleSheet(self._main_stylesheet())
        self._build_ui()
        self.data_text = ""
        self.chat_history = []

    # --- UI Build ---
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 12)
        layout.setSpacing(10)

        # Top Title (main title + subtitle with smaller font, no HTML)
        title_layout = QVBoxLayout()
        title_label = QLabel("🧠 AI-Powered Data Chatbot")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #222;")
        subtitle = QLabel("A Demo by Bobby Azad")
        subtitle.setFont(QFont("Segoe UI", 12, QFont.Weight.Normal))
        subtitle.setStyleSheet("color: #333; margin-bottom: 12px; margin-left: 4px;")
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)

        # Splitter (Left: Data Paste; Right: Chat)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter, 1)

        # -- Left: Data Paste/Load Panel --
        data_box = QFrame()
        data_layout = QVBoxLayout(data_box)
        data_layout.setContentsMargins(18, 12, 18, 12)
        data_layout.setSpacing(6)

        data_label = QLabel("Paste your data (CSV, TSV, or any table):")
        data_label.setFont(QFont("Segoe UI", 12))
        data_layout.addWidget(data_label)

        self.data_edit = QPlainTextEdit()
        self.data_edit.setPlaceholderText("Paste or load your file content here...")
        self.data_edit.setFont(QFont("Consolas", 11))
        self.data_edit.setMinimumHeight(220)
        # Fix: Set black text color and white bg for visibility
        data_palette = self.data_edit.palette()
        data_palette.setColor(QPalette.ColorRole.Text, QColor("#111"))
        data_palette.setColor(QPalette.ColorRole.Base, QColor("#fafbfc"))
        self.data_edit.setPalette(data_palette)
        data_layout.addWidget(self.data_edit, 1)

        btn_row = QHBoxLayout()
        paste_btn = QPushButton("Paste")
        paste_btn.clicked.connect(self._paste_clipboard)
        load_btn = QPushButton("Load File")
        load_btn.clicked.connect(self._load_file)
        btn_row.addWidget(paste_btn)
        btn_row.addWidget(load_btn)
        btn_row.addStretch(1)
        data_layout.addLayout(btn_row)

        splitter.addWidget(data_box)
        splitter.setStretchFactor(0, 2)

        # -- Right: Chat Panel --
        chat_box = QFrame()
        chat_layout = QVBoxLayout(chat_box)
        chat_layout.setContentsMargins(18, 12, 18, 12)
        chat_layout.setSpacing(8)

        chat_label = QLabel("💬 Ask questions about your data:")
        chat_label.setFont(QFont("Segoe UI", 12))
        chat_layout.addWidget(chat_label)

        # Chat history area (QTextEdit for HTML formatting)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Segoe UI", 11))
        self.chat_area.setMinimumHeight(260)
        self.chat_area.setStyleSheet(
            "background: #f8f8fa; border-radius: 12px; padding: 8px; color: #111;"
        )
        chat_layout.addWidget(self.chat_area, 1)

        # Chat input row
        chat_input_row = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your question (e.g., Convert to JSON, Find correlation between columns x and y, etc.)")
        self.chat_input.setFont(QFont("Segoe UI", 11))
        # Fix: Set black font color for input field
        chat_input_palette = self.chat_input.palette()
        chat_input_palette.setColor(QPalette.ColorRole.Text, QColor("#111"))
        self.chat_input.setPalette(chat_input_palette)
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._on_send)
        self.chat_input.returnPressed.connect(self._on_send)
        chat_input_row.addWidget(self.chat_input, 1)
        chat_input_row.addWidget(send_btn)
        chat_layout.addLayout(chat_input_row)

        splitter.addWidget(chat_box)
        splitter.setStretchFactor(1, 3)

        # -- Status bar --
        self.status = QLabel("")
        self.status.setStyleSheet("color: #666; font-size: 11pt; margin-top:6px")
        layout.addWidget(self.status)

    # --- UI Actions ---
    def _paste_clipboard(self):
        text = QApplication.clipboard().text()
        if text:
            self.data_edit.setPlainText(text)
            self.status.setText("Clipboard content pasted.")
        else:
            self.status.setText("Clipboard is empty.")

    def _load_file(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Select file", "", "CSV/TSV/Text (*.csv *.tsv *.txt);;All Files (*)")
        if fpath:
            try:
                with open(fpath, encoding="utf-8") as f:
                    self.data_edit.setPlainText(f.read())
                self.status.setText(f"Loaded: {os.path.basename(fpath)}")
            except Exception as ex:
                self.status.setText(f"Error loading file: {ex}")

    def _on_send(self):
        user_question = self.chat_input.text().strip()
        self.data_text = self.data_edit.toPlainText().strip()
        if not self.data_text:
            self.status.setText("Paste or load your data first.")
            return
        if not user_question:
            self.status.setText("Type your question.")
            return
        self._add_to_chat("You", user_question)
        self.chat_input.clear()
        self.status.setText("Waiting for AI response...")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        try:
            ai_response = self._ask_llm(self.data_text, user_question)
            self._add_to_chat("AI", ai_response)
            self.status.setText("AI response received.")
        except Exception as ex:
            self._add_to_chat("AI", f"Error: {ex}")
            self.status.setText(f"Error: {ex}")
        QApplication.restoreOverrideCursor()

    def _add_to_chat(self, sender, msg):
        msg = msg.strip()
        if not msg: return
        self.chat_history.append((sender, msg))
        formatted = ""
        for s, m in self.chat_history:
            if s == "You":
                formatted += f"<b style='color:#137333'>{s}:</b> {m}<br>"
            else:
                formatted += f"<b style='color:#005eaa'>{s}:</b> {m}<br>"
        self.chat_area.setHtml(formatted)
        self.chat_area.moveCursor(QTextCursor.MoveOperation.End)

    # --- LLM Backend ---
    def _ask_llm(self, data, question):
        prompt = (
            "You are a data expert assistant. The user has pasted some data "
            "(such as CSV, TSV, or table text) below. "
            "Analyze the data and answer the user's question clearly and precisely. "
            "If the user asks for code (like JSON), return just the result or a clear answer.\n\n"
            f"User data:\n{data}\n\nUser question:\n{question}"
        )

        messages = [
            {"role": "system", "content": "You are a helpful, expert data scientist assistant."},
            {"role": "user", "content": prompt}
        ]
        # Call OpenAI
        resp = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.0,
            max_tokens=2048,
        )
        return resp.choices[0].message.content.strip()

    # --- Styling ---
    def _main_stylesheet(self):
        return """
        QWidget {
            background: #f2f3f7;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12.5pt;
        }
        QFrame {
            background: #fff;
            border-radius: 18px;
            border: 1.2px solid #e3e6ec;
            padding: 8px;
        }
        QPushButton {
            padding: 6px 18px;
            font-size: 12pt;
            border-radius: 10px;
            background: #00e676;
            color: #111;
            border: 1px solid #28a745;
            font-weight: 600;
        }
        QPushButton:hover {
            background: #69f0ae;
            border: 1.2px solid #2ec866;
            color: #111;
        }
        QLineEdit, QPlainTextEdit {
            border-radius: 8px;
            border: 1.2px solid #e0e0e0;
            background: #fafbfc;
            padding: 8px;
            font-size: 12pt;
            color: #111;
        }
        QTextEdit {
            color: #111;
        }
        """

# ====== Main Runner ======
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = DataChatBotDemo()
    w.show()
    sys.exit(app.exec())
