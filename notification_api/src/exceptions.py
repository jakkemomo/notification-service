class AppBaseException(Exception):
    pass


class DocNotFound(AppBaseException):
    msg = "Document not found"


class DocAlreadyExists(AppBaseException):
    msg = "Document exists"
