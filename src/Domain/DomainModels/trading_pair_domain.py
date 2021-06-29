from enum import Enum
from functools import reduce

from src.Infra.Models import trade_product_message_model


class TradingPairType(Enum):
    BTC_USD = 'BTC_USD'
    ETH_BTC = 'ETH_BTC'
    ETH_USD = 'ETH_USD'


class TradingPair:
    trades_product_by_type = {
        TradingPairType.BTC_USD: trade_product_message_model.TradeProductMessageModel.BTC_USD,
        TradingPairType.ETH_BTC: trade_product_message_model.TradeProductMessageModel.ETH_BTC,
        TradingPairType.ETH_USD: trade_product_message_model.TradeProductMessageModel.ETH_USD,
    }

    type_by_trades_product = {
        trade_product_message_model.TradeProductMessageModel.BTC_USD: TradingPairType.BTC_USD,
        trade_product_message_model.TradeProductMessageModel.ETH_BTC: TradingPairType.ETH_BTC,
        trade_product_message_model.TradeProductMessageModel.ETH_USD: TradingPairType.ETH_USD,
    }

    def __init__(self, trading_pair_type: TradingPairType):
        self.type = trading_pair_type
        self.trades = []
        self.volume_weight_average_price = 0

    def update_trades(self, trades):
        self.trades = trades
        return self

    def calculate_volume_weight_average_price(self):
        if len(self.trades) == 0:
            return 0

        total_trades_volume = reduce(
            lambda trade1, trade2: trade1 + trade2,
            map(lambda trade: trade.volume, self.trades),
            0,
        )

        cumulative_total = reduce(
            lambda trade1, trade2: trade2 + trade1,
            map(lambda trade: trade.price * trade.volume, self.trades),
            0,
        )

        return round(cumulative_total / total_trades_volume, 3)

    def update_volume_weight_average_price(self, vwap):
        self.volume_weight_average_price = vwap
        return self
