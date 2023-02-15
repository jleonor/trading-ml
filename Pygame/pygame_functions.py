from Pygame.pygame_config import *
import pygame_widgets


def draw_trader_status(win, trader, status_info):
    trader.update_status(status_info[0])
    # Draw header
    STATUS_HEADER_LABEL = STATUS_HEADER_FONT.render('STATUS & PERFORMANCE OVERVIEW', bool(1), WHITE_COLOUR)
    win.blit(STATUS_HEADER_LABEL, (STATUS_COLUMN1, STATUS_VIEW_TOP))

    # Draw status in first column
    WALLET_AMOUNT_LABEL = STATUS_CONTENT_FONT.render('WALLET AMOUNT: ' + str(round(trader.wallet_amount, 2)) + ' $',
                                                     bool(1), WHITE_COLOUR)
    win.blit(WALLET_AMOUNT_LABEL, (STATUS_COLUMN1, STATUS_LINE1 + WALLET_AMOUNT_LABEL.get_height()))

    CURRENCY_OWNED_USD_LABEL = STATUS_CONTENT_FONT.render(
        'CURRENCY OWNED (USD): ' + str(round(trader.currency_owned_USD, 2)) + ' $', bool(1), WHITE_COLOUR)
    win.blit(CURRENCY_OWNED_USD_LABEL, (STATUS_COLUMN1, STATUS_LINE2 + CURRENCY_OWNED_USD_LABEL.get_height()))

    PORTFOLIO_LABEL = STATUS_CONTENT_FONT.render('PORTFOLIO VALUE: ' + str(round(trader.portfolio_value, 2)) + ' $',
                                                 bool(1), WHITE_COLOUR)
    win.blit(PORTFOLIO_LABEL, (STATUS_COLUMN1, STATUS_LINE3 + PORTFOLIO_LABEL.get_height()))

    GAINS_LABEL = STATUS_CONTENT_FONT.render('RETURN (%): ' + str(round(trader.gains, 3)) + ' %', bool(1), WHITE_COLOUR)
    win.blit(GAINS_LABEL, (STATUS_COLUMN1, STATUS_LINE4 + GAINS_LABEL.get_height()))

    # Draw status in second column
    CURRENCY_OWNED_CUR_LABEL = STATUS_CONTENT_FONT.render(
        'CURRENCY OWNED (CUR): ' + str(round(trader.currency_owned_CUR, 5)) + ' BTC', bool(1), WHITE_COLOUR)
    win.blit(CURRENCY_OWNED_CUR_LABEL, (STATUS_COLUMN2, STATUS_LINE1 + CURRENCY_OWNED_CUR_LABEL.get_height()))

    last_buy_str = str(trader.last_buy) + ' $'
    if trader.last_buy == 0:
        last_buy_str = 'N/A'

    LAST_BUY_LABEL = STATUS_CONTENT_FONT.render('HELD POSITION: ' + last_buy_str, bool(1), WHITE_COLOUR)
    win.blit(LAST_BUY_LABEL, (STATUS_COLUMN2, STATUS_LINE2 + LAST_BUY_LABEL.get_height()))

    TRADE_COUNT_LABEL = STATUS_CONTENT_FONT.render('TRADE COUNT: ' + str(trader.trade_count) + ' trades', bool(1),
                                                   WHITE_COLOUR)
    win.blit(TRADE_COUNT_LABEL, (STATUS_COLUMN2, STATUS_LINE3 + TRADE_COUNT_LABEL.get_height()))

    TRADE_FREQ_LABEL = STATUS_CONTENT_FONT.render(
        'TRADE FREQUENCY: ' + str(round(trader.trade_frequency, 2)) + ' per instance', bool(1), WHITE_COLOUR)
    win.blit(TRADE_FREQ_LABEL, (STATUS_COLUMN2, STATUS_LINE4 + TRADE_FREQ_LABEL.get_height()))

    # Draw status in third column
    DATE_LABEL = STATUS_CONTENT_FONT.render('DATE: ' + str(status_info[1]), bool(1), WHITE_COLOUR)
    win.blit(DATE_LABEL, (STATUS_COLUMN3, STATUS_LINE1 + DATE_LABEL.get_height()))

    TIME_LABEL = STATUS_CONTENT_FONT.render('TIME: ' + str(status_info[2]), bool(1), WHITE_COLOUR)
    win.blit(TIME_LABEL, (STATUS_COLUMN3, STATUS_LINE2 + TIME_LABEL.get_height()))

    PRICE_USD_LABEL = STATUS_CONTENT_FONT.render('PRICE (USD per CUR): ' + str(status_info[0]) + ' $', bool(1), WHITE_COLOUR)
    win.blit(PRICE_USD_LABEL, (STATUS_COLUMN3, STATUS_LINE3 + PRICE_USD_LABEL.get_height()))

    PRICE_CUR_LABEL = STATUS_CONTENT_FONT.render('PRICE (CUR per USD): ' + str(round(1 / status_info[0], 7)) + ' BTC',
                                                 bool(1), WHITE_COLOUR)
    win.blit(PRICE_CUR_LABEL, (STATUS_COLUMN3, STATUS_LINE4 + PRICE_CUR_LABEL.get_height()))

    # Draw price movement indicator
    if status_info[3] == 1:
        pygame.draw.polygon(win, GREEN_BAR_COLOUR, [
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 10, STATUS_LINE3 + PRICE_USD_LABEL.get_height() + 7),
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 5, STATUS_LINE3 + (PRICE_USD_LABEL.get_height() * 2) - 7),
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 15, STATUS_LINE3 + (PRICE_USD_LABEL.get_height() * 2) - 7)])

    if status_info[3] == -1:
        pygame.draw.polygon(win, RED_BAR_COLOUR, [
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 10, STATUS_LINE3 + (PRICE_USD_LABEL.get_height() * 2) - 7),
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 5, STATUS_LINE3 + PRICE_USD_LABEL.get_height() + 7),
            (STATUS_COLUMN3 + PRICE_USD_LABEL.get_width() + 15, STATUS_LINE3 + PRICE_USD_LABEL.get_height() + 7)])


def draw_PERFORMANCE_border(win):
    PORTFOLIO_PERFORMANCE_LABEL = STATUS_CONTENT_FONT.render('PORTFOLIO PERFORMANCE VS MARKET PERFORMANCE HISTORY', bool(1), WHITE_COLOUR)
    win.blit(PORTFOLIO_PERFORMANCE_LABEL, ((((STATUS_GRAPH_RIGHT - MARGIN_LEFT) / 2) + MARGIN_LEFT) - (PORTFOLIO_PERFORMANCE_LABEL.get_width() / 2), STATUS_LINE4 + PORTFOLIO_PERFORMANCE_LABEL.get_height()))

    pygame.draw.line(win, WHITE_COLOUR, (MARGIN_LEFT, PERF_TOP_BORDER), (STATUS_GRAPH_RIGHT, PERF_TOP_BORDER))
    pygame.draw.line(win, WHITE_COLOUR, (MARGIN_LEFT, STATUS_LINE4 + 15), (STATUS_GRAPH_RIGHT, STATUS_LINE4 + 15))
    pygame.draw.line(win, WHITE_COLOUR, (MARGIN_LEFT, PERF_TOP_BORDER), (MARGIN_LEFT, STATUS_LINE4 + 15))
    pygame.draw.line(win, WHITE_COLOUR, (STATUS_GRAPH_RIGHT, PERF_TOP_BORDER), (STATUS_GRAPH_RIGHT, STATUS_LINE4 + 15))


def draw_PERFORMANCE(win, trader):
    if len(trader.portfolio_history) > 1:
        identical_check = all(element == trader.portfolio_history[0] for element in trader.portfolio_history)
        if identical_check:
            trader.portfolio_history = [trader.portfolio_history[-1]]
            trader.market_history = [trader.market_history[-1]]
        else:
            trader.portfolio_history_display = trader.portfolio_history
            trader.market_history_display = trader.market_history
            # Thin portfolio history data points
            if len(trader.portfolio_history_display) > 200:
                if len(trader.portfolio_history) % 200 == 0:
                    trader.slice_counter += 1
                if len(trader.portfolio_history_display) > 200:
                    trader.portfolio_history_chunks = (trader.portfolio_history[i::trader.slice_counter] for i in range(trader.slice_counter))
                    trader.portfolio_history_display = [sum(x) / len(x) for x in zip(* trader.portfolio_history_chunks)]

                if len(trader.market_history_display) > 200:
                    trader.market_history_chunks = (trader.market_history[i::trader.slice_counter] for i in range(trader.slice_counter))
                    trader.market_history_display = [sum(x) / len(x) for x in zip(* trader.market_history_chunks)]

            scaler = [max(trader.market_history_display), max(trader.portfolio_history_display), min(trader.market_history_display), min(trader.portfolio_history_display)]
            draw_LINE_chart(win, trader.market_history_display, DARK_GREY_COLOUR, STATUS_GRAPH_DIMENSIONS, scaler)
            draw_LINE_chart(win, trader.portfolio_history_display, WHITE_COLOUR, STATUS_GRAPH_DIMENSIONS, scaler)


def draw_TRADE_HISTORY(win, trader):
    idx = -1

    if trader.trade_history is not None:
        for i in trader.trade_history:
            trade_type_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][1])), bool(1), WHITE_COLOUR)
            trade_return_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][3])) + ' $', bool(1), WHITE_COLOUR)
            trade_portfolio_LABEL = TRADE_HISTORY_FONT.render((str(round(trader.trade_history[idx][4], 2))), bool(1), WHITE_COLOUR)
            trade_time_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][2])), bool(1), WHITE_COLOUR)

            if trader.trade_history[idx][0] == 1:
                if trader.trade_history[idx][3] > 0:
                    trade_type_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][1])), bool(1), GREEN_BAR_COLOUR)
                    trade_return_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][3])) + ' %', bool(1), GREEN_BAR_COLOUR)
                    trade_portfolio_LABEL = TRADE_HISTORY_FONT.render((str(round(trader.trade_history[idx][4], 2))), bool(1), GREEN_BAR_COLOUR)
                if trader.trade_history[idx][3] < 0:
                    trade_type_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][1])), bool(1), RED_BAR_COLOUR)
                    trade_return_LABEL = TRADE_HISTORY_FONT.render((str(trader.trade_history[idx][3])) + ' %', bool(1), RED_BAR_COLOUR)
                    trade_portfolio_LABEL = TRADE_HISTORY_FONT.render((str(round(trader.trade_history[idx][4], 2))), bool(1), RED_BAR_COLOUR)

            if idx > -24:
                win.blit(trade_time_LABEL, (MARGIN_LEFT + 30, MARGIN_TOP + (abs(idx) * 20)))
                win.blit(trade_type_LABEL, (MARGIN_LEFT + 50 + 13, MARGIN_TOP + (abs(idx) * 20)))
                win.blit(trade_return_LABEL, (MARGIN_LEFT + 50 + 65, MARGIN_TOP + (abs(idx) * 20)))
                win.blit(trade_portfolio_LABEL, (MARGIN_LEFT + 50 + 130, MARGIN_TOP + (abs(idx) * 20)))
            idx -= 1


def draw_CANDLE_border(win, min_price, low_middle_price, high_middle_price, max_price):
    # Draw candlestick graph borders
    pygame.draw.line(win, WHITE_COLOUR, (GRAPH_LEFT_BORDER, MARGIN_TOP), (MARGIN_RIGHT, MARGIN_TOP))
    pygame.draw.line(win, WHITE_COLOUR, (GRAPH_LEFT_BORDER, GRAPH_BOTTOM_BORDER), (MARGIN_RIGHT, GRAPH_BOTTOM_BORDER))
    pygame.draw.line(win, WHITE_COLOUR, (GRAPH_LEFT_BORDER, MARGIN_TOP), (GRAPH_LEFT_BORDER, GRAPH_BOTTOM_BORDER))
    pygame.draw.line(win, WHITE_COLOUR, (MARGIN_RIGHT, MARGIN_TOP), (MARGIN_RIGHT, GRAPH_BOTTOM_BORDER))

    MIN_PRICE_LABEL = STATUS_CONTENT_FONT.render(str(min_price) + ' $', bool(1), WHITE_COLOUR)
    win.blit(MIN_PRICE_LABEL, (GRAPH_LEFT_BORDER - MIN_PRICE_LABEL.get_width() - 10,
                               (GRAPH_BOTTOM_BORDER - (MIN_PRICE_LABEL.get_height() / 2))))

    LOW_MIDDLE_PRICE_LABEL = STATUS_CONTENT_FONT.render(str(low_middle_price) + ' $', bool(1), WHITE_COLOUR)
    win.blit(LOW_MIDDLE_PRICE_LABEL, (GRAPH_LEFT_BORDER - LOW_MIDDLE_PRICE_LABEL.get_width() - 10,
                                      ((((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) * 2) + MARGIN_TOP) - (LOW_MIDDLE_PRICE_LABEL.get_height() / 2)))

    HIGH_MIDDLE_PRICE_LABEL = STATUS_CONTENT_FONT.render(str(high_middle_price) + ' $', bool(1), WHITE_COLOUR)
    win.blit(HIGH_MIDDLE_PRICE_LABEL, (GRAPH_LEFT_BORDER - HIGH_MIDDLE_PRICE_LABEL.get_width() - 10,
                                       (((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) + MARGIN_TOP) - (HIGH_MIDDLE_PRICE_LABEL.get_height() / 2)))

    MAX_PRICE_LABEL = STATUS_CONTENT_FONT.render(str(max_price) + ' $', bool(1), WHITE_COLOUR)
    win.blit(MAX_PRICE_LABEL, (GRAPH_LEFT_BORDER - MAX_PRICE_LABEL.get_width() - 10,
                               (MARGIN_TOP - (MAX_PRICE_LABEL.get_height() / 2))))


def draw_CANDLE_grid(win):
    pygame.draw.line(win, DARK_GREY_COLOUR,
                     (GRAPH_LEFT_BORDER, (((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) + MARGIN_TOP)),
                     (MARGIN_RIGHT, (((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) + MARGIN_TOP)))
    pygame.draw.line(win, DARK_GREY_COLOUR,
                     (GRAPH_LEFT_BORDER, ((((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) * 2) + MARGIN_TOP)),
                     (MARGIN_RIGHT, ((((GRAPH_BOTTOM_BORDER - MARGIN_TOP) / 3) * 2) + MARGIN_TOP)))
    pygame.draw.line(win, DARK_GREY_COLOUR,
                     (((MARGIN_RIGHT - GRAPH_LEFT_BORDER) / 3) + GRAPH_LEFT_BORDER, MARGIN_TOP),
                     (((MARGIN_RIGHT - GRAPH_LEFT_BORDER) / 3) + GRAPH_LEFT_BORDER, GRAPH_BOTTOM_BORDER))
    pygame.draw.line(win, DARK_GREY_COLOUR,
                     ((((MARGIN_RIGHT - GRAPH_LEFT_BORDER) / 3) * 2) + GRAPH_LEFT_BORDER, MARGIN_TOP),
                     ((((MARGIN_RIGHT - GRAPH_LEFT_BORDER) / 3) * 2) + GRAPH_LEFT_BORDER, GRAPH_BOTTOM_BORDER))


def draw_CANDLESTICKS(win, candlesticks, instance_counter, norm_hist_info):
    # Update candlesticks dimensions on graph
    list_idx = 0
    for sticks in candlesticks:
        if instance_counter > 2:
            sticks.resize(instance_counter, list_idx, norm_hist_info)
            list_idx += 1
        sticks.move()
        sticks.draw_chart(win)


def draw_LINE_chart(win, line_data, colour, chart_dimensions, scaler):
    top_border, bottom_border, left_border, right_border = chart_dimensions[0], chart_dimensions[1], chart_dimensions[2], chart_dimensions[3]
    if len(line_data) > 1:
        display_data_norm = normalize(line_data, scaler)
        x_data_divider = (right_border - left_border) / (len(display_data_norm) - 1)
        idx = -1
        line_data_coord = []

        # Convert normalized list into coordinates
        for i in display_data_norm:
            idx += 1
            x_coord = left_border + (x_data_divider * idx)
            y_coord = bottom_border - ((bottom_border - top_border) * i)
            if y_coord > chart_dimensions[1]:
                y_coord = chart_dimensions[1]
            if y_coord < chart_dimensions[0]:
                y_coord = chart_dimensions[0]
            x_y_coord = (x_coord, y_coord)
            line_data_coord.append(x_y_coord)

        # Draw line chart
        pygame.draw.lines(win, colour, False, line_data_coord)


def draw_window(win, trader, candlesticks, instance_counter, events, status_info, min_max_info, norm_hist_info):
    # Draw candlestick and indicator graph

    draw_PERFORMANCE_border(win)
    draw_CANDLE_border(win, min_max_info[0], min_max_info[1], min_max_info[2], min_max_info[3])

    draw_CANDLE_grid(win)
    draw_TRADE_HISTORY(win, trader)
    draw_trader_status(win, trader, status_info)
    draw_PERFORMANCE(win, trader)
    draw_CANDLESTICKS(win, candlesticks, instance_counter, norm_hist_info)
    pygame_widgets.update(events)
    pygame.display.update()


def normalize(unnorm_list, min_max_scaler):
    # Normalization function for display
    if len(unnorm_list) > 1:
        hist_min, hist_max = min(min_max_scaler), max(min_max_scaler)
        norm_list = []
        for i, val in enumerate(unnorm_list):
            norm = (val - hist_min) / (hist_max - hist_min)
            norm_list.append(norm)
        return norm_list
    else:
        pass


def normalize_negative(unnorm_list, min_max_scaler):
    # Normalization function for display
    if len(unnorm_list) > 1:
        hist_min, hist_max = min(min_max_scaler), max(min_max_scaler)
        norm_list = []
        for i, val in enumerate(unnorm_list):
            norm = (2 * ((val - hist_min) / (hist_max - hist_min)))-1
            norm_list.append(norm)
        return norm_list
    else:
        pass
