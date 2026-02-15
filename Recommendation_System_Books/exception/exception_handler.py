import os
import sys

class AppException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = AppException.get_detailed_error_message(error_message=error_message, error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: sys) -> str:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename

        # Extracting line number from the traceback
        line_number = exc_tb.tb_lineno

        # Creating a detailed error message with file name, line number and error message
        detailed_error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] with error message: [{error_message}]"
        return detailed_error_message

    def __repr__(self):
        """
        Formatting object of AppException in a way that it returns the name of the class and error message when we print the object.
        """
        return AppException.__name__.__str__()
    
    def __str__(self):
        """
        This function is used to return the error message when we print the object of AppException class.
        """
        return self.error_message