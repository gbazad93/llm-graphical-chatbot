"""
Main application module for the AI-Powered Data Chatbot.

This module contains the main UI components and application logic,
providing a PyQt6-based interface for data analysis using AI.
"""

import os
import sys
from typing import List, Tuple, Optional
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPlainTextEdit,
    QPushButton, QFileDialog, QLineEdit, QFrame, QSplitter, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import local modules
from styles import (
    get_main_stylesheet, get_header_frame_style, get_splitter_style,
    get_container_style, get_data_edit_style, get_primary_button_style,
    get_danger_button_style, get_chat_area_style, get_chat_input_style,
    get_send_button_style, get_status_container_style, get_welcome_message,
    STYLE_CONFIG
)
from llm_helper import LLMHelper


class DataChatBotDemo(QWidget):
    """
    Main application widget for the AI-Powered Data Chatbot.
    
    This class provides a complete UI for loading data and interacting
    with an AI assistant to analyze the data using natural language queries.
    """
    
    def __init__(self) -> None:
        """Initialize the DataChatBotDemo widget."""
        super().__init__()
        self.data_text: str = ""
        self.chat_history: List[Tuple[str, str]] = []
        self.llm_helper: LLMHelper = LLMHelper()
        
        self._setup_window()
        self._build_ui()
    
    def _setup_window(self) -> None:
        """
        Set up the main window properties.
        
        Configures window title, size, and applies the main stylesheet.
        """
        self.setWindowTitle("AI-Powered Data Chatbot - Demo by Bobby Azad")
        self.setMinimumSize(1200, 700)
        self.setStyleSheet(get_main_stylesheet())
    
    def _build_ui(self) -> None:
        """
        Build the complete user interface.
        
        Creates and arranges all UI components including header, data input panel,
        chat interface, and status bar.
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(16)

        # Enhanced Header Section
        header_frame = self._create_header_section()
        layout.addWidget(header_frame)

        # Main Splitter with improved proportions
        splitter = self._create_main_splitter()
        layout.addWidget(splitter, 1)

        # Enhanced status bar
        status_container = self._create_status_bar()
        layout.addWidget(status_container)
    
    def _create_header_section(self) -> QFrame:
        """
        Create the header section with title and subtitle.
        
        Returns:
            QFrame: The configured header frame widget.
        """
        header_frame = QFrame()
        header_frame.setStyleSheet(get_header_frame_style())
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 16, 20, 16)
        
        title_label = QLabel("🤖 AI-Powered Data Chatbot")
        title_label.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["title"], QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a365d; margin: 0; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Analyze your data with natural language • Demo by Bobby Azad")
        subtitle.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["subtitle"], QFont.Weight.Normal))
        subtitle.setStyleSheet("color: #2c5282; margin: 4px 0 0 0; background: transparent;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle)
        
        return header_frame
    
    def _create_main_splitter(self) -> QSplitter:
        """
        Create the main splitter containing data input and chat panels.
        
        Returns:
            QSplitter: The configured splitter widget.
        """
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(6)
        splitter.setStyleSheet(get_splitter_style())
        
        # Left Panel: Data Input
        data_container = self._create_data_input_panel()
        splitter.addWidget(data_container)
        
        # Right Panel: Chat Interface
        chat_container = self._create_chat_panel()
        splitter.addWidget(chat_container)
        
        # Set splitter proportions (40% data, 60% chat)
        splitter.setSizes([480, 720])
        
        return splitter
    
    def _create_data_input_panel(self) -> QWidget:
        """
        Create the data input panel with text area and control buttons.
        
        Returns:
            QWidget: The configured data input panel widget.
        """
        data_container = QWidget()
        data_container.setStyleSheet(get_container_style())
        data_layout = QVBoxLayout(data_container)
        data_layout.setContentsMargins(24, 20, 24, 20)
        data_layout.setSpacing(12)

        # Header
        data_header = QLabel("📊 Data Input")
        data_header.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["header"], QFont.Weight.Bold))
        data_header.setStyleSheet("color: #2d3748; margin-bottom: 8px;")
        data_layout.addWidget(data_header)

        # Instruction
        data_instruction = QLabel("Paste your CSV, TSV, or tabular data below:")
        data_instruction.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["normal"]))
        data_instruction.setStyleSheet("color: #4a5568; margin-bottom: 4px;")
        data_layout.addWidget(data_instruction)

        # Data input text area
        self.data_edit = QPlainTextEdit()
        self.data_edit.setPlaceholderText("Paste your data here or use the buttons below to load from clipboard/file...")
        self.data_edit.setFont(QFont("JetBrains Mono, Consolas, Monaco", STYLE_CONFIG["font_sizes"]["code"]))
        self.data_edit.setMinimumHeight(280)
        self.data_edit.setStyleSheet(get_data_edit_style())
        data_layout.addWidget(self.data_edit, 1)

        # Button container
        btn_container = self._create_data_buttons()
        data_layout.addWidget(btn_container)
        
        return data_container
    
    def _create_data_buttons(self) -> QWidget:
        """
        Create the button container for data input controls.
        
        Returns:
            QWidget: The configured button container widget.
        """
        btn_container = QWidget()
        btn_container.setMinimumHeight(60)
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(4, 12, 4, 12)
        btn_layout.setSpacing(12)
        
        # Paste button
        paste_btn = QPushButton("📋 Paste from Clipboard")
        paste_btn.setMinimumHeight(40)
        paste_btn.setStyleSheet(get_primary_button_style())
        paste_btn.clicked.connect(self._paste_clipboard)
        
        # Load file button
        load_btn = QPushButton("📁 Load File")
        load_btn.setMinimumHeight(40)
        load_btn.setStyleSheet(get_primary_button_style())
        load_btn.clicked.connect(self._load_file)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setMinimumHeight(40)
        clear_btn.setStyleSheet(get_danger_button_style())
        clear_btn.clicked.connect(lambda: self.data_edit.clear())
        
        btn_layout.addWidget(paste_btn)
        btn_layout.addWidget(load_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(clear_btn)
        
        return btn_container
    
    def _create_chat_panel(self) -> QWidget:
        """
        Create the chat interface panel.
        
        Returns:
            QWidget: The configured chat panel widget.
        """
        chat_container = QWidget()
        chat_container.setStyleSheet(get_container_style())
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(24, 20, 24, 20)
        chat_layout.setSpacing(12)

        # Header
        chat_header = QLabel("💬 AI Assistant")
        chat_header.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["header"], QFont.Weight.Bold))
        chat_header.setStyleSheet("color: #2d3748; margin-bottom: 8px;")
        chat_layout.addWidget(chat_header)

        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["small"]))
        self.chat_area.setMinimumHeight(320)
        self.chat_area.setStyleSheet(get_chat_area_style())
        self.chat_area.setHtml(get_welcome_message())
        chat_layout.addWidget(self.chat_area, 1)

        # Input section
        input_container = self._create_chat_input()
        chat_layout.addWidget(input_container)
        
        return chat_container
    
    def _create_chat_input(self) -> QWidget:
        """
        Create the chat input section with text field and send button.
        
        Returns:
            QWidget: The configured chat input container widget.
        """
        input_container = QWidget()
        input_container.setMinimumHeight(90)
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(4, 12, 4, 12)
        input_layout.setSpacing(8)
        
        # Input label
        input_label = QLabel("Ask your question:")
        input_label.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["small"], QFont.Weight.Medium))
        input_label.setStyleSheet("color: #4a5568;")
        input_layout.addWidget(input_label)
        
        # Input row with text field and button
        chat_input_row = QHBoxLayout()
        chat_input_row.setSpacing(12)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("e.g., 'What patterns do you see?' or 'Convert to JSON'...")
        self.chat_input.setFont(QFont("Segoe UI", STYLE_CONFIG["font_sizes"]["normal"]))
        self.chat_input.setMinimumHeight(44)
        self.chat_input.setStyleSheet(get_chat_input_style())
        
        send_btn = QPushButton("Send ➤")
        send_btn.setMinimumHeight(44)
        send_btn.setMinimumWidth(100)
        send_btn.setStyleSheet(get_send_button_style())
        send_btn.clicked.connect(self._on_send)
        self.chat_input.returnPressed.connect(self._on_send)
        
        chat_input_row.addWidget(self.chat_input, 1)
        chat_input_row.addWidget(send_btn)
        input_layout.addLayout(chat_input_row)
        
        return input_container
    
    def _create_status_bar(self) -> QFrame:
        """
        Create the status bar at the bottom of the application.
        
        Returns:
            QFrame: The configured status bar widget.
        """
        status_container = QFrame()
        status_container.setStyleSheet(get_status_container_style())
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(8, 4, 8, 4)
        
        self.status = QLabel("Ready • Load your data and start asking questions")
        self.status.setStyleSheet("color: #4a5568; font-size: 11pt; font-weight: 500;")
        status_layout.addWidget(self.status)
        
        return status_container
    
    def _paste_clipboard(self) -> None:
        """
        Paste content from the system clipboard into the data text area.
        
        Updates the status label to indicate success or failure.
        """
        text = QApplication.clipboard().text()
        if text:
            self.data_edit.setPlainText(text)
            self.status.setText("✅ Clipboard content pasted successfully")
        else:
            self.status.setText("⚠️ Clipboard is empty")
    
    def _load_file(self) -> None:
        """
        Open a file dialog to load data from a file.
        
        Supports CSV, TSV, TXT, and JSON files. Updates the status label
        to indicate success or failure of the file loading operation.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select data file", 
            "", 
            "Data Files (*.csv *.tsv *.txt *.json);;CSV Files (*.csv);;TSV Files (*.tsv);;Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    self.data_edit.setPlainText(content)
                filename = os.path.basename(file_path)
                self.status.setText(f"✅ Successfully loaded: {filename}")
            except Exception as ex:
                self.status.setText(f"❌ Error loading file: {str(ex)}")
    
    def _on_send(self) -> None:
        """
        Handle the send button click or Enter key press.
        
        Validates input, sends the question to the AI, and updates the chat area
        with both the user question and AI response.
        """
        user_question = self.chat_input.text().strip()
        self.data_text = self.data_edit.toPlainText().strip()
        
        if not self.data_text:
            self.status.setText("⚠️ Please paste or load your data first")
            return
        if not user_question:
            self.status.setText("⚠️ Please type your question")
            return
            
        # Add user message to chat history
        self._add_to_chat("You", user_question)
        self.chat_input.clear()
        
        # Show loading state
        self.status.setText("🤔 AI is analyzing your data...")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents()
        
        try:
            ai_response = self.llm_helper.ask_llm(self.data_text, user_question)
            self._add_to_chat("AI", ai_response)
            self.status.setText("✅ Response received")
        except Exception as ex:
            error_msg = f"I apologize, but I encountered an error: {str(ex)}"
            self._add_to_chat("AI", error_msg)
            self.status.setText(f"❌ Error: {str(ex)}")
        finally:
            QApplication.restoreOverrideCursor()
    
    def _add_to_chat(self, sender: str, message: str) -> None:
        """
        Add a message to the chat history and update the display.
        
        Args:
            sender (str): The sender of the message ("You" or "AI").
            message (str): The message content to add.
        """
        message = message.strip()
        if not message: 
            return
            
        self.chat_history.append((sender, message))
        
        # Build formatted HTML using the helper
        formatted_html = self.llm_helper.build_chat_history_html(self.chat_history)
        self.chat_area.setHtml(formatted_html)
        
        # Scroll to bottom
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_chat_history(self) -> None:
        """
        Clear the chat history and reset the chat area to welcome message.
        """
        self.chat_history.clear()
        self.chat_area.setHtml(get_welcome_message())
        self.status.setText("Chat history cleared")
    
    def get_chat_history(self) -> List[Tuple[str, str]]:
        """
        Get the current chat history.
        
        Returns:
            List[Tuple[str, str]]: List of (sender, message) tuples.
        """
        return self.chat_history.copy()
    
    def set_data_text(self, data: str) -> None:
        """
        Set the data text programmatically.
        
        Args:
            data (str): The data text to set.
        """
        self.data_edit.setPlainText(data)
        self.data_text = data
    
    def get_data_text(self) -> str:
        """
        Get the current data text.
        
        Returns:
            str: The current data text.
        """
        return self.data_edit.toPlainText().strip()


def main() -> None:
    """
    Main entry point for the application.
    
    Creates the QApplication, initializes the main widget,
    and starts the event loop.
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better cross-platform appearance
    
    # Check if API key is available
    if not LLMHelper.validate_api_key():
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key before running the application.")
        sys.exit(1)
    
    try:
        widget = DataChatBotDemo()
        widget.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
