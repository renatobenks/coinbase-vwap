from src.Infra.Models.trade_product_message_model import TradeProductMessageModel
from src.Domain.DomainModels.trading_pair_domain import TradingPair, TradingPairType


class TestWhenBitcoinForDolarTradingPairHasBeenCreated:
    def test_access_to_trades_product_by_bitcoin_dolar_trading_pair(self):
        assert TradingPair.trades_product_by_type[TradingPairType.BTC_USD] == TradeProductMessageModel.BTC_USD

    def test_access_to_bitcoin_dolar_trading_pair_by_trades_product(self):
        assert TradingPair.type_by_trades_product[TradeProductMessageModel.BTC_USD] == TradingPairType.BTC_USD

    def test_bitcoin_for_dolar_trading_pair_creation(self):
        assert TradingPair(trading_pair_type=TradingPairType.BTC_USD).type == TradingPairType.BTC_USD


class TestWhenEthereumForDolarTradingPairHasBeenCreated:
    def test_access_to_trades_product_by_ethereum_dolar_trading_pair(self):
        assert TradingPair.trades_product_by_type[TradingPairType.ETH_USD] == TradeProductMessageModel.ETH_USD

    def test_access_to_ethereum_dolar_trading_pair_by_trades_product(self):
        assert TradingPair.type_by_trades_product[TradeProductMessageModel.ETH_USD] == TradingPairType.ETH_USD

    def test_ethereum_for_dolar_trading_pair_creation(self):
        assert TradingPair(trading_pair_type=TradingPairType.ETH_USD).type == TradingPairType.ETH_USD


class TestWhenEthereumForBitcoinTradingPairHasBeenCreated:
    def test_access_to_trades_product_by_ethereum_bitcoin_trading_pair(self):
        assert TradingPair.trades_product_by_type[TradingPairType.ETH_BTC] == TradeProductMessageModel.ETH_BTC

    def test_access_to_ethereum_bitcoin_trading_pair_by_trades_product(self):
        assert TradingPair.type_by_trades_product[TradeProductMessageModel.ETH_BTC] == TradingPairType.ETH_BTC

    def test_ethereum_for_bitcoin_trading_pair_creation(self):
        assert TradingPair(trading_pair_type=TradingPairType.ETH_BTC).type == TradingPairType.ETH_BTC


class TradeMock:
    def __init__(self, volume, price):
        self.price = price
        self.volume = volume


class TestWhenTradingPairIsUpdatingTrades:
    def test_update_new_trades_to_trading_pair(self):
        trades = [TradeMock(price=100.3, volume=0.35)]

        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)

        trading_pair.update_trades(trades)

        assert trading_pair.trades == trades

    def test_update_replace_old_trades_to_trading_pair(self):
        trades = [TradeMock(price=100.3, volume=0.35)]

        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)
        trading_pair.trades = [TradeMock(price=200.3, volume=0.70)]

        trading_pair.update_trades(trades)

        assert trading_pair.trades == trades

    def test_update_old_trades_to_trading_pair(self):
        old_trades = [TradeMock(price=100.3, volume=0.35)]

        trades = old_trades + [TradeMock(price=100.3, volume=0.35)]

        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)
        trading_pair.trades = old_trades

        trading_pair.update_trades(trades)

        assert trading_pair.trades == trades


class TestWhenTradingPairIsUpdatingVolumeWeightAveragePrice:
    def test_update_to_trading_pair_vwap(self):
        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)

        trading_pair.update_volume_weight_average_price(165.5)

        assert trading_pair.volume_weight_average_price == 165.5


class TestWhenTradingPairIsCalculatingVolumeWeightAveragePrice:
    def test_volume_weight_average_price_calculation_to_nonexistent_trades(self):
        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)

        assert trading_pair.calculate_volume_weight_average_price() == 0

    def test_volume_weight_average_price_calculation_to_single_trade(self, mocker):
        trade_mock = TradeMock(volume=10, price=112312.319)

        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)
        trading_pair.trades = [trade_mock]

        assert trading_pair.calculate_volume_weight_average_price() == 112312.319

    def test_volume_weight_average_price_calculation_to_couple_trades(self, mocker):
        trade_mock = TradeMock(price=100, volume=10)
        trade2_mock = TradeMock(price=100.5, volume=10)
        trade3_mock = TradeMock(price=101, volume=10)

        trading_pair = TradingPair(trading_pair_type=TradingPairType.BTC_USD)
        trading_pair.trades = [trade_mock, trade2_mock, trade3_mock]

        assert trading_pair.calculate_volume_weight_average_price() == 100.5
