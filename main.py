import random
import time


# Removes a piece, right now you are able to remove from a mill even if the opponent is not in phase 3, this should only be doable if the opponent is in phase 3
def removePiece(board, piece, mill_list, phase):
    """
    Lets the user remove one of the ai's pieces

    @param board: The current board
    @param piece: The symbol representing the ai
    @param mill_list the current active mills of the ai
    @param phase: The current phase of the player
    @return: The updated board with the ai piece removed


    """
    print()
    updateBoard(board)
    removeCoord = str(input("Please input piece to remove: "))
    removeCoord = removeCoord.split(',')
    removeCoord[0] = int(removeCoord[0])
    removeCoord[1] = int(removeCoord[1])
    # Only in phase 3 it is allowed to remove a piece from a active mill

    if (phase == 3):
        if board[removeCoord[0]][removeCoord[1]] == piece:
            board[removeCoord[0]][removeCoord[1]] = '.'
            print(f"The piece at{removeCoord} is removed\n")
            return board
        else:
            return removePiece(board, piece, mill_list, phase)

    if board[removeCoord[0]][removeCoord[1]] == piece and (removeCoord[0], removeCoord[1]) not in mill_list:
        board[removeCoord[0]][removeCoord[1]] = '.'
        print(f"The piece at{removeCoord} is removed\n")
        return board
    else:
        return removePiece(board, piece, mill_list, phase)


# verify the move for phase 1
def veryifyMovep1(board, coord):
    """
    Verifies the proposed move by the player during phase 1

    @param board: The current board
    @param coord: the proposed placement of a piece
    @return: True if the placement is allowed by the rules of the game false otherwise


    """

    row, col = coord

    # Check if the coordinate is within the bounds of the board
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        # Check if the coordinate is empty ('.')
        if board[row][col] == '.':
            return True
        print("Please place a piece on a available spot")
        return False

    print("Please only place pieces on the board")
    return False


# verify the move for phase 2 and 3
def verifyMovePiece(board, playerPiece, chosenPieceCoord, moveCoord, phase):
    """
    Verifies the proposed move by the player during phase 2 & 3

    @param board: The current board
    @param playerPiece: the symbol representing the player
    @param choosenPieceCoord: The coordinates of the piece the player wants to move
    @param moveCoord: The coordinates of the move the player wants to perform
    @param phase: The current phase of the player
    @return: True if the move is allowed by the rules of the game false otherwise


    """
    # Check if the chosen piece coordinate is within boundss
    if not (0 <= chosenPieceCoord[0] < len(board) and 0 <= chosenPieceCoord[1] < len(board[0])):
        print("Invalid chosen piece coordinate. Please select a valid piece to move.")
        return False

    # Check if the chosen piece belongs to the current player
    if board[chosenPieceCoord[0]][chosenPieceCoord[1]] != playerPiece:
        print("You can only move your own pieces. Please select a valid piece to move.")
        return False

    # Check if the move coordinate is within bounds
    if not (0 <= moveCoord[0] < len(board) and 0 <= moveCoord[1] < len(board[0])):
        print("Invalid move coordinate. Please select a valid adjacent spot to move the piece.")
        return False

    # Check if the move coordinate is empty ('.')
    if board[moveCoord[0]][moveCoord[1]] != '.':
        print("The chosen move coordinate is not empty. Please select an available spot.")
        return False

    if (phase == 2):
        # Check if the move coordinate is adjacent to the chosen piece coordinate
        if abs(moveCoord[0] - chosenPieceCoord[0]) + abs(moveCoord[1] - chosenPieceCoord[1]) != 1:
            print("You can only move the piece to an adjacent spot (one coordinate away).")
            return False
    return True


# Verifies all moves in all phases
def verifyMove(phase, board, Playerpiece):
    """
    Verifies the proposed move by the player
    @param phase: the current phase of the player
    @param board: The current board
    @param Playerpiece: the symbol representing the player
    @return: The verified move coordinates


    """
    validMove = False
    coord = 0
    while not validMove:
        if (phase == 1):
            coord = verifyFormat("Please input coordinates for placement in format rownr,columnnr: ")
            validMove = veryifyMovep1(board, coord)
        if (phase == 2):
            coord = verifyFormat2()
            validMove = verifyMovePiece(board, Playerpiece, coord[0], coord[1], phase)
        if (phase == 3):
            coord = verifyFormat2()
            validMove = verifyMovePiece(board, Playerpiece, coord[0], coord[1], phase)

    return coord


# Updates the board
def updateBoard(board):
    print(' ', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    rownr = 0
    for row in board:
        print(rownr, row)
        rownr += 1


# Takes in one coordinate and checks if it's in the right format
def verifyFormat(Question):
    while True:
        coord_input = input(Question)
        coord = coord_input.split(',')
        if len(coord) != 2:
            print("Invalid input format. Please use the format rownr,columnnr (e.g., 2,3).")
            continue
        try:
            row = int(coord[0])
            col = int(coord[1])
        except ValueError:
            print("Invalid input. Please enter integers for row and column numbers.")
            continue
        return [row, col]


# Takes in two different coordinates, used for phase 2 and 3 which needs 2 sets of coordinates
def verifyFormat2():
    piece = verifyFormat("Please input coordinates for the chosen piece to move in format rownr,columnnr: ")
    move = verifyFormat("Please input coordinates for placement in format rownr,columnnr: ")
    return piece, move


# Moves or places a piece depending on the phase
def doMove(board, move, piece, phase):
    # playermove is (x,y) if the phase is 1 otherwise (piece,move)
    if (phase == 1):
        board[move[0]][move[1]] = piece  # In phase 1 we just need to place a piece on the coordinate
        return board

    chosenPieceCoord = move[0]
    moveCoord = move[1]

    board[moveCoord[0]][moveCoord[1]] = piece
    board[chosenPieceCoord[0]][chosenPieceCoord[1]] = '.'
    return board


########################## AI CODE
def aiRemovePiece(board, playerPiece, mills_list, phase):
    """
    Removes a random available piece from the player

    @param board: The current board
    @param playerPiece: The symbol representing the player
    @param mills_list: all of the active player mills
    @param phase: the current phase of the player
    @return: The updated board with the a player piece removed


    """
    available = []
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if board[i][j] == playerPiece and (i, j):
                available.append([i, j])  # Finds all the playerpieces on the board
    # The ai should be able to remove pieces in a active mill if the player is in phase 3 only
    if phase != 3:
        for piece_coord in available.copy():
            if piece_coord in mills_list:
                available.remove(piece_coord)

    if available:
        index = random.randint(0, len(available) - 1)
        board[available[index][0]][available[index][1]] = '.'
        print(f"the AI removes the piece at {[available[index][0], available[index][1]]} ")

    return board


def aiSmartMoveP3(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills):
    """
    Tries to find a move during phase 3 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.

    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param playerPiece: The symbol representing the player
    @param aiMills: the current mills created by the AI
    @param prevPrevAIMills the AI mills from two rounds back
    @param playerMills: The current player mills
    @param prevPrevPlayerMills: the player mills from two rounds back
    @return: The updated board with the resulting AI move

    """

    ai_Pieces = []
    empty_spots = []

    # Find all  Ai's pieces and empty spots
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == aiPiece:
                ai_Pieces.append((i, j))
            elif board[i][j] == '.':
                empty_spots.append((i, j))

    # Check if we can complete a mill in the next move
    for piece in ai_Pieces:
        for spot in empty_spots:
            temp_board = [row[:] for row in board]  # Create a copy of the board
            temp_board[piece[0]][piece[1]] = '.'  # Move the piece
            temp_board[spot[0]][spot[1]] = aiPiece
            if checkNewMill(temp_board, aiPiece, AIMills, prevPrevAIMills):
                move = (piece, spot)
                board = doMove(board, move, aiPiece, phase=3)
                print(f"AI moves a piece from {[piece[0], piece[1]]} to {[spot[0], spot[1]]}")

                return board

    # Check if we need to block the opponent from completing a mill
    for spot in empty_spots:
        for piece in ai_Pieces:
            temp_board = [row[:] for row in board]  # Create a copy of the board
            temp_board[piece[0]][piece[1]] = '.'  # Move the piece
            temp_board[spot[0]][spot[1]] = playerPiece
            if checkNewMill(temp_board, playerPiece, playerMills, prevPrevPlayerMills):
                move = (piece, spot)
                board = doMove(board, move, aiPiece, phase=3)
                print(f"AI moves a piece from {[piece[0], piece[1]]} to {[spot[0], spot[1]]}")
                return board
    board = aiRandomMove(board, aiPiece, 3)  # If no good moves found just use a random move
    return board


def aiSmartMoveP2(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills):
    """
    Tries to find a move during phase 2 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.

    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param playerPiece: The symbol representing the player
    @param aiMills: the current mills created by the AI
    @param prevPrevAIMills the AI mills from two rounds back
    @param playerMills: The current player mills
    @param prevPrevPlayerMills: the player mills from two rounds back
    @return: The updated board with the resulting AI move.


    """

    ai_Pieces = []
    empty_spots = []

    # Find all AI's pieces and empty spots
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == aiPiece:
                ai_Pieces.append((i, j))
            elif board[i][j] == '.':
                empty_spots.append((i, j))

    # Check if we can complete a mill in the next move
    for piece in ai_Pieces:
        for spot in empty_spots:
            # Check if the move coordinate is adjacent to the chosen piece coordinate
            if abs(spot[0] - piece[0]) + abs(spot[1] - piece[1]) == 1:
                temp_board = [row[:] for row in board]  # Create a copy of the board
                temp_board[piece[0]][piece[1]] = '.'  # Move the piece
                temp_board[spot[0]][spot[1]] = aiPiece
                if checkNewMill(temp_board, aiPiece, AIMills, prevPrevAIMills):
                    move = (piece, spot)
                    board = doMove(board, move, aiPiece, phase=2)
                    print(f"AI moves a piece from {[piece[0], piece[1]]} to {[spot[0], spot[1]]}")
                    return board

    # Check if we need to block the opponent from completing a mill
    for spot in empty_spots:
        for piece in ai_Pieces:
            # Check if the move coordinate is adjacent to the chosen piece coordinate
            if abs(spot[0] - piece[0]) + abs(spot[1] - piece[1]) == 1:
                temp_board = [row[:] for row in board]  # Create a copy of the board
                temp_board[piece[0]][piece[1]] = '.'  # Move the piece
                temp_board[spot[0]][spot[1]] = playerPiece
                if checkNewMill(temp_board, playerPiece, playerMills, prevPrevPlayerMills):
                    move = (piece, spot)
                    board = doMove(board, move, aiPiece, phase=2)
                    print(f"AI moves a piece from {[piece[0], piece[1]]} to {[spot[0], spot[1]]}")
                    return board

    # If no good moves found, just use a random move
    return aiRandomMove(board, aiPiece, 2)


def aiSmartMoveP1(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills):
    """
    Tries to find a move during phase 1 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.
    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param playerPiece: The symbol representing the player
    @param aiMills: the current mills created by the AI
    @param prevPrevAIMills the AI mills from two rounds back
    @param playerMills: The current player mills
    @param prevPrevPlayerMills: the player mills from two rounds back
    @return: The updated board with the resulting AI move.


    """

    empty_spots = []

    # Find all empty spots on the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '.':
                empty_spots.append((i, j))

    # Check if placing a piece in an empty spot completes a mill
    for spot in empty_spots:
        temp_board = [row[:] for row in board]  # Create a copy of the board
        temp_board[spot[0]][spot[1]] = aiPiece
        if checkNewMill(temp_board, aiPiece, AIMills, prevPrevAIMills):
            board[spot[0]][spot[1]] = aiPiece
            print(f"AI places a piece at {[spot[0], spot[1]]}")
            return board

    # Check if the ai can block the player from creating a mill
    for spot in empty_spots:
        temp_board = [row[:] for row in board]  # Create a copy of the board
        temp_board[spot[0]][spot[1]] = playerPiece
        if checkNewMill(temp_board, playerPiece, playerMills, prevPrevPlayerMills):
            board[spot[0]][spot[1]] = aiPiece
            print(f"AI places a piece at {[spot[0], spot[1]]}")
            return board
    # If no good moves found, just use a random move
    board = aiRandomMove(board, aiPiece, 1)
    return board


# Dummy function, needs to be implemented with aleast some calculation on how the ai should act
def generateSmartMove(board, aiPiece, playerPiece, phase, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills):
    """
    Creates a calculated move by the AI depending on the current phase of the AI.
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @param playerPiece: The symbol representing the player
    @param phase: the current phase of AI
    @param aiMills: the current mills created by the AI
    @param prevPrevAIMills the AI mills from two rounds back
    @param playerMills: The current player mills
    @param prevPrevPlayerMills: the player mills from two rounds back
    @return: The updated board with the resulting AI move.


    """

    if (phase == 1):
        board = aiSmartMoveP1(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills)

    if (phase == 2):
        board = aiSmartMoveP2(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills)

    if (phase == 3):
        board = aiSmartMoveP3(board, aiPiece, playerPiece, AIMills, prevPrevAIMills, playerMills, prevPrevPlayerMills)

    return board


def aiRandomMoveP1(board, aiPiece):
    """
    Creates a random move for the AI during phase 1
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @return: The updated board with the resulting AI move.


    """
    xcoord = random.randint(0, 9)
    ycoord = random.randint(0, 9)
    if board[xcoord][ycoord] == '.':
        print('AI places a piece at: ', [xcoord, ycoord])
        board[xcoord][ycoord] = aiPiece
        return board
    else:
        return aiRandomMoveP1(board, aiPiece)


# Returns the right direction
def getMoveCoord(coord, direction):
    """
    Helper function for aiRandomMoveP2. translatees direction into change of coordinates.
    @param coord: The coordinate of a piece
    @param direciton: a direction the piece can go.
    @return: The updated coordinate of the piece depending on the given direction.


    """
    row, col = coord
    if direction == "up":
        return (row - 1, col)
    elif direction == "down":
        return (row + 1, col)
    elif direction == "left":
        return (row, col - 1)
    elif direction == "right":
        return (row, col + 1)
    else:
        raise ValueError("Invalid direction")


# Choose a random piece and a random movement, used for phase 2
def aiRandomMoveP2(board, aiPiece):
    """
    Creates a random move for the AI during phase 2
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @return: The updated board with the resulting AI move.


    """

    available_pieces = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == aiPiece:
                available_pieces.append([i, j])
    # Find all the ai pieces

    if available_pieces:
        piece_to_move = random.choice(available_pieces)
        possible_moves = []
        for direction in ["up", "down", "left", "right"]:
            move_coord = getMoveCoord(piece_to_move, direction)
            if (
                    0 <= move_coord[0] < len(board)
                    and 0 <= move_coord[1] < len(board[0])
                    and board[move_coord[0]][move_coord[1]] == "."
            ):
                possible_moves.append(move_coord)
        # Calculates all possible moves for an piece

        if possible_moves:
            move_coord = random.choice(possible_moves)
            move = (piece_to_move, move_coord)
            board = doMove(board, move, aiPiece, phase=2)
            print(f"AI moves a piece from {[piece_to_move[0], piece_to_move[1]]} to {[move_coord[0], move_coord[1]]}")
    # Perform a random move out of the possible moves
    return board


# Chooses a random piece and moves it randomly, used for phase 3 random
def aiRandomMoveP3(board, aiPiece):
    """
    Creates a random move for the AI during phase 3
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @return: The updated board with the resulting AI move.


    """

    available_pieces = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == aiPiece:
                available_pieces.append([i, j])
    piece = random.choice(available_pieces)  # Choosese a random piece
    while True:
        xcoord = random.randint(0, 9)
        ycoord = random.randint(0, 9)
        if board[ycoord][xcoord] == '.':
            move = (piece, (xcoord, ycoord))
            board = doMove(board, move, aiPiece, phase=3)
            print(f"AI moves a piece from {[piece[0], piece[1]]} to {[xcoord, ycoord]}")
            return board


# Handle all random movements needed for all phases
def aiRandomMove(board, aiPiece, aiPhase):
    """
    Makes the ai perform a random move for the right phase
    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param aiPhase: The current phase of the AI
    @return: The updated board with the resulting AI move.


    """
    if (aiPhase == 1):
        move = aiRandomMoveP1(board, aiPiece)
    if (aiPhase == 2):
        move = aiRandomMoveP2(board, aiPiece)
    if (aiPhase == 3):
        move = aiRandomMoveP3(board, aiPiece)
    return move


# Checks the difficulity of the AI. Easy AI always uses random moves, medium ai uses 1/4 calculated moves rest random, hard uses 1/2 calculated and rest random.
def aiMove(board, playerpiece, aiPiece, aiPhase, difficulty, rounds, AIMills, prevPrevAIMills, playerMills,
           prevPrevPlayerMills):
    """
    Makes the ai perform a move depending on the difficulity. Easy will always perform random moves meanwhile medium uses 1/4 smart moves and hard 1/2 smart moves, the rest are random.
    @param board: The current board
    @param playerpiece: The symbol representing the player
    @param aiPiece: The symbol representing the AI
    @param aiPhase: The current phase of the AI
    @param difficulity: the chosen difficulity of the AI
    @param rounds: The current round of the game
    @param aiMills: the current mills created by the AI
    @param prevPrevAIMills the AI mills from two rounds back
    @param playerMills: The current player mills
    @param prevPrevPlayerMills: the player mills from two rounds back
    @return: The updated board with the resulting AI move.


    """
    newBoard = 0
    if (difficulty == 2):
        if (rounds % 4 == 0):
            newBoard = generateSmartMove(board, aiPiece, playerpiece, aiPhase, AIMills, prevPrevAIMills, playerMills,
                                         prevPrevPlayerMills)
            return newBoard
    if (difficulty == 3):
        if (rounds % 2 == 0):
            newBoard = generateSmartMove(board, aiPiece, playerpiece, aiPhase, AIMills, prevPrevAIMills, playerMills,
                                         prevPrevPlayerMills)
            return newBoard
    newBoard = aiRandomMove(board, aiPiece, aiPhase)  # Easy always uses random moves
    return newBoard


###################### AI CODE


# Just checks if one only has two pieces left
def checkWinner(board, piece):
    count = 0
    for row in board:
        count += row.count(piece)
    if count < 3:
        return True
    return False


# Returns 0 for draw, 1 for player and 2 for ai
def gameLoop(board, playerPiece, opponentPiece, difficulty):
    """

    Plays a game of UUgame until a result is made
    @param rounds: The current round of the game
    @param board: The current board
    @param playerpiece: The symbol representing the player
    @param opponentPiece: The symbol representing the opponnent, human or AI
    @param difficulity: the chosen difficulity of the AI
    @return: 0 if a draw is made, 1 if the player wins, 2 if the AI wins


    """
    rounds = 0
    aiPhase = 1
    playerPhase = 1
    piecestoPlace = 12  # Pieces the player can place in phase 1
    aiPiecestoplace = 12  # Pieces the AI can place in phase 1
    pieceCount = 9  # How many pieces needed to be removed from player so that they enter phase 3
    aipieceCount = 9  # How many pieces needed to be removed from the AI so that they enter phase 3
    # Setup the game state

    playerMills = []
    prevPlayerMills = []  # The players mill two turns ago, used to make sure that the same mill can not be made in consecutive turns
    prevPrevPlayerMills = []  # The players mills one turn ago

    aiMills = []
    prevAIMills = []  # The AI mills two turns ago, used to make sure that the same mill can not be made in consecutive turns
    prevPrevAIMills = []  # The AI mills one turn ago

    while (rounds < 200):
        updateBoard(board)
        rounds = rounds + 1
        prevPrevPlayerMills = prevPlayerMills.copy()
        prevPlayerMills = playerMills.copy()
        playerMove = verifyMove(playerPhase, board, playerPiece)
        board = doMove(board, playerMove, playerPiece, playerPhase)
        playerMills = checkDestroyedMills(board, playerPiece,
                                          playerMills)  # Check if any mills have been broken by a move
        piecestoPlace = piecestoPlace - 1

        # player enters phase 2
        if piecestoPlace <= 0 and pieceCount > 1:
            playerPhase = 2
        # player enters phase 3
        elif piecestoPlace <= 0 and pieceCount < 1:
            playerPhase = 3

        new_mill = checkNewMill(board, playerPiece, playerMills, prevPrevPlayerMills)

        if new_mill:
            playerMills = updateMillList(board, playerPiece, playerMills, prevPrevPlayerMills)

            removePiece(board, opponentPiece, aiMills, playerPhase)
            aipieceCount = aipieceCount - 1
            if not (aiPhase == 1):
                # Checks to see if after removing the piece that ai only has 2 left
                if (checkWinner(board, opponentPiece)):
                    return 1

        # AI opponent's turn
        time.sleep(1)  # Simulate AI thinking time
        prevPrevAIMills = prevAIMills.copy()
        prevAIMills = aiMills.copy()

        board = aiMove(board, playerPiece, opponentPiece, aiPhase, difficulty, rounds, aiMills, prevPrevAIMills,
                       playerMills, prevPrevPlayerMills)
        aiPiecestoplace = aiPiecestoplace - 1
        # ai enters phase 2
        if aiPiecestoplace <= 0 and aipieceCount > 1:
            aiPhase = 2
        # ai enters phase 3
        elif aiPiecestoplace <= 0 and aipieceCount < 1:
            aiPhase = 3
        new_mill = checkNewMill(board, opponentPiece, aiMills, prevPrevAIMills)
        # Check if the AI opponent has formed a new three-in-a-row
        if new_mill:
            aiMills = updateMillList(board, opponentPiece, aiMills)
            aiRemovePiece(board, playerPiece, playerMills, playerPhase)
            pieceCount = pieceCount - 1
            if not (playerPhase == 1):
                if (checkWinner(board, playerPiece)):
                    return 2

    return 0  # The game took too many turns and ended in a draw


def findMills(board, piece):
    """

    Finds all possible mills on the board
    @param board: The current board
    @param piece: the symbol to check for mills
    @return: A list of all the possible mills


    """
    mills = []

    # Check for horizontal mills
    for i in range(10):
        for j in range(8):
            if all(board[i][j + k] == piece for k in range(3)):
                mills.append([[i, j], [i, j + 1], [i, j + 2]])

    # Check for vertical mills
    for i in range(8):
        for j in range(10):
            if all(board[i + k][j] == piece for k in range(3)):
                mills.append([[i, j], [i + 1, j], [i + 2, j]])

    return mills


def addMillToList(mills_list, new_mill):
    """

    Adds a mill to the mill as long none of the coordinates are already in the list
    @param mills_list: All of the current mills
    @param new_mill: a mill
    @return: The mill list with a new mill list added if it's new


    """
    # Check if any of the coordinates of the new mill are already in the list
    for mill in mills_list:
        for coord in new_mill:
            if coord in mill:
                return mills_list  # If any coordinate is already in a mill, don't add it

    # If none of the coordinates are already in a mill, add the new mill to the list
    mills_list.append(new_mill)
    return mills_list


def updateMillList(board, piece, mill_list, prev_mill_list):
    """

    Adds a mill to the mill as long none of the coordinates are already in the list
    @param board: the current board
    @param mills_list: All of the current mills
    @param piece: the symbol to check for mills
    @return: The mill list with a new mill list added if it's new


    """
    new_mills = findMills(board, piece)
    if new_mills:
        for mill in new_mills:
            if mill not in prev_mill_list:
                mill_list = addMillToList(mill_list, mill)

    return mill_list


def checkNewMill(board, piece, mill_list, prev_mill_list):
    """

    Checks if a new mill will be added to the list
    @param board: the current board
    @param piece: the symbol to check for mills
    @param mills_list: All of the current mills
    @return: True if a new mill will be added to the list, false otherwise


    """
    tem_list = mill_list.copy()
    tem_list = updateMillList(board, piece, tem_list, prev_mill_list)
    if (len(tem_list) > len(mill_list)):
        return True
    return False


def checkDestroyedMills(board, piece, mill_list):
    """

    Checks if any mills have been broken and updates the mill list accordingly
    @param board: the current board
    @param piece: the symbol to check for mills
    @param mills_list: All of the current mills
    @return: The mill list with curent mills


    """
    valid_mills = []  # Create a list to store valid mills

    for mill in mill_list:
        mill_valid = True  # Assume the mill is valid initially
        for coord in mill:
            row, col = coord
            if board[row][col] != piece:
                mill_valid = False  # If any coordinate doesn't have the same piece, the mill is not valid
                break

        if mill_valid:
            valid_mills.append(mill)  # If the mill is still valid, add it to the list of valid mills

    return valid_mills


# Add function that checks for deleted mills


def resultHandler(result):
    """

    Handles the result of the game accordingly and allow the player to play again
    @param result: Result of the game
    @return: The inputted choice of playing again or quitting by the player


    """
    if (result == 0):
        print("The game has ended in a draw")
    if (result == 1):
        print("Congratulations you won the game!")
    if (result == 2):
        print("The AI won the game, better luck next time")
    print("Do you want to play again? enter 'c' to play again or 'q' to quit")
    while (True):
        answer = input()
        if (answer == "q"):
            return answer
        if (answer == "c"):
            return answer
        print("Please input 'c' to play again or 'q' to quit")


# Gets the Difficulity and Piece from the player
def startGame():
    while True:
        difficulty = str(input("Please choose a difficulty for the ai. Easy (e) , Medium (m) or Hard(h) "))
        if (difficulty == "e"):
            difficulty = 1
            break
        if (difficulty == "m"):
            difficulty = 2
            break
        if (difficulty == "h"):
            difficulty = 3
            break
        print("Please input a valid difficulty")

    while True:
        choosenPiece = str(input("Please input 'X' or 'O' to choose that piece to play "))
        if (choosenPiece == "X"):
            aiPiece = "O"
            break
        if (choosenPiece == "O"):
            aiPiece = "X"
            break
        print("Please choose X or O for the piece to play")

    board = [['.' for _ in range(10)] for _ in range(10)]
    result = gameLoop(board, choosenPiece, aiPiece, difficulty)

    return result


# Just the start screen
def startScreen():
    print("Welcome to the UU-Game, please enter 's' to start the game, 'r' for the rules or 'q' to stop the game ")

    while True:
        choice = str(input())
        if (choice == "q"):
            break

        if (choice == "r"):
            print("Insert rules here")
            print(
                "Welcome to the UU-Game, please enter 's' to start the game, 'r' for the rules or 'q' to stop the game ")
            continue

        if (choice == "s"):
            result = startGame()
            answer = resultHandler(result)
            if (answer == "q"):
                break
            print(
                "Welcome to the UU-Game, please enter 's' to start the game, 'r' for the rules or 'q' to stop the game ")
            continue

        print("Please enter 'r', 'q' or 's' ")

    print("thank you for playing")


# Initialize the previous board state
startScreen()