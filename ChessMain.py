from ChessEngine import GameState, Move
import pygame as pg

# Constants
BOARD_WIDTH = BOARD_HEIGHT = 600
WINDOW_WIDTH = BOARD_WIDTH + 400
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    allPieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in allPieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))


'''
Draw the squares of the board. 
PS : Top Left is always white.
'''
def drawBoard(screen):
    colors = (pg.Color("white"), pg.Color("light gray"))
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pg.draw.rect(screen, color, pg.Rect((c * SQUARE_SIZE), (r * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))


'''
Draw the pieces on the board.
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # Draw the piece only if it is not an empty square
            if board[r][c] != '--':
                screen.blit(IMAGES[board[r][c]],
                            pg.Rect((c * SQUARE_SIZE), (r * SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))


'''
Draw the current game state.
'''
def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)


def main():
    # Setting up the board's graphics
    pg.init()
    screen = pg.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    pg.display.set_caption("My Chess Engine")
    clock = pg.time.Clock()
    screen.fill("white")
    # Loading the pieces' images
    loadImages()
    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False # Flag to detect changes whenever a move is made
    squareSelected = ()  # contains a tuple (x, y) of the selected square
    playerClicks = []  # contains at most 2 tuples : (x, y)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = not running
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Get the mouse position in (x, y) format
                mouse_pos = pg.mouse.get_pos()
                col, row = mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE
                # Check if the last selected square is the same as the one selected now : Undo the selection
                if squareSelected == (row, col):
                    squareSelected = ()  # Deselect the selected square
                    playerClicks = []  # Clear the clicks
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                    if len(playerClicks) == 2:  # After the 2nd move
                        move = Move(playerClicks[0], playerClicks[1], gameState.board)
                        # print(move.getChessNotation())
                        if move in validMoves:
                            gameState.makeMove(move)
                            moveMade = True
                            squareSelected = ()  # Deselect the selected square
                            playerClicks = []  # Clear the clicks
                        else:
                            playerClicks = [squareSelected]
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    gameState.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gameState.getValidMoves()
            print(f"There are currently {len(validMoves)} valid moves .\n{'-' * 35}")
            moveMade = False

        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == '__main__':
    main()
