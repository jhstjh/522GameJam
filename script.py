from threading import Thread
from maya import cmds
import maya.utils
from math import sin, cos

import time
Continue = 1
Winning = 0
Pause = 0
LeftScore = 0
RightScore = 0

cmds.group( em=True, n='GameScene' )

ball = cmds.polySphere(sx = 20, sy = 20)
cmds.parent( ball[0], 'GameScene' )

boardU = cmds.polyCube(w = 14)
cmds.parent( boardU[0], 'GameScene' )

boardD = cmds.polyCube(w = 14)
cmds.parent( boardD[0], 'GameScene' )

cmds.setAttr(boardU[0] + '.translate', 0, 0.5, -4.5)
cmds.setAttr(boardD[0] + '.translate', 0, 0.5, 4.5)
            
boardL = cmds.polyCube(d = 4)
cmds.parent( boardL[0], 'GameScene' )
boardR = cmds.polyCube(d = 4)
cmds.parent( boardR[0], 'GameScene' )
        
cmds.setAttr(boardL[0] + '.translate', -7.5, 0.5, 0)
cmds.setAttr(boardR[0] + '.translate', 7.5, 0.5, 0)
velocity = [4, 0, 4]
title = cmds.textCurves( f='Times-Roman', t='MayaPingPong' )
#cmds.parent( title[0], 'GameScene' )  
cmds.setAttr(title[0] + '.scale', 0.5, 0.5, 0.5)   
cmds.setAttr(title[0] + '.translate', -7, 0.5, -8)   
cmds.setAttr(title[0] + '.rotateX', -90)  

LeftScoreObj = cmds.textCurves( f='Times-Roman', t=LeftScore )  
cmds.parent( LeftScoreObj[0], 'GameScene' ) 
cmds.setAttr(LeftScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
cmds.setAttr(LeftScoreObj[0] + '.translate', -3, 0.5, -6)   
cmds.setAttr(LeftScoreObj[0] + '.rotateX', -90) 

Colon = cmds.textCurves( f='Times-Roman', t=':' )
cmds.parent( Colon[0], 'GameScene' )   
cmds.setAttr(Colon[0] + '.scale', 0.5, 0.5, 0.5)   
cmds.setAttr(Colon[0] + '.translate', 0, 0.5, -6)   
cmds.setAttr(Colon[0] + '.rotateX', -90) 

RightScoreObj = cmds.textCurves( f='Times-Roman', t=RightScore ) 
cmds.parent( RightScoreObj[0], 'GameScene' )  
cmds.setAttr(RightScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
cmds.setAttr(RightScoreObj[0] + '.translate', 3, 0.5, -6)   
cmds.setAttr(RightScoreObj[0] + '.rotateX', -90) 

LeftWinObj = cmds.textCurves( f='Times-Roman', t='Left Win!' ) 
cmds.xform(cp = True)
cmds.setAttr(LeftWinObj[0] + '.scale', 0, 0, 0)   
cmds.setAttr(LeftWinObj[0] + '.translate', -8.95, 0.5, 0)   
cmds.setAttr(LeftWinObj[0] + '.rotateX', -90) 


RightWinObj = cmds.textCurves( f='Times-Roman', t='Right Win!' ) 
cmds.xform(cp = True)
cmds.setAttr(RightWinObj[0] + '.scale', 0, 0, 0)   
cmds.setAttr(RightWinObj[0] + '.translate', -10.25, 0.5, 0)   
cmds.setAttr(RightWinObj[0] + '.rotateX', -90) 


def GameFunc():
    global velocity
    global ball
    global boardL
    global boardR
    global LeftScore
    global LeftScoreObj
    global RightScore
    global RightScoreObj
    global Winning
    global Continue
    pos = cmds.getAttr(ball[0] + '.translate')
    newPos = [pos[0][0], pos[0][1], pos[0][2]]
    if (LeftScore >= 10 or RightScore >= 10) and abs(LeftScore - RightScore) >= 2:
        Winning = True
        Continue = False
        return
    if newPos[0] <= -7:
        RightScore += 1
        cmds.setAttr(ball[0] + '.translate', 0, 0, 0)
        velocity = [4, 0, 4]
        cmds.delete(RightScoreObj[0], RightScoreObj[1])
        RightScoreObj = cmds.textCurves( f='Times-Roman', t=RightScore ) 
        cmds.parent( RightScoreObj[0], 'GameScene' ) 
        cmds.setAttr(RightScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        cmds.setAttr(RightScoreObj[0] + '.translate', 3, 0.5, -6)   
        cmds.setAttr(RightScoreObj[0] + '.rotateX', -90) 
        return
    elif newPos[0] >= 7:
        LeftScore += 1
        cmds.setAttr(ball[0] + '.translate', 0, 0, 0)
        velocity = [4, 0, 4]
        cmds.delete(LeftScoreObj[0], LeftScoreObj[1])
        LeftScoreObj = cmds.textCurves( f='Times-Roman', t=LeftScore )  
        cmds.parent( LeftScoreObj[0], 'GameScene' ) 
        cmds.setAttr(LeftScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        cmds.setAttr(LeftScoreObj[0] + '.translate', -3, 0.5, -6)   
        cmds.setAttr(LeftScoreObj[0] + '.rotateX', -90) 
        return
    if newPos[0] < -6:
        posZBoardL = cmds.getAttr(boardL[0] + '.translate')[0][2]
        if newPos[2] >= posZBoardL - 2.5 and newPos[2] <= posZBoardL + 2.5:
            velocity[0] = -velocity[0]
            newPos[0] = -6
    elif newPos[0] > 6:
        posZBoardR = cmds.getAttr(boardR[0] + '.translate')[0][2]
        if newPos[2] >= posZBoardR - 2.5 and newPos[2] <= posZBoardR + 2.5:
            velocity[0] = -velocity[0]
            newPos[0] = 6
    if newPos[0] >= -6 and newPos[0] <= 6:
        if newPos[2] < -3 or newPos[2] > 3:
            velocity[2] = -velocity[2]
    newPos[0] += velocity[0] / 30.0
    newPos[1] += velocity[1] / 30.0
    newPos[2] += velocity[2] / 30.0
    cmds.setAttr(ball[0] + '.translate', newPos[0], newPos[1], newPos[2])
   
def MoveBoard(boardName, direction):
    posZBoard = cmds.getAttr(boardName + '.translate')[0][2] 
    posZBoard += direction * 1
    cmds.setAttr(boardName + '.translateZ', posZBoard)
    
def WinFunc(i):
    global LeftWinObj
    global RightWinObj
    global LeftScore
    global RightScore
    global Winning
    
    if i <= 20:
        gameScale = 1 - i * 0.05
        cmds.setAttr('GameScene' + '.scale', gameScale, gameScale, gameScale)
        cmds.setAttr('GameScene' + '.rotateY', i * 10)
    elif i <= 56:
        barScale = ( i- 20 ) * 0.03
        if LeftScore > RightScore:
            cmds.setAttr(LeftWinObj[0] + '.scale', barScale, barScale, barScale)
            cmds.setAttr(LeftWinObj[0] + '.rotateY', (i - 20) * 10)
        else:
            cmds.setAttr(RightWinObj[0] + '.scale', barScale, barScale, barScale) 
            cmds.setAttr(RightWinObj[0] + '.rotateY', (i - 20) * 10) 
    else:
        Winning = False
        
    
window = cmds.window( title="MayaPingPong", iconName='MPP', widthHeight=(200, 200) )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='Start', command=('velocity = [4, 0, 4];Continue=1;Winning = 0;t = MyThread();t.start();LeftScore=0;RightScore=0'))
cmds.button( label='Left Up', command=('MoveBoard(boardL[0], -1)') )
cmds.button( label='Left Down', command=('MoveBoard(boardL[0], 1)') )
cmds.button( label='Right Up', command=('MoveBoard(boardR[0], -1)') )
cmds.button( label='Right Down', command=('MoveBoard(boardR[0], 1)') )
cmds.button( label='Stop', command=('Continue = False;Winning = False') )
cmds.button( label='Close Window', command=('cmds.delete(\'GameScene\', LeftWinObj[0], RightWinObj[0], title[0]);Continue = False;Winning = False;cmds.deleteUI(\"' + window + '\", window=True)') )
cmds.setParent( '..' )
cmds.showWindow( window )

class MyThread(Thread):
    def run(self):
        global Continue
        global Winning
        while Continue:
            if Pause == 1:
                continue
            maya.utils.executeDeferred(GameFunc)
            time.sleep(1 / 30.0) 
        i = 0
        while Winning:
            maya.utils.executeDeferred(WinFunc, i)
            time.sleep(1 / 30.0) 
            i += 1
            
