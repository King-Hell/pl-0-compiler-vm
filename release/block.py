from symbol import KEYWORDS,OPERATORS,DELIMITERS,SYM,ident,number,IDi,NUM
from table import Table,Entry,isConst,KIND
from inst import Code
p = 0
pid=0
pnum=0
table=Table()#table表
code=[]#CODE数组
startCode=Code('JMP',0,None)
code.append(startCode)
code.append(Code)
def error():  # 出错
    print("Error:",p)
    exit(-1)


def advance():
    global p
    p = p+1
    

def block():
    A(table)


def A(table):#<程序>
    startAddr=B(table)
    startCode.a=startAddr
    if SYM[p] == DELIMITERS['.']:
        advance()
        if p==len(SYM):
            print("目标代码已生成")
        else:
            error()
    else:
        error()


def B(table):#<分程序>
    C(table)
    E(table)
    if SYM[p] == KEYWORDS['procedure']:
        F(table)
    startAddr=len(code)
    code.append(Code('INT',0,table.getSize()))
    H(table) 
    code.append(Code('OPR',0,0))
    return startAddr

def C(table):#<常量说明部分>
    if SYM[p] == KEYWORDS['const']:
        advance()
        D(table)
        while SYM[p] == DELIMITERS[',']:
            advance()
            D(table)
        if SYM[p] == DELIMITERS[';']:
            advance()
        else:
            error()


def D(table):#<常量定义>
    if SYM[p] == ident:
        name=X(table)
        advance()
        if SYM[p] == OPERATORS['=']:
            advance()
            if SYM[p] == number:
                val=W(table)
                advance()
                entry=Entry(name,KIND.CONSTANT,val)
                table.add(entry)
            else:
                error()
        else:
            error()
    else:
        error()


def E(table):#<变量说明部分>
    if SYM[p] == KEYWORDS['var']:
        advance()
        if SYM[p] == ident:
            name=X(table)
            entry=Entry(name,KIND.VARIABLE)
            table.add(entry)
            advance()
            while SYM[p] == DELIMITERS[',']:
                advance()
                if SYM[p]==ident:
                    name=X(table)
                    entry=Entry(name,KIND.VARIABLE)
                    table.add(entry)
                    advance()
                else:
                    error()
            if SYM[p] == DELIMITERS[';']:
                advance()
            else:
                error()
        else:
            error()


def F(table):#<过程说明部分>
    childTable=G(table)
    B(childTable)
    if SYM[p] == DELIMITERS[';']:
        advance()
        while SYM[p] == KEYWORDS['procedure']:
            F(table)
    else:
        error()


def G(table):#<过程首部>
    if SYM[p] == KEYWORDS['procedure']:
        advance()
        if SYM[p] == ident:
            name=X(table)
            entry=Entry(name,KIND.PROCEDURE)
            table.add(entry)
            table.entries[name].adr=len(code)
            childTable=Table(table)
            advance()
            if SYM[p]==DELIMITERS[';']:
                advance()
                return childTable
            else:
                error()
        else:
            error()
    else:
        error()


def H(table):#<语句> 
    if SYM[p]==ident:
        I(table)
    elif SYM[p]==KEYWORDS['if']:
        R(table)
    elif SYM[p]==KEYWORDS['while']:
        T(table)
    elif SYM[p]==KEYWORDS['call']:
        S(table)
    elif SYM[p]==OPERATORS['read']:
        U(table)
    elif SYM[p]==OPERATORS['write']:
        V(table)
    elif SYM[p]==KEYWORDS['begin']:
        J(table)
    else:
        return


def I(table):#<赋值语句>
    if SYM[p] == ident:
        name=X(table)
        advance()
        if SYM[p] == OPERATORS[':=']:
            advance()
            L(table)
            (l,a,flag)=table.find(name)
            if flag==isConst:
                print('对常量的非法赋值:'+name)
                error()
            else:
                code.append(Code('STO',l,a))
        else:
            error()
    else:
        error()


def J(table):#<复合语句>
    if SYM[p] == KEYWORDS['begin']:
        advance()
        H(table)
        while SYM[p] == DELIMITERS[';']:
            advance()
            H(table)
        if SYM[p] == KEYWORDS['end']:
            advance()
        else:
            error()
    else:
        error()

def K(table):#<条件>
    if SYM[p] == OPERATORS['+'] or SYM[p] == OPERATORS['-'] or SYM[p] == ident or SYM[p] == number or SYM[p] == DELIMITERS['(']:
        L(table)
        opr=Q(table)
        L(table)
        code.append(Code('OPR',0,opr))
    elif SYM[p] == OPERATORS['odd']:
        advance()
        L(table)
        code.append(Code('OPR',0,OPERATORS['odd']))
    else:
        error()


def L(table):#<表达式>
    if SYM[p] == OPERATORS['+']:
        advance()
        M(table)
    elif SYM[p] == OPERATORS['-']:
        advance()
        M(table)
        code.append(Code('LIT',0,-1))
        code.append(Code('OPR',0,OPERATORS['*']))#如果是-号做取负运算
    else:
        M(table)
    while SYM[p]==OPERATORS['+'] or SYM[p]==OPERATORS['-']:
        opr=SYM[p]
        O(table)
        M(table)
        code.append(Code('OPR',0,opr))


def M(table):#<项>
    N(table)
    while SYM[p]==OPERATORS['*'] or SYM[p]==OPERATORS['/']:
        opr=SYM[p]
        P(table)
        N(table)
        code.append(Code('OPR',0,opr))

def N(table):#<因子>
    if SYM[p] == ident:
        name=X(table)
        advance()
        (l,a,flag)=table.find(name)
        if flag==isConst:#常量
            code.append(Code('LIT',0,a))
        else:#变量
            code.append(Code('LOD',l,a))
    elif SYM[p] == number:
        val=W(table)        
        advance()
        code.append(Code('LIT',0,val))
    elif SYM[p] == DELIMITERS['(']:
        advance()
        L(table)
        if SYM[p] == DELIMITERS[')']:
            advance()
        else:
            error()
    else:
        error()


def O(table):#<加减运算符>
    if SYM[p] == OPERATORS['+']:       
        advance()
    elif SYM[p] == OPERATORS['-']:    
        advance()
    else:
        error()


def P(table):#<乘除运算符>
    if SYM[p] == OPERATORS['*']:
        advance()
    elif SYM[p] == OPERATORS['/']:
        advance()
    else:
        error()


def Q(table):#<关系运算符>
    if SYM[p] == OPERATORS['='] or SYM[p] == OPERATORS['#'] or SYM[p] == OPERATORS['<'] or SYM[p] == OPERATORS['<='] or SYM[p] == OPERATORS['>'] or SYM[p] == OPERATORS['>=']:
        opr=SYM[p]
        advance()
        return opr
    else:
        error()


def R(table):#<条件语句>
    if SYM[p] == KEYWORDS['if']:
        advance()
        K(table)
        ret=Code('JPC',0,None)
        code.append(ret)
        if SYM[p] == KEYWORDS['then']:
            advance()
            H(table)
            ret.a=len(code)
        else:
            error()
    else:
        error()


def S(table):#<过程调用语句>
    if SYM[p] == KEYWORDS['call']:
        advance()
        if SYM[p] == ident:
            name=X(table)
            advance()
            (l,a,flag)=table.find(name)
            if l>1:#当调用超出范围时出错
                print('非法的过程调用')
                exit(-1)
            code.append(Code('CAL',l,a))
        else:
            error()
    else:
        error()


def T(table):#<当型循环语句>
    if SYM[p] == KEYWORDS['while']:
        advance()
        ret=len(code)
        K(table)
        fret=Code('JPC',0,None)
        code.append(fret)
        if SYM[p] == KEYWORDS['do']:
            advance()
            H(table)
            code.append(Code('JMP',0,ret))
            fret.a=len(code)
        else:
            error()
    else:
        error()


def U(table):#<读语句>
    if SYM[p] == OPERATORS['read']:
        advance()
        if SYM[p] == DELIMITERS['(']:
            advance()
            if SYM[p] == ident:
                name=X(table)
                advance()
                code.append(Code('OPR',0,OPERATORS['read']))
                (l,a,flag)=table.find(name)
                if flag==isConst:
                    print('对常量的非法赋值:'+name)
                else:
                    code.append(Code('STO',l,a))
                while SYM[p] == DELIMITERS[',']:
                    advance()
                    if SYM[p] == ident:
                        name=X(table)
                        advance()
                        code.append(Code('OPR',0,OPERATORS['read']))
                        (l,a,flag)=table.find(name)
                        if flag==isConst:
                            print('对常量的非法赋值:'+name)
                        else:
                            code.append(Code('STO',l,a))
                    else:
                        error()
                if SYM[p] == DELIMITERS[')']:
                    advance()
                else:
                    error()
            else:
                error()
        else:
            error()
    else:
        error()


def V(table):#<写语句>
    if SYM[p] == OPERATORS['write']:
        advance()
        if SYM[p] == DELIMITERS['(']:
            advance()
            L(table)
            code.append(Code('OPR',0,OPERATORS['write']))
            while SYM[p] == DELIMITERS[',']:
                advance()
                L(table)
                code.append(Code('OPR',0,OPERATORS['write']))
            if SYM[p] == DELIMITERS[')']:
                advance()
            else:
                error()
        else:
            error()
    else:
        error()

def W(table):#<无符号整数>
    global pnum
    val=NUM[pnum]
    pnum+=1
    return val

def X(table):#<标识符>
    global pid
    name=IDi[pid]
    pid+=1
    return name