from enum import Enum
KIND=Enum('KIND',('CONSTANT','VARIABLE','PROCEDURE'))
class Table:
    def __init__(self,parent=None):
        self.parent=parent
        self.entries={}
        self.dx=3
        if parent==None:
            self.level=0
        else:
            self.level=parent.level+1
    
    def add(self,entry):
        if entry.name in self.entries:
            print(entry.name+' 重定义')
            return
        entry.level=self.level
        if entry.kind!=KIND.CONSTANT:
            entry.adr=self.dx
            self.dx+=1
        self.entries[entry.name]=entry

    def __str__(self):
        msg='________________________________________\n'
        for i in self.entries.keys():
            msg+=self.entries[i].__str__()+'\n'
        msg+='________________________________________'
        return msg

class Entry:
    def __init__(self,name,kind,val=None):
        self.name=name
        self.kind=kind
        if kind!=KIND.CONSTANT and val!=None:
            print('非常量无法初始化值')
        else:
            self.val=val
        self.level=None
        self.adr=None

    def __str__(self):
        msg='NAME:'+self.name+'\t\t'+self.kind.name+'\t\t'
        if self.val!=None:
            msg+='VAL:'+str(self.val)+'\t\t'
        else:
            msg+='LEVEL:'+str(self.level)+'\t\t'
        msg+='ADR:'+str(self.adr)
        return msg

