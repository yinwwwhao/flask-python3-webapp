使用 flask＆uikit 编写的博客。

这个项目本来是学廖雪峰的 Python 教程中的实战部分的时候，觉得那个啥有点头疼，所以选了 Flask。

当然嘛，有可能未来会不定期停更，原因嘛，上学。

那就这样吧。

### 计划：

> 1. 优化 Python 代码
> 2. 完善用户界面
> 3. 奋笔疾书
> 4. 优化前端代码

另外，如果你想要在你自己的电脑上搞，请项目根目录新建一个文件，名为`config.py`

内容如下：

```python
mode = 'dev'
smtp_server = 'smtp.xxx.com'
from_addr = 'xxx@xxx.com'
password = 'xxxxxx'
```

mode 表示是开发（dev）还是生产（prod），你也可以把他改成 prod

当然，如果你想尝试邮箱验证码的话，你就要开启`smtp`，然后啥啥啥（抱歉作者语文并不是那么好
