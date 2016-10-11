# awesome-python3-webapp
python3-webapp
#Demo App for learning python
## Tips
### Day3
    - `SQL`语句的占位符是`?`,而`MySQL`的占位符是`%s`,`select()`函数在内部自动替换.注意要始终坚持使用带参数的`SQL`,而不是自己拼接`SQL`字符串,这样可以防止`SQL`注入攻击
    - 注意到`yield from`将调用一个子协程(也就是在一个协程中调用另一个协程)并直接获得子协程的返回结果.
    - 如果传入`size`参数,就通过`fetchmany()`获取最多指定数量的记录,否则,通过`fetchall()`获取所有记录
    - `execute()`函数和`select()`函数所不同的是,`cursor`对象不返回结果集,而是通过`rowcount`返回结果数