# Constants

# The board characteristics
BOARD_HEIGHT = 656
BOARD_WIDTH = 656

# The right part characteristics
MOVE_LOG_DISPLAY_WIDTH = 220

# The left part characteristics
LEFT_MENU_WIDTH = 164 # A square is (82, 82) so the width of two squares will be 2 * 82 = 164
BLACK_VERTICAL_LINE_WIDTH = 16
FULL_LEFT_PART_WIDTH = LEFT_MENU_WIDTH + BLACK_VERTICAL_LINE_WIDTH

# The window characteristics (The height will be the same as the board's height)
WINDOW_WIDTH = LEFT_MENU_WIDTH + BLACK_VERTICAL_LINE_WIDTH + BOARD_WIDTH + MOVE_LOG_DISPLAY_WIDTH

# Colors
PALE_YELLOW_COLOR = (227, 193, 111)
BROWNISH_ORANGE_COLOR = (184, 139, 74)
TEAL_COLOR = (14, 174, 107)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
FOREST_GREEN_COLOR = (5, 122, 74)

# Others
BORDER_WIDTH = 16
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}