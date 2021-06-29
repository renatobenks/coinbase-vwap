from src.Domain.DomainModels.trade_domain import Trade
from src.Domain.DomainModels.trading_pair_domain import TradingPair, TradingPairType


class TradingPairService:
    def __init__(self):
        self.trading_pairs = {
            TradingPairType.BTC_USD: TradingPair(TradingPairType.BTC_USD),
            TradingPairType.ETH_USD: TradingPair(TradingPairType.ETH_USD),
            TradingPairType.ETH_BTC: TradingPair(TradingPairType.ETH_BTC),
        }

    def update_new_trade(self, trade: Trade):
        if (
            trade.product is None or
            trade.product not in TradingPair.type_by_trades_product or
            TradingPair.type_by_trades_product[trade.product] not in self.trading_pairs
        ):
            return None

        trading_pair = self.trading_pairs[TradingPair.type_by_trades_product[trade.product]]

        old_trades = trading_pair.trades
        new_trades = old_trades + [trade] if len(old_trades) < 200 else old_trades[:-1] + [trade]

        return trading_pair.update_trades(new_trades)

    def calculate_all_volume_weight_average_price(self):
        return dict(map(lambda trading_pair: (
            trading_pair.type,
            trading_pair.update_volume_weight_average_price(
                trading_pair.calculate_volume_weight_average_price()
            )
        ), self.trading_pairs.values()))
