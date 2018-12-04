from inst import Code,FUN
from symbol import OPERATORS
class Reg:
    def __init__(self,data=None):
        self.__data=data

    def set(self,data):#设置内容
        self.__data=data

    def get(self):#获取内容
        return self.__data

    def __add__(self,other):
        return self.get()+other.get()
    
    def inc(self):#寄存器自增一
        self.__data+=1

    def dec(self):#寄存器自减一
        self.__data-=1

class Machine:
    def __init__(self,code,debugFlag=False):#初始化虚拟机
        self.code=code#代码段
        self.data=[]#数据段
        self.I=Reg()
        self.P=Reg()
        self.T=Reg()
        self.B=Reg()
        self.debugFlag=debugFlag

    def top(self):
        return self.data[len(self.data)-1]

    def push(self,data):
        self.data.append(data)
        self.T.inc()

    def pop(self):
        self.T.dec()
        return self.data.pop()
    
    def initReg(self):
        self.P.set(0)
        self.T.set(-1)
        self.B.set(0)

    def debug(self,info):
        if self.debugFlag:
            print(info)

    def run(self):
        self.debug('开始运行')
        self.initReg()
        while self.P.get()!=1:
            addr=self.P.get()#获取地址
            inst=self.code[addr]
            self.I.set(inst)#读指令
            self.debug('Addr:'+str(addr)+'\t|\tInst:'+str(inst))
            if inst.f==FUN.LIT:#将常数放到运栈顶，a 域为常数。
                self.push(inst.a)
                self.P.inc()
            elif inst.f==FUN.LOD:#将变量放到栈顶。a 域为变量在所说明层中的相对位置，l 为调用层与说明层的层差值。
                badr=self.B.get()
                for i in range(0,inst.l):
                    badr=self.data[badr+1]
                self.push(self.data[badr+inst.a])
                self.P.inc()
            elif inst.f==FUN.STO:#将栈顶的内容送到某变量单元中。a,l 域的含义与LOD 的相同。
                badr=self.B.get()
                for i in range(0,inst.l):
                    badr=self.data[badr+1]
                self.data[badr+inst.a]=self.pop()
                self.P.inc()
            elif inst.f==FUN.CAL:#调用过程的指令。a 为被调用过程的目标程序的入中地址，l 为层差。 
                self.data.append(self.P.get())#设定返回地址
                self.data.append(self.B.get())#设定动态链
                self.data.append(None)#设定静态链
                self.P.set(inst.a)#设定入口地址
                self.B.set(self.B+self.T+1)#设置基址寄存器
                self.T.set(3)#设置栈指针寄存器
            elif inst.f==FUN.INT:#为被调用的过程（或主程序）在运行栈中开辟数据区。a 域为开辟的个数。
                while len(self.data)<self.B.get()+inst.a:
                    self.push(0)
                self.P.inc()
            elif inst.f==FUN.JMP:#无条件转移指令，a 为转向地址。
                self.P.set(inst.a)
            elif inst.f==FUN.JPC:#条件转移指令，当栈顶的布尔值为非真时，转向a 域的地址，否则顺序执行。
                if self.pop()==0:#为假
                    self.P.inc()            
                else:#为真
                    self.P.set(inst.a)
            elif inst.f==FUN.OPR:#关系和算术运算。具体操作由a 域给出。运算对象为栈顶和次顶的内容进行运算，结果存放在次顶。a 域为0 时是退出数据区。
                if inst.a==OPERATORS['+']:#加法
                    b=self.pop()
                    a=self.pop()
                    self.push(a+b)
                elif inst.a==OPERATORS['-']:#减法
                    b=self.pop()
                    a=self.pop()
                    self.push(a-b)
                elif inst.a==OPERATORS['*']:#乘法
                    b=self.pop()
                    a=self.pop()
                    self.push(a*b)
                elif inst.a==OPERATORS['/']:#除法
                    b=self.pop()
                    a=self.pop()
                    self.push(a//b)
                elif inst.a==OPERATORS['#']:#不等于
                    b=self.pop()
                    a=self.pop()
                    if a!=b:
                        self.push(1)   
                    else:
                        self.push(0)   
                elif inst.a==OPERATORS['<']:#小于
                    b=self.pop()
                    a=self.pop()
                    if a<b:
                        self.push(1)   
                    else:
                        self.push(0)  
                elif inst.a==OPERATORS['<=']:#小于等于
                    b=self.pop()
                    a=self.pop()
                    if a<=b:
                        self.push(1)   
                    else:
                        self.push(0)  
                elif inst.a==OPERATORS['>']:#大于
                    b=self.pop()
                    a=self.pop()
                    if a>b:
                        self.push(1)   
                    else:
                        self.push(0)  
                elif inst.a==OPERATORS['>=']:#大于等于
                    b=self.pop()
                    a=self.pop()
                    if a>=b:
                        self.push(1)   
                    else:
                        self.push(0) 
                elif inst.a==OPERATORS['>=']:#判断奇数
                    a=self.pop()
                    if a%2==1:
                        self.push(1)   
                    else:
                        self.push(0)
                elif inst.a==OPERATORS['read']:#读
                    s = input('input:')
                    if not s.isdigit():
                        print('输入错误')
                        exit(-1)
                    else:
                        self.push(int(s))
                elif inst.a==OPERATORS['write']:#写
                    print('output:'+str(self.pop()))
                elif inst.a==0:#退出数据区
                    badr=self.data[self.B.get()+1]
                    self.P.set(self.data[self.B.get()])#恢复返回地址
                    while len(self.data)>self.B.get():#退栈
                        self.data.pop()
                    self.T.set(self.B.get()-1)#恢复栈指针寄存器
                    self.B.set(badr)#恢复基址寄存器
                self.P.inc()
