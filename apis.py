
class Page(object):
    '''
    定义page，用于处理MySQL分段查询
    '''

    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        # 一共有多少个内容
        self.page_size = page_size
        # 每一页有多少个内容
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        # 一共有多少页
        if (item_count == 0) or (page_index > self.page_count):
            # 如果数据库中没有一条信息（item_count == 0）或当前页打印一共页数
            self.offset = 0
            self.limit = 0
            self.page_index = 1
            # 设置当前页为1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
            '''
            offest: 起始位置
            limit: 结束位置
            '''
        self.has_next = self.page_index < self.page_count
        # 是否还有下一页
        self.has_previous = self.page_index > 1
        # 是否还有上一页

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % (
        self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__




class APIError(Exception):
    '''
    定义最基础的apierror，所有error都从此继承
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        # 引发xxxError: message
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    '''
    指示输入值有误或无效
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    '''
    找不到资源而产生的错误
    '''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

class APIPermissionError(APIError):
    '''
    api权限不足产生的错误
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)