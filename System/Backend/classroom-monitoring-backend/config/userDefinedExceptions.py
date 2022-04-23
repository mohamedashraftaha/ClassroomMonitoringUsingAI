
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

## user defined exceptions
class NotFound(Error):
    pass

class IncorrectData(Error):
    pass