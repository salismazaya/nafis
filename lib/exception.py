class BaseException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)

        self.message = message

    def get_message(self):
        return self.message
    
class SystemError(BaseException): pass

class NotFoundError(BaseException): pass