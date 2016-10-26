# 遇到的概念
- [Python 3.5的async和await特性(PEP492翻译)] (https://my.oschina.net/cppblog/blog/469926)
- [深刻理解Python中的元类(metaclass)] (http://blog.jobbole.com/21351/)
- [Web编程之Cookie详解] (http://victor-jan.iteye.com/blog/964688)
- [JS中的！=、== 、！==、===的用法和区别] (http://www.cnblogs.com/liluping860122/p/3539291.html)
- [Referer详解] (http://www.cnblogs.com/maifengqiang/archive/2011/08/01/2124267.html)
- [W3school] (http://www.w3school.com.cn)
- `MVVM`初识
    > 初始化Vue时，我们指定3个参数：
    > el：根据选择器查找绑定的View，这里是#vm，就是id为vm的DOM，对应的是一个<div>标签；
    > data：JavaScript对象表示的Model，我们初始化为{ name: '', summary: '', content: ''}；
    > methods：View可以触发的JavaScript函数，submit就是提交表单时触发的函数。
    > 我们在<form>标签中，用几个简单的v-model，就可以让Vue把Model和View关联起来：
    
        ```
        <!-- input的value和Model的name关联起来了 -->
        <input v-model="name" class="uk-width-1-1">
        ```

    > Form表单通过`<form v-on="submit: submit">`把提交表单的事件关联到submit方法.
- [Python 中 str 和 repr 的区别] (http://www.oschina.net/translate/difference-between-str-and-repr-in-python)
    ``` python
     class Sic(object): pass
     ... 
     print str(Sic())
     <__main__.Sic object at 0x8b7d0>
     print repr(Sic())
     <__main__.Sic object at 0x8b7d0>
    
     class Sic(object): 
     ... def __repr__(object): return 'foo'
     ... 
     print str(Sic())
     foo
     print repr(Sic())
     foo
     class Sic(object):
     ... def __str__(object): return 'foo'
     ... 
     print str(Sic())
     foo
     print repr(Sic())
     <__main__.Sic object at 0x2617f0>
     ```
    
- [Javascript之confirm的用法] (http://www.cnblogs.com/netserver/p/4573512.html)
