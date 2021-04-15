class AppBaseException(Exception):
    def __init(self, msg, *args):
        super(Exception, self).__init__(*args)
        self.msg = msg


class DocNotFound(AppBaseException):
    pass


class DocAlreadyExists(AppBaseException):
    pass
