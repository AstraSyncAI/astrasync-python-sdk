"""
AstraSync exceptions
"""

class AstraSyncError(Exception):
    """Base exception for AstraSync SDK"""
    pass

class RegistrationError(AstraSyncError):
    """Error during agent registration"""
    pass

class ValidationError(AstraSyncError):
    """Error during data validation"""
    pass

class APIError(AstraSyncError):
    """Error from AstraSync API"""
    def __init__(self, message, status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
