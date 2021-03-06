# Pl/0编译器与虚拟机使用说明
山东大学，计算机科学与技术学院，编译原理

---
## 1. 目录说明
`/release/` 目录下为发布版
`/release/dist/`目录下为生成的exe格式文件

---
## 2. 本项目包含两个应用程序
compiler用于编译源代码
vm用于执行目标代码

---
## 3. 源代码格式需符合Pl/0语法
lv1.txt source.txt source2.txt 为示例文件

---
## 4. Pl/0语言文法的BNF表示：
> <程序>→<分程序>.  
<分程序>→ [<常量说明部分>][<变量说明部分>][<过程说明部分>]<语句>  
 <常量说明部分> → CONST<常量定义>{ ,<常量定义>}；  
 <常量定义> → <标识符>=<无符号整数>  
 <无符号整数> → <数字>{<数字>}  
 <变量说明部分> → VAR<标识符>{ ,<标识符>}；  
 <标识符> → <字母>{<字母>|<数字>}  
 <过程说明部分> → <过程首部><分程序>；{<过程说明部分>}  
 <过程首部> → procedure<标识符>；  
 <语句> → <赋值语句>|<条件语句>|<当型循环语句>|<过程调用语句>|<读语句>|<写语句>|<复合语句>|<空>  
 <赋值语句> → <标识符>:=<表达式>  
 <复合语句> → begin<语句>{ ；<语句>}end  
 <条件> → <表达式><关系运算符><表达式>|odd<表达式>  
 <表达式> → [+|-]<项>{<加减运算符><项>}  
 <项> → <因子>{<乘除运算符><因子>}  
 <因子> → <标识符>|<无符号整数>|(<表达式>)  
 <加减运算符> → +|-  
 <乘除运算符> → *|/  
 <关系运算符> → =|#|<|<=|>|>=  
 <条件语句> → if<条件>then<语句>  
 <过程调用语句> → call<标识符>  
 <当型循环语句> → while<条件>do<语句>  
 <读语句> → read(<标识符>{ ，<标识符>})  
 <写语句> → write(<表达式>{，<表达式>})  
 <字母> → a|b|c…x|y|z  
 <数字> → 0|1|2…7|8|9  
