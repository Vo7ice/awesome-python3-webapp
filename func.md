# 记录遇到的函数用法和实例

- `Python` `join()` 方法用于将序列中的元素以指定的字符连接生成一个新的字符串.

    ``` python
        #!/usr/bin/python
        str = "-";
        seq = ("a", "b", "c"); # 字符串序列
        print str.join( seq );
        以上实例输出结果如下：
        a-b-c
    ```
    
- `python` `rfind()`  返回字符串最后一次出现的位置,如果没有匹配项则返回-1.
    
    ``` python
        rfind()方法语法：
        str.rfind(str, beg=0 end=len(string))
        
        str -- 查找的字符串
        beg -- 开始查找的位置，默认为0
        end -- 结束查找位置，默认为字符串的长度。
        
        #!/usr/bin/python
    
        str = "this is really a string example....wow!!!";
        substr = "is";
        
        print str.rfind(substr);
        print str.rfind(substr, 0, 10);
        print str.rfind(substr, 10, 0);
        
        print str.find(substr);
        print str.find(substr, 0, 10);
        print str.find(substr, 10, 0);
        以上实例输出结果如下：
        
        5
        5
        -1
        2
        2
        -1
    ```

- `python` `__import__` `python`内建函数,用来导入模块

    ``` python
    使用__import__函数获得特定函数 
    def getfunctionbyname(module_name,function_name):
        module = __import__(module_name)
        return getattr(module,function_name)
    ```
    
- `python` `globals() & locals()`
> 1.局部名字空间 - 特指当前函数或类的方法.如果函数定义了一个局部变量 x,Python将使用
  这个变量，然后停止搜索.
> 2.全局名字空间 - 特指当前的模块.如果模块定义了一个名为 x 的变量,函数或类,Python
  将使用这个变量然后停止搜索.
> 3.内置名字空间 - 对每个模块都是全局的.作为最后的尝试,Python将假设 x 是内置函数或变量.

- `python` `callable(object)`检查对象`object`是否可调用.如果返回`True`,`object`仍然可能调用失败;但如果返回`False`,调用对象`object`绝对不会成功.
    `Caution` 类是可调用的,而类的实例实现了`__call__()`方法才可调用.
    
- `python` 正确拼写是`startswith`,不能写成`startwith`

- `python` 将`dict`转换成可以用x.y形式的类`Dict`时候
    ``` python
    # 将dict转化为可以x.y形式的Dict
    def toDict(d):
        D = Dict()#这里为转换后的类名
        for k, v in d.items():
            D[k] = toDict(v) if isinstance(v, dict) else v
        return D
    ```

- `python` `set_cookie`
    ``` python
    def set_cookie(self, name, value, *, expires=None,
                   domain=None, max_age=None, path='/',
                   secure=None, httponly=None, version=None):
    参数	描述
    name	必需 规定 cookie 的名称
    value	必需 规定 cookie 的值
    expire	可选 规定 cookie 的有效期
    path	可选 规定 cookie 的服务器路径 如果path设置为"/",那就是在整个domain都有效
    domain	可选 规定 cookie 的域名
    secure	可选 规定是否通过安全的 HTTPS 连接来传输 cookie 值为0或1
    max_age	可选 cookie需要延续的时间(以秒为单位)
    ```
    
- `python` `map函数`
    [Python中map()函数浅析] (https://my.oschina.net/zyzzy/blog/115096)
    map(func, seq) 
    1. 对可迭代函数'iterable'中的每一个元素应用‘function’方法，将结果作为list返回
    2. 如果给出了额外的可迭代参数，则对每个可迭代参数中的元素‘并行’的应用‘function’
    3. 如果'function'给出的是‘None’，自动假定一个‘identity’函数
    
    ``` python
        list1 = [11,22,33]
        map(None,list1)
        [11, 22, 33]
        list1 = [11,22,33]
        list2 = [44,55,66]
        list3 = [77,88,99]
        map(None,list1,list2,list3)
        [(11, 44, 77), (22, 55, 88), (33, 66, 99)]
    ```

- `python` `filter函数`
    filter()也接收一个函数和一个序列.
    和map()不同的时,filter()把传入的函数依次作用于每个元素
    然后根据返回值是True还是False决定保留还是丢弃该元素
   
- `JavaScript` `preventDefault()`
    1. 定义和用法
    
        方法阻止元素发生默认的行为(例如，当点击提交按钮时阻止对表单的提交)
    2. 语法
    
        `event.preventDefault()`
    3. 参数	描述
    
        `event` 	必需,规定阻止哪个事件的默认动作,这个`event`参数来自事件绑定函数.

- `JavaScript` `confirm`
    1. 定义和用法
        confirm函数用于提供确认功能
        
        - 首先显示给定的message参数所包含的信息,并提供两个可选择的回答"OK"和"CANCEL"
        - 然后等待用户选择其中的一个
        - 如果用户选择"OK"则返回true;否则,如若选择"CANCEL"则返回false
    2. 语法
    
        `window.confirm (message, ok, cancel)`
        
        [Javascript之confirm的用法] (http://www.cnblogs.com/netserver/p/4573512.html)

