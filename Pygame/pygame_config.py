import pygame

# PyGame module initialization
pygame.init()

# Window constants
FPS = 30
WIN_WIDTH = 1640
WIN_HEIGHT = 800
MARGIN_TOP = 30
MARGIN_BOTTOM = WIN_HEIGHT - MARGIN_TOP
MARGIN_LEFT = 50
MARGIN_RIGHT = WIN_WIDTH - MARGIN_LEFT

# Graph constants
GRAPH_LEFT_BORDER = MARGIN_LEFT + 300
GRAPH_BOTTOM_BORDER = MARGIN_BOTTOM - 350 + 190
GRAPH_FONT = pygame.font.SysFont('segoeuisemilight', 10)
VEL = 10
STICK_SIZE = 5
GRAPH_DIMENSIONS = [MARGIN_TOP, GRAPH_BOTTOM_BORDER, GRAPH_LEFT_BORDER, MARGIN_RIGHT]

# Menu constants
LEGEND_GAP = 40

# Trade history constants
TRADE_HISTORY_FONT = pygame.font.SysFont('segoeuisemilight', 10)

# Status overview constants
STATUS_VIEW_TOP = GRAPH_BOTTOM_BORDER + 20
STATUS_HEADER_FONT = pygame.font.SysFont('bahnschrift', 30)
STATUS_CONTENT_FONT = pygame.font.SysFont('segoeuisemilight', 14)
LINE_GAP = 30
STATUS_LINE1 = STATUS_VIEW_TOP + LINE_GAP
STATUS_LINE2 = STATUS_VIEW_TOP + (LINE_GAP * 2)
STATUS_LINE3 = STATUS_VIEW_TOP + (LINE_GAP * 3)
STATUS_LINE4 = STATUS_VIEW_TOP + (LINE_GAP * 4)

STATUS_COLUMN1 = (WIN_WIDTH / 6) * 3
STATUS_COLUMN2 = (WIN_WIDTH / 6) * 4
STATUS_COLUMN3 = (WIN_WIDTH / 6) * 5
STATUS_GRAPH_RIGHT = STATUS_COLUMN1 - 40

# Performance history constants
PERF_TOP_BORDER = STATUS_VIEW_TOP
PERF_BOTTOM_BORDER = STATUS_LINE4 + 15
STATUS_GRAPH_DIMENSIONS = [PERF_TOP_BORDER, PERF_BOTTOM_BORDER, MARGIN_LEFT, STATUS_GRAPH_RIGHT]

# Colour constants
BG_COLOUR = pygame.Color('grey12')
DARK_GREY_COLOUR = pygame.Color('gray30')
WHITE_COLOUR = pygame.Color('white')
GREEN_BAR_COLOUR = pygame.Color('green1')
RED_BAR_COLOUR = pygame.Color('red1')
MACD_HISTOGRAM_COLOUR = pygame.Color('cadetblue')
PINK_LINE_COLOUR = pygame.Color('deeppink')
BLUE_LINE_COLOUR = pygame.Color('royalblue')
TURQUOISE_LINE_COLOUR = pygame.Color('turquoise')
ORANGE_LINE_COLOUR = pygame.Color('darkorange')
LIGHTCORAL_LINE_COLOUR = pygame.Color('lightcoral')
CYAN_LINE_COLOUR = pygame.Color('cyan')
PURPLE_LINE_COLOUR = pygame.Color('orchid')
GOLD_LINE_COLOUR = pygame.Color('gold')
PEACH_LINE_COLOUR = pygame.Color('peachpuff')
PLUM_LINE_COLOUR = pygame.Color('plum')

# Trading bot constants
INITIAL_WALLET_AMOUNT = 1000
BUY_AMOUNT = 1