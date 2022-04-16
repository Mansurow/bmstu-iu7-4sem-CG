# --------------------------------------------------------------------------------------------------------
# Параматры масштабирования интерфейса программы
# --------------------------------------------------------------------------------------------------------
MAIN_COLOUR = "#2b2b2b"
MAIN_FRAME_COLOR = "#313335"
ADD_COLOUR = "#3c3f41"
TEXT_ENTRY_COLOUR = "#eeeeee"

WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 900

# Frame sizes (relative).
BORDERS_PART = 0.05
BORDERS_SPACE = 10
BORDERS_MAIN_MAKE = 1/6
COLUMNS_DATA_BORDERS_HEIGHT = 1/5

DATA_PART_WIDTH = 0.28 - 2 * BORDERS_PART
DATA_PART_HEIGHT = 0.8 - 2 * BORDERS_PART
DATA_K_LABEL = 1 - BORDERS_MAIN_MAKE
DATA_WIDTH = int(WINDOW_WIDTH * BORDERS_MAIN_MAKE)
DATA_HEIGHT = int(WINDOW_HEIGHT - BORDERS_SPACE * 2)


FIELD_WIDTH = WINDOW_WIDTH * (1 - BORDERS_MAIN_MAKE) - 3 * BORDERS_SPACE
FIELD_HEIGHT = WINDOW_HEIGHT - 2 * BORDERS_SPACE

POINT_SIZE = 6
LINE_WIDTH = 2

SCALE = 100
STEP = 1 * 10 / SCALE
INCLINE = 1
MAX_LIMIT_X = (FIELD_WIDTH / SCALE) // 2
MAX_LIMIT_Y = (FIELD_HEIGHT / SCALE) // 2
MIN_LIMIT_X = -MAX_LIMIT_X
MIN_LIMIT_Y = -MAX_LIMIT_Y

COLUMNS = 23

INFO_PART_HEIGHT = (1 - DATA_PART_HEIGHT - 2 * BORDERS_PART) - 1 * BORDERS_PART
INFO_PART_WIDTH = DATA_PART_WIDTH
INFO_WIDTH = int(INFO_PART_WIDTH * WINDOW_WIDTH)
INFO_HEIGHT = int(INFO_PART_HEIGHT * WINDOW_HEIGHT)
INFO_COLS = 4
# --------------------------------------------------------------------------------------------------------
