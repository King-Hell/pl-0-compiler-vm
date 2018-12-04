from symbol import *
# 读入源程序

def getsym(filename):
    buffer = []
    idNum=0
    f = open(filename, 'r')
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
                    print(len(SYM)-1,'<%s,%d,->' % (word,KEYWORDS[word]))
                elif word in OPERATORS:
                    SYM.append(OPERATORS[word])
                else:
                    SYM.append(ident)  # 是标识符
                    if word not in ID:
                        ID[word]=idNum
                        idNum=idNum+1
                    IDi.append(word)
                    print(len(SYM)-1,'<%s,%d,%s>' % (word,ident,ID[word]))
                buffer.clear()  # 清空缓冲区
            elif line[i].isdigit():  # 数字开头
                buffer.append(line[i])
                i = i+1
                while i < len(line) and line[i].isdigit():
                    buffer.append(line[i])
                    i = i+1
                word = ''.join(buffer)
                SYM.append(number)
                NUM.append(int(word))
                print(len(SYM)-1,'<%s,%d,%s>' % ('number',number,word))
                buffer.clear()
            elif line[i] == ':' and i+1 < len(line) and line[i+1] == '=':
                SYM.append(OPERATORS[':='])
                print(len(SYM)-1,'<:=,%s,->'%OPERATORS[':='])
                i = i+2
            elif line[i] == '<' and i+1 < len(line) and line[i+1] == '=':
                SYM.append(OPERATORS['<='])
                print(len(SYM)-1,'<=,%s,->'%OPERATORS['<='])
                i = i+2
            elif line[i] == '>'and i+1 < len(line) and line[i+1] == '=':
                SYM.append(OPERATORS['>='])
                print(len(SYM)-1,'>=,%s,->'%OPERATORS['>='])
                i = i+2
            elif line[i] in OPERATORS:
                SYM.append(OPERATORS[line[i]])
                print(len(SYM)-1,'<%s,%s,->' % (line[i],OPERATORS[line[i]]))
                i = i+1
            elif line[i] in DELIMITERS:
                SYM.append(DELIMITERS[line[i]])
                print(len(SYM)-1,'<%s,%s,->' % (line[i],DELIMITERS[line[i]]))
                i = i+1
            else:
                i=i+1