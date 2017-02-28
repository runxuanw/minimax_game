'''
@author: Administrator
'''
from grid import grid
from time import time
import os
import sys

def printAlphaBetaInfinity(_name,_depth,_value,_a,_b,_file):
    line=_name+","+str(_depth+1)+","
    if _value==9999:
        line+="Infinity,"
    elif _value==-9999:
        line+="-Infinity,"
    else:
        line+=str(_value)+","
    if _a==9999:
        line+="Infinity,"
    elif _a==-9999:
        line+="-Infinity,"
    else:
        line+=str(_a)+","
    if _b==9999:
        line+="Infinity"
    elif _b==-9999:
        line+="-Infinity"
    else:
        line+=str(_b)
    line+="\n"
    _file.write(line)
    

def printWinner(_board,_player,_enemy):
    '''turn should be 0, and player is player'''
    score=evaluateValue(_board,_player,_enemy,0)
    print "score is: "+str(score)
    if score>0:
        print _player+" win!"
    elif score==0:
        print "draw!"
    else:
        print _player+" lose!"

def executeTask(_algorithm,_board,_player,_enemy,_rest_step,_depth,_file,_task):
    if _algorithm==1:
        initTask1(_board, _player, _enemy,_file)
    if _algorithm==2:
        initTask2(_board, _player, _enemy, _rest_step, _depth,_file,"",_task)
    if _algorithm==3:
        initTask3(_board, _player, _enemy, _rest_step, _depth,_file,"",_task)

def printboard(_board):
    print "\n"
    for i in _board:
        line=""
        for j in i:
            line+=j.occupied
        print line
        
def writeboard(_board,_file):
    for i in _board:
        line=""
        for j in i:
            line+=j.occupied
        line+="\n"
        _file.write(line)
    

def initTask1(_board,_player,_enemy,_file):
    '''find the type move for a grid and then calc its value, save the highest value grid for next move'''
    '''0 means sneak, 1 means raid, -1 means occupied'''
    move_type=0
    highest_score=-1
    move_grid=""
    best_move_type=0
    for i in _board:
        for j in i:
            move_type=0
            if j.occupied=="*":
                move_type=nearTerritory(_board,_player, j)
                if move_type==0:
                    if highest_score<j.value:
                        highest_score=j.value
                        move_grid=j
                        best_move_type=0
                elif move_type==1:
                    if highest_score<raidValue(_board,_enemy,j):
                        highest_score=raidValue(_board,_enemy,j)
                        move_grid=j
                        best_move_type=1
    moveGrid(_board,_player,_enemy,best_move_type,move_grid)
    writeboard(_board,_file)
    
    
def initTask2(_board,_player,_enemy,_rest_step,_depth,_statefile,_logfile,_task):
    if _task!="4":
        _logfile.write("Node,Depth,Value\n")
    max_value=-9999
    max_grid=""
    for i in _board:
        for j in i:
            if j.occupied=="*":
                if _rest_step<_depth:
                    _depth=_rest_step
                temp_value=minimax(_board,j,_depth,_enemy,_player,1,0,_logfile,_task)
                if temp_value>max_value:
                    max_value=temp_value
                    max_grid=j
                if _task!="4":
                    _logfile.write("root,0,"+str(max_value)+"\n")
    moveGrid(_board,_player,_enemy,nearTerritory(_board, _player, max_grid),max_grid)
    writeboard(_board, _statefile)

    
def initTask3(_board,_player,_enemy,_rest_step,_depth,_statefile,_logfile,_task):
    if _task!="4":
        _logfile.write("Node,Depth,Value,Alpha,Beta\n")
    max_value=-9999
    max_a=-9999
    min_b=9999
    max_grid=""
    for i in _board:
        for j in i:
            if j.occupied=="*":
                if _rest_step<_depth:
                    _depth=_rest_step
                temp_value=alphabeta(_board,j,_depth,max_a,min_b,_enemy,_player,1,0,_logfile,_task)
                if temp_value>max_value:
                    max_value=temp_value
                if max_a<max_value:
                    max_a=max_value
                    max_grid=j
                if _task!="4":
                    printAlphaBetaInfinity("root", -1, max_value, max_a, min_b, _logfile)
    moveGrid(_board,_player,_enemy,nearTerritory(_board, _player, max_grid),max_grid)
    writeboard(_board, _statefile)
    
def initTask4(_algorithm,_enemy_algorithm,_board,_player,_enemy,_rest_step,_depth,_enemy_depth,_file,_task):
    turn=0
    while _rest_step>0:
        if turn==0:
            turn=1
            executeTask(_algorithm, _board, _player, _enemy, _rest_step, _depth,_file,_task)
        elif turn==1:
            turn=0
            executeTask(_enemy_algorithm, _board, _enemy, _player, _rest_step, _enemy_depth,_file,_task)
        _rest_step=_rest_step-1
        #printboard(_board)

def constructBoard(_board,_temp_board):
    row=0
    for i in _board:
        _temp_board.append([])
        for idx,j in enumerate(i):
            tempgrid=grid(row,idx)
            tempgrid.value=j.value
            tempgrid.occupied=j.occupied
            _temp_board[row].append(tempgrid)
        row=row+1

'''if turn=1, it's enemy's turn; =0, player's turn'''
def alphabeta(_board,_grid,_maxdepth,_a,_b,_player,_enemy,_turn,_depth,_logfile,_task):
    if _maxdepth==_depth:
        return evaluateValue(_board,_player,_enemy,_turn)
    value=0
    a=_a
    b=_b
    temp_board=[]
    constructBoard(_board,temp_board)
    moveGrid(temp_board,_enemy, _player, nearTerritory(temp_board, _enemy, _grid), _grid)
    if _turn==1:
        value=9999
        endRedundantLoop=False
        for i in temp_board:
            if not endRedundantLoop:
                for j in i:
                    if j.occupied=="*":
                        temp_value=alphabeta(temp_board,j, _maxdepth,a,b,_enemy,_player,0,_depth+1,_logfile,_task)
                        if value>temp_value:
                            value=temp_value
                        if b>value:
                            if value<a:
                                endRedundantLoop=True
                                break
                            b=value
                        if _depth+1==_maxdepth:
                            endRedundantLoop=True
                            break
                        if b<=a:
                            endRedundantLoop=True
                            break
                        if _task!="4":
                            printAlphaBetaInfinity(_grid.name, _depth, value, a, b, _logfile)
    else:               
        value=-9999
        endRedundantLoop=False
        for i in temp_board:
            if not endRedundantLoop:
                for j in i:
                    if j.occupied=="*":
                        temp_value=alphabeta(temp_board,j, _maxdepth,a,b,_enemy,_player,1,_depth+1,_logfile,_task)
                        if temp_value>value:
                            value=temp_value
                        if value>a:
                            if value>b:
                                endRedundantLoop=True
                                break
                            a=value
                        if _depth+1==_maxdepth:
                            endRedundantLoop=True
                            break
                        if b<=a:
                            endRedundantLoop=True
                            break
                        if _task!="4":
                            printAlphaBetaInfinity(_grid.name, _depth, value, a, b, _logfile)
    if value==-9999 or value==9999:
        value=evaluateValue(_board,_player,_enemy,_turn)
    if _task!="4":
        printAlphaBetaInfinity(_grid.name, _depth, value, a, b, _logfile)
    return value



'''if turn=1, it's enemy's turn; =0, player's turn'''
def minimax(_board,_grid,_maxdepth,_player,_enemy,_turn,_depth,_logfile,_task):
    if _maxdepth==_depth:
        return evaluateValue(_board,_player,_enemy,_turn)
    value=0
    temp_board=[]
    constructBoard(_board,temp_board)
    moveGrid(temp_board,_enemy, _player, nearTerritory(temp_board, _enemy, _grid), _grid)
    if _turn==1:
        value=9999
        endRedundantLoop=False
        for i in temp_board:
            if not endRedundantLoop:
                for j in i:
                    if j.occupied=="*":
                        temp_value=minimax(temp_board,j, _maxdepth,_enemy,_player,0,_depth+1,_logfile,_task)
                        if value>temp_value:
                            value=temp_value
                        if _depth+1==_maxdepth:
                            endRedundantLoop=True
                            break
                        if _task!="4":
                            if value!=9999:
                                _logfile.write(_grid.name+","+str(_depth+1)+","+str(value)+"\n")
                            else:
                                _logfile.write(_grid.name+","+str(_depth+1)+",Infinity\n")
    else:
        value=-9999
        endRedundantLoop=False
        for i in temp_board:
            if not endRedundantLoop:
                for j in i:
                    if j.occupied=="*":
                        temp_value=minimax(temp_board,j, _maxdepth,_enemy,_player,1,_depth+1,_logfile,_task)
                        if temp_value>value:
                            value=temp_value
                        if _depth+1==_maxdepth:
                            endRedundantLoop=True
                            break
                        if _task!="4":
                            if value!=-9999:
                                _logfile.write(_grid.name+","+str(_depth+1)+","+str(value)+"\n")
                            else:
                                _logfile.write(_grid.name+","+str(_depth+1)+",-Infinity\n")
    if value==-9999 or value==9999:
        value=evaluateValue(_board,_player,_enemy,_turn)
    if _task!="4":
        _logfile.write(_grid.name+","+str(_depth+1)+","+str(value)+"\n")
    return value
    

def evaluateValue(_board,_player,_enemy,_turn):
    value=0
    if _turn==0:
        for i in _board:
            for j in i:
                if j.occupied==_player:
                    value+=j.value
                if j.occupied==_enemy:
                    value-=j.value
    else:
        for i in _board:
            for j in i:
                if j.occupied==_enemy:
                    value+=j.value
                if j.occupied==_player:
                    value-=j.value
    return value
            
    '''1 is raid, 0 is sneak'''
def nearTerritory(_board,_player,_grid):
    _row=_grid.row
    _col=_grid.col
    if _row>0:
        if _board[_row-1][_col].occupied==_player:
            return 1
    if _row<4:
        if _board[_row+1][_col].occupied==_player:
            return 1
    if _col>0:
        if _board[_row][_col-1].occupied==_player:
            return 1
    if _col<4:
        if _board[_row][_col+1].occupied==_player:
            return 1
    return 0


def raidValue(_board,_enemy,_grid):
    _row=_grid.row
    _col=_grid.col
    value=_board[_row][_col].value
    if _row>0:
        if _board[_row-1][_col].occupied==_enemy:
            value+=_board[_row-1][_col].value
    if _row<4:
        if _board[_row+1][_col].occupied==_enemy:
            value+=_board[_row+1][_col].value
    if _col>0:
        if _board[_row][_col-1].occupied==_enemy:
            value+=_board[_row][_col-1].value
    if _col<4:
        if _board[_row][_col+1].occupied==_enemy:
            value+=_board[_row][_col+1].value
    if _board[_row][_col].occupied!="*":
        print "error: raid occupied grid"
    return value

'''move_type 1 means raid'''
def moveGrid(_board,_player,_enemy,_move_type,_grid):
    _row=_grid.row
    _col=_grid.col
    _board[_row][_col].occupied=_player
    if _move_type==1:
        if _row>0:
            if _board[_row-1][_col].occupied==_enemy:
                _board[_row-1][_col].occupied=_player
        if _row<4:
            if _board[_row+1][_col].occupied==_enemy:
                _board[_row+1][_col].occupied=_player
        if _col>0:
            if _board[_row][_col-1].occupied==_enemy:
                _board[_row][_col-1].occupied=_player
        if _col<4:
            if _board[_row][_col+1].occupied==_enemy:
                _board[_row][_col+1].occupied=_player


def main(folder,inputfile):
    task=-1
    player=""
    enemy=""
    depth=-1
    enemy_depth=-1
    algorithm=-1
    enemy_algorithm=-1
    board=[]
    rest_step=25
    location="\\"+str(folder)+"\\"+inputfile
    path=os.getcwd()+location
    file=open(path,'r')
    row=0
    rowstate=0
#read file is hard coded
    for line in file:
        line=line.strip('\n')
        if task==-1:
            task=line
        elif task!="4" and task!=-1:
            if player=="":
                player=line
                if player=="X":
                    enemy="O"
                if player=="O":
                    enemy="X"
            elif depth==-1:
                depth=int(line)
            else:
                if row<5:
            #append a new row
                    board.append([])
                    values=line.split(' ')
                    for idx,i in enumerate(values):
                        tempgrid=grid(row,idx)
                        tempgrid.value=int(i)
                        board[row].append(tempgrid)
                    row=row+1
                else:
                    for idx,i in enumerate(line):
                        board[rowstate][idx].occupied=i
                        if i!="*":
                            rest_step=rest_step-1
                    rowstate=rowstate+1
        elif task=="4":
            if player=="":
                player=line
            elif algorithm==-1:
                algorithm=int(line)
            elif depth==-1:
                depth=int(line)
            elif enemy=="":
                enemy=line
            elif enemy_algorithm==-1:
                enemy_algorithm=int(line)
            elif enemy_depth==-1:
                enemy_depth=int(line)
            else:
                if row<5:
            #append a new row
                    board.append([])
                    values=line.split(' ')
                    for idx,i in enumerate(values):
                        tempgrid=grid(row,idx)
                        tempgrid.value=int(i)
                        board[row].append(tempgrid)
                    row=row+1
                else:
                    for idx,i in enumerate(line):
                        board[rowstate][idx].occupied=i
                        if i!="*":
                            rest_step=rest_step-1
                    rowstate=rowstate+1
    starttime=time()
    '''greedy best first search'''
    if task=="1":
        statefile=open("next_state.txt","w+")
        initTask1(board,player,enemy,statefile)
        endtime=time()
        print "task 1 took: "+str(endtime-starttime)
        statefile.close()
    
    '''minimax algorithm'''
    if task=="2":
        statefile=open("next_state.txt","w+")
        logfile=open("traverse_log.txt","w+")
        initTask2(board,player,enemy,rest_step,depth,statefile,logfile,task)
        endtime=time()
        print "task 2 took: "+str(endtime-starttime)
        statefile.close()
        logfile.close()
    
    '''alpha-beta pruning'''
    if task=="3":
        statefile=open("next_state.txt","w+")
        logfile=open("traverse_log.txt","w+")
        initTask3(board,player,enemy,rest_step,depth,statefile,logfile,task)
        endtime=time()
        print "task 3 took: "+str(endtime-starttime)
        statefile.close()
        logfile.close()

    '''simulation game'''
    if task=="4":
        traceStateFile=open("trace_state.txt","w+")
        initTask4(algorithm,enemy_algorithm,board,player,enemy,rest_step,depth,enemy_depth,traceStateFile,task)
    #printWinner(board,player,enemy)
        endtime=time()
        print "task 4 took: "+str(endtime-starttime)
        traceStateFile.close()
    
#printboard(board)
#printWinner(board, player, enemy)
if __name__ == "__main__":
    main(4,"input.txt")
