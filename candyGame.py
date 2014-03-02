import sys
import json
import itertools
from copy import deepcopy

opponent = {"blue" : "green", "green" : "blue"}
depthCap = 2
class CandyGame:
#         state0 = {
#                 'finished' : finished,
#                 'vacantCount' : vacantCount,
#                 'N' : n, 
#                 'lastX' : x,
#                 'lastY' : y,
#                 'player' : opponent[player],
#                 'blueScore' : blueScore,                
#                 'blueScore': greenScore,
#                 'board' : board
#         }
    def __init__(self, blue, green, size):    
        self.playerBlue = blue
        self.playerGreen = green
        self.size = size

    def setBoard(self, board):
        n = self.size
        gameBoard = [[[board[x][y], 'V'] for y in xrange(n)] for x in xrange(n)]
        self.board = gameBoard
        print gameBoard

    def run(self):
        print self.playerBlue, self.playerGreen
    
    def loadFromClient(self):
        
        state = {}
        n = int(sys.stdin.readline().strip())
        player = sys.stdin.readline().strip()
        vacantCount = 0
        state['N'] = n
        state['player'] = player
        
        px, py = [int(val) for val in sys.stdin.readline().split()]
        sys.stdin.readline()
        gameBoard = [[[0, 'V'] for y in xrange(n)] for x in xrange(n)]
        for i in xrange(n * n):
            x, y, val, status = [v for v in sys.stdin.readline().split()]
            x, y, val = int(x), int(y), int(val)
            if status == 'V':
                vacantCount += 1
            gameBoard[x][y][0] = val
            gameBoard[x][y][1] = status
        state['board'] = gameBoard
        state['vacantCount'] = vacantCount
        state['finished'] = False
        state['blueScore'] = 0
        state['greenScore'] = 0
        
#         print state
#         print '-' * 80
#         nextMoveSgest = self.miniMax(state, 0)
#         print '-' * 80
#         print nextMoveSgest
#         print '-' * 80
        
        nextState = self.drop(px, py, state)
#         robotMoveX, robotMoveY, robotExpScore = self.miniMax(nextState, 0)
        robotMoveX, robotMoveY, alphaBeta = self.alphaBeta(nextState, -100 * n * n, 100 * n * n, 0)
        #print alphaBeta 
        nextState = self.drop(robotMoveX, robotMoveY, nextState)
        jsonInfo = json.dumps(nextState)
        sys.stdout.write(jsonInfo)
    
    def miniMax(self, posInfo, depth):
        if (depth >= depthCap or posInfo['vacantCount'] == 0):
            hVal = posInfo['blueScore'] - posInfo['greenScore']
            return posInfo['lastX'], posInfo['lastY'], hVal
        bestActionSoFarX = 0 
        bestActionSoFarY = 0 
        exptScoreDiff = 0
        n = len(posInfo['board'])
        
        player = posInfo['player']
        if posInfo['player'] == 'blue':
            exptScoreDiff = -100 * n * n
        else: # green min
            exptScoreDiff = 100 * n * n
            
        for x in xrange(n):
            for y in xrange(n):
                if posInfo['board'][x][y][1] == 'V':
                    posInfoCopy =  deepcopy(posInfo)
                    planInfo = self.drop(x, y, posInfoCopy)
                    if player =='blue':
                        aX, aY, esd = self.miniMax(planInfo, depth + 1)
                        # print aX, aY, esd
                        if esd > exptScoreDiff:
                            bestActionSoFarX = x
                            bestActionSoFarY = y
                            exptScoreDiff = esd
                    elif player =='green':
                        aX, aY, esd = self.miniMax(planInfo, depth + 1)
                        if esd < exptScoreDiff:
                            bestActionSoFarX = x
                            bestActionSoFarY = y
                            exptScoreDiff = esd
                                  
        return bestActionSoFarX, bestActionSoFarY, exptScoreDiff
    
    def alphaBeta(self, posInfo, alpha, beta, depth):
        if (depth >= depthCap or posInfo['vacantCount'] == 0):
            # print (posInfo['blueScore'] - posInfo['greenScore'])
            hVal = posInfo['blueScore'] - posInfo['greenScore']
            return posInfo['lastX'], posInfo['lastY'],  hVal
        bestActionSoFarX = 0 
        bestActionSoFarY = 0 
        n = len(posInfo['board'])
        
        player = posInfo['player']
            
        for x, y in itertools.product(xrange(n), repeat=2):
            if posInfo['board'][x][y][1] == 'V':
                posInfoCopy =  deepcopy(posInfo)
                planInfo = self.drop(x, y, posInfoCopy)
                if player =='blue':
                    aX, aY, alphaBeta = self.alphaBeta(planInfo, alpha, beta, depth + 1)
                    alpha = max(alpha, alphaBeta)
                    if beta <= alpha:
                        break
                    elif alpha == alphaBeta:
                        bestActionSoFarX = x
                        bestActionSoFarY = y
                elif player =='green':
                    aX, aY, alphaBeta = self.alphaBeta(planInfo, alpha, beta, depth + 1)
                    beta = min(beta, alphaBeta)
                    if beta <= alpha:
                        break;
                    elif beta == alphaBeta:
                        bestActionSoFarX = x
                        bestActionSoFarY = y
        
        alphaBeta = alpha if (player =='blue') else beta

        return bestActionSoFarX, bestActionSoFarY, alphaBeta
    

    def stdDisplayBoard(self):
        n = self.size
        board = self.gameBoard
        for x in xrange(n):
            for y in xrange(n):
                print x, y, board[x][y][0],  board[x][y][1]
        
    def drop(self, x, y, gameState):
        player = gameState['player']
        board = gameState['board']
        n = len(board)
        if x < 0 or x >= n or y < 0 or y >= n:
            print "Invaid Position : Out of Boundary! "
            return

        if (board[x][y][1] != 'V'):
            print "Invaid Position : Occupied! "
            return

        if player == "blue":
            board[x][y][1] = 'B'    
            if (x + 1 < n and board[x+1][y][1] == 'B') or \
                (y + 1 < n and board[x][y+1][1] == 'B') or \
                (x >= 0 and board[x-1][y][1] == 'B') or \
                (y >= 0 and board[x][y-1][1] == 'B'):

                if (x + 1 < n and board[x+1][y][1] == 'G'):
                    board[x+1][y][1] = 'B'
                if (y + 1 < n and board[x][y+1][1] == 'G'):
                    board[x][y+1][1] = 'B'
                if (x >= 0 and board[x-1][y][1] == 'G'):
                    board[x-1][y][1] = 'B'
                if (y >= 0 and board[x][y-1][1] == 'G'):
                    board[x][y-1][1] = 'B'

        elif player == "green":
            board[x][y][1] = 'G'    
            if (x + 1 < n and board[x+1][y][1] == 'G') or \
                (y + 1 < n and board[x][y+1][1] == 'G') or \
                (x >= 0 and board[x-1][y][1] == 'G') or \
                (y >= 0 and board[x][y-1][1] == 'G'):

                if (x + 1 < n and board[x+1][y][1] == 'B'):
                    board[x+1][y][1] = 'G'
                if (y + 1 < n and board[x][y+1][1] == 'B'):
                    board[x][y+1][1] = 'G'
                if (x >= 0 and board[x-1][y][1] == 'B'):
                    board[x-1][y][1] = 'G'
                if (y >= 0 and board[x][y-1][1] == 'B'):
                    board[x][y-1][1] = 'G'
        
        blueScore = 0
        greenScore = 0
        vacantCount = 0
        for row in board:
            for cell in row:
                if (cell[1] == 'B'):
                    blueScore += cell[0]
                elif (cell[1] == 'G'):
                    greenScore += cell[0]
                elif (cell[1] == 'V'):
                    vacantCount += 1
                else:
                    print "Invalid Marker !"
        finished = (vacantCount == 0)
                
        nextState = {
                'finished' : finished,
                'vacantCount' : vacantCount,
                'N' : n, 
                'lastX' : x,
                'lastY' : y,
                'player' : opponent[player],
                'blueScore' : blueScore,                
                'greenScore': greenScore,
                'board' : board
        }
        
        return nextState


if __name__=="__main__":
    candyGame = CandyGame("human", "human", 6)
    rawBoard = [
        [66, 76, 28, 66, 11, 9],
        [31, 39, 50, 8, 33, 14],
        [80, 76, 39, 59, 2, 48],
        [50, 73, 43, 3, 13, 3],
        [99, 73, 43, 3, 13, 3],
        [80, 63, 92, 28, 61, 53] 

    ]
    candyGame.loadFromClient()
