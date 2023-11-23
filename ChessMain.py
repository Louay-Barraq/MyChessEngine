from ChessEngine import GameState, Move
from consts import *
import pygame as pg


def loadImages():
    allPieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in allPieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))


# Drawing the squares of the board.
# PS : Top Left is always white.
def drawBoard(screen):
    colors = (pg.Color(PALE_YELLOW_COLOR), pg.Color(BROWNISH_ORANGE_COLOR))
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pg.draw.rect(screen, color, pg.Rect(((c * SQUARE_SIZE) + FULL_LEFT_PART_WIDTH), (r * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))


# Drawing the pieces on the board.
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # Draw the piece only if it is not an empty square
            if board[r][c] != '--':
                screen.blit(IMAGES[board[r][c]],
                            pg.Rect(((c * SQUARE_SIZE) + FULL_LEFT_PART_WIDTH), (r * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))


# Drawing the left menu and the right move log menu
def drawLeftMenu(screen, pawnPromotionHappening = False, promotingPlayer = ''):
    # Treating the cases where a pawn promotion move is being made
    if not pawnPromotionHappening:
        leftMenuDimensions = (0, 0, LEFT_MENU_WIDTH, BOARD_HEIGHT)
    else:
        if promotingPlayer == 'w':
            leftMenuDimensions = (0, 0, LEFT_MENU_WIDTH, BOARD_HEIGHT - (2 * SQUARE_SIZE))
        else:
            leftMenuDimensions = (0, (2 * SQUARE_SIZE) + BORDER_WIDTH, LEFT_MENU_WIDTH, BOARD_HEIGHT - ((2 * SQUARE_SIZE) + BORDER_WIDTH))

    # Drawing the Menu
    pg.draw.rect(screen, pg.Color(TEAL_COLOR), leftMenuDimensions)

    # Drawing the black borders
    upperBorderDimensions = (0, (2 * SQUARE_SIZE), LEFT_MENU_WIDTH, BORDER_WIDTH)
    pg.draw.rect(screen, pg.Color(BLACK_COLOR), upperBorderDimensions)
    lowerBorderDimensions = (0, BOARD_HEIGHT - ((2 * SQUARE_SIZE) + BORDER_WIDTH), LEFT_MENU_WIDTH, BORDER_WIDTH)
    pg.draw.rect(screen, pg.Color(BLACK_COLOR), lowerBorderDimensions)


def drawRightMenu(screen):
    # Drawing the moves log title text
    x, y = BOARD_WIDTH + FULL_LEFT_PART_WIDTH, 0
    width, height = MOVE_LOG_DISPLAY_WIDTH, SQUARE_SIZE
    pg.draw.rect(screen, pg.Color(TEAL_COLOR), pg.Rect(BOARD_WIDTH + FULL_LEFT_PART_WIDTH, 0, MOVE_LOG_DISPLAY_WIDTH, SQUARE_SIZE))
    font = pg.font.Font(None, 45)
    moves_log_text = font.render("Moves Log", True, (WHITE_COLOR))
    text_rect = moves_log_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(moves_log_text, text_rect)


# Draw the options if the player made a pawn promotion move
def drawPawnPromotionOptions(screen, thereIsPawnPromotion = False, pawnPromotionColor = ''):
    # Initializing values
    idx = 0
    pieces = [color + piece for color in ['w', 'b'] for piece in ['Q', 'R', 'N', 'B']]
    colors = [pg.Color(FOREST_GREEN_COLOR), pg.Color(TEAL_COLOR)]

    # Adding a bigger loop to print blit the images of both players
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for repetition in range(2):
        for r, c in positions:
            heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if pieces[idx][0] == 'w' else 0
            pieceRect = pg.Rect(c * SQUARE_SIZE, (r * SQUARE_SIZE) + heightOffset, SQUARE_SIZE, SQUARE_SIZE)
            pg.draw.rect(screen, colors[(r + c) % 2], pieceRect)
            screen.blit(IMAGES[pieces[idx]], pieceRect)
            idx += 1

    # Highlighting the pieces in case there is not any pawn promotion
    if not thereIsPawnPromotion:
        surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        # Defining the opacity of the highlighting
        surface.set_alpha(MEDIUM_HIGHLIGHTING)
        surface.fill(pg.Color(YELLOW_COLOR))

        idx = 0
        for repetitions in range(2):
            for r, c in positions:
                heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if pieces[idx][0] == 'w' else 0
                screen.blit(surface, (c * SQUARE_SIZE, (r * SQUARE_SIZE) + heightOffset, SQUARE_SIZE, SQUARE_SIZE))
                idx += 1

    else:
        surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        # Defining the opacity of the highlighting
        surface.set_alpha(MEDIUM_HIGHLIGHTING)
        surface.fill(pg.Color(YELLOW_COLOR))

        idx = 0
        toBeHighlightedPieces = [piece for piece in pieces if piece[0] != pawnPromotionColor]
        for r, c in positions:
            heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if toBeHighlightedPieces[idx][0] == 'w' else 0
            screen.blit(surface, (c * SQUARE_SIZE, (r * SQUARE_SIZE) + heightOffset, SQUARE_SIZE, SQUARE_SIZE))
            idx += 1


def getPawnPromotionOption(screen, color):
    selectedPieceRow, selectedPieceColumn = 0, 0
    piecesPositions = {(0, 0): 'Q', (0, 1): 'R', (1, 0): 'N', (1, 1): 'B'}
    heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if color == 'w' else 0

    drawPawnPromotionOptions(screen, color)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = not running
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Getting only the valid mouse clicks' position
                mouse_pos_x, mouse_pos_y = pg.mouse.get_pos()
                while not ((0 <= mouse_pos_x <= LEFT_MENU_WIDTH) and (heightOffset <= mouse_pos_y <= heightOffset + (2 * SQUARE_SIZE))):
                    mouse_pos_x, mouse_pos_y = pg.mouse.get_pos()

                selectedPieceRow, selectedPieceColumn = (mouse_pos_y - heightOffset) // SQUARE_SIZE, mouse_pos_x // SQUARE_SIZE
                running = not running
                break

    return color + piecesPositions[(selectedPieceRow, selectedPieceColumn)]


def highlightValidSquares(screen, gameState, validMoves, squareSelected):
    # Highlighting the last played move
    if len(gameState.moveLog) > 0:
        lastPlayedMove = gameState.moveLog[-1]
        surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        # Defining the opacity of the highlighting
        surface.set_alpha(100)
        surface.fill(pg.Color(MEDIUM_BLUE_COLOR))
        screen.blit(surface, ((lastPlayedMove.endingColumn * SQUARE_SIZE) + FULL_LEFT_PART_WIDTH, lastPlayedMove.endingRow * SQUARE_SIZE))

    # Highlighting the selected square and all the valid squares that the player can move his piece to
    if squareSelected != ():
        selectedRow, selectedCol = squareSelected
        if (gameState.board[selectedRow][selectedCol][0] == ('w' if gameState.whiteToMove else 'b')):
            # Highlighting the selected square
            surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
            surface.set_alpha(100)
            surface.fill(pg.Color(TURQUOISE_COLOR))
            screen.blit(surface, ((selectedCol * SQUARE_SIZE) + FULL_LEFT_PART_WIDTH, selectedRow * SQUARE_SIZE))

            # Highlighting the valid squares
            surface.fill((pg.Color(DARK_WASHED_RED_COLOR)))
            selectedPieceValidMoves = [move for move in validMoves if (move.startingColumn == selectedCol) and (move.startingRow == selectedRow)]
            for move in selectedPieceValidMoves:
                screen.blit(surface, ((move.endingColumn * SQUARE_SIZE) + FULL_LEFT_PART_WIDTH, move.endingRow * SQUARE_SIZE))


def displayMoveLog(screen, gameState, font):
    moveLogRect = pg.Rect(BOARD_WIDTH + FULL_LEFT_PART_WIDTH, SQUARE_SIZE, MOVE_LOG_DISPLAY_WIDTH, BOARD_HEIGHT - SQUARE_SIZE)
    move_log = gameState.moveLog
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += "|| " + str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 1
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, pg.Color(WHITE_COLOR))
        text_location = moveLogRect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

# Draw the current game state.
def drawGameState(screen, gameState, validMoves, squareSelected, font, color='', isPawnPromotion=False):
    drawBoard(screen)
    highlightValidSquares(screen, gameState, validMoves, squareSelected)
    drawPieces(screen, gameState.board)
    drawRightMenu(screen)
    displayMoveLog(screen, gameState, font)

    if isPawnPromotion:
        drawLeftMenu(screen, pawnPromotionHappening=True, promotingPlayer=color)
        toPromoteToPiece = getPawnPromotionOption(screen, color)
        while toPromoteToPiece is None:
            toPromoteToPiece = getPawnPromotionOption(screen, color)
        return toPromoteToPiece  # Return the selected piece
    else:
        drawLeftMenu(screen)

    return None  # Return None if no selection is made yet


# Main Function
def main():
    # Setting up the board's graphics
    global pawnPromotionColor
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, BOARD_HEIGHT))
    pg.display.set_caption("My Chess Engine")
    clock = pg.time.Clock()
    screen.fill("black")
    MOVE_LOG_FONT = pg.font.SysFont("Arial", 25, False, False)
    # Loading the pieces' images
    loadImages()
    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False  # Flag to detect changes whenever a move is made
    squareSelected = ()  # contains a tuple (x, y) of the selected square
    playerClicks = []  # contains at most 2 tuples : (x, y)
    running = True
    pawnPromotionMade = False
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = not running
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Get the mouse position in (x, y) format
                mouse_pos_x, mouse_pos_y = pg.mouse.get_pos()
                # In case the click was on the board
                if FULL_LEFT_PART_WIDTH < mouse_pos_x < WINDOW_WIDTH:
                    col, row = (mouse_pos_x - FULL_LEFT_PART_WIDTH) // SQUARE_SIZE, mouse_pos_y // SQUARE_SIZE
                    # Check if the last selected square is the same as the one selected now : Undo the selection
                    if squareSelected == (row, col):
                        squareSelected = ()  # Deselect the selected square
                        playerClicks = []  # Clear the clicks
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                        if len(playerClicks) == 2:  # After the 2nd move
                            move = Move(playerClicks[0], playerClicks[1], gameState.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    if validMoves[i].isPawnPromotion: # the move is a pawn promotion
                                        pawnPromotionMade, pawnPromotionColor = True, 'w' if gameState.whiteToMove else 'b'
                                        break
                                    else:
                                        gameState.makeMove(validMoves[i]) # Play the move generated by the engine
                                        moveMade = True
                                        squareSelected = ()  # Deselect the selected square
                                        playerClicks = []  # Clear the clicks
                            if (not moveMade) and (not pawnPromotionMade):
                                playerClicks = [squareSelected]
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gameState.undoMove()
                    moveMade = True

        if not pawnPromotionMade:
            drawGameState(screen, gameState, validMoves, squareSelected, MOVE_LOG_FONT)
            drawPawnPromotionOptions(screen)
        else:
            # Draw and wait for a valid selection
            toPromoteToPiece = drawGameState(screen, gameState, validMoves, squareSelected, MOVE_LOG_FONT, color=pawnPromotionColor, isPawnPromotion=True)

            # If a valid selection is made, make the move
            if toPromoteToPiece is not None:
                gameState.makeMove(Move(playerClicks[0], playerClicks[1], gameState.board), True, toPromoteToPiece)
                pawnPromotionMade, pawnPromotionColor = False, ''
                squareSelected = ()
                playerClicks = []
                moveMade = True

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        # drawPawnPromotionOptions(screen, pawnPromotionColor)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
