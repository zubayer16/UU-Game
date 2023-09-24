import random
import time


def placePiece(board, coord, piece):
    # coord = tuple like [2,3]
    board[coord[0]][coord[1]] = piece
    return board


def removePiece(board, piece):
    updateBoard(board)
    removeCoord = str(input("Please input piece to remove"))
    removeCoord = removeCoord.split(',')
    removeCoord[0] = int(removeCoord[0])
    removeCoord[1] = int(removeCoord[1])
    if board[removeCoord[0]][removeCoord[1]] == piece:
        board[removeCoord[0]][removeCoord[1]] = '.'
        return board
    else:
        removePiece(board, piece)


def updateBoard(board):
    print(' ', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    rownr = 0
    for row in board:
        print(rownr, row)
        rownr += 1


def inputCoord(board, playerPiece, opponentPiece):
    coord = str(input("Please input coordinates for placement in format rownr,columnnr: "))
    coord = coord.split(',')
    coord[0] = int(coord[0])
    coord[1] = int(coord[1])
    # print(coord)

    if board[coord[0]][coord[1]] != playerPiece and board[coord[0]][coord[1]] != opponentPiece:
        print('piece placed at', coord)
        return coord
    else:
        print("Place occupied, input again")
        return inputCoord(board, playerPiece, opponentPiece)


def aiGenerateCoord(board, playerPiece, opponentPiece):
    print('AI is attempting to make move!')
    time.sleep(0.5)
    xcoord = random.randint(0, 9)
    ycoord = random.randint(0, 9)
    if board[ycoord][xcoord] != playerPiece and board[ycoord][xcoord] != opponentPiece:
        print('AI places a piece at: ', [ycoord, xcoord])
        return [ycoord, xcoord]
    else:
        return aiGenerateCoord(board, playerPiece, opponentPiece)


def aiGenerateMove(board, playerPiece, opponentPiece):
    coord = aiGenerateCoord(board, playerPiece, opponentPiece)
    board = placePiece(board, coord, opponentPiece)
    return board


def aiRemovePiece(board, playerPiece):
    available = []
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if board[i][j] == playerPiece:
                available.append([i, j])
    index = random.randint(0, len(available) - 1)
    # print(type(available))
    # print(available)
    board[available[index][0]][available[index][1]] = '.'
    removedPiece = [available[index][0], available[index][1]]
    print('AI removes piece at :', removedPiece)
    return board


def playerMillChecker(board, playerPiece, opponentPiece):
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if board[i][j] == playerPiece and board[i + 1][j] == playerPiece and board[i + 2][j] == playerPiece:
                board = removePiece(board, opponentPiece)
            if board[i][j] == playerPiece and board[i][j + 1] == playerPiece and board[i][j + 2] == playerPiece:
                board = removePiece(board, opponentPiece)
    return board


def opponentMillChecker(board, playerPiece, opponentPiece):
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if board[i][j] == opponentPiece and board[i + 1][j] == opponentPiece and board[i + 2][j] == opponentPiece:
                board = aiRemovePiece(board, playerPiece)
            if board[i][j] == opponentPiece and board[i][j + 1] == opponentPiece and board[i][j + 2] == opponentPiece:
                board = aiRemovePiece(board, playerPiece)


def gameLoop(rounds, board, playerPiece, opponentPiece):
    updateBoard(board)
    coord = inputCoord(board, playerPiece, opponentPiece)
    board = placePiece(board, coord, playerPiece)
    playerMillChecker(board, playerPiece, opponentPiece)
    board = aiGenerateMove(board, playerPiece, opponentPiece)
    opponentMillChecker(board, playerPiece, opponentPiece)

    rounds += 1
    if rounds < 10:
        gameLoop(rounds, board, playerPiece, opponentPiece)
    else:
        print("Game Ended!")


playerPiece = 'X'
opponentPiece = 'O'
playerPieces = 12
opponentPieces = 12
board = [['.', '.', '.', '.', '.', '.', '.', 'O', 'O', 'O'], ['.', '.', 'X', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', 'X', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', 'X', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
rounds = 0
gameLoop(rounds, board, playerPiece, opponentPiece)