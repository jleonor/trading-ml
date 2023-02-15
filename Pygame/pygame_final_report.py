from Pygame.pygame_config import *

def final_report(df_history, trader):
    print('Start Date & Time:', str(df_history['Date'].iloc[1]), str(df_history['Time'].iloc[1]))
    print('End Date & Time:', str(df_history['Date'].iloc[-1]), str(df_history['Time'].iloc[-1]))
    print('Profit/Loss:', str(round(trader.portfolio_value - INITIAL_WALLET_AMOUNT, 2)), '$')
    print('Return:', str(round(trader.gains, 2)), '%')
    print('Market Performance:', str(round(((df_history['Close'].iloc[-1]/trader.start_close) - 1) * 100, 2)), '%')

