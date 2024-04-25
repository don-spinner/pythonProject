class StockRepository:
    def __init__(self):
        self.stocks = {}

    def list_stocks(self, page_number=1, page_size=10):
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return {symbol: stock for symbol, stock in list(self.stocks.items())[start_index:end_index]}

    def update_stock_prices(self, new_prices):
        for symbol, price in new_prices.items():
            if symbol in self.stocks:
                self.stocks[symbol].price = price
            else:
                print(f"Stock {symbol} not found")

    def get_total_records(self):
        return len(self.stocks)

    def add_stock(self, stock):
        self.stocks[stock.symbol] = stock

    def get_stock_by_symbol(self, symbol):
        return self.stocks.get(symbol, None)
