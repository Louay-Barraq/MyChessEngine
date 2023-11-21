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
def drawLeftMenu(screen):
    # Pawn Promotion Menu
    leftMenuDimensions = (0, 0, LEFT_MENU_WIDTH, BOARD_HEIGHT)
    pg.draw.rect(screen, pg.Color(TEAL_COLOR), leftMenuDimensions)

    upperBorderDimensions = (0, (2 * SQUARE_SIZE), LEFT_MENU_WIDTH, BORDER_WIDTH)
    pg.draw.rect(screen, pg.Color(BLACK_COLOR), upperBorderDimensions)
    lowerBorderDimensions = (0, BOARD_HEIGHT - ((2 * SQUARE_SIZE) + BORDER_WIDTH), LEFT_MENU_WIDTH, BORDER_WIDTH)
    pg.draw.rect(screen, pg.Color(BLACK_COLOR), lowerBorderDimensions)

def drawRightMenu(screen):
    # Moves Log Text
    x, y = BOARD_WIDTH + FULL_LEFT_PART_WIDTH, 0
    width, height = MOVE_LOG_DISPLAY_WIDTH, SQUARE_SIZE
    pg.draw.rect(screen, pg.Color(TEAL_COLOR), pg.Rect(BOARD_WIDTH + FULL_LEFT_PART_WIDTH, 0, MOVE_LOG_DISPLAY_WIDTH, SQUARE_SIZE))
    font = pg.font.Font(None, 45)
    moves_log_text = font.render("Moves Log", True, (WHITE_COLOR))
    text_rect = moves_log_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(moves_log_text, text_rect)


# Draw the options if the player made a pawn promotion move
def drawPawnPromotionOptions(screen, color):
    # Initializing values
    idx = 0
    pieces = [color + piece for piece in ['Q', 'R', 'N', 'B']]
    heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if color == 'w' else 0
    colors = [pg.Color(FOREST_GREEN_COLOR), pg.Color(TEAL_COLOR)]

    for r in range(2):
        for c in range(2):
            pieceRect = pg.Rect(c * SQUARE_SIZE, (r * SQUARE_SIZE) + heightOffset, SQUARE_SIZE, SQUARE_SIZE)
            pg.draw.rect(screen, colors[(r + c) % 2], pieceRect)
            screen.blit(IMAGES[pieces[idx]], pieceRect)
            idx += 1
    # print("inside drawPawn...Options")

def getPawnPromotionOption(color):
    selectedPieceRow, selectedPieceColumn = 0, 0
    piecesPositions = {(0, 0): 'Q', (0, 1): 'R', (1, 0): 'N', (1, 1): 'B'}
    heightOffset = BOARD_HEIGHT - (2 * SQUARE_SIZE) if color == 'w' else 0

    # drawPawnPromotionOptions(screen, color)
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

    # Revert back to the normal state
    # drawLeftMenu(screen)
    return color + piecesPositions[(selectedPieceRow, selectedPieceColumn)]


# Draw the current game state.
def drawGameState(screen, gameState, color='', isPawnPromotion=False):
    drawBoard(screen)
    drawPieces(screen, gameState.board)
    drawLeftMenu(screen)
    drawRightMenu(screen)

    if isPawnPromotion:
        toPromoteToPiece = getPawnPromotionOption(color)
        while toPromoteToPiece is None:
            drawPawnPromotionOptions(screen, color)
            toPromoteToPiece = getPawnPromotionOption(screen, color)
        return toPromoteToPiece  # Return the selected piece

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
            drawGameState(screen, gameState)
        else:
            # Draw and wait for a valid selection
            toPromoteToPiece = drawGameState(screen, gameState, pawnPromotionColor, True)
            # drawPawnPromotionOptions(screen, pawnPromotionColor)

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

        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()
