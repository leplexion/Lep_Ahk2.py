from Lep_Ahkh2 import Lep_Ahkh2, get_main_dir, is32ptr, loop_long_sleep

# get dll file full path, you should make sure ahk and py both 32 or 64 bit program
# 获取dll文件绝对路径, 可以写死, 但要保证dll与python同为32或64位, 如 dllpath = "C:\\ahk2x32.dll"
ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
dllpath = ah2dll32 if is32ptr() else ah2dll64


if __name__ == '__main__':
    ah2 = Lep_Ahkh2(dllpath)
    ah2.do("MsgBox 'hello world'")
    
