"""
Background workers for the AI-Powered Data Chatbot.

Qt repaints the window from its main thread, so any call that takes more than a
few milliseconds has to happen somewhere else. This module keeps that plumbing
in one place: the UI creates a worker, moves it to a QThread, and listens for a
signal instead of waiting for a return value.
"""

from PyQt6.QtCore import QObject, pyqtSignal

from llm_helper import LLMHelper


class AskWorker(QObject):
    """
    Runs a single LLMHelper.ask_llm() call away from the GUI thread.

    Signals:
        succeeded (str): Emitted with the model answer when the call returns.
        failed (str): Emitted with a message when the call raises.
    """

    succeeded = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, llm_helper: LLMHelper, data: str, question: str) -> None:
        """
        Store everything the call needs.

        Args:
            llm_helper (LLMHelper): Configured helper used to reach the API.
            data (str): The tabular data the question is about.
            question (str): The natural language question to answer.
        """
        super().__init__()
        self._llm_helper = llm_helper
        self._data = data
        self._question = question

    def run(self) -> None:
        """
        Perform the request and report the outcome through a signal.

        Every exception is converted into a failed signal on purpose: an
        unhandled exception on a worker thread would terminate it silently and
        leave the UI disabled with no explanation.
        """
        try:
            answer = self._llm_helper.ask_llm(self._data, self._question)
        except Exception as exc:  # noqa: BLE001 - reported to the user instead
            self.failed.emit(str(exc))
        else:
            self.succeeded.emit(answer)
