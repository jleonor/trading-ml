from Pygame.pygame_config import *
from Pygame.pygame_trader import *
from Pygame.pygame_functions import *
from Pygame.pygame_candlesticks import *
from Pygame.pygame_final_report import *
import pandas as pd
import random
import sys


# Loading market data
df = pd.read_csv('bitcoin.csv')
df = df.drop(columns=['Weighted_Price', 'Volume_(Currency)', 'Volume_(BTC)'])
df = df.iloc[df.where(df['Close'] == 1000).last_valid_index():]
df_full = df.reset_index(drop=True)
df_full = df_full.fillna(method='pad')
df_full['Date'] = pd.to_datetime(df_full['Timestamp'], unit='s').dt.date
df_full['Time'] = pd.to_datetime(df_full['Timestamp'], unit='s').dt.time
df_full['Time'] = df_full['Time'].map(lambda x: str(x)[:-3])


def main():
    # Initialize window
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    MAX_DISPLAY = 240
    pygame.display.set_caption('TradingSim V3')
    clock = pygame.time.Clock()

    # Initialize random price start
    instance_randomizer = random.randint(0, len(df_full) - MAX_DISPLAY)
    instance_counter = 1
    df_prices = df_full[instance_randomizer:].reset_index(drop=True)

    # Initialize display lists
    display_open = []
    display_low = []
    display_high = []
    display_close = []

    max_hist = []
    min_hist = []
    trend_state = 0
    RSI_state = 0

    # Initialize graph, trading bot and candlesticks
    trader = TraderBot()
    candlesticks = []
    all_prices_display = []

    # Game loop
    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()

        # Update price history and last price info for every instance
        df_history = df_prices[:instance_counter]
        new_open = df_history['Open'].iloc[-1]
        new_low = df_history['Low'].iloc[-1]
        new_high = df_history['High'].iloc[-1]
        new_close = df_history['Close'].iloc[-1]
        new_date = df_history['Date'].iloc[-1]
        new_time = df_history['Time'].iloc[-1]

        # Set last close as the new open for smoother chart and get RSI
        if len(df_history) > 1:
            new_open = df_history['Close'].iloc[-2]

        # Update price intervals on the left side of the graph
        if len(all_prices_display) / 4 > MAX_DISPLAY:
            all_prices_display = all_prices_display[4:]
        all_prices_display.extend([new_open, new_low, new_high, new_close])
        min_price, max_price = min(all_prices_display), max(all_prices_display)
        low_middle_price = round(min_price + ((max_price - min_price) / 3), 2)
        high_middle_price = round(min_price + (((max_price - min_price) / 3) * 2), 2)

        # Set trend state
        if len(max_hist) > 1 and len(min_hist) > 1:

            max_hist = max_hist[1:]
            min_hist = min_hist[1:]

        max_hist.append(max_price)
        min_hist.append(min_price)

        # Add last price info to list of displayed price info
        display_open.append(new_open)
        display_low.append(new_low)
        display_high.append(new_high)
        display_close.append(new_close)

        # Remove candlestick if it goes over the left border of the graph
        for stick in candlesticks:
            if stick.bar.x < GRAPH_LEFT_BORDER + 20:
                candlesticks.remove(stick)
                MAX_DISPLAY = len(candlesticks)

        # Match the number of infos displayed to the number of candlesticks
        try:
            if len(df_history) > len(candlesticks) + 1:
                display_open = display_open[1:]
                display_low = display_low[1:]
                display_high = display_high[1:]
                display_close = display_close[1:]

        except TypeError:
            pass

        # Normalize market data for candlesticks
        norm_open_history = normalize(display_open, all_prices_display)
        norm_low_history = normalize(display_low, all_prices_display)
        norm_high_history = normalize(display_high, all_prices_display)
        norm_close_history = normalize(display_close, all_prices_display)

        # Determine price movement direction for price movement indicator
        price_type = 0
        if new_open < new_close:
            price_type = 1
        if new_open > new_close:
            price_type = -1

        # Set bar size only at the start depending on price type
        if instance_counter == 1:
            norm_low_history = [0.0]
            norm_high_history = [1.0]
            if price_type == 1:
                norm_open_history = [0.0]
                norm_close_history = [1.0]
            if price_type == -1:
                norm_open_history = [0.0]
                norm_close_history = [1.0]
            if price_type == 0:
                norm_open_history = [0.5]
                norm_close_history = [0.5]

        # Create info lists
        status_info = [new_close, new_date, new_time, price_type]
        min_max_info = [min_price, low_middle_price, high_middle_price, max_price]
        norm_hist_info = [norm_open_history, norm_low_history, norm_high_history, norm_close_history]

        # Move to next frame and update window
        instance_counter += 1
        WIN.fill(BG_COLOUR)
        candlesticks.append(CandleSticks(instance_counter, norm_hist_info, status_info))
        draw_window(WIN, trader, candlesticks, instance_counter, events, status_info, min_max_info, norm_hist_info)

        # Quit command
        for event in events:
            if event.type == pygame.QUIT:
                final_report(df_history, trader)
                pygame.quit()
                sys.exit()

            # Buy and sell commands for testing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    trader.buy(new_close, new_time)
                if event.key == pygame.K_BACKSPACE:
                    trader.sell(new_close, new_time, instance_counter)

        if MAX_DISPLAY + 1 == len(candlesticks):
            if trend_state == 1 and RSI_state == -1:
                trader.buy(new_close, new_time)
            elif RSI_state == 1:
                trader.sell(new_close, new_time, instance_counter)


if __name__ == '__main__':
    main()
