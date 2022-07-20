import ctypes
from ctypes import c_int, c_uint, c_void_p, c_wchar_p, _SimpleCData, create_string_buffer, pointer, cast, sizeof, string_at
import json
import platform
import __main__, sys, pathlib
from time import sleep

def loop_long_sleep():
    while True: sleep(86400)

def is32ptr()->bool:
    '''判断本进程是32位程序'''
    return platform.architecture()[0] == '32bit'

def get_main_dir():
    '''获取 入口 文件所在目录'''
    if getattr(sys, 'frozen', False): return sys.executable
    return str(pathlib.Path(__main__.__file__).parent.absolute())

def getptrnum(ptr, ctype:_SimpleCData):
    '''
        # 获取数字类型指针的
        getptrnum(buff.ptr, c_int)
    '''
    return ctype.from_address(ptr).value
    
def setptrnum(ptr, ctype:_SimpleCData, val):
    '''
        # 设置数字类型指针的值, ctype 为 类型, 非实例化对象
        setptrnum(buff.ptr, c_int, 567)
    '''
    ctype.from_address(ptr).value = val

def getptrstr(ptr, size:int, encoding:str):
    '''
        # 获取指针的指向的字符串
        b = Lep_Buffer.create_from_str('你好世界')
        print(getptrstr(b.ptr, b.size, 'utf-8'))
    '''
    b = string_at(ptr, size)
    buff = create_string_buffer(b)
    return buff.raw.decode(encoding=encoding)

def getptr(buff:_SimpleCData):
    '''
        # 获取已实例化的 ctype 的指针
        i = c_int(0)
        p = getbuffptr(i)
        print(getptrnum(i, c_int))
    '''
    return cast(pointer(buff), c_void_p).value

def getptrhex(buff:_SimpleCData):
    '''
        # 获取已实例化的 ctype 的指针, 返回十六进制字符串
    '''
    return hex(getptr(buff))

def create_buff_str(string:str, encoding:str='utf8'):
    string += '\0\0'
    bytes_ = string.encode(encoding)
    buff = create_string_buffer(bytes_)
    return (buff, sizeof(buff), getptrhex(buff))

class Lep_Ahkh2_Orgin:

    ah2dll:ctypes.CDLL = None

    @staticmethod
    def settypes(ah2dll:ctypes.CDLL):
        '''该dll导出函数皆为CDecl Call'''    
        # ah2dll.MinHookEnable.restype=
        # ah2dll.MinHookEnable.argtypes=

        # ah2dll.MinHookDisable.restype=
        # ah2dll.MinHookDisable.argtypes=

        # ah2dll.g_ThreadExitApp.restype=
        # ah2dll.g_ThreadExitApp.argtypes=

        # ah2dll.g_FirstThreadID.argtypes=
        # ah2dll.g_FirstThreadID.restype=

        # (Script, cmd, Title) 
        # -> ThreadID: 线程id
        ah2dll.NewThread.restype=c_uint
        ah2dll.NewThread.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p]

        # (ThreadID) 
        # -> IsRunning: 1 正在运行 0 不在运行
        ah2dll.ahkReady.restype=c_int
        ah2dll.ahkReady.argtypes=[c_uint]

        # (FuncName, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, ThreadId) 
        # -> IsCalled: 1 找到函数并已调用, 0 未找到函数并未调用
        ah2dll.ahkPostFunction.restype=c_uint
        ah2dll.ahkPostFunction.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_uint]
        
        # (PauseFlag, ThreadId) : PauseFlag: 字符串 On / Off / TRUE / FALSE / 1 / 0 
        # -> IsPaused: 1 已暂停 0 
        ah2dll.ahkPause.restype=c_int
        ah2dll.ahkPause.argtypes=[c_wchar_p, c_uint]

        # (LabelName, IsWait, ThreadId) : IsWait: 整数 1 等待label执行结束, 0 不等待
        # -> IsLabelFoundAndExec: 标签找到并执行了 
        ah2dll.ahkLabel.restype= c_int
        ah2dll.ahkLabel.argtypes= [c_wchar_p, c_uint, c_uint]

        # (VarName, GetVarPointer, ThreadId): GetVarPointer: 1 获取指针 0 获取内容
        # -> VarPointer: 指针或内容
        ah2dll.ahkgetvar.restype=c_void_p
        ah2dll.ahkgetvar.argtypes= [c_wchar_p, c_uint, c_uint]

        # (FuncName, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, ThreadID)
        # -> ReturnStr: ahk函数返回值
        ah2dll.ahkFunction.restype=c_wchar_p
        ah2dll.ahkFunction.argtypes=[c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_wchar_p, c_uint]

        # (LabelName, ThreadId)
        # -> LabelPointer: 标签指针, 返回0没找到标签
        ah2dll.ahkFindLabel.restype=c_void_p
        ah2dll.ahkFindLabel.argtypes=[c_wchar_p, c_uint]
        
        # (FuncName, ThreadId)
        # -> FuncPointer: 函数指针, 返回0没找到函数
        ah2dll.ahkFindFunc.restype=c_void_p
        ah2dll.ahkFindFunc.argtypes=[c_wchar_p, c_uint]

        # (LinePointer, Mode, ThreadId): Mode: 0 执行且返回下一行的指针 / 1 UNTIL_RETURN 直到遇到return / 2 UNTIL_BLOCK_END / 直到block块结束 / 3 ONLY_ONE_LINE 仅执行这一行
        # -> NextLinePointer: 下一行的函数指针
        ah2dll.ahkExecuteLine.restype=c_void_p
        ah2dll.ahkExecuteLine.argtypes=[c_void_p, c_uint, c_uint]

        # (Script, ThreadId)
        # -> IsExecSuccess: 1 执行成功 0 执行失败
        ah2dll.ahkExec.restype=c_uint
        ah2dll.ahkExec.argtypes=[c_wchar_p, c_uint]

        # (VarName, Value, ThreadId)
        # -> IsAssignSuccess: -1 失败 0 成功
        ah2dll.ahkassign.restype=c_int
        ah2dll.ahkassign.argtypes=[c_wchar_p, c_wchar_p, c_uint]

        # (NewCode, WaitExecute, ThreadId): WaitExecute: 0 仅添加代码, 不执行 / 1 添加代码且等待执行代码直到遇上return / 2 添加代码且立刻返回(不等待它执行完毕)
        # -> LinePointerOfNewCode
        ah2dll.addScript.restype=c_void_p
        ah2dll.addScript.argtypes=[c_wchar_p, c_int, c_uint]

    def __init__(self, dllpath) -> None:
        self.dllpath = dllpath
        self.ah2dll:ctypes.CDLL = Lep_Ahkh2_Orgin.ah2dll if Lep_Ahkh2_Orgin.ah2dll else ctypes.cdll.LoadLibrary(dllpath)

        # self.ah2dll:ctypes.CDLL = ctypes.cdll.LoadLibrary(dllpath)
        Lep_Ahkh2_Orgin.settypes(self.ah2dll)

class ShareMem:
    def __init__(self) -> None:
        self.size_ahk_type:str = 'UInt'
        self.size_py_type:_SimpleCData = c_uint
        self.size_buff:_SimpleCData = self.size_py_type(0)
        self.size_ptrx = getptrhex(self.size_buff)

        self.ptr_ahk_type:str = 'Ptr'
        self.ptr_py_type:_SimpleCData = c_void_p
        self.ptr_buff = self.ptr_py_type(0)
        self.ptr_ptrx = getptrhex(self.ptr_buff)
        self.encoding = 'utf-8'
        self.buff = None

    def getstr(self)->str:
        size = self.size_buff.value
        ptr = self.ptr_buff.value
        if (size > 0) and (ptr != 0):
            return getptrstr(ptr, size, self.encoding)
        return ''

    def setstr(self, s:str)->None:
        if len(s) < 1:
            self.size_buff.value = 0
            self.ptr_buff = 0
            self.buff = None
            return 
        bin = (s + '\0\0\0\0\0\0\0\0').encode(self.encoding) 
        binl = len(bin)
        self.buff = create_string_buffer(binl)
        self.buff.value = bin
        self.size_buff.value = binl
        self.ptr_buff.value = getptr(self.buff)

class Lep_Ahkh2(Lep_Ahkh2_Orgin):
    ''' AHK阻塞执行 '''
    def __init__(self, dllpath:str='', title:str='', cmdline:str='') -> None:
        '''dllpath第一次初始化要填路径, 最好是完整路径, 成功载入之后该参数无效'''
        super().__init__(dllpath)
        self.title = ''
        self.threadid = self.ah2dll.NewThread('#NoTrayIcon\nPersistent True', cmdline, title)
        while not self.ah2dll.ahkReady(self.threadid):
            pass

        self.add(f"""
            class __AHK_PYTHON_SHARE_MEMORY__ {{
                __New(size_ptrx, size_type, ptr_ptrx, ptr_type) {{
                    this.size_ptrx  := size_ptrx 
                    this.size_type  := size_type  
                    this.ptr_ptrx   := ptr_ptrx 
                    this.ptr_type   := ptr_type  
                    this.buff       := ''
                    this.encoding := 'utf-8'
                }}
                size {{
                    get => NumGet(this.size_ptrx, this.size_type)
                    set => NumPut(this.size_type, Value, this.size_ptrx) 
                }}
                ptr {{
                    get => NumGet(this.ptr_ptrx, this.ptr_type)
                    set => NumPut(this.ptr_type, Value, this.ptr_ptrx) 
                }}
                str {{
                    get{{
                        if not this.size
                            return ''
                        ptr := this.ptr
                        if not ptr
                            return ''
                        return StrGet(ptr, this.encoding)
                    }}
                    set {{
                        lstr := strlen(Value)
                        if not lstr {{
                            this.size := 0
                            this.ptr := 0
                            this.buff := ''
                        }} else {{
                            size := StrPut(Value, this.encoding) + 8
                            this.buff := Buffer(size, 0)
                            StrPut(Value, this.buff, this.encoding)
                            this.ptr := this.buff.Ptr
                            this.size := size
                            ; msgbox this.size 
                        }}
                    }}
                }}
            }}
        """)

        self.ahk_return_buff = ShareMem()
        self.init_ahk_return_buff()

        self.py_cbinfo_buff = ShareMem()
        self.py_cb = None
        self.py_cb_map = {}
        self.py_cb_buff = None
        self.pyfncb_hexptr = None
        self.init_py_cb_buff()

        self.add_pyutil4ahk()
        
    def init_ahk_return_buff(self):
        self.add(f'''
            ; 用于ahk给python的返回值
            global _return := ''

            global _return_buff := __AHK_PYTHON_SHARE_MEMORY__(
                {self.ahk_return_buff.size_ptrx},
                '{self.ahk_return_buff.size_ahk_type}',
                {self.ahk_return_buff.ptr_ptrx},
                '{self.ahk_return_buff.ptr_ahk_type}'
            )
            __return_emtpy() {{
                global _return
                _return := ''
            }}
            __return_ensure() {{    ; 仅返回字符串
                global _return, _return_buff
                _return_buff.str := (strlen(_return) < 1) ? '' : _return
                _return := ''
            }}
        ''' )

    def init_py_cb_buff(self):
        def pycb():
            pycbinfo = json.loads(self.py_cbinfo_buff.getstr().rstrip('\0'))
            fnname = pycbinfo['fnname']
            args = pycbinfo['args']
            fn = self.py_cb_map[fnname]
            res = fn(*args)
            self.py_cbinfo_buff.setstr(json.dumps([res]))
        self.py_cb = pycb
        self.py_cb_buff = ctypes.CFUNCTYPE(c_void_p)(pycb)
        self.py_cb_ptrx = hex(cast(self.py_cb_buff, c_void_p).value)

        self.add(f'''
            ; 用于ahk给python的返回值
            global _py_cb_buff := __AHK_PYTHON_SHARE_MEMORY__(
                {self.py_cbinfo_buff.size_ptrx},
                '{self.py_cbinfo_buff.size_ahk_type}',
                {self.py_cbinfo_buff.ptr_ptrx},
                '{self.py_cbinfo_buff.ptr_ahk_type}'
            )
            __pyfncb(pycbinfo) {{
                _py_cb_buff.str := JSON.stringify(pycbinfo)
                DllCall({self.py_cb_ptrx}, 'Cdecl')
                return JSON.parse(_py_cb_buff.str)[1]
            }}

            global __pyhkcbmap := Map()
            __pyhkcb(ThisHotkey) {{
                global __pyhkcbmap
                fnname := __pyhkcbmap[ThisHotkey]
                __pyfncb({{fnname: fnname, args: []}})
            }}
        ''' )
        pass

    def add_pyutil4ahk(self):
        def pyprint(*txt):
            print(*txt)
        self.add_pyfn(pyprint, 'print')

    def add_pyfn(self, pyfunc, alias:str=''):
        '''
            pyfunc: python函数
            alias: ahk调用所用的函数名, 默认为空, 即用的python的函数名
        '''

        fnname = alias if alias else pyfunc.__name__
        if self.py_cb_map.__contains__(fnname) and self.py_cb_map[fnname] != pyfunc:
            raise Exception('不允许多次添加同一个函数或已被声明过的函数别名(alias)')
        self.py_cb_map[fnname] = pyfunc
        self.add(f"""
            {fnname}(args*) {{
                return __pyfncb({{fnname: '{fnname}', args: args}})
            }}
            return
        """)
        return fnname

    def add_pyhk(self, hotkey:str, pyfunc, alias:str=''):
        fnname = self.add_pyfn(pyfunc, alias)

        self.add(f"""
            __pyhkcbmap['{hotkey}'] := '{fnname}'
            Hotkey('{hotkey}', __pyhkcb)
            Hotkey('{hotkey}', __pyhkcb, 'On')
        """)
        pass
    
    def del_pyhk(self, hotkey:str):
        self.do(f"""Hotkey('{hotkey}', __pyhkcb, 'Off')""")

    def setval(self, name:str, value):
        '''设置线程中的全局变量'''
        if value == '':
            self.add(f'global {name} := ""')
        else:
            self.ahk_return_buff.setstr(json.dumps([value]))
            self.add(f'global {name} := JSON.parse(_return_buff.str)[1]')

    def getval(self, name:str):
        '''读取线程中的全局变量'''
        return self.do2(f"""
            if (IsSet({name})) {{
                _return := {name}
            }}
            else {{
                _return := ""
            }}  
        """)

    def __del__(self):
        # print('结束线程')
        if self.ah2dll.ahkReady(self.threadid):
            self.do('ExitApp(0)')

    def isrunning(self):
        return self.ah2dll.ahkReady(self.threadid)

    def add(self, ahkscript:str):
        '''
            添加ahk代码, 永久保留此代码
            请勿去掉sleep 函数, 否则可能报错
        '''
        done = False
        for i in range(0, 3):
            try:
                self.ah2dll.addScript(ahkscript, 1, self.threadid)
                done = True
                break
            except Exception as e:
                continue
        return done
    
    def add_file(self, ahkfile:str, encoding='utf-8'):
        '''
            从文件添加ahk代码, 永久保留此代码
        '''
        with open(ahkfile, 'r', encoding=encoding) as f:
            script = f.read()
            f.close()
        self.add(script)

    def do0(self, ahkscript:str)->None:
        '''无返回值, 执行速度最快'''
        self.ah2dll.ahkExec(f"{ahkscript}", self.threadid)

    def do(self, ahkscript:str)->str:
        '''仅返回字符串, 执行速度偏慢, 立即执行ahk代码, 为 ahk变量 _return 赋值将输出为字符串, 将作为 do() 的返回值, 类型为python的str '''
        self.ah2dll.ahkExec(f"__return_emtpy()\n{ahkscript}\n__return_ensure()", self.threadid)
        return self.ahk_return_buff.getstr()

    def do2(self, ahkscript:str)->str:
        '''
            返回复杂类型的, 执行速度最慢 立即执行ahk代码, 将 ahk 变量_return赋值为 map, array 或者 object 类型数据, 将作为 doj() 的返回值, 类型为 python 的 dict 或者 list
        '''
        endscript = '''
        try {
            if (_return != '') {
                _return := JSON.stringify([_return])
            } else {
                _return := ''
            }
        } catch {
            _return := ''
        }
        '''
        self.ah2dll.ahkExec(f'__return_emtpy()\n{ahkscript}\n{endscript}\n__return_ensure()', self.threadid)
        res = self.ahk_return_buff.getstr().rstrip('\0')
        # print('res', res.encode('utf-8'))
        if (res):
            res = json.loads(res)
            return res[0]
        else:
            return None

if __name__ == '__main__':

    # ah2dll32 = f'{get_main_dir()}\\bin\\ahkh2x32mt.dll'
    # ah2dll64 = f'{get_main_dir()}\\bin\\ahkh2x64mt.dll'
    # dllpath = ah2dll32 if is32ptr() else ah2dll64


    # ah2 = Lep_Ahkh2(dllpath)
    # ah2.setval('abc', '123')
    # print(ah2.getval('abc'))
    
    # print(ah2.do('_return := "hello world"'))
    # print(ah2.do2('_return := {abc: 123}')['abc'])

    # def fn(a):
    #     a += 1
    #     return a

    # ah2.add_pyfn(fn)
    
    # ah2.setval('a', 0)

    # def hk1():
    #     print('来自hk1')

    # def hk2():
    #     print('来自hk2')

    # ah2.add_pyhk('f1', hk1)
    # ah2.add_pyhk('f3', hk2)
    # ah2.del_pyhk('f3')

    # while (True):
    #     print(ah2.do('a+=1\n_return := fn(a)'))
    #     sleep(1)
    pass
        