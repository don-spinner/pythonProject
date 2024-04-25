class Trade:
    def __init__(self, trade_id, quantity, indicator, price, timestamp, stock_name):
        self.trade_id = trade_id
        self.quantity = quantity
        self.indicator = indicator
        self.price = price
        self.timestamp = timestamp
        self.stock_name = stock_name