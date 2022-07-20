# Lep_Ahk2.py

use Autohotkey H v2 dll in python, you can set hotkey on python or use all autohotkey functions

在Python中调用 Autohotkey H v2 dll 的功能库, 可设置热键, 调用所有ahk功能等

个人Q群: 690058080 - Coder FriendShip | 码农贼船


# methods / 方法
- __init__(self, dllpath:str='', title:str='', cmdline:str='')  # just entry the dllpath param / 正常使用只要填入 dllpath

- add_pyfn(self, pyfunc, alias:str='') # add python function for autohotkey
- del_pyhk(self, hotkey:str) # only exec hotkey off / 只是调用了 hotkey 'off'

- setval(self, name:str, value) # set ahk thread global variable / 设置 ahk 线程全局变量
- getval(self, name:str) # get ahk thread global variable / 获取 ahk 线程中的全局变量

- add(self, ahkscript:str) # add ahk script to exec, you can use it for ahk lib / 添加ahk字符串并执行, 通常用来添加ahk库
- add_file(self, ahkfile:str, encoding='utf-8') # add ahk file to exec, you can use it for ahk lib / 添加字符串并执行, 通常用来添加ahk库

- do0 / do / do2 : it may be delete after exec /  执行完可能将被删除
- do0(self, ahkscript:str)->None  # run ahk script, none return, fast / 无返回值, 最快
- do(self, ahkscript:str)->str    # assgign variable _return as string type will return string to python / 赋值给 _return 变量以字符串将返回字符串给python
- do2(self, ahkscript:str)->Any   # assign any type could translate to json will return to python, slow /  赋值任意可转json的对象返回给python, 偏慢

# capture img / 截图

![capture](https://raw.githubusercontent.com/leplexion/Lep_Ahk2.py/main/4-capture-%E6%88%AA%E5%9B%BE.PNG)


