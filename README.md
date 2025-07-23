# AI-Powered Data Chatbot (PyQt6 + OpenAI LLM)

A visually modern, creative desktop demo app (by Bobby Azad) showing how LLMs can make data analysis conversational. Users paste or load CSV/TSV/tabular data, ask natural language questions ("Convert this to JSON", "Find the correlation between x and y column", etc), and get instant answers via OpenAI API. Built with PyQt6 for an interactive, professional UI.

---

## Features
- Paste or load any CSV/TSV/text data (from file or clipboard)
- Clean chat interface: ask any data question and get an AI-powered response
- Conversation history maintained in a modern, resizable UI
- Supports code/text output (JSON, summaries, stats, etc)
- UI and logic cleanly separated; robust error handling

---

## Quick Start (using pixi for environment management)

### 1. Install [pixi](https://pixi.sh/latest/#available-software) (if you haven’t already)

```bash
pip install pixi  # or see pixi docs for latest install command
```

### 2. Clone this repo

```bash
git clone https://github.com/gbazad93/llm-graphical-chatbot
cd <your-repo-folder>
```

### 3. Set up the pixi environment

If you already have a `pixi.toml` file (shared or in this repo):

```bash
pixi install
```

This will create a new environment with all required dependencies (see [pixi.toml](./pixi.toml)).

### 4. Set your OpenAI API key

You can store your API key in a `.env` file in the project root (where the main `.py` file is):

```
OPENAI_API_KEY=sk-...your-openai-api-key...
```

However, for improved security, **we recommend storing your API key as a system environment variable**.

**On Windows:**  
Open a command prompt window and run:
```cmd
setx OPENAI_API_KEY "<your-openai-api-key>"
```

To verify it's set, open a new command prompt and run:
```cmd
echo %OPENAI_API_KEY%
```

**On Linux or macOS:**  
Add the following line to your `~/.bashrc`, `~/.zshrc`, or appropriate shell config file:
```bash
export OPENAI_API_KEY="sk-...your-openai-api-key..."
```
Then reload your shell or run:
```bash
source ~/.bashrc  # or source ~/.zshrc
```
You can check the variable with:
```bash
echo $OPENAI_API_KEY
```

### 5. Run the app

```bash
pixi run python small_chatbot.py
```

---

## Dependencies
- [PyQt6](https://pypi.org/project/PyQt6/)
- [openai](https://pypi.org/project/openai/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

(Handled automatically by pixi install)

---

## Example Usage
- Paste or load a CSV file into the left panel.
- Type a question like `What is the correlation between Price and Sales?`.
- Click **Send**. The AI will analyze the data and show the result in the chat window.

---

## Screenshots

![screenshot1](./img/screenshot1.png)

---

## Customization
- Update `MODEL` in the code to use a different OpenAI model if desired.
- All UI colors/styles are defined in `_main_stylesheet()` method in the code for easy theming.

---

## Credits
- Demo and concept by Bobby Azad
- Built using [PyQt6](https://riverbankcomputing.com/software/pyqt/intro) and [OpenAI API](https://platform.openai.com/docs/api-reference)

