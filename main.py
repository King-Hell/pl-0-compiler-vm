from getsym import getsym
from block import block,root,table,code,tableList
from treePlotter import createPlot
from machine import Machine
import pickle
filename='test.txt'
#getsym('lv1.txt')#词法分析
print('开始词法分析')
getsym(filename)
print('词法分析完成')
print('开始语法和语义分析')
block()  # 语法分析
print(root)
print('语法和语义分析完成')
#createPlot(root)
for i in tableList:
    print(i)
for i,x in enumerate(code):
    print(str(i)+':\t\t'+str(x))
# with open(filename.split('.')[0]+'.litong', 'wb') as fp:
#     pickle.dump(code,fp)
#     fp.close()
machine=Machine(code)#指令运行
machine.run()
print('目标程序结束')