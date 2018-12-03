from getsym import getsym
from block import block,root,table
from treePlotter import createPlot

# getsym('lv1.txt')#词法分析
getsym('source.txt')
block()  # 语法分析
print(root)
#createPlot(root)
print(table)
