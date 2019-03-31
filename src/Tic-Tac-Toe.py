from random import *
import time


# how to improve
# make minmax add values for each win/loss

def main():
    def display(arr):
        print()
        print(arr[0] + "|" + arr[1] + "|" + arr[2] + "   " + "1|2|3")
        print("-----" + "   " + "-----")
        print(arr[3] + "|" + arr[4] + "|" + arr[5] + "   " + "4|5|6")
        print("-----" + "   " + "-----")
        print(arr[6] + "|" + arr[7] + "|" + arr[8] + "   " + "7|8|9")
        print()

    def setup(arr):
        for i in range(0, 9):
            arr.append(" ")

    def move(arr, turn):
        print("choose a square (1 to 9): ")
        square = input()
        square = int(square) - 1
        if square < 0 or square > 8 or arr[square] != ' ':
            print('Illegal move!')
            return move(arr, turn)
        if turn % 2 == 0:
            pieceType = "X"
        else:
            pieceType = "O"
        arr[square] = pieceType

    # right now only diagonal tests work
    def checkWinner(arr):
        winner = ""
        allFilled = True
        # vertical Tic-Tac-Toe
        for i in range(0, 3):
            if arr[i] != " ":  # 0, 1, 2
                if arr[i] == arr[3 + i] and arr[i] == arr[2 * 3 + i]:
                    winner = arr[i]
        # horizontal Tic-Tac-Toe
        for i in range(0, 3):
            if arr[3 * i] != " ":  # 0, 3, 6
                if arr[3 * i] == arr[3 * i + 1] and arr[3 * i] == arr[3 * i + 2]:
                    winner = arr[3 * i]
        # diagonal Tic-Tac-Toe
        if arr[0] != " ":
            if arr[0] == arr[4] and arr[0] == arr[8]:
                winner = arr[0]
        if arr[2] != " ":
            if arr[2] == arr[4] and arr[2] == arr[6]:
                winner = arr[2]
        # no winner
        if winner == "":
            for i in range(0, 9):
                if arr[i] == " ":
                    allFilled = False
            if allFilled:
                winner = "none"
        return winner

    def selectDifficulty():
        choice = input('Choose a difficulty level (1 for easy, 2 for medium, 3 for hard): ')
        if choice == '3':
            return 'hard'
        elif choice == '2':
            return 'medium'
        else:
            return 'easy'

    # return the board after a computer opponent makes a move
    def cpuMove(arr, difficulty):
        if difficulty == 'easy':
            locationsLeft = []
            turn = getTurn(arr)
            if turn == 'X':
                turn = 0
            else:
                turn = 1

            for i in range(0, 9):
                if arr[i] == " ":
                    locationsLeft.append(i)
            location = sample(locationsLeft, 1)
            if turn % 2 == 0:
                pieceType = "X"
            else:
                pieceType = "O"
            arr[location[0]] = pieceType
            return arr

        if difficulty == 'medium':  # 50% chance to make hard move, 50% chance to make easy move
            randomChoice = randint(0, 1)
            if randomChoice == 0:
                return cpuMove(arr, 'easy')
            else:
                return cpuMove(arr, 'hard')

        if difficulty == 'hard':
            # store the 1st move (it takes the longest)
            if isBlankBoard(arr):
                return ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

            arr = getBestMove(arr)
            return arr

    def isBlankBoard(arr):
        isBlank = True
        for i in arr:
            if i != ' ':
                isBlank = False
        return isBlank

    # choose if you want to play a human
    def getOpponent():
        print("Select opponent (type h for human, c for computer): ")
        opponent = input()
        if opponent == "c" or opponent == "h":
            return opponent
        return getOpponent()

    # runs a game of tic tac toe
    def run():
        board = []
        turn = 0
        winner = ""
        opponent = getOpponent()

        r = randint(0, 1)  # random number to see who goes 1st

        setup(board)
        if opponent == "c":
            difficulty = selectDifficulty()
            while (winner == ""):
                if turn % 2 == r:
                    display(board)
                    move(board, turn)
                else:
                    startTime = time.time()  # check time
                    board = cpuMove(board, difficulty)
                    print('Thinking time: ' + str(time.time() - startTime))  # check time
                winner = checkWinner(board)
                turn += 1
        else:
            while (winner == ""):
                display(board)
                move(board, turn)
                winner = checkWinner(board)
                turn += 1
        display(board)
        print("Winner is " + winner)
        print("Play again (y/n): ")
        again = input()
        if again == "y":
            run()

    # Trying to create a simple AI opponent

    # use minimax on all possible moves. if turn == 'X', get max, if turn == 'o' get min
    def getBestMove(arr):
        turn = getTurn(arr)

        if (turn == 'X'):
            playerX = True
        else:
            playerX = False

        bestBoard = []

        for i in possibleBoards(arr):
            value = minimax(i, 9,
                            not playerX)  # set to 'not playerX' because possibleBoards gives moves for the next player

            # Note: hardcoded the 1st move to be the top left square.
            # This can be removed, but will lead to more thinking time.
            if len(bestBoard) == 0:  # this is the 1st time through the loop
                bestBoard = i
                bestBoardValue = value
            if playerX:  # looking for max
                if value > bestBoardValue:
                    bestBoard = i
                    bestBoardValue = value
            else:  # looking for min
                if value < bestBoardValue:
                    bestBoard = i
                    bestBoardValue = value

        return bestBoard

    # return True if the game is over (winner equals 'none' or 'X' or 'O'
    def isWinner(arr):
        if checkWinner(arr) != '':
            return True
        return False

    # return 0 for tie, 1 for X win, and -1 for O win
    def valueOfBoard(arr):
        winner = checkWinner(arr)
        if winner == 'X':
            return 1
        if winner == 'O':
            return -1
        return 0

    # return the boards of all possible next moves
    def possibleBoards(arr):
        boards = []
        if isWinner(arr):
            return boards
        turn = getTurn(arr)
        for i in range(0, len(arr)):
            if arr[i] == ' ':
                tempBoard = copyBoard(arr)
                tempBoard[i] = turn
                boards.append(tempBoard)
        return boards

    def getTurn(arr):
        count = 0
        for i in arr:
            if i == 'X':
                count += 1
            if i == 'O':
                count += -1
        if count == 1:
            return 'O'
        return 'X'

    def copyBoard(arr):
        newBoard = []
        for i in arr:
            newBoard.append(i)
        return newBoard

    # return the value of the current board
    def minimax(arr, depth, playerX):
        count = 0  # keep track of how many times a win was found

        if depth == 0 or isWinner(arr):  # if the game is over
            return valueOfBoard(arr)
        if playerX:  # look for moves that have value 1
            maximum = -100
            for i in possibleBoards(arr):
                value = minimax(i, depth - 1, False)
                if value > maximum:
                    maximum = value
                    # count = 0
                # if value == maximum:
                # count += 1
            return maximum  # + .001*count
        else:  # look for moves that lead to value of -1
            minimum = 100
            for i in possibleBoards(arr):
                value = minimax(i, depth - 1, True)
                if value < minimum:
                    minimum = value
                    # count = 0
                # if value == minimum:
                # count += 1
            return minimum  # - .001*count

    run()


main()
