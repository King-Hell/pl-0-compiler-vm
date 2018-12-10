from getsym import getsym
from block import block,table,code
import pickle
version=0.3
print('Pl/0编译器,version:',version)
filename=input('请输入要编译的文件名:')
with open(filename,'r') as fp:
#getsym('lv1.txt')#词法分析
    print('开始词法分析')
    getsym(filename)
    print('词法分析完成')
    print('开始语法和语义分析')
    block()  # 语法分析
    print('语法和语义分析完成')
    print(table)
    for i,x in enumerate(code):
        print(str(i)+':\t\t'+str(x))
    with open(filename.split('.')[0]+'.litong', 'wb') as fp:
        pickle.dump(code,fp)
        print('可执行文件已生成,文件名:'+fp.name)
input('按任意键退出')