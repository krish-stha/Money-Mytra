

from googleapiclient import _helpers as util

__author__ = ...
class Error(Exception):
 
    ...


class HttpError(Error):
 
    @util.positional(3)
    def __init__(self, resp, content, uri=...) -> None:
        ...
    
    @property
    def status_code(self):
     
        ...
    
    def __repr__(self): # -> str:
        ...
    
    __str__ = ...


class InvalidJsonError(Error):
  
    ...


class UnknownFileType(Error):
  
    ...


class UnknownLinkType(Error):
   
    ...


class UnknownApiNameOrVersion(Error):
    
    ...


class UnacceptableMimeTypeError(Error):
  
    ...


class MediaUploadSizeError(Error):

    ...


class ResumableUploadError(HttpError):
 
    ...


class InvalidChunkSizeError(Error):

    ...


class InvalidNotificationError(Error):

    ...


class BatchError(HttpError):
    """Error occurred during batch operations."""
    @util.positional(2)
    def __init__(self, reason, resp=..., content=...) -> None:
        ...
    
    def __repr__(self): # -> LiteralString:
        ...
    
    __str__ = ...


class UnexpectedMethodError(Error):
    """Exception raised by RequestMockBuilder on unexpected calls."""
    @util.positional(1)
    def __init__(self, methodId=...) -> None:
        """Constructor for an UnexpectedMethodError."""
        ...
    


class UnexpectedBodyError(Error):
    """Exception raised by RequestMockBuilder on unexpected bodies."""
    def __init__(self, expected, provided) -> None:
        """Constructor for an UnexpectedMethodError."""
        ...
    


