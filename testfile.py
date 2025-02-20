import unittest
from unittest.mock import patch
import logging
from exception_handlers import MissingEnvironmentVariableError, CustomRetryException

class TestCustomExceptions(unittest.TestCase):

    def test_missing_environment_variable_error(self):
        """Test the MissingEnvironmentVariableError exception"""
        variable_names = ["DB_HOST", "API_KEY"]
        with self.assertRaises(MissingEnvironmentVariableError) as context:
            raise MissingEnvironmentVariableError(variable_names)

        self.assertIn("DB_HOST", str(context.exception))
        self.assertIn("API_KEY", str(context.exception))
        self.assertIn("is missing", str(context.exception))

    def test_custom_retry_exception(self):
        """Test the CustomRetryException exception"""
        message = "Retry failed for request"
        status_code = 500
        exception_details = {"retry_count": 3}

        with self.assertRaises(CustomRetryException) as context:
            raise CustomRetryException(message, status_code=status_code, exception_details=exception_details)

        self.assertEqual(context.exception.message, message)
        self.assertEqual(context.exception.status_code, status_code)
        self.assertEqual(context.exception.exception_details, exception_details)

    @patch("logging.error")  # Mock the logging.error function
    def test_logging_in_custom_retry_exception(self, mock_logging_error):
        """Test if CustomRetryException logs the error message using @patch"""
        message = "Logging test"
        
        with self.assertRaises(CustomRetryException):
            raise CustomRetryException(message)

        # Assert that logging.error was called once with the correct message
        mock_logging_error.assert_called_once_with(message)

if __name__ == "__main__":
    unittest.main()