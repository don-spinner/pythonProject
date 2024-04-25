class Stock:
    def __init__(self, symbol, stock_type, last_dividend, fixed_dividend_ratio, par_value, price):
        self.symbol = symbol
        self.type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend_ratio = fixed_dividend_ratio
        self.par_value = par_value
        self.price = price