from queue import Queue
from Lep_Ahkh2 import Lep_Ahkh2, get_main_dir, is32ptr, loop_long_sleep

# get dll file full path, you should make sure ahk and py both 32 or 64 bit program
# 获取dll文件绝对路径, 可以写死, 但要保证dll与python同为32或64位, 如 dllpath = "C:\\ahk2x32.dll"
ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
dllpath = ah2dll32 if is32ptr() else ah2dll64

if __name__ == '__main__':

    ah2 = Lep_Ahkh2(dllpath)

    # ------------------------
    # none param call
    # 无参
    def pycb():
        print('1. hello world')
        print('1. 你好世界')
        
    ah2.add_pyfn(pycb)
    ah2.do('pycb()')

    # ------------------------5
    # py function alias
    # py 函数别名
    def pycb2():
        print('2. hello world again')
        print('2. 再次你好世界')
    ah2.add_pyfn(pycb, 'pycb2alias')
    ah2.do('pycb2alias()')


    # ------------------------
    # pass param through py fun, print() is the preset function by .add() method
    # ahk给py函数传参, print() 为预设的函数
    def pycb_add(a, b):
        return a + b
    ah2.add_pyfn(pycb_add)
    ah2.do('print("2.111+222=" pycb_add(111, 222))')
    print(ah2.do('_return := "2.111+222=" pycb_add(111, 222)'))

    # ------------------------
    # hotkey
    # a = 0 # not thread save, you should use dict, list or Queue thread save type data using in python call back
    # a = 0 # 线程不安全, 要用dict, list, Queue 之类线程安全的对象可在python回调函数里使用
    a = [0]
    q = Queue()
    q.put(123)
    def hk():
        a[0] += 1
        print(a[0])

    def hk2():
        print('hk2')

    ah2.add_pyhk('f1', hk)

    ah2.add_pyhk('f3', hk2)
    from time import sleep

    # ah2.add('F3::hk()')
    while (True):
        sleep(100)



