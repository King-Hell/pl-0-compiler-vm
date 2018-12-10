import pickle
from machine import Machine
version=0.3
print('Pl/0虚拟机,version:',version)
filename=input('请输入要执行的文件:')
with open(filename,'rb') as fp:
        code=pickle.load(fp)
        machine=Machine(code)#指令运行
        flag=True
        while flag:
            print('目标程序开始执行')
            machine.run()
            print('目标程序结束')
            con=input('是否重新运行[Y/N]:')
            if con.upper()!='Y':
                flag=False
