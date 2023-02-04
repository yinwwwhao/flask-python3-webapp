class Message(dict):
    def __init__(self, message):
        super(Message, self).__init__(message=message)
    

class APIError(Message):
    def __init__(self, error_type, error_text):
        super(APIError, self).__init__({'error': {'type': error_type,'text': error_text}})


class APIValueError(APIError):
    '''
    指示输入值有误或无效
    '''
    def __init__(self, message):
        super(APIValueError, self).__init__('value:invalid', message)

class APIResourceNotFoundError(APIError):
    '''
    找不到资源而产生的错误
    '''
    def __init__(self, message):
        super(APIResourceNotFoundError, self).__init__('value:notfound', message)

class APIPermissionError(APIError):
    '''
    api权限不足产生的错误
    '''
    def __init__(self, message):
        super(APIPermissionError, self).__init__('permission:forbidden', message)