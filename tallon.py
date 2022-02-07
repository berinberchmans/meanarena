# tallon.py
#
# The code that defines the behaviour of Tallon. This is the place
# (the only place) where you should write code, using access methods
# from world.py, and using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 12/01/22
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)

import csv

import random


import world
import random
from config import worldLength, worldBreadth, partialVisibility, visibilityLimit
import utils
from utils import Directions

import mdptoolbox
import numpy as np

class Tallon():

    def __init__(self, arena):

        # Make a copy of the world an attribute, so that Tallon can
        # query the state of the world
        self.gameWorld = arena

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        
    def makeMove(self):
        # This is the function you need to define

        # For now we have a placeholder, which always moves Tallon
        # directly towards any existing bonuses. It ignores Meanies
        # and pits.
        # 
        # Get the location of the Bonuses.
        allBonuses = self.gameWorld.getBonusLocation()
        # firstBonus = allBonuses[0]
        allPits = self.gameWorld.getPitsLocation() 
        allMeanies = self.gameWorld.getMeanieLocation()
        myPosition = self.gameWorld.getTallonLocation()
        a=[]
        cc =[]
        tt =[]
        mm =[]
        mmProx =[]
        for ik in allBonuses:
            cc.append([ik.x,(worldBreadth-1)-ik.y])
        for pts in allPits:
            tt.append([pts.x,(worldBreadth-1)-pts.y])
        
        for mns in allMeanies:
            mm.append([mns.x,(worldBreadth-1)-mns.y])
        for mns in allMeanies:
            mmProx.append([mns.x+1,(worldBreadth-1)-mns.y])
            mmProx.append([mns.x-1,(worldBreadth-1)-mns.y])
            mmProx.append([mns.x,((worldBreadth-1)-mns.y)+1])
            mmProx.append([mns.x,((worldBreadth-1)-mns.y)+1])

   
        # Meaniproximity = self.gameWorld.tallonWindy()
        # print(Meaniproximity)


        # cc =[]
        # tt =[]
        # cc.append([firstBonus.x,(worldBreadth-1)-firstBonus.y])
        # tt.append([allPits[0].x,(worldBreadth-1)-allPits[0].y])
        print(tt)


       #    QUESTION B
        cudBBonus =[]
        newModal = np.zeros((worldBreadth,worldLength))
        if(len(cc) ==0):
            if(partialVisibility == True):
                    for ee02 in range (worldBreadth):
                        for ff02 in range (worldLength):
                            if([ff02,ee02] in tt):
                                newModal[ff02][ee02]=666
                    
                    newModal = np.transpose(newModal)
                    newModal = np.flipud(newModal)
                    for ee0 in range (worldBreadth):
                        for ff0 in range (worldLength):
                            xtrue = False
                            ytrue = False
                            if(ff0 > myPosition.x):
                                if((ff0 - myPosition.x)+1 < visibilityLimit):
                                    xtrue= True
                            else:
                                if((myPosition.x - ff0)+1 < visibilityLimit):
                                    xtrue= True
                            if(ee0 > myPosition.y):
                                if((ee0 -myPosition.y)+1 < visibilityLimit):
                                    ytrue= True
                            else:
                                if((myPosition.y)+1 - ee0 < visibilityLimit):
                                    ytrue= True
                            if(xtrue == True and ytrue == True):
                                newModal[ff0][(worldBreadth-1)- ee0]=666
                 
                    for gy in range (worldBreadth):
                        for gx in range (worldLength):
                            if(newModal[gx][gy]!=666):
                                cudBBonus.append([gx,gy])
                    print(newModal)
















        #  END OF QUESTION B


        cost = -0.04
        for k in range (worldBreadth):
            for j in range(worldLength):
                if([j,k] in tt):
                    a.append([-3,-3,-3,-3])
                elif([j,k] in mm):
                    a.append([-3,-3,-3,-3])
                elif([j,k] in mmProx):
                    a.append([-1.5,-1.5,-1.5,-1.5])
                elif([j,k] in cc):
                     a.append([5,5,5,5])
                elif([j,k] in cudBBonus):
                     rndd = random.uniform(0, 3)
                     a.append([1+rndd,1+rndd,1+rndd,1+rndd])
                else:
                    a.append([cost,cost,cost,cost])
     
        R3 = np.array(a)
        # R3 = np.flipud(R3)
        # print(R3)
      
       
        rightDir = .8
        wrongDir = .1
        fullAction = []

        rmatTotal =[]
       
        rmat =[]

        # right
        for actCounty in range (worldBreadth):
            for actCountx in range (worldLength):
                if([actCountx,actCounty] in tt):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in tt):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mm):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mm):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mmProx):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mmProx):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cc):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cc):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cudBBonus):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cudBBonus):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                else:
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            # if(actCountx == m and actCounty == n and [m,n] in cc):
                            #     rmat.append(1)
                            # else:
                                if(actCountx == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx+1 == m and actCounty == n):
                                    rmat.append(rightDir)
                                elif(actCountx == m and actCounty+1 == n):
                                    rmat.append(wrongDir)
                                elif(actCountx == m and actCounty-1 == n):
                                    rmat.append(wrongDir)
                                else:
                                    rmat.append(0)
                ans = sum(rmat)
                if(ans<1):
                    done = 0
                    for jj in rmat:
                        
                        if(jj>0 and done ==0):
                            compliment = 1-ans
                            rmat[rmat.index(jj)] = jj+compliment
                            done = 1
                if(ans>1):
                    done = 0
                    for jj in rmat:
                      
                        if(jj>0 and done ==0):
                            compliment = ans -1
                            if(jj > compliment):
                                rmat[rmat.index(jj)] =    round(jj - compliment, 1)

                                done = 1
                ans = sum(rmat)
                # print(rmat,ans)
                
                rmatTotal.append(rmat)
                rmat = []     
        rmatTotal2= np.array(rmatTotal)
        # rmatTotal2 = np.flipud(rmatTotal2)
        fullAction.append(rmatTotal2)

        rmatTotal =[]
        rmat =[]
        #Left
        for actCounty in range (worldBreadth):
            for actCountx in range (worldLength):
                if([actCountx,actCounty] in tt):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in tt):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mm):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mm):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mmProx):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mmProx):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cc):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cc):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cudBBonus):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cudBBonus):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                else:
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            # if(actCountx == m and actCounty == n and [m,n] in cc):
                            #     rmat.append(1)
                            # else:
                                if(actCountx == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx-1 == m and actCounty == n):
                                    rmat.append(rightDir)
                                elif(actCountx == m and actCounty+1 == n):
                                    rmat.append(wrongDir)
                                elif(actCountx == m and actCounty-1 == n):
                                    rmat.append(wrongDir)
                                else:
                                    rmat.append(0)
                ans = sum(rmat)
                if(ans<1):
                    done = 0
                    for jj in rmat:
                        
                        if(jj>0 and done ==0):
                            compliment = 1-ans
                            rmat[rmat.index(jj)] = jj+compliment
                            done = 1
                if(ans>1):
                    done = 0
                    for jj in rmat:
                      
                        if(jj>0 and done ==0):
                            compliment = ans -1
                            if(jj > compliment):
                                rmat[rmat.index(jj)] =    round(jj - compliment, 1)

                                done = 1
                
                rmatTotal.append(rmat)
                rmat = []     
        rmatTotal2= np.array(rmatTotal)
        # rmatTotal2 = np.flipud(rmatTotal2)
        fullAction.append(rmatTotal)
        # print(fullAction)


        rmatTotal =[]
        rmat =[]
         #UP
        for actCounty in range (worldBreadth):
            for actCountx in range (worldLength):
                if([actCountx,actCounty] in tt):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in tt):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mm):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mm):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mmProx):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mmProx):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cc):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cc):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cudBBonus):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cudBBonus):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                
                else:
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            # if(actCountx == m and actCounty == n and [m,n] in cc):
                            #     rmat.append(1)
                            # else:
                                if(actCountx == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx+1 == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx == m and actCounty-1 == n):
                                    rmat.append(rightDir)
                                elif(actCountx-1 == m and actCounty == n):
                                    rmat.append(wrongDir)
                                else:
                                    rmat.append(0)
                ans = sum(rmat)
                if(ans<1):
                    done = 0
                    for jj in rmat:
                        
                        if(jj>0 and done ==0):
                            compliment = 1-ans
                            rmat[rmat.index(jj)] = jj+compliment
                            done = 1
                if(ans>1):
                    done = 0
                    for jj in rmat:
                      
                        if(jj>0 and done ==0):
                            compliment = ans -1
                            if(jj > compliment):
                                rmat[rmat.index(jj)] =    round(jj - compliment, 1)

                                done = 1
                
                                    
                rmatTotal.append(rmat)
                rmat = []   
        rmatTotal2= np.array(rmatTotal)
        # rmatTotal2 = np.flipud(rmatTotal2)  
        fullAction.append(rmatTotal)


        rmatTotal =[]
        rmat =[]
         #DOWN
        for actCounty in range (worldBreadth):
            for actCountx in range (worldLength):
                if([actCountx,actCounty] in tt):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in tt):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mm):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mm):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in mmProx):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in mmProx):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cc):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cc):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                elif([actCountx,actCounty] in cudBBonus):
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            if(actCountx == m and actCounty == n and [m,n] in cudBBonus):
                                rmat.append(1)
                            else:
                                rmat.append(0)
                else:
                    for n in range(worldBreadth):
                        for m in range(worldLength):
                            # if(actCountx == m and actCounty == n and [m,n] in cc):
                            #     rmat.append(1)
                            # else:
                                if(actCountx == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx+1 == m and actCounty == n):
                                    rmat.append(wrongDir)
                                elif(actCountx == m and actCounty+1 == n):
                                    rmat.append(rightDir)
                                elif(actCountx-1 == m and actCounty == n):
                                    rmat.append(wrongDir)
                                else:
                                    rmat.append(0)
                           
                ans = sum(rmat)
                if(ans<1):
                    done = 0
                    for jj in rmat:
                        
                        if(jj>0 and done ==0):
                            compliment = 1-ans
                            rmat[rmat.index(jj)] = jj+compliment
                            done = 1
                if(ans>1):
                    done = 0
                    for jj in rmat:
                      
                        if(jj>0 and done ==0):
                            compliment = ans -1
                            if(jj > compliment):
                                rmat[rmat.index(jj)] =    round(jj - compliment, 1)

                                done = 1
                
                rmatTotal.append(rmat)
                rmat = []     
        rmatTotal2= np.array(rmatTotal)
        # rmatTotal2 = np.flipud(rmatTotal2)
        fullAction.append(rmatTotal)
        fullAction = np.array(fullAction)
       

        mdptoolbox.util.check(fullAction, R3)
        vi2 = []
      
        # else:
        vi2 = mdptoolbox.mdp.PolicyIteration(fullAction, R3, 0.9)
        #vi2 = mdptoolbox.mdp.PolicyIteration(fullAction, R3, 0.9)
        vi2.run()       

        dd =[]
        vv =[]
        finaldd = []
        finaldd2 = []
        countd = 0
        countd2 = 0
        for ee in range (worldBreadth):
            for ff in range (worldLength):
                dd.append(vi2.policy[countd])
                countd = countd +1
            finaldd.append(dd)
            dd = []
        
        for ee in range (worldBreadth):
            for ff in range (worldLength):
                vv.append(vi2.V[countd2])
                countd2 = countd2 +1
            finaldd2.append(vv)
            vv = []
        
        # print([myPosition.x,myPosition.y],finaldd)
        finaldd  =np.array(finaldd)
        finaldd = np.flipud(finaldd)
        # print(finaldd)
        finaldd2  =np.array(finaldd2)
        finaldd2 = np.flipud(finaldd2)
       

        

        print(finaldd2)

        themove = finaldd[myPosition.x][(worldBreadth-1)-myPosition.y]
        
      

        gg=[]
        #UP
        ox = myPosition.x
        oy = myPosition.y
        if(ox>=0 and ox<worldLength):
            if(oy+1>=0 and oy+1<worldBreadth):
                # print("position",[ox,oy])
                gg.append(finaldd2[oy+1][ox])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #DOWN
        if(ox>=0 and ox<worldLength):
            if(oy-1>=0 and oy-1<worldBreadth):
                # print("position",[ox,oy])
                gg.append(finaldd2[oy-1][ox])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #RIGHT
        if(ox+1>=0 and ox+1<worldLength):
            if(oy>=0 and oy<worldBreadth):
                # print("position",[ox,oy])
                gg.append(finaldd2[oy][ox+1])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #LEFT
        if(ox-1>=0 and ox-1<worldLength):
            if(oy>=0 and oy<worldBreadth):
                # print("position",[ox,oy])
                gg.append(finaldd2[oy][ox-1])
            else:
                gg.append(-100)
        else:
                gg.append(-100)

 
        
        max_value = max(gg)
        
        # print(gg,"-->",max_value)
        max_index = gg.index(max_value)


  

        # f = open('D:/Uni projects/AI/git/meanArena/ztemptext.csv', 'a')
        # writer = csv.writer(f)
        # cccc = finaldd2
        # for ynt in range(worldBreadth):
        #     for xnt in range(worldLength):
        #         if(ynt == oy and xnt == ox ):
        #             cccc[ynt][xnt] =666
        #     writer.writerow(cccc[ynt])
        # writer.writerow("################################")
        # f.close()
        



        if(max_index == 0):
                print("SOUTH")
                return Directions.SOUTH
        elif(max_index == 1):
                print("NORTH")
                return Directions.NORTH
        elif(max_index == 2):
                print("EAST")
                return Directions.EAST
        elif(max_index == 3):
                print("WEST")
                return Directions.WEST
            
        # Policy movement
        # if(themove == 0):
        #     print("Right")
        #     return Directions.EAST
        # elif(themove == 1):
        #     print("Left")
        #     return Directions.WEST
        # elif(themove == 2):
        #     print("Up")
        #     return Directions.SOUTH
        # elif(themove == 3):
        #     print("Down")
        #     return Directions.NORTH
        

      #################################################################################
    #     Rtable = np.zeros((worldLength,worldBreadth))
    #     Utable = np.zeros((worldLength,worldBreadth))
    #     discount = .9
    #     allBonuses = self.gameWorld.getBonusLocation()
    #     allPits = self.gameWorld.getPitsLocation() 
    #     allMeanies = self.gameWorld.getMeanieLocation()

    #     bOne = allBonuses[0]
    #     pOne = allPits[0]

    #     for ynt in range(worldBreadth):
    #         for xnt in range(worldLength):
    #             if(ynt == (worldBreadth-1)-bOne.y and xnt == bOne.x):
    #                 Rtable[xnt][ynt] = 1
    #             elif(ynt == (worldBreadth-1)-pOne.y and xnt == pOne.x):
    #                 Rtable[xnt][ynt] = -1
    #             else:
    #                  Rtable[xnt][ynt] = -0.4
    #     Rtable = np.array(Rtable)
    #     # print(Rtable)
    #     for yny in range(worldBreadth):
    #         for xny in range(worldLength):
    #             if(yny == (worldBreadth-1)-bOne.y and xny == bOne.x):
    #                 Utable[xny][yny] = 1
    #             elif(yny == (worldBreadth-1)-pOne.y and xny == pOne.x):
    #                 Utable[xny][yny] = -1
    #             else:
    #                  Utable[xny][yny] = 0
    #     Utable = np.array(Utable)
    #     print(Utable)

    #     rfliped = np.flipud(Rtable)
    #     uflipped = np.flipud(Utable)
    #     # print(fullAction)

    #     while condition:
    #         Ucopy  = Utable
    #         for vy in range(worldBreadth):
    #             for vx in range(worldLength):
    #                 uflipped[vx,vy] = rfliped[vx,vy] + discount * calcUti(fullAction, vx,vy)
            

        
    # def calcUti(actiontable,x,y):
    #     for i in actiontable:
            



