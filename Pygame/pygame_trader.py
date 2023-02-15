from Pygame.pygame_config import *


class TraderBot:
    def __init__(self):
        self.wallet_amount = INITIAL_WALLET_AMOUNT
        self.currency_owned_USD = 0
        self.portfolio_value = 0
        self.market_value = 0
        self.gains = 0

        self.currency_owned_CUR = 0
        self.last_buy = 0
        self.trade_count = 0
        self.trade_frequency = 0
        self.buy_amount = 0
        self.sell_amount = 0

        self.state = 0
        self.start_close = 0

        self.slice_counter = 2
        self.market_history = []
        self.market_history_display = []
        self.portfolio_history = []
        self.portfolio_history_display = []

        self.buy_history = []
        self.sell_history = []
        self.trade_history = []

    def buy(self, new_close, new_time):
        if self.wallet_amount != 0:
            self.buy_history = [0, 'BOUGHT:', new_time, new_close, self.portfolio_value]
            self.trade_history.append(self.buy_history)

            self.buy_amount = self.wallet_amount * BUY_AMOUNT
            self.wallet_amount = self.wallet_amount - self.buy_amount
            self.currency_owned_CUR = self.currency_owned_CUR + (self.buy_amount / new_close)
            self.last_buy = new_close
            self.state = 1

            if self.start_close == 0:
                self.start_close = new_close
        else:
            pass

    def hold(self):
        pass

    def sell(self, new_close, new_time, instance_counter):
        if self.state == 1:
            self.state = 0
            self.sell_amount = self.currency_owned_CUR * new_close
            self.currency_owned_CUR = 0
            self.wallet_amount = self.wallet_amount + self.sell_amount
            self.trade_count += 1
            self.trade_frequency = self.trade_count / instance_counter

            self.sell_history = [1, 'SOLD:', new_time, round(((new_close / self.last_buy) * 100) - 100, 2), self.portfolio_value]
            self.last_buy = 0

            self.trade_history.append(self.sell_history)
        else:
            pass

    def update_status(self, new_close):
        self.currency_owned_USD = self.currency_owned_CUR * new_close
        self.portfolio_value = self.wallet_amount + self.currency_owned_USD
        self.gains = ((self.portfolio_value / INITIAL_WALLET_AMOUNT) - 1) * 100
        self.portfolio_history.append(self.portfolio_value)
        self.market_value = (new_close / self.start_close) * INITIAL_WALLET_AMOUNT
        if self.start_close == 0:
            self.market_value = INITIAL_WALLET_AMOUNT
        self.market_history.append(self.market_value)