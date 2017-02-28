'''
@author: Administrator
'''

class grid:
    '''
    -1 mean init value, occupied would be X or O or *
    '''
    value=-1
    occupied=""
    name=""
    row=-1
    col=-1

    def __init__(self, _row,_col):
        '''
        Constructor
        '''
        if _col==0:
            self.name+="A"
        elif _col==1:
            self.name+="B"
        elif _col==2:
            self.name+="C"
        elif _col==3:
            self.name+="D"
        elif _col==4:
            self.name+="E"
        else:
            print "error: too many rows"
        self.name+=str(_row+1)
        self.row=_row
        self.col=_col