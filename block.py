from symbol import *
from node import Node
from table import *
p = 0
pid=0
pnum=0
root=Node('<程序>')
table=Table()

def error():  # 出错
    print("Error:",p)


def advance():
    global p
    p = p+1
    

def block():
    A(root,table)


def A(root,table):#<程序>
    B(root,table)
    if SYM[p] == DELIMITERS['.']:
        root.add(Node('.'))
        advance()
        if p==len(SYM):
            print("Correct")
        else:
            error()
    else:
        error()


def B(parent,table):#<分程序>
    child=Node('<分程序>')
    parent.add(child)
    C(child,table)
    E(child,table)
    if SYM[p] == KEYWORDS['procedure']:
        F(child,table)
    H(child,table)


def C(parent,table):#<常量说明部分>
    if SYM[p] == KEYWORDS['const']:
        child=Node('<常量说明部分>')
        parent.add(child)
        child.add(Node('const'))
        advance()
        D(child,table)
        while SYM[p] == DELIMITERS[',']:
            child.add(Node(','))
            advance()
            D(child,table)
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
        else:
            error()


def D(parent,table):#<常量定义>
    child=Node('<常量定义>')
    parent.add(child)
    if SYM[p] == ident:
        name=X(child,table)
        advance()
        if SYM[p] == OPERATORS['=']:
            child.add(Node('='))
            advance()
            if SYM[p] == number:
                val=W(child,table)
                advance()
                entry=Entry(name,KIND.CONSTANT,val)
                table.add(entry)
            else:
                error()
        else:
            error()
    else:
        error()


def E(parent,table):#<变量说明部分>
    if SYM[p] == KEYWORDS['var']:
        child=Node('<变量说明部分>')
        parent.add(child)
        child.add(Node('var'))
        advance()
        if SYM[p] == ident:
            name=X(child,table)
            entry=Entry(name,KIND.VARIABLE)
            table.add(entry)
            advance()
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                if SYM[p]==ident:
                    name=X(child,table)
                    entry=Entry(name,KIND.VARIABLE)
                    table.add(entry)
                    advance()
                else:
                    error()
            if SYM[p] == DELIMITERS[';']:
                child.add(Node(';'))
                advance()
            else:
                error()
        else:
            error()


def F(parent,table):#<过程说明部分>
    child=Node('<过程说明部分>')
    parent.add(child)
    childTable=G(child,table)
    B(child,childTable)
    if SYM[p] == DELIMITERS[';']:
        child.add(Node(';'))
        advance()
        while SYM[p] == KEYWORDS['procedure']:
            F(child,table)
    else:
        error()


def G(parent,table):#<过程首部>
    if SYM[p] == KEYWORDS['procedure']:
        child=Node('<过程首部>')
        parent.add(child)
        child.add(Node('procedure'))
        advance()
        if SYM[p] == ident:
            name=X(child,table)
            entry=Entry(name,KIND.PROCEDURE)
            table.add(entry)
            childTable=Table(table)
            advance()
            if SYM[p]==DELIMITERS[';']:
                child.add(Node(';'))
                advance()
                return childTable
            else:
                error()
        else:
            error()
    else:
        error()


def H(parent,table):#<语句>
    child=Node('<语句>')  
    if SYM[p]==ident:
        I(child,table)
    elif SYM[p]==KEYWORDS['if']:
        R(child,table)
    elif SYM[p]==KEYWORDS['while']:
        T(child,table)
    elif SYM[p]==KEYWORDS['call']:
        S(child,table)
    elif SYM[p]==KEYWORDS['read']:
        U(child,table)
    elif SYM[p]==KEYWORDS['write']:
        V(child,table)
    elif SYM[p]==KEYWORDS['begin']:
        J(child,table)
    else:
        return
    parent.add(child)


def I(parent,table):#<赋值语句>
    if SYM[p] == ident:
        child=Node('<赋值语句>')
        parent.add(child)
        X(child,table)
        advance()
        if SYM[p] == OPERATORS[':=']:
            child.add(Node(':='))
            advance()
            L(child,table)
        else:
            error()
    else:
        error()


def J(parent,table):#<复合语句>
    child=Node('<复合语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['begin']:
        child.add(Node('begin'))
        advance()
        H(child,table)
        while SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
            H(child,table)
        if SYM[p] == KEYWORDS['end']:
            child.add(Node('end'))
            advance()
        else:
            error()
    else:
        error()

def K(parent,table):#<条件>
    child=Node('<条件>')
    parent.add(child)
    if SYM[p] == OPERATORS['+'] or SYM[p] == OPERATORS['-'] or SYM[p] == ident or SYM[p] == number or SYM[p] == DELIMITERS['(']:
        L(child,table)
        Q(child,table)
        L(child,table)
    elif SYM[p] == KEYWORDS['odd']:
        child.add(Node('odd'))
        advance()
        L(child,table)
    else:
        error()


def L(parent,table):#<表达式>
    child=Node('<表达式>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))
        advance()
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))
        advance()
    M(child,table)
    while SYM[p]==OPERATORS['+'] or SYM[p]==OPERATORS['-']:
        O(child,table)
        M(child,table)


def M(parent,table):#<项>
    child=Node('<项>')
    parent.add(child)
    N(child,table)
    while SYM[p]==OPERATORS['*'] or SYM[p]==OPERATORS['/']:
        P(child,table)
        N(child,table)


def N(parent,table):#<因子>
    child=Node('<因子>')
    parent.add(child)
    if SYM[p] == ident:
        X(child,table)
        advance()
    elif SYM[p] == number:
        W(child,table)        
        advance()
    elif SYM[p] == DELIMITERS['(']:
        child.add(Node('('))        
        advance()
        L(child,table)
        if SYM[p] == DELIMITERS[')']:
            child.add(Node(')'))        
            advance()
        else:
            error()
    else:
        error()


def O(parent,table):#<加减运算符>
    child=Node('<加减运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))        
        advance()
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))        
        advance()
    else:
        error()


def P(parent,table):#<乘除运算符>
    child=Node('<乘除运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['*']:
        child.add(Node('*'))        
        advance()
    elif SYM[p] == OPERATORS['/']:
        child.add(Node('/'))        
        advance()
    else:
        error()


def Q(parent,table):#<关系运算符>
    child=Node('<关系运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['='] or SYM[p] == OPERATORS['#'] or SYM[p] == OPERATORS['<'] or SYM[p] == OPERATORS['<='] or SYM[p] == OPERATORS['>'] or SYM[p] == OPERATORS['>=']:
        child.add(Node(list(OPERATORS.keys())[list(OPERATORS.values()).index(SYM[p])]))
        advance()
    else:
        error()


def R(parent,table):#<条件语句>
    child=Node('<条件语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['if']:
        child.add(Node('if')) 
        advance()
        K(child,table)
        if SYM[p] == KEYWORDS['then']:
            child.add(Node('then')) 
            advance()
            H(child,table)
        else:
            error()
    else:
        error()


def S(parent,table):#<过程调用语句>
    child=Node('<过程调用语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['call']:
        child.add(Node('call'))
        advance()
        if SYM[p] == ident:
            X(child,table)
            advance()
        else:
            error()
    else:
        error()


def T(parent,table):#<当型循环语句>
    child=Node('<当型循环语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['while']:
        child.add(Node('while'))
        advance()
        K(child,table)
        if SYM[p] == KEYWORDS['do']:
            child.add(Node('do'))
            advance()
            H(child,table)
        else:
            error()
    else:
        error()


def U(parent,table):#<读语句>
    child=Node('<读语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['read']:
        child.add(Node('read'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            if SYM[p] == ident:
                X(child,table)
                advance()
                while SYM[p] == DELIMITERS[',']:
                    child.add(Node(','))
                    advance()
                    if SYM[p] == ident:
                        X(child,table)
                        advance()
                    else:
                        error()
                if SYM[p] == DELIMITERS[')']:
                    child.add(Node(')'))
                    advance()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()


def V(parent,table):#<写语句>
    child=Node('<写语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['write']:
        child.add(Node('write'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            L(child,table)
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                L(child,table)
            if SYM[p] == DELIMITERS[')']:
                child.add(Node(')'))
                advance()
            else:
                error()
        else:
            error()
    else:
        error()

def W(parent,table):#<无符号整数>
    global pnum
    child=Node('<无符号整数>')
    parent.add(child)
    val=NUMi[pnum]
    child.add(Node(val))
    pnum+=1
    return val

def X(parent,table):#<标识符>
    global pid
    child=Node('<标识符>')
    parent.add(child)
    name=IDi[pid]
    child.add(Node(name))
    pid+=1
    return name