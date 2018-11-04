KEYWORDS = {'const': 1, 'var': 2, 'procedure': 3, 'begin': 4, 'end': 5, 'odd': 6,
            'if': 7, 'then': 8, 'call': 9, 'while': 10, 'do': 11, 'read': 12, 'write': 13}
OPERATORS = {'=': 14, ':=': 15, '+': 16, '-': 17, '*': 18,
             '/': 19, '#': 20, '<': 21, '<=': 22, '>': 23, '>=': 24}
DELIMITERS = {',': 25, ';': 26, '(': 27, ')': 28}
ident = 29
number = 30
SYM = []
ID = {}
NUM = {}
buffer = []
idNum=0
numNum=0
# 读入源程序
f = open('lv1.txt', 'r')
lines = f.readlines()
for line in lines:
    i = 0
    while i < len(line):
        if line[i] == ' ':  # 空格跳过
            i = i+1
            continue
        elif line[i].isalpha():  # 字母开头
            buffer.append(line[i])
            i = i+1
            while i < len(line) and (line[i].isalpha() or line[i].isdigit()):
                buffer.append(line[i])
                i = i+1
            word = ''.join(buffer)
            if word in KEYWORDS:
                SYM.append(KEYWORDS[word])  # 是关键字
                print('<%s,%d,->' % (word,KEYWORDS[word]))
            else:
                SYM.append(ident)  # 是标识符
                if word not in ID:
                    ID[word]=idNum
                    idNum=idNum+1
                print('<%s,%d,%s>' % (word,ident,ID[word]))
            buffer.clear()  # 清空缓冲区
        elif line[i].isdigit():  # 数字开头
            buffer.append(line[i])
            i = i+1
            while i < len(line) and line[i].isdigit():
                buffer.append(line[i])
                i = i+1
            word = ''.join(buffer)
            SYM.append(number)
            if word not in NUM:
                NUM[word]=numNum
                numNum=numNum+1
            print('<%s,%d,%s>' % (word,number,NUM[word]))
            buffer.clear()
        elif line[i] == ':' and i+1 < len(line) and line[i+1] == '=':
            SYM.append(OPERATORS[':='])
            print('<:=,%s,->'%OPERATORS[':='])
            i = i+2
        elif line[i] == '<' and i+1 < len(line) and line[i+1] == '=':
            SYM.append(OPERATORS['<='])
            print('<=,%s,->'%OPERATORS['<='])
            i = i+2
        elif line[i] == '>'and i+1 < len(line) and line[i+1] == '=':
            SYM.append(OPERATORS['>='])
            print('>=,%s,->'%OPERATORS['>='])
            i = i+2
        elif line[i] in OPERATORS:
            SYM.append(OPERATORS[line[i]])
            print('<%s,%s,->' % (line[i],OPERATORS[line[i]]))
            i = i+1
        elif line[i] in DELIMITERS:
            SYM.append(DELIMITERS[line[i]])
            print('<%s,%s,->' % (line[i],DELIMITERS[line[i]]))
            i = i+1
        else:
            i = i+1