#!/usr/bin/env python
# coding: utf-8

# In[426]:


import tkinter as tk
from tkinter import *
import sys
import numpy as np
import time
from copy import copy, deepcopy
import ctypes
import itertools
import datetime


# In[427]:


root = tk.Tk()


# In[428]:


Canvas = tk.Canvas(root)
Canvas.grid()


# In[429]:
global lblMtr
global intMtr
# global probMtr
# global fatMtr
global itKeeper
global frsChcNum
global sttNum
global rngNum
global preStt
global timeTab
global epoch
global ustel
#You can confgure the hardness of the iteration and brute force by changing these below variables. Higher the values, harder the iteration.
#rngNum can be set to 9 maximum
#sttNum can be set to max 81
#frsChcNum can be set to max 9
frsChcNum = 6
rngNum = 7
sttNum = 10
timeTab = None
epoch = datetime.datetime.utcfromtimestamp(0)
ustel = 2.1
#tk.Label(root, text="test").grid()

lblMtr = [[None for i in range(9)] for j in range(9)]
intMtr = [[0 for i in range(9)] for j in range(9)]
# probMtr = [[[] for i in range(9)] for j in range(9)]
# fatMtr = [[[] for i in range(9)] for j in range(9)]
# priorCordList = []


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0
    
# Assigns values to cells and modifies the Label texts accordingly. Binded with mouse click
def setNum(event, row, col):
    tmp = lblMtr[row][col]["text"]
    if tmp == "":
        lblMtr[row][col].configure(text = "1")
        intMtr[row][col] = 1
        preStt += 1
    else:
        tmp = ((int(tmp) + 1) % 10) 
        if tmp == 0:
            tmp = 1
        lblMtr[row][col].configure(text = str(tmp))
        intMtr[row][col] = tmp


#Create Labels within the canvas. All the LAbel objects are refenced in lblMtr LabelMatrix
#Default text of label is test. lblMtr value is 0 (zero) it is not assigned yet
for i in range(9):
    for j in range(9):
        tmpLbl = tk.Label(Canvas, text="", borderwidth=2, relief="groove")
        lblMtr[i][j] = tmpLbl
        tmpLbl.grid(row = i, column = j, padx=0, pady = 0, ipadx=10, ipady=10, sticky="nsew")
        
#All the label objs are binded with mouse click to SetNum function
for i in range(9):
    for j in range(9):
        lblMtr[i][j].bind('<Button-1>', lambda event, row = i, col = j: setNum(event, row, col))

#This button starts the process
tk.Button(Canvas, text="Solve the Puzzle", command=lambda: startSolving()).grid(row=10,column=1,columnspan=9,sticky=W)

#moves list is to keep all the moves that have been done till the last iteration
moves = []

isDone = False
preStt = 0

#starter function
def startSolving():
    startUp(2)
    global timeTab
    timeTab = [[0,0, (82 - preStt - j)**0.5, False] for j in range(81 - preStt)]
    sidTb = [0 for j in range(81 - preStt)] #0 should not dec 1 should dec
    # print("timeTab old: \n", timeTab)
    for i in range(81 - preStt):
        for j in range(80 - preStt - i):
            timeTab[i][2] *= timeTab[i+1+j][2]*(81 - preStt - i - j -1)
            
        timeTab[i][2] = (timeTab[i][2]**(1/((81 - preStt - i)**0.7)))/(ustel**((1.1*(81 - preStt - i)))**0.5)
    # print("timeTab new: \n", timeTab)
    itNum = 0
    recursive(itNum)
    print("Tamamlanamadı!")
    return False

#this is a well known sudoku example set
def startUp(i):
    if i == 0:
        setCell([1,0], 6, -1)
        setCell([1,1], 8, -1)
        setCell([2,0], 1, -1)
        setCell([2,1], 9, -1)
        setCell([3,0], 8, -1)
        setCell([3,1], 2, -1)
        setCell([4,2], 4, -1)
        setCell([5,1], 5, -1)
        setCell([6,2], 9, -1)
        setCell([7,1], 4, -1)
        setCell([8,0], 7, -1)
        setCell([8,2], 3, -1)

        setCell([0,3], 2, -1)
        setCell([0,4], 6, -1)
        setCell([1,4], 7, -1)
        setCell([2,5], 4, -1)
        setCell([3,3], 1, -1)
        setCell([4,3], 6, -1)
        setCell([4,5], 2, -1)
        setCell([5,5], 3, -1)
        setCell([6,3], 3, -1)
        setCell([7,4], 5, -1)
        setCell([8,4], 1, -1)
        setCell([8,5], 8, -1)


        setCell([0,6], 7, -1)
        setCell([0,8], 1, -1)
        setCell([1,7], 9, -1)
        setCell([2,6], 5, -1)
        setCell([3,7], 4, -1)
        setCell([4,6], 9, -1)
        setCell([5,7], 2, -1)
        setCell([5,8], 8, -1)
        setCell([6,7], 7, -1)
        setCell([6,8], 4, -1)
        setCell([7,7], 3, -1)
        setCell([7,8], 6, -1)
        
        preStt = 36
    elif i == 1:
        setCell([0,1], 2, -1)
        setCell([2,1], 7, -1)
        setCell([2,2], 4, -1)
        setCell([4,1], 8, -1)
        setCell([5,0], 6, -1)
        setCell([7,0], 5, -1)
        
        setCell([1,3], 6, -1)
        setCell([2,4], 8, -1)
        setCell([3,5], 3, -1)
        setCell([4,4], 4, -1)
        setCell([5,3], 5, -1)
        setCell([6,4], 1, -1)
        setCell([7,5], 9, -1)
    
        setCell([1,8], 3, -1)
        setCell([3,8], 2, -1)
        setCell([4,7], 1, -1)
        setCell([6,6], 7, -1)
        setCell([6,7], 8, -1)
        setCell([8,7], 4, -1)
        
        preStt = 19
    elif i == 2:
        setCell([0,1], 2, -1)
        setCell([1,0], 5, -1)
        setCell([1,1], 8, -1)
        setCell([3,0], 3, -1)
        setCell([3,1], 7, -1)
        setCell([4,0], 6, -1)
        setCell([5,2], 8, -1)
        setCell([7,2], 9, -1)
        
        setCell([0,3], 6, -1)
        setCell([0,5], 8, -1)
        setCell([1,5], 9, -1)
        setCell([2,4], 4, -1)
        
        setCell([6,4], 2, -1)
        setCell([7,3], 8, -1)
        setCell([8,3], 3, -1)
        setCell([8,5], 6, -1)
    
        setCell([1,6], 7, -1)
        
        setCell([3,6], 5, -1)
        setCell([4,8], 4, -1)
        setCell([5,7], 1, -1)
        setCell([5,8], 3, -1)
        
        setCell([7,7], 3, -1)
        setCell([7,8], 6, -1)
        setCell([8,7], 9, -1)
        preStt = 24
    Canvas.update()

def updTT(itNum):
    stp = unix_time_millis(datetime.datetime.now())
    global timeTab
    for i in range(itNum):
        timeTab[i][1] = stp - timeTab[i][0]
        if timeTab[i][1] > timeTab[i][2]:
            for j in range(itNum-i):
                # timeTab[i+j][0] = 0
                # timeTab[i+j][1] = 0
                # timeTab[i+j][2] = 0
                timeTab[i+j][3] = True
                timeTab[i+j][0] = stp
                timeTab[i+j][1] = 0
            break
        else:
            timeTab[i][3] = False
            

    
def isFinished():
    # stt = datetime.datetime.now()
    if wholeChc() and completeChc():
        isDone = True
        Canvas.update()
        ctypes.windll.user32.MessageBoxW(0, "SuDoku Çözüldü!", "Helal!", 1)
        # stp = datetime.datetime.now()
        # print("isFinished time: ", stp - stt)
        return True
    else:
        # stp = datetime.datetime.now()
        # print("isFinished time: ", stp - stt)
        return False

#this is the dynamic solver.
def recursive(itNum):
    global timeTab
    # print("itNum: ", itNum, " moves: ", moves)
    global sttNum
    global frsChcNum
    global rngNum
    timeTab[itNum][0] = unix_time_millis(datetime.datetime.now())
    updTT(itNum)
    print("timeTab: \n", timeTab)
    print("itNum: ", itNum)
    sttNum = int((81 - preStt - itNum + 1)/((81 - preStt - itNum/5 + 1)/2.9))
    frsChcNum = int((81 - preStt - itNum + 1)/((81 - preStt - itNum/5 + 1)/(7)))
    rngNum = int((81 - preStt - itNum + 1)/((81 - preStt - itNum/7 + 1)/5))
    # print("sttNum: ", sttNum, "/n", "frsChcNum: ", frsChcNum, "/n", "rngNum: ", rngNum, "/n")
    if not isFinished() and not shlItDec(itNum) and not frstLvlChc(frsChcNum) and not timeTab[itNum][3]:
    # if not isFinished() and not shlItDec(itNum) and not frstLvlChc(frsChcNum):
        fatMtrY = fatChanceMatrix()
        tempMFC = findMinFatCh(itNum, fatMtrY)

        for i in range(len(tempMFC)):
            if timeTab[itNum][3]:
                break
            tempProbs = len(fatMtrY[tempMFC[i][1][0]][tempMFC[i][1][1]][1])
            for j in range(tempProbs):
                if timeTab[itNum][3]:
                    break
                tempVal = fatMtrY[tempMFC[i][1][0]][tempMFC[i][1][1]][1][j]
                tempCor = tempMFC[i][1]
                setCell(tempCor, tempVal, -1)
                moves.append([tempCor, tempVal])
                Canvas.update()
                if not frstLvlChc(frsChcNum):
                    recursive(itNum + 1)
                reSetCell(tempCor)
                Canvas.update()
        
        print("fordan çıktı \n")
      
#reverses the last move. reSets cell and pops the last move from the list
def reverseLastIt():
    reSetCell(moves[-1][1])
    moves.pop()
       
#reverses all the moves within an iteration. resets all cells that are assigned within an iteration
def reverseIteration(itNum):
    ctr = len(moves)
    stt = False
    for i in range(ctr):
        if moves[ctr-1-i][0] == itNum:            
            reSetCell(moves[ctr-1-i][1])
            moves.pop(ctr-1-i)
            stt = True
        else:
            if stt:
                break
    
#returns true if the box meets the sudoke rule 
# there are 9 boxes
def boxChc(rowInd, colInd):
    tempBox = [intMtr[rowInd*3][colInd*3:colInd*3+3],
              intMtr[rowInd*3+1][colInd*3:colInd*3+3],
              intMtr[rowInd*3+2][colInd*3:colInd*3+3]]
    tmpChLs = [0 for i in range(9)]
    for i in range(3):
        for j in range(3):
            if tempBox[i][j] != 0:
                tmpChLs[tempBox[i][j]-1] += 1
    for i in tmpChLs:
        if i > 1:
            return False #Yani OK değil
    return True

#returns true if the column meets the sudoke rule 
def colChc(col):
    tmpMtr = np.array(intMtr)
    tempLst = tmpMtr[:,col]
    tmpChLs = [0 for i in range(9)]
    for i in range(9):
        if tempLst[i] != 0:
            tmpChLs[tempLst[i]-1] += 1
    for i in tmpChLs:
        if i > 1:
            return False #Yani OK değil
    return True
    
#returns true if the row meets the sudoke rule
def rowChc(row):
    tmpMtr = np.array(intMtr)
    tempLst = tmpMtr[row,:]
    tmpChLs = [0 for i in range(9)]
    for i in range(9):
        if tempLst[i] != 0:
            tmpChLs[tempLst[i]-1] += 1
    for i in tmpChLs:
        if i > 1:
            return False #Yani OK değil
    return True

#returns true if the cell meets the sudoke rule
def fullChc(row, col):
    return rowChc(row) and colChc(col) and boxChc(int(row/3), int(col/3))


#return True if everything seems in order False if not
def wholeChc():
    for i in range(9):
        if not rowChc(i):
            return False
        if not colChc(i):
            return False
    for i in range(3):
        for j in range(3):
            if not boxChc(i,j):
                return False
    return True

#returns True if all cells are filled
def completeChc():
    for i in range(9):
        for j in range(9):
            if intMtr[i][j] == 0:
                return False
    return True

#within the box, this function extracts the possible values to assign in empty cells
# [1,4,6] gibi 3 boş kutuya yerleşebilecek kalan value'lar
def boxSpace(rowInd, colInd):
    tempBox = [intMtr[rowInd*3][colInd*3:colInd*3+3],
              intMtr[rowInd*3+1][colInd*3:colInd*3+3],
              intMtr[rowInd*3+2][colInd*3:colInd*3+3]]
    tmpChLs = [0 for i in range(9)]
    boxSpc = []
    for i in range(3):
        for j in range(3):
            if tempBox[i][j] != 0:
                tmpChLs[tempBox[i][j]-1] += 1
    for i in range(9):
        if tmpChLs[i] == 0:
            boxSpc.append(i+1)
    return boxSpc
    
#within the column, this function extracts the possible values to assign in empty cells
def colSpace(col):
    tmpMtr = np.array(intMtr)
    tempLst = tmpMtr[:,col]
    tmpChLs = [0 for i in range(9)]
    colSpc = []
    for i in range(9):
        if tempLst[i] != 0:
            tmpChLs[tempLst[i]-1] += 1
    for i in range(9):
        if tmpChLs[i] == 0:
            colSpc.append(i+1)
    return colSpc

#within the row, this function extracts the possible values to assign in empty cells
def rowSpace(row):
    tmpMtr = np.array(intMtr)
    tempLst = tmpMtr[row,:]
    tmpChLs = [0 for i in range(9)]
    rowSpc = []
    for i in range(9):
        if tempLst[i] != 0:
            tmpChLs[tempLst[i]-1] += 1
    for i in range(9):
        if tmpChLs[i] == 0:
            rowSpc.append(i+1)
    return rowSpc
           

def recPrm(it, arr):
    if it == len(arr):
        pass
    else:
        for i in arr[it][1]:
            intMtr[arr[it][0][0]][arr[it][0][1]] = i
            recPrm(it + 1, arr)
            intMtr[arr[it][0][0]][arr[it][0][1]] = 0
        
           
def permutCheck():
    if whlSpcRnk() < 16:
        tempPrmt = list(itertools.permutations(wholeSpc(), r=whlSpcRnk()))
        for i in tempPrmt:   
            for j in i:
                for k in j[1]:
                    intMtr[tempPrmt[j][0][0]][tempPrmt[j][0][1]] = k
           
def wholeSpc():
    tmpArr = []
    for i in range(9):
        for j in range(9):
            if intMtr[i][j] == 0:
                tmpArr.append([[i,j], []])
                for k in range(9):
                    intMtr[i][j] = k+1
                    if fullChc(i,j):
                        tmpArr[-1][1].append(k+1)
                intMtr[i][j] = 0
    return tmpArr

def whlSpcRnk():
    tmp = 0
    for i in range(9):
        for j in range(9):
            if intMtr[i][j] == 0:
                tmp += 1
    return tmp
                
def frstLvlChc(rng):      
    # stt = datetime.datetime.now()
      
    for i in range(9):
        clSp = colSpace(i)
        rwSp = rowSpace(i)
        chCol = True
        if len(clSp) < rng:
            tmpArr = []
            tempPrmt = list(itertools.permutations(clSp, r=len(clSp)))
            for j in range(9):
                if intMtr[j][i] == 0:
                    tmpArr.append([j,i])
            for j in tempPrmt:
                for k in range(len(tmpArr)):
                    intMtr[tmpArr[k][0]][tmpArr[k][1]] = j[k]
                if wholeChc():
                    chCol = False
                for k in range(len(tmpArr)):
                    intMtr[tmpArr[k][0]][tmpArr[k][1]] = 0
        else:
            chCol = False
            
        chRow = True            
        if len(rwSp) < rng:
            tmpArr = []
            tempPrmt = list(itertools.permutations(rwSp, r=len(rwSp)))
            for j in range(9):
                if intMtr[i][j] == 0:
                    tmpArr.append([i,j])
            for j in tempPrmt:
                for k in range(len(tmpArr)):
                    intMtr[tmpArr[k][0]][tmpArr[k][1]] = j[k]
                if wholeChc():
                    chRow = False
                for k in range(len(tmpArr)):
                    intMtr[tmpArr[k][0]][tmpArr[k][1]] = 0
        else:
            chRow = False
            
        if chCol or chRow:
            # stp = datetime.datetime.now()
            # print("frstLvlChc time: ", stp - stt)
            return True
            
    # stp = datetime.datetime.now()
    # print("frstLvlChc time: ", stp - stt)
    return False
            
#for each row and col, it creates probMtr[i][j] = [0,2,4...] it means in intMtr[i][j] cell can have values [0,2,4...]
#without violating the rules
def updProbMatrix():
    probMtr = [[[] for i in range(9)] for j in range(9)]

    for i in range(9):
        for j in range(9):
            if intMtr[i][j] != 0:
                probMtr[i][j] = []
            else:
                for k in range(9):
                    intMtr[i][j] = k + 1
                    if fullChc(i, j):
                        probMtr[i][j].append(k + 1)
                intMtr[i][j] = 0
    return probMtr
    
#this function creates fatMtr which is the shrinked probMtr to be more precise.
#fatMtr[i][j] has two elements, i,j is coordinates corresponding to the intMtr
#fatMtr[i][j][0] is the probability score. If it is higerher, probability is less:
#meaning, its probable values also others pobable values.
#but if fatMtr[i][j][0] is 1 than it means only i,j can have that value, hence, i,j has that value
#if fatMtr[i][j][0] is 0 it means that cords is already set
#fatMtr[i][j][1] is the probable values that i,j can have
def fatChanceMatrix():
    fatMtr = [[[] for i in range(9)] for j in range(9)]
    probMtr = updProbMatrix()
    tProbMtr = np.array(probMtr)
    for k in range(9):
        tProbMtr[:,k] = dedComRwCl(tProbMtr[:,k])
        tProbMtr[k,:] = dedComRwCl(tProbMtr[k,:])
    for i in range(9):
        for j in range(9):
            fatMtr[i][j] = [len(tProbMtr[i][j]), tProbMtr[i][j]]

    return fatMtr

#this function returns minFatCrds. which is minimumFatCoordinates. 
# minFatCrds[i][0] is ith index items probability score. Again less the better.
# minFatCrds[i][1] is [row,col] the coordinates which correspondsto the coordinates on intMtr
#
def findMinFatCh(iterNum, fatMtr):

    minFatCrds = [] 
    for i in range(9):
        for j in range(9):
            if fatMtr[i][j][0] != 0:
                if len(minFatCrds) == 0:
                    minFatCrds.append([fatMtr[i][j][0], [i,j]])
                else:
                    ch = 0
                    for k in range(len(minFatCrds)):
                        if minFatCrds[k][0] < fatMtr[i][j][0]:
                            minFatCrds.insert(k, [fatMtr[i][j][0], [i,j]])
                            break
                        ch += 1
                    if ch == len(minFatCrds):
                        minFatCrds.append([fatMtr[i][j][0], [i,j]])
    minFatCrds.reverse()
    
    #newcode piece trial
    newMinFatCrds =[]
    for i in range(len(minFatCrds)):
        if minFatCrds[i][0] == 1:
            newMinFatCrds.append(minFatCrds[i])
        else:
            break
    
    if len(newMinFatCrds) > 0:
        return newMinFatCrds

    return minFatCrds
                   

def shlItDec(itNum):
    if timeTab[itNum][3]:
        return True
    stt = unix_time_millis(datetime.datetime.now())
    global itKeeper
    maxStop = 0
    if shouldItDec(0, sttNum, rngNum, itNum):
        itKeeper = True
        stp = unix_time_millis(datetime.datetime.now())
        # print("shlItDec time: ", stp - stt)
        return True
    else:
        itKeeper = False
        stp = unix_time_millis(datetime.datetime.now())
        # print("shlItDec time: ", stp - stt)
        return False
    

    
#if in row, col and box spaces, there is only one possible value and if we put it it doesnt fit to the rule than it returns
# True, warning you should step down the iteration and make a clear start
def shouldItDec(sttIt, stpIt, rng, itNum):
    if timeTab[itNum][3]:
        return True
    if sttIt < stpIt:
        # print("sttIt: ", sttIt)
        for it in range(rng):
            itr = it + 1
            ch = False
            for i in range(9):
                tempColSpc = colSpace(i)
                if len(tempColSpc) == itr:
                    tempPrmt = list(itertools.permutations(tempColSpc, r=itr))
                    # print("tempPrmt:", tempPrmt)
                    tArr = []
                    for j in range(9):
                        if intMtr[j][i] == 0:
                            tArr.append([j,i])
                    iChc = True
                    for k in tempPrmt:
                        for g in range(itr):
                            setCell([tArr[g][0],tArr[g][1]], k[g], -1)
                        if wholeChc():
                            if not shouldItDec(sttIt+1, stpIt, rng, itNum):
                                iChc = False
                        for g in range(itr):
                            reSetCell([tArr[g][0],tArr[g][1]])
                        if not iChc:
                            break
                    if iChc:
                        ch = True
                        break
                    
            if ch:  
                # print(sttIt, "!!!!!! Returned True!!!!!!")
                return True
                

            for i in range(9):
                tempRowSpc = rowSpace(i)
                if len(tempRowSpc) == itr:
                    tempPrmt = list(itertools.permutations(tempRowSpc, r=itr))
                    # print("tempPrmt:", tempPrmt)
                    tArr = []
                    for j in range(9):
                        if intMtr[i][j] == 0:
                            tArr.append([i,j])
                    iChc = True
                    for k in tempPrmt:
                        for g in range(itr):
                            setCell([tArr[g][0],tArr[g][1]], k[g], -1)
                        if wholeChc():
                            if not shouldItDec(sttIt+1, stpIt, rng, itNum):
                                iChc = False
                        for g in range(itr):
                            reSetCell([tArr[g][0],tArr[g][1]])
                        if not iChc:
                            break
                    if iChc:
                        ch = True
                        break
            if ch:
                # print(sttIt, "!!!!!! Returned True!!!!!!")
                return True
            
            for i in range(3):
                for j in range(3):
                    tempBoxSpc = boxSpace(i, j)
                    if len(tempBoxSpc) == itr:
                        tempPrmt = list(itertools.permutations(tempBoxSpc, r=itr))
                        # print("tempPrmt:", tempPrmt)
                        tArr = []
                        for k in range(3):
                            for l in range(3):
                                if intMtr[i*3+k][j*3+l] == 0:
                                    tArr.append([i*3+k,j*3+l])
                        iChc = True
                        for k in tempPrmt:
                            for g in range(itr):
                                setCell([tArr[g][0],tArr[g][1]], k[g], -1)
                            if wholeChc():
                                if not shouldItDec(sttIt+1, stpIt, rng, itNum):
                                    iChc = False
                            for g in range(itr):
                                reSetCell([tArr[g][0],tArr[g][1]])
                            if not iChc:
                                break
                        if iChc:
                            ch = True
                            break
            if ch:
                # print(sttIt, "!!!!!! Returned True!!!!!!")
                return True
            # else:
                # return False
        # print(sttIt, " !!!!!! Returned False!!!!!!")
        return False
        
def chStCl(crd, val):
    if intMtr[crd[0]][crd[1]] != 0:
        return False
    intMtr[crd[0]][crd[1]] = val
    if wholeChc():
        intMtr[crd[0]][crd[1]] = 0
        return True
    else:
        return False
    
def setCell(crd, val, iterNum):
    intMtr[crd[0]][crd[1]] = val
    lblMtr[crd[0]][crd[1]].configure(text = str(val))
    if iterNum != -1:
        moves.append([iterNum, crd, val])

    
def reSetCell(crd):
    intMtr[crd[0]][crd[1]] = 0
    lblMtr[crd[0]][crd[1]].configure(text = "")
    
#this method removes te common probable values of each cell in in each cell
#example, if one cell has 1,2,3,4 and other all has 1,2,3 probable values, 
#it returns 1 for the cell and [] for all others
def deductCommons(arr):
    tmpChLs = [0 for i in range(9)]
    # tmpChLs = [[0 for i in range(3)] for j in range(3)]
    ch = 0
    # arrLst = []
    arrLst = [[[] for i in range(3)] for j in range(3)]
    
    for i in range(3):
        for j in range(3):
            if arr[i][j] == []:
                ch += 1
            else:
                arr[i][j].sort()
                for k in arr[i][j]:
                    arrLst[i][j].append(k)
                    tmpChLs[k-1] += 1
    
    tmpBox = [[[] for i in range(3)] for j in range(3)]
            
    minT = 9
    for i in range(3):
        if tmpChLs[i] != 0:
            if tmpChLs[i] < minT:
                minT = tmpChLs[i]

    for i in range(9):
        if tmpChLs[i] == minT:
            for j in range(3):
                for k in range(3):
                    if i+1 in arr[j][k]:
                        tmpBox[j][k].append(i+1)
    
    arr = tmpBox
    return arr
    
def dedComRwCl(arr):
    tmpChLs = [0 for i in range(9)]
    ch = 0
    arrLst = []
    for i in range(9):
        if arr[i] == []:
            ch += 1
        else:
            arr[i].sort()
            arrLst.append(arr[i])
            for j in arr[i]:
                tmpChLs[j-1] += 1
    tmparr = [[] for i in range(9)]
    index = 0
    minT = 9
    for i in range(9):
        if tmpChLs[i] != 0:
            if tmpChLs[i] < minT:
                minT = tmpChLs[i]
    for i in range(9):
        if tmpChLs[i] == minT:
            for j in range(9):
                if i+1 in arr[j]:
                    tmparr[j].append(i+1)
                    
    arr = tmparr
                            
    return arr

    
def frstPriorCords():
    updProbMatrix()
    for i in range(9):
        for j in range(9):
            if len(probMtr[i][j]) != 0:
                tmpLen = len(probMtr[i][j])
                if len(priorCordList) == 0:
                    priorCordList.append([i,j])
                else:
                    ch = 0
                    for k in range(len(priorCordList)):
                        if tmpLen < len(probMtr[priorCordList[k][0]][priorCordList[k][1]]):
                            priorCordList.insert(k, [i,j])
                            break
                        ch += 1
                    if ch == len(priorCordList):
                        priorCordList.append([i,j])

    


mainloop()





