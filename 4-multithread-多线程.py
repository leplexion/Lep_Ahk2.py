import threading
from Lep_Ahkh2 import Lep_Ahkh2, get_main_dir, is32ptr, loop_long_sleep

# get dll file full path, you should make sure ahk and py both 32 or 64 bit program
ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
_ = {'dllpath': ah2dll32 if is32ptr() else ah2dll64}

def t1():
    ah2 = Lep_Ahkh2(_['dllpath'])
    ah2.do("""
        ; py thread will exit after ahk loop break
        ; 若不在ahk循环中, 执行完ahk代码将退出, t2同
        print('thread t1 start.`n')
        CoordMode 'tooltip', 'screen'
        Loop {
            ToolTip 't1:' A_Index, 100, 100
            sleep(10)
        }   
    """)

def t2():
    ah2 = Lep_Ahkh2(_['dllpath'])
    ah2.do("""
        print('thread t2 start.`n')
        CoordMode 'tooltip', 'screen'
        Loop {
            ToolTip 't2:' A_Index, 300, 100
            sleep(10)
        }    
    """)

def t3():
    ah2 = Lep_Ahkh2(_['dllpath'])
    def hk():
        ah2.do('print("you press hotkey" A_ThisHotkey)')
        ah2.do('print("你按下了热键:" A_ThisHotkey)')
        
    ah2.add_pyhk('f1', hk)
    
    loop_long_sleep()   # while True: sleep(86400)

if __name__ == '__main__':
    ts = []
    for fn in [t1, t2, t3]:
        t = threading.Thread(target=fn)
        t.start()
        ts.append(t)

    for t in ts:
        t.join()