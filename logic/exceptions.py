class NoInternetConnectionException(Exception):
    def __init__(self):
        self.message = 'No internet connection'
        super().__init__(self.message)

class RequestLimitExceededException(Exception):
    def __init__(self):
        self.message = 'Request limit exceeded'
        super().__init__(self.message)

class NoFileSelectedException(Exception):
    def __init__(self):
        self.message = 'No file selected'
        super().__init__(self.message)


class SmthWrongWithFileException(Exception):
    def __init__(self):
        self.message = 'Something wrong with the file'
        super().__init__(self.message)


class CantLoadDefaultSentencesException(Exception):
    def __init__(self):
        self.message = 'Can\'t load default sentences'
        super().__init__(self.message)

class InputCharacterException(Exception):
    def __init__(self):
        self.message = 'The entered character is not supported'
        super().__init__(self.message)