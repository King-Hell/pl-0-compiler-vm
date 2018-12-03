
from node import Node

s=Node('<分程序>')
print(s.getTreeDepth())
a=Node('A')
s.add(a)
print(s)
print(s.getTreeDepth())
b=Node('B')
s.add(b)
print(s)
print(s.getTreeDepth())
print(u'分程序')