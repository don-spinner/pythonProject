from collections import defaultdict
import time


class TradeRepository:
    def __init__(self):
        self.trades = defaultdict(list)

    def add_trade(self, trade):
        self.trades[trade.stock_name].append({
            'trade_id': trade.trade_id,
            'quantity': trade.quantity,
            'indicator': trade.indicator,
            'price': trade.price,
            'timestamp': trade.timestamp
        })

    def get_trades(self, stock_symbol, timestamp=None):
        trades = self.trades[stock_symbol]
        if timestamp is None:
            return trades
        else:
            current_time = time.time()
            trades_in_time_range = [trade for trade in trades if current_time - trade['timestamp'] <= timestamp]
            return trades_in_time_range