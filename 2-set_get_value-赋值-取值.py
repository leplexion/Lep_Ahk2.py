from Lep_Ahkh2 import Lep_Ahkh2, get_main_dir, is32ptr, loop_long_sleep

# get dll file full path, you should make sure ahk and py both 32 or 64 bit program
# 获取dll文件绝对路径, 可以写死, 但要保证dll与python同为32或64位, 如 dllpath = "C:\\ahk2x32.dll"
ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
dllpath = ah2dll32 if is32ptr() else ah2dll64

if __name__ == '__main__':
    ah2 = Lep_Ahkh2(dllpath)

    # -----------------------------------------------
    # 未赋值故的变量返回None
    result = ah2.getval('never_assgined')
    print(f'1. never_assgined={result}')

    # -----------------------------------------------
    # setval 与 getval 作用的是全局变量
    ah2.setval('num', 123)
    result = ah2.getval('num')
    print(f'2. num={result}')

    # -----------------------------------------------
    # list 列表
    # for j in range(0, 99999):
    ah2.setval('arr', [55,66,77,88,99])
    ah2.do("""
        pyprint('3.1 arr - ah2')
        for i, v in arr
            pyprint('  - ' i ': ' v)
    """)
    print('3.2 arr - py')
    arr = ah2.getval('arr')
    for i in range(0, len(arr)):
        print(f'  py - {i}: {arr[i]}')

    # -----------------------------------------------
    # dict 字典
    for j in range(0, 5):
        ah2.setval('obj', {'idx': j, 'name': f'im idx{j}'})
        ah2.do("""

            for key, val in obj {
                pyprint('-----------------')
                pyprint('  - ' key ': ' val)
            }
        """)
        

