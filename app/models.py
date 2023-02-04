from app.extensions import db
import time
import uuid

class Dict(dict):
    '''
    能使orm对象用xxx.xxx形式引用
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


def to_dict(self):
    return toDict({c.name: getattr(self, c.name, None) for c in self.__table__.columns})

db.Model.to_dict = to_dict
# 为了转换为字典

def next_id():
    return '%015d%s' % (int(time.time() * 1000), uuid.uuid4().hex)
# 生成id

class User(db.Model):
    __tablename__ = 'users'
    # 创建users model
    id = db.Column(db.String(50), primary_key=True, default=next_id)
    email = db.Column(db.String(50))
    passwd = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(50))
    image = db.Column(db.String(500))
    created_at = db.Column(db.Float, default=time.time)
    

class Blog(db.Model):
    __tablename__ = 'blogs'
    # 创建blogs model
    id = db.Column(db.String(50), primary_key=True, default=next_id)
    user_id = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    user_image = db.Column(db.String(50))
    name = db.Column(db.String(50))
    summary = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.Float, default=time.time)
    tag = db.Column(db.String(10))


class Comment(db.Model):
    __tablename__ = 'comments'
    # 创建comments model
    id = db.Column(db.String(50), primary_key=True, default=next_id)
    blog_id = db.Column(db.String(50))
    user_id = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    user_image = db.Column(db.String(500))
    content = db.Column(db.Text)
    created_at = db.Column(db.Float, default=time.time)

class Atlas(db.Model):
    __tablename__ = 'atlas'
    # 创建atlas model
    name = db.Column(db.String(50))
    url = db.Column(db.String(50), primary_key=True)
    created_at = db.Column(db.Float, default=time.time)
    private = db.Column(db.Boolean)