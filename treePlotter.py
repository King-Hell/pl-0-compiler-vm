import matplotlib.pyplot as plt
from node import Node

# 定义决策树决策结果的属性，用字典来定义  
# 下面的字典定义也可写作 decisionNode={boxstyle:'sawtooth',fc:'0.8'}  
# boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细  
decisionNode = dict(boxstyle="round", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    # annotate是关于一个数据点的文本  
    # nodeTxt为要显示的文本，centerPt为文本的中心点，箭头所在的点，parentPt为指向文本的点 
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )

def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])# 定义横纵坐标轴，无内容  
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops) # 绘制图像,无边框,无坐标轴  
    #createPlot.ax1 = plt.subplot(111, frameon=False) 
    plotTree.totalW = float(inTree.getNumLeafs())   #全局变量宽度 = 叶子数
    plotTree.totalD = float(inTree.getTreeDepth())  #全局变量高度 = 深度
    #图形的大小是0-1 ，0-1
    plotTree.xOff = -0.5/plotTree.totalW  #例如绘制3个叶子结点，坐标应为1/3,2/3,3/3
    #但这样会使整个图形偏右因此初始的，将x值向左移一点。
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5,1.0))
    plt.show()

def plotTree(myTree, parentPt):
    numLeafs = myTree.getNumLeafs()  #当前树的叶子数
    firstStr = myTree.name
    #cntrPt文本中心点   parentPt 指向文本中心的点 
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree.child
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD #从上往下画
    for key in secondDict:
        if key.isLeaf():#打印叶子结点
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(key, (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            #plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, key.name)
        else:
            plotTree(key,cntrPt) 
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD 