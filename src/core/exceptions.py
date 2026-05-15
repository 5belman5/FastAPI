class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(BaseAppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class InfrastructureException(BaseAppException):
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500)

class DomainException(BaseAppException):
    def __init__(self, message: str = "Domain logic error"):
        super().__init__(message, status_code=400)
