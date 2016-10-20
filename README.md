# awesome-python3-webapp
python3-webapp
Demo App for learning python
## Tips
### Day3
- `SQL`语句的占位符是`?`,而`MySQL`的占位符是`%s`,`select()`函数在内部自动替换.注意要始终坚持使用带参数的`SQL`,而不是自己拼接`SQL`字符串,这样可以防止`SQL`注入攻击
- 注意到`yield from`将调用一个子协程(也就是在一个协程中调用另一个协程)并直接获得子协程的返回结果.
- 如果传入`size`参数,就通过`fetchmany()`获取最多指定数量的记录,否则,通过`fetchall()`获取所有记录
- `execute()`函数和`select()`函数所不同的是,`cursor`对象不返回结果集,而是通过`rowcount`返回结果数
- [Python 3.5的async和await特性(PEP492翻译)] (https://my.oschina.net/cppblog/blog/469926)
- [深刻理解Python中的元类(metaclass)] (http://blog.jobbole.com/21351/)

### Day4
- `test`中在`create_pool`时需要对属性进行比对.比对成功才能打开
- ```AttributeError: 'Connection' object has no attribute '_writer'```常见错误
- `pycham`不能导入本地包,需要将文件夹设为`sources root`,右键->`make dictionary as`
- ~~`map函数`为什么会不起作用?~~(调通,去除`@classmethod` `save`,`update`,`remove`为对象调用函数,不是类函数)

### Day5
- `web`框架,装饰器装饰`get`和`post`函数,能让用户更快的使用
- `RequestHandler`是一个类,由于定义了`__call__()`方法，因此可以将其实例视为函数.
- [`join()函数`](./func.md) 用于将序列中的元素以指定的字符连接生成一个新的字符串.
- [`rfind()函数`](./func.md) 返回字符串最后一次出现的位置,如果没有匹配项则返回-1.

### Day6
- `app[__templating__]`可以获得模版
- ~~`index(*request)/index(**request)`需要变长参数或者关键字参数~~
- `coreweb.py`中有对参数进行对比和获取的,之前`request`参数没有进行返回,永远不能为`True` 已修改

### Day7
- `favicon.ico`是浏览器的标签头上面显示了一个图标
- 前端的`MVC`模式通常可以通过框架实现,这里用的是可以响应式编程的`uikit`
- 定义了`__base__.html`模版框架,让具体页面填充相对应的`block`来完成页面内容

### Day8
- `register.html`中通过`$('#vm').show();`来显示表单
- [Web编程之Cookie详解] (http://victor-jan.iteye.com/blog/964688)

### Day9
- [JS中的！=、== 、！==、===的用法和区别] (http://www.cnblogs.com/liluping860122/p/3539291.html)