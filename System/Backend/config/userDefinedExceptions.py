
'''This is the implementation of user defined Exception that is used extensively
in the implementation of the APIs'''

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

## user defined exceptions
class NotFound(Error):
    pass
