"""
CSS styling module for the AI-Powered Data Chatbot application.

This module contains all styling constants and methods for the PyQt6 application,
providing a centralized location for UI styling definitions.
"""

from typing import Dict, Any


def get_main_stylesheet() -> str:
    """
    Get the main application stylesheet.
    
    Returns:
        str: The main stylesheet string for the application.
    """
    return """
    QWidget {
        background: #f1f5f9;
        font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
        font-size: 12pt;
    }
    
    /* Default button styling - will be overridden by individual button styles */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #4299e1, stop:1 #3182ce);
        color: white;
        border: 2px solid #3182ce;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 12pt;
        font-weight: 600;
        min-height: 20px;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #63b3ed, stop:1 #4299e1);
        border-color: #4299e1;
    }
    
    QPushButton:pressed {
        background: #2c5282;
        border-color: #2c5282;
    }
    
    QPushButton:disabled {
        background: #a0aec0;
        color: #718096;
        border-color: #cbd5e0;
    }
    """


def get_header_frame_style() -> str:
    """
    Get the header frame stylesheet.
    
    Returns:
        str: The header frame stylesheet string.
    """
    return """
    QFrame {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #e6f3ff, stop:1 #f0f8ff);
        border-radius: 16px;
        padding: 24px;
        border: 2px solid #bee3f8;
    }
    """


def get_splitter_style() -> str:
    """
    Get the splitter stylesheet.
    
    Returns:
        str: The splitter stylesheet string.
    """
    return """
    QSplitter::handle {
        background: #e1e5e9;
        border-radius: 3px;
    }
    QSplitter::handle:hover {
        background: #cbd5e0;
    }
    """


def get_container_style() -> str:
    """
    Get the container widget stylesheet.
    
    Returns:
        str: The container stylesheet string.
    """
    return """
    QWidget {
        background: white;
        border-radius: 16px;
        border: 2px solid #e2e8f0;
    }
    """


def get_data_edit_style() -> str:
    """
    Get the data edit text area stylesheet.
    
    Returns:
        str: The data edit stylesheet string.
    """
    return """
    QPlainTextEdit {
        background: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        color: #2d3748;
        line-height: 1.4;
    }
    QPlainTextEdit:focus {
        border-color: #4299e1;
        background: #edf2f7;
    }
    """


def get_primary_button_style() -> str:
    """
    Get the primary button stylesheet.
    
    Returns:
        str: The primary button stylesheet string.
    """
    return """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #4299e1, stop:1 #3182ce);
        color: white;
        border: 2px solid #3182ce;
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 12pt;
        font-weight: 600;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #63b3ed, stop:1 #4299e1);
        border-color: #4299e1;
    }
    """


def get_danger_button_style() -> str:
    """
    Get the danger button stylesheet.
    
    Returns:
        str: The danger button stylesheet string.
    """
    return """
    QPushButton {
        background: #fed7d7;
        color: #c53030;
        border: 2px solid #feb2b2;
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 12pt;
        font-weight: 600;
    }
    QPushButton:hover {
        background: #fbb6ce;
        border-color: #f687b3;
    }
    """


def get_chat_area_style() -> str:
    """
    Get the chat area stylesheet.
    
    Returns:
        str: The chat area stylesheet string.
    """
    return """
    QTextEdit {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        color: #2d3748;
        selection-background-color: #bee3f8;
    }
    QScrollBar:vertical {
        background: #edf2f7;
        width: 12px;
        border-radius: 6px;
    }
    QScrollBar::handle:vertical {
        background: #cbd5e0;
        border-radius: 6px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #a0aec0;
    }
    """


def get_chat_input_style() -> str:
    """
    Get the chat input stylesheet.
    
    Returns:
        str: The chat input stylesheet string.
    """
    return """
    QLineEdit {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 22px;
        padding: 12px 18px;
        color: #2d3748;
        font-size: 12pt;
    }
    QLineEdit:focus {
        border-color: #4299e1;
        background: #f7fafc;
    }
    """


def get_send_button_style() -> str:
    """
    Get the send button stylesheet.
    
    Returns:
        str: The send button stylesheet string.
    """
    return """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #4299e1, stop:1 #3182ce);
        color: white;
        border: 2px solid #3182ce;
        border-radius: 22px;
        padding: 10px 20px;
        font-size: 12pt;
        font-weight: 600;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #63b3ed, stop:1 #4299e1);
        border-color: #4299e1;
    }
    QPushButton:pressed {
        background: #2c5282;
        border-color: #2c5282;
    }
    """


def get_status_container_style() -> str:
    """
    Get the status container stylesheet.
    
    Returns:
        str: The status container stylesheet string.
    """
    return """
    QFrame {
        background: #edf2f7;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        padding: 8px 16px;
    }
    """


def get_welcome_message() -> str:
    """
    Get the welcome message HTML for the chat area.
    
    Returns:
        str: The welcome message HTML string.
    """
    return """
    <div style="text-align: center; color: #718096; margin: 40px 20px;">
        <h3 style="color: #4a5568; margin-bottom: 12px;">👋 Welcome to your AI Data Assistant!</h3>
        <p style="margin: 8px 0; line-height: 1.6;">Load your data on the left, then ask questions like:</p>
        <ul style="text-align: left; max-width: 400px; margin: 16px auto;">
            <li style="margin: 6px 0;">"What are the main trends in this data?"</li>
            <li style="margin: 6px 0;">"Convert this to JSON format"</li>
            <li style="margin: 6px 0;">"Show me correlations between columns"</li>
            <li style="margin: 6px 0;">"Summarize the key insights"</li>
        </ul>
    </div>
    """


# Style configuration dictionary
STYLE_CONFIG: Dict[str, Any] = {
    "font_sizes": {
        "title": 24,
        "subtitle": 13,
        "header": 16,
        "normal": 12,
        "small": 11,
        "code": 10,
    },
    "colors": {
        "primary": "#4299e1",
        "secondary": "#3182ce",
        "success": "#38b2ac",
        "danger": "#c53030",
        "text_primary": "#2d3748",
        "text_secondary": "#4a5568",
        "background": "#f1f5f9",
        "white": "white",
    },
    "spacing": {
        "small": 8,
        "medium": 12,
        "large": 16,
        "extra_large": 20,
    },
    "border_radius": {
        "small": 8,
        "medium": 12,
        "large": 16,
        "extra_large": 22,
    },
}