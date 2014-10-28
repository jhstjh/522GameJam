from threading import Thread
from maya import cmds
import maya.utils
from math import sin, cos

import time
Continue = 1
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
cmds.parent( title[0], 'GameScene' )  
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


def DeferredFunc(i, customDict):
    global velocity
    global ball
    global boardL
    global boardR
    global LeftScore
    global LeftScoreObj
    global RightScore
    global RightScoreObj
    pos = cmds.getAttr(ball[0] + '.translate')
    newPos = [pos[0][0], pos[0][1], pos[0][2]]
    if newPos[0] <= -6.5:
        RightScore += 1
        cmds.setAttr(ball[0] + '.translate', 0, 0, 0)
        velocity = [4, 0, 4]
        cmds.delete(RightScoreObj[0], RightScoreObj[1])
        RightScoreObj = cmds.textCurves( f='Times-Roman', t=RightScore ) 
        cmds.setAttr(RightScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        cmds.setAttr(RightScoreObj[0] + '.translate', 3, 0.5, -6)   
        cmds.setAttr(RightScoreObj[0] + '.rotateX', -90) 
        return
    elif newPos[0] >= 6.5:
        LeftScore += 1
        cmds.setAttr(ball[0] + '.translate', 0, 0, 0)
        velocity = [4, 0, 4]
        cmds.delete(LeftScoreObj[0], LeftScoreObj[1])
        LeftScoreObj = cmds.textCurves( f='Times-Roman', t=LeftScore )  
        cmds.setAttr(LeftScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        cmds.setAttr(LeftScoreObj[0] + '.translate', -3, 0.5, -6)   
        cmds.setAttr(LeftScoreObj[0] + '.rotateX', -90) 
        return
    if newPos[0] < -6:
        posZBoardL = cmds.getAttr(boardL[0] + '.translate')[0][2]
        if newPos[2] >= posZBoardL - 2 and newPos[2] <= posZBoardL + 2:
            velocity[0] = -velocity[0]
            newPos[0] = -6
    elif newPos[0] > 6:
        posZBoardR = cmds.getAttr(boardR[0] + '.translate')[0][2]
        if newPos[2] >= posZBoardR - 2 and newPos[2] <= posZBoardR + 2:
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

window = cmds.window( title="MayaPingPong", iconName='MPP', widthHeight=(200, 200) )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='Start', command=('velocity = [4, 0, 4];Continue=1;t = MyThread();t.start();'))
cmds.button( label='Left Up', command=('MoveBoard(boardL[0], -1)') )
cmds.button( label='Left Down', command=('MoveBoard(boardL[0], 1)') )
cmds.button( label='Right Up', command=('MoveBoard(boardR[0], -1)') )
cmds.button( label='Right Down', command=('MoveBoard(boardR[0], 1)') )
cmds.button( label='Stop', command=('Continue = False') )
cmds.button( label='Close Window', command=('cmds.delete(ball[0], ball[1], boardL[0], boardL[1], boardR[0], boardR[1], boardU[0], boardU[1], boardD[0], boardD[1], title[0], title[1]) ;Continue = False;cmds.deleteUI(\"' + window + '\", window=True)') )
cmds.setParent( '..' )
cmds.showWindow( window )

class MyThread(Thread):
    def run(self):
        #title = cmds.textCurves( f='Times-Roman', t='MayaPingPong' )  
        #cmds.setAttr(title[0] + '.scale', 0.5, 0.5, 0.5)   
        #cmds.setAttr(title[0] + '.translate', -7, 0.5, -8)   
        #cmds.setAttr(title[0] + '.rotateX', -90)  
        
        #LeftScoreObj = cmds.textCurves( f='Times-Roman', t=LeftScore )  
        #cmds.setAttr(LeftScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        #cmds.setAttr(LeftScoreObj[0] + '.translate', -3, 0.5, -6)   
        #cmds.setAttr(LeftScoreObj[0] + '.rotateX', -90) 
        
        #Colon = cmds.textCurves( f='Times-Roman', t=':' )  
        #cmds.setAttr(Colon[0] + '.scale', 0.5, 0.5, 0.5)   
        #cmds.setAttr(Colon[0] + '.translate', 0, 0.5, -6)   
        #cmds.setAttr(Colon[0] + '.rotateX', -90) 
        
        #RightScoreObj = cmds.textCurves( f='Times-Roman', t=RightScore )  
        #cmds.setAttr(RightScoreObj[0] + '.scale', 0.5, 0.5, 0.5)   
        #cmds.setAttr(RightScoreObj[0] + '.translate', 3, 0.5, -6)   
        #cmds.setAttr(RightScoreObj[0] + '.rotateX', -90) 
        

        
        i = 0
        global Continue
        while Continue:
            if Pause == 1:
                continue
            maya.utils.executeDeferred(DeferredFunc, i, {'frame': i * 3})
            i += 1
            time.sleep(1 / 30.0)
                       

