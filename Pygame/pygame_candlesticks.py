from Pygame.pygame_config import *


class CandleSticks:
    def __init__(self, instance_counter, norm_hist_info, status_info):
        self.x = MARGIN_RIGHT
        self.y = MARGIN_TOP
        self.height = 0
        self.width = STICK_SIZE
        self.colour = WHITE_COLOUR
        self.low = GRAPH_BOTTOM_BORDER
        self.high = MARGIN_TOP
        self.price_type = status_info[3]

        # Set bar colour
        if self.price_type == 1:
            self.colour = GREEN_BAR_COLOUR
        if self.price_type == -1:
            self.colour = RED_BAR_COLOUR

        # Set candlestick dimensions
        self.y, self.height, self.low, self.high = self.convert_norm_vals(instance_counter, -1, norm_hist_info)
        self.bar = pygame.Rect(self.x, self.y, self.width, self.height)

    def convert_norm_vals(self, instance_counter, idx, norm_hist_info):
        if instance_counter > 2:
            # Scale high/low line
            self.low = GRAPH_BOTTOM_BORDER - ((GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[1][idx])
            self.high = GRAPH_BOTTOM_BORDER - ((GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[2][idx])
            if self.price_type == 1:
                # Scale green bar
                self.y = GRAPH_BOTTOM_BORDER - ((GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[3][idx])
                self.height = (GRAPH_BOTTOM_BORDER - self.y) - (
                            (GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[0][idx])
            if self.price_type == -1:
                # Scale red bar
                self.y = GRAPH_BOTTOM_BORDER - ((GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[0][idx])
                self.height = (GRAPH_BOTTOM_BORDER - self.y) - (
                            (GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[3][idx])
            if self.price_type == 0:
                self.y = GRAPH_BOTTOM_BORDER - ((GRAPH_BOTTOM_BORDER - MARGIN_TOP) * norm_hist_info[3][idx])
        if 1 > self.height >= 0:
            self.height = 1

        return self.y, self.height, self.low, self.high

    def move(self):
        self.bar.x -= VEL

    def resize(self, instance_counter, idx, norm_hist_info):
        self.y, self.height, self.low, self.high = self.convert_norm_vals(instance_counter, idx, norm_hist_info)
        self.bar.update(self.bar.x, self.y, self.width, self.height)

    def draw_chart(self, win):
        pygame.draw.line(win, self.colour, (self.bar.x + (self.bar.width/2), self.high), (self.bar.x + (self.bar.width/2), self.low))
        pygame.draw.rect(win, self.colour, self.bar)
