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
