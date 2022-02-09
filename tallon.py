# tallon.py
#
# The code that defines the behaviour of Tallon. This is the place
# (the only place) where you should write code, using access methods
# from world.py, and using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 12/01/22
import sys



import random


import world
import random
from config import worldLength, worldBreadth, partialVisibility, visibilityLimit, directionProbability
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
        # Get the location of the Pits.
        allPits = self.gameWorld.getPitsLocation() 
        # Get the location of the Meanies.
        allMeanies = self.gameWorld.getMeanieLocation()
        # Get the location of Tallon.
        myPosition = self.gameWorld.getTallonLocation()

        a=[]
        cc =[]
        tt =[]
        mm =[]
        mmProx =[]

        # Creating arrays storing the location of bonuses, meanies, locations adjacent to meanies and pits.
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
            mmProx.append([mns.x,((worldBreadth-1)-mns.y)-1])


       # Code segment specific to  QUESTION B
       # This part checks if there are no bonuses visible. If no, it takes all the locations
       # that are not within visibility limit and are not pits, and later I assign them a 
       # random positive reward.
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


        # END OF QUESTION B

        # Making the rewards array | pits -> -3 | meanie -> -3 | meannie proximity -> -1.5
        # bonus -> 5 | potential bonus - > random value between 1 and 4 | other -> -0.04
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
       
        # Getting the probability for non-deterministic action
        goodaction = directionProbability
        badaction = (1 - directionProbability)/2
        fullAction = []
        rmatTotal =[]
        rmat =[]
       
        # calculating the transition model for actions -> right ,left, up and down
        for inx in range(4):
            rmatTotal =[]
            rmat =[]
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
                        if(inx==0):
                            for n in range(worldBreadth):
                                for m in range(worldLength):
                                        if(actCountx == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx+1 == m and actCounty == n):
                                            rmat.append(goodaction)
                                        elif(actCountx == m and actCounty+1 == n):
                                            rmat.append(badaction)
                                        elif(actCountx == m and actCounty-1 == n):
                                            rmat.append(badaction)
                                        else:
                                            rmat.append(0)
                        elif(inx==1):
                            for n in range(worldBreadth):
                                for m in range(worldLength):
                                        if(actCountx == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx-1 == m and actCounty == n):
                                            rmat.append(goodaction)
                                        elif(actCountx == m and actCounty+1 == n):
                                            rmat.append(badaction)
                                        elif(actCountx == m and actCounty-1 == n):
                                            rmat.append(badaction)
                                        else:
                                            rmat.append(0)
                        elif(inx==2):
                            for n in range(worldBreadth):
                                for m in range(worldLength):
                                        if(actCountx == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx+1 == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx == m and actCounty-1 == n):
                                            rmat.append(goodaction)
                                        elif(actCountx-1 == m and actCounty == n):
                                            rmat.append(badaction)
                                        else:
                                            rmat.append(0)
                        else:
                            for n in range(worldBreadth):
                                for m in range(worldLength):
                                        if(actCountx == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx+1 == m and actCounty == n):
                                            rmat.append(badaction)
                                        elif(actCountx == m and actCounty+1 == n):
                                            rmat.append(goodaction)
                                        elif(actCountx-1 == m and actCounty == n):
                                            rmat.append(badaction)
                                        else:
                                            rmat.append(0)        
                    rowsum = sum(rmat)
                    if(rowsum<1):
                        done = 0
                        for jj in rmat:
                            
                            if(jj>0 and done ==0):
                                compliment = 1-rowsum
                                rmat[rmat.index(jj)] = jj+compliment
                                done = 1
                    if(rowsum>1):
                        done = 0
                        for jj in rmat:
                        
                            if(jj>0 and done ==0):
                                compliment = rowsum -1
                                if(jj > compliment):
                                    rmat[rmat.index(jj)] =    jj - compliment
                                    done = 1             
                    rmatTotal.append(rmat)
                    rmat = []   
            rmatTotal2= np.array(rmatTotal)
            fullAction.append(rmatTotal2)
            rmatTotal =[]
            rmat =[]
        
        # generating utility values using value iteration - (using mdptoolbox)
        mdptoolbox.util.check(fullAction, R3)
        vi2 = []
        vi2 = mdptoolbox.mdp.ValueIteration(fullAction, R3, 0.9)
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
        
        # Making the utility value matrix
        for ee in range (worldBreadth):
            for ff in range (worldLength):
                vv.append(vi2.V[countd2])
                countd2 = countd2 +1
            finaldd2.append(vv)
            vv = []
        
        finaldd  =np.array(finaldd)
        finaldd = np.flipud(finaldd)
    
        finaldd2  =np.array(finaldd2)
        finaldd2 = np.flipud(finaldd2)
       
        
        
        # Greedy checking the utility values of next states to find optimal action
        gg=[]
        #UP
        ox = myPosition.x
        oy = myPosition.y
        if(ox>=0 and ox<worldLength):
            if(oy+1>=0 and oy+1<worldBreadth):
                gg.append(finaldd2[oy+1][ox])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #DOWN
        if(ox>=0 and ox<worldLength):
            if(oy-1>=0 and oy-1<worldBreadth):
                gg.append(finaldd2[oy-1][ox])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #RIGHT
        if(ox+1>=0 and ox+1<worldLength):
            if(oy>=0 and oy<worldBreadth):
                gg.append(finaldd2[oy][ox+1])
            else:
                gg.append(-100)
        else:
                gg.append(-100)
        #LEFT
        if(ox-1>=0 and ox-1<worldLength):
            if(oy>=0 and oy<worldBreadth):
                gg.append(finaldd2[oy][ox-1])
            else:
                gg.append(-100)
        else:
                gg.append(-100)

    
        max_value = max(gg)
        max_index = gg.index(max_value)

        # Applying the optimal action
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
 
    