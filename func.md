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