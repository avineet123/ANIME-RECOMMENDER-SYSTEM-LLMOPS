import sys
import traceback
from typing import Optional


class CustomException(Exception):
    """
    A custom exception that includes detailed information about the error:
    - Original message
    - Underlying exception
    - Filename and line number where it occurred
    """

    def __init__(self, message: str, error_detail: Optional[Exception] = None):
        """
        Initializes the CustomException with a message and optional error detail.

        Args:
            message (str): A custom error message.
            error_detail (Exception, optional): The original exception caught (if any).
        """
        self.error_message = self._format_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def _format_error_message(message: str, error_detail: Optional[Exception]) -> str:
        """
        Formats a detailed error message including file and line number.

        Args:
            message (str): The custom message.
            error_detail (Exception): The underlying exception (if any).

        Returns:
            str: A detailed error message.
        """
        exc_type, _, exc_tb = sys.exc_info()

        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown File"
            line_number = "Unknown Line"

        return (
            f"{message} | "
            f"Error: {error_detail} | "
            f"File: {file_name} | "
            f"Line: {line_number}"
        )

    def __str__(self) -> str:
        return self.error_message
