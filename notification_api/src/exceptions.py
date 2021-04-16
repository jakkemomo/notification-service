class AppBaseException(Exception):
    def __init__(self, msg, *args):
        super(Exception, self).__init__(*args)
        self.msg = msg


class DocNotFound(AppBaseException):
    pass


class DocAlreadyExists(AppBaseException):
    pass
