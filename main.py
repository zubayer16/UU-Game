import random
import time


# Removes a piece, right now you are able to remove from a mill even if the opponent is not in phase 3, this should only be doable if the opponent is in phase 3
def removePiece(board, piece):
    """
    Lets the user remove one of the ai's piece

    @param board: The current board
    @param piece: The symbol representing the ai
    @return: The updated board with the ai piece removed


    """
    print()
    updateBoard(board)
    removeCoord = str(input("Please input piece to remove: "))
    removeCoord = removeCoord.split(',')
    removeCoord[0] = int(removeCoord[0])
    removeCoord[1] = int(removeCoord[1])
    if board[removeCoord[0]][removeCoord[1]] == piece:
        board[removeCoord[0]][removeCoord[1]] = '.'
        print(f"The piece at{removeCoord} is removed\n")
        return board
    else:
        return removePiece(board, piece)


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


# Verifies all moves
def verifyMove(phase, board, Playerpiece):
    """
    Verifies the proposed move by the player during phase 2 & 3

    @param board: The current board
    @param playerPiece: the symbol representing the player
    @param choosenPieceCoord: The coordinates of the piece the player wants to move
    @param moveCoord: The coordinates of the move the player wants to perform
    @param phase: The current phase of the player
    @return: True if the move is allowed by the rules of the game false otherwise


    """
    validMove = False
    coord = 0
    while not validMove:
        if (phase == 1):
            coord = inputCoord2("Please input coordinates for placement in format rownr,columnnr: ")
            validMove = veryifyMovep1(board, coord)
        if (phase == 2):
            coord = inputCoord4()
            validMove = verifyMovePiece(board, Playerpiece, coord[0], coord[1], phase)
        if (phase == 3):
            coord = inputCoord4()
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
def inputCoord2(Question):
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
def inputCoord4():
    piece = inputCoord2("Please input coordinates for the chosen piece to move in format rownr,columnnr: ")
    move = inputCoord2("Please input coordinates for placement in format rownr,columnnr: ")
    return piece, move


# Removes a piece randomly by the ai, also are able to remove a piece from a mill even if the player is not in phase 3, should only be able to do it if the player is phase 3


# Moves or places a piece depending on the phase
def doMove(board, playerMove, playerPiece, phase):
    if (phase == 1):
        board[playerMove[0]][playerMove[1]] = playerPiece  # In phase 1 we just need to place a piece on the coordinate
        return board

    chosenPieceCoord = playerMove[0]
    moveCoord = playerMove[1]

    board[moveCoord[0]][moveCoord[1]] = playerPiece
    board[chosenPieceCoord[0]][chosenPieceCoord[1]] = '.'
    return board


def aiRemovePiece(board, playerPiece):
    """
    Removes a random available piece from the player

    @param board: The current board
    @param playerPiece: The symbol representing the player
    @return: The updated board with the a player piece removed


    """
    available = []
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if board[i][j] == playerPiece:
                available.append([i, j])
    index = random.randint(0, len(available) - 1)
    board[available[index][0]][available[index][1]] = '.'
    return board


def aiSmartMoveP3(board, aiPiece, playerPiece):
    """
    Tries to find a move during phase 3 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.

    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param playerPiece: The symbol representing the player
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
            if hasNewThreeInARow(temp_board, aiPiece):
                move = (piece, spot)
                board = doMove(board, move, aiPiece, phase=3)
                print(f"AI moves a piece from {piece} to {spot}")

                return board

    # Check if we need to block the opponent from completing a mill
    for spot in empty_spots:
        for piece in ai_Pieces:
            temp_board = [row[:] for row in board]  # Create a copy of the board
            temp_board[piece[0]][piece[1]] = '.'  # Move the piece
            temp_board[spot[0]][spot[1]] = playerPiece
            if hasNewThreeInARow(temp_board, playerPiece):
                move = (piece, spot)
                board = doMove(board, move, aiPiece, phase=3)
                print(f"AI moves a piece from {piece} to {spot}")
                return board
    board = aiRandomMove(board, aiPiece, 3)  # If no good moves found just use a random move
    return board


def aiSmartMoveP2(board, aiPiece, playerPiece):
    """
    Tries to find a move during phase 2 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.

    @param board: The current board
    @param aiPiece: The symbol representing the AI
    @param playerPiece: The symbol representing the player
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
                if hasNewThreeInARow(temp_board, aiPiece):
                    move = (piece, spot)
                    board = doMove(board, move, aiPiece, phase=2)
                    print(f"AI moves a piece from {piece} to {spot}")
                    return board

    # Check if we need to block the opponent from completing a mill
    for spot in empty_spots:
        for piece in ai_Pieces:
            # Check if the move coordinate is adjacent to the chosen piece coordinate
            if abs(spot[0] - piece[0]) + abs(spot[1] - piece[1]) == 1:
                temp_board = [row[:] for row in board]  # Create a copy of the board
                temp_board[piece[0]][piece[1]] = '.'  # Move the piece
                temp_board[spot[0]][spot[1]] = playerPiece
                if hasNewThreeInARow(temp_board, playerPiece):
                    move = (piece, spot)
                    board = doMove(board, move, aiPiece, phase=2)
                    print(f"AI moves a piece from {piece} to {spot}")
                    return board

    # If no good moves found, just use a random move
    return aiRandomMove(board, aiPiece, 2)


def aiSmartMoveP1(board, aiPiece, playerPiece):
    """
    Tries to find a move during phase 1 wich can create a mill for the AI or block the player from creating mill.
    If none of these moves exist it will do a random move.
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @param playerPiece: The symbol representing the player
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
        if hasNewThreeInARow(temp_board, aiPiece):
            board[spot[0]][spot[1]] = aiPiece
            print(f"AI places a piece at {spot}")
            return board

    # Check if the ai can block the player from creating a mill
    for spot in empty_spots:
        temp_board = [row[:] for row in board]  # Create a copy of the board
        temp_board[spot[0]][spot[1]] = playerPiece
        if hasNewThreeInARow(temp_board, playerPiece):
            board[spot[0]][spot[1]] = aiPiece
            print(f"AI places a piece at {spot}")
            return board

    # If no good moves found, just use a random move
    board = aiRandomMove(board, aiPiece, 1)
    return board


# Dummy function, needs to be implemented with aleast some calculation on how the ai should act
def generateSmartMove(board, aiPiece, playerPiece, phase):
    """
    Creates a calculated move by the AI depending on the current phase of the AI.
    @param board: The current board
    @param aiPiece: The symbol reprenseting the AI
    @param playerPiece: The symbol representing the player
    @param phase: the current phase of AI
    @return: The updated board with the resulting AI move.


    """

    if (phase == 1):
        board = aiSmartMoveP1(board, aiPiece, playerPiece)

    if (phase == 2):
        board = aiSmartMoveP2(board, aiPiece, playerPiece)

    if (phase == 3):
        board = aiSmartMoveP3(board, aiPiece, playerPiece)

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
            print(f"AI moves a piece from {piece_to_move} to {move_coord}")
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
            print(f"AI moves a piece from {piece} to {(xcoord, ycoord)}")
            return board


# Handle all random movements needed for all phases
def aiRandomMove(board, aiPiece, aiPhase):
    if (aiPhase == 1):
        move = aiRandomMoveP1(board, aiPiece)
    if (aiPhase == 2):
        move = aiRandomMoveP2(board, aiPiece)
    if (aiPhase == 3):
        move = aiRandomMoveP3(board, aiPiece)
    return move


# Checks the difficulity of the AI. Easy AI always uses random moves, medium ai uses 1/4 calculated moves rest random, hard uses 1/2 calculated and rest random.
def aiMove(board, playerpiece, aiPiece, aiPhase, difficulty, rounds):
    newBoard = 0
    if (difficulty == 2):
        if (rounds % 4 == 0):
            newBoard = generateSmartMove(board, aiPiece, playerpiece, aiPhase)
            return newBoard
    if (difficulty == 3):
        if (rounds % 2 == 0):
            newBoard = generateSmartMove(board, aiPiece, playerpiece, aiPhase)
            return newBoard
    newBoard = aiRandomMove(board, aiPiece, aiPhase)  # Easy always uses random moves
    return newBoard


# Just checks if one only has two pieces left
def checkWinner(board, piece):
    count = 0
    for row in board:
        count += row.count(piece)
    if count < 3:
        return True
    return False


# Returns 0 for draw, 1 for player and 2 for ai


def gameLoop(rounds, board, playerPiece, opponentPiece, difficulty):
    aiPhase = 1
    playerPhase = 1
    piecestoPlace = 12
    aiPiecestoplace = 12
    pieceCount = 9
    aipieceCount = 9
    while (rounds < 200):
        updateBoard(board)
        rounds = rounds + 1
        prev_board = [row[:] for row in board]
        playerMove = verifyMove(playerPhase, board, playerPiece)
        board = doMove(board, playerMove, playerPiece, playerPhase)
        piecestoPlace = piecestoPlace - 1

        # player enters phase 2
        if piecestoPlace <= 0 and pieceCount > 1:
            playerPhase = 2
        # player enters phase 3
        elif piecestoPlace <= 0 and pieceCount < 1:
            playerPhase = 3

        if hasNewThreeInARow(board,
                             playerPiece):
            removePiece(board, opponentPiece)
            aipieceCount = aipieceCount - 1
            if not (aiPhase == 1):
                # Checks to see if after removing the piece that ai only has 2 left
                if (checkWinner(board, opponentPiece)):
                    return 1

        # AI opponent's turn
        # print("AI is making a move...")
        time.sleep(1)  # Simulate AI thinking time
        board = aiMove(board, playerPiece, opponentPiece, aiPhase, difficulty, rounds)
        aiPiecestoplace = aiPiecestoplace - 1
        # ai enters phase 2
        if aiPiecestoplace <= 0 and aipieceCount > 1:
            aiPhase = 2
        # ai enters phase 3
        elif aiPiecestoplace <= 0 and aipieceCount < 1:
            aiPhase = 3

        # Check if the AI opponent has formed a new three-in-a-row
        if hasNewThreeInARow(board, opponentPiece):
            aiRemovePiece(board, playerPiece)
            pieceCount = pieceCount - 1
            if not (playerPhase == 1):
                if (checkWinner(board, playerPiece)):
                    return 2

    return 0  # The game took too many turns and ended in a draw


def gameLoop2(rounds, board, playerPiece, opponentPiece, difficulty):
    aiPhase = 1
    playerPhase = 1
    piecestoPlace = 4
    aiPiecestoplace = 4
    pieceCount = 9
    aipieceCount = 9

    playerMills = []
    aiMills = []
    while (rounds < 200):
        updateBoard(board)
        rounds = rounds + 1
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

        new_mill = checkNewMill(board, playerPiece, playerMills)

        if new_mill:
            playerMills = updateMillList(board, playerPiece, playerMills)

            removePiece(board, opponentPiece)
            aipieceCount = aipieceCount - 1
            if not (aiPhase == 1):
                # Checks to see if after removing the piece that ai only has 2 left
                if (checkWinner(board, opponentPiece)):
                    return 1

        # AI opponent's turn
        # print("AI is making a move...")
        time.sleep(1)  # Simulate AI thinking time
        board = aiMove(board, playerPiece, opponentPiece, aiPhase, difficulty, rounds)
        aiPiecestoplace = aiPiecestoplace - 1
        # ai enters phase 2
        if aiPiecestoplace <= 0 and aipieceCount > 1:
            aiPhase = 2
        # ai enters phase 3
        elif aiPiecestoplace <= 0 and aipieceCount < 1:
            aiPhase = 3
        new_mill = checkNewMill(board, opponentPiece, aiMills)
        # Check if the AI opponent has formed a new three-in-a-row
        if new_mill:
            aiMills = updateMillList(board, opponentPiece, aiMills)
            aiRemovePiece(board, playerPiece)
            pieceCount = pieceCount - 1
            if not (playerPhase == 1):
                if (checkWinner(board, playerPiece)):
                    return 2

    return 0  # The game took too many turns and ended in a draw


# Fix consectuive mills and it does two mills if 4 in row
def hasNewThreeInARow(board, piece):
    # Check for new horizontal or vertical three-in-a-row
    mills = []
    for i in range(len(board) - 2):
        for j in range(len(board[i]) - 2):
            if (board[i][j] == piece and board[i + 1][j] == piece and board[i + 2][j] == piece) or \
                    (board[i][j] == piece and board[i][j + 1] == piece and board[i][j + 2] == piece):
                mill = [[i, j], [i + 1, j], [i + 2, j]] if board[i][j] == piece else [[i, j], [i, j + 1], [i, j + 2]]
                mills.append(mill)

    # Check if these mills are already present on the previous board
    unique_mills = [mill for mill in mills if mill not in prev_board]

    if unique_mills:
        return unique_mills[0]  # Return the first unique mill found
    else:
        return None


def findMills(board, piece):
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
    # Check if any of the coordinates of the new mill are already in the list
    for mill in mills_list:
        for coord in new_mill:
            if coord in mill:
                return mills_list  # If any coordinate is already in a mill, don't add it

    # If none of the coordinates are already in a mill, add the new mill to the list
    mills_list.append(new_mill)
    return mills_list


def updateMillList(board, piece, mill_list):
    new_mills = findMills(board, piece)
    if new_mills:
        for mill in new_mills:
            mill_list = addMillToList(mill_list, mill)

    return mill_list


def checkNewMill(board, piece, mill_list):
    tem_list = mill_list.copy()
    tem_list = updateMillList(board, piece, tem_list)
    if (len(tem_list) > len(mill_list)):
        return True
    return False


def checkDestroyedMills(board, piece, mill_list):
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
    rounds = 0
    result = gameLoop2(rounds, board, choosenPiece, aiPiece, difficulty)

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
prev_board = [['.' for _ in range(10)] for _ in range(10)]

startScreen()