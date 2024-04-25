import time

from exceptions.CalculateDividenYieldError import CalculateDividenYieldError
from exceptions.CalculateGeometricMeanException import CalculateGeometricMeanException
from Repositories.Entities.Stock import Stock
from Repositories.StockRepository import StockRepository
from Repositories.TradeRepository import TradeRepository
from Repositories.Entities.Trade import Trade
from exceptions.VolumeWeightedStockPriceException import VolumeWeightedStockPriceException


class StockMarketService:
    LAST_X_MINUTES = 15

    def __init__(self, stock_repository, trade_repository):
        self.stock_repository = stock_repository
        self.trade_repository = trade_repository

    def list_stocks(self, page_number=1, page_size=10):
        return self.stock_repository.list_stocks(page_number, page_size)

    def calculate_dividend_yield(self, stock_symbol):
        stock_found = self.stock_repository.get_stock_by_symbol(stock_symbol)
        if not stock_found:
            raise CalculateDividenYieldError("Stock not found")

        if stock_found.type == 'Common':
            if stock_found.price == 0:
                raise CalculateDividenYieldError("Price cannot be zero")
            return stock_found.last_dividend / stock_found.price
        elif stock_found.type == 'Preferred':
            if stock_found.price == 0:
                raise CalculateDividenYieldError("Price cannot be zero")
            return (stock_found.fixed_dividend_ratio * stock_found.par_value) / stock_found.price
        else:
            raise CalculateDividenYieldError("Invalid stock type")

    def calculate_timestamp_minutes_ago(self, minutes):
        return time.time() - (minutes * 60)

    def calculate_volume_weighted_stock_price(self, stock_symbol, last_x_minutes):
        timestamp_x_minutes_ago = self.calculate_timestamp_minutes_ago(last_x_minutes)
        trades_in_last_x_minutes = self.trade_repository.get_trades_by_stock_symbol(stock_symbol,
                                                                                    timestamp_x_minutes_ago)

        if not trades_in_last_x_minutes:
            raise VolumeWeightedStockPriceException("No trades in the last {} minutes".format(last_x_minutes))

        total_value = sum(trade['price'] * trade['quantity'] for trade in trades_in_last_x_minutes)
        total_quantity = sum(trade['quantity'] for trade in trades_in_last_x_minutes)

        if total_quantity == 0:
            raise VolumeWeightedStockPriceException("Total quantity cannot be zero")

        return total_value / total_quantity

    def record_trade(self, trade_id, stock_symbol, quantity, indicator, price):
        timestamp = time.time()
        trade = Trade(trade_id, quantity, indicator, price, timestamp, stock_symbol)
        self.trade_repository.add_trade(trade)

    def calculate_geometric_mean(self):
        total_records = self.stock_repository.get_total_records()
        page_size = 10  # Assuming 10 records per page
        total_pages = (total_records + page_size - 1) // page_size

        product = 1
        count = 0

        for page_number in range(1, total_pages + 1):
            stocks = self.stock_repository.list_stocks(page_number=page_number, page_size=page_size)
            for symbol, stock in stocks.items():
                if stock.price != 0:
                    product *= stock.price
                    count += 1

        if count == 0:
            raise CalculateGeometricMeanException("No valid stock prices found")
        return product ** (1 / count)

    def update_stock_prices(self, new_prices):
        self.stock_repository.update_stock_prices(new_prices)


# usage
stock_repository = StockRepository()
trade_repository = TradeRepository()
stock_repository.add_stock(Stock('TEA', 'Common', 0, None, 100, 34.42))
stock_repository.add_stock(Stock('POP', 'Preferred', 10, 0.035, 100, 47.48))
stock_repository.add_stock(Stock('ALE', 'Common', 23, None, 60, 24.43))
stock_repository.add_stock(Stock('GIN', 'Preferred', 8, 0.02, 100, 15.45))
stock_repository.add_stock(Stock('JOE', 'Common', 13, None, 250, 33.52))

service = StockMarketService(stock_repository, trade_repository)
stocks = service.list_stocks(page_number=1, page_size=10)
for symbol, stock in stocks.items():
    print(symbol, stock.price)

print("calculate_dividend_yield", service.calculate_dividend_yield('POP'))
new_prices = {'TEA': 35.0, 'POP': 49.0, 'ALE': 25.0, 'GIN': 16.0, 'JOE': 34.0}
service.update_stock_prices(new_prices)
print("calculate_dividend_yield after price update", service.calculate_dividend_yield('POP'))

service.record_trade(1, 'TEA', 1000, 'BUY', 35)
service.record_trade(2, 'TEA', 60000, 'SELL', 36)
print("Volume Weighted Stock Price for TEA last 15 minutes:",
      service.calculate_volume_weighted_stock_price('TEA', StockMarketService.LAST_X_MINUTES))
print("Geometric Mean of prices for all stocks:", service.calculate_geometric_mean())
