from src.Infra.Models.trade_message_model import TradeMessageModel

from src.Domain.DomainModels.trade_domain import Trade
from src.Domain.DomainModels.trading_pair_domain import TradingPair, TradingPairType

from src.Domain.DomainServices.trading_pair_domain_service import TradingPairService


class TestWhenTradingPairIsUpdatingNewTrade:
    def test_update_to_new_first_trade(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD'
        }))

        updated_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert updated_trading_pair.trades == [new_trade]

    def test_update_to_new_trade(self):
        old_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD'
        }))

        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = [old_trade]

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD'
        }))

        updated_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert updated_trading_pair.trades == [old_trade, new_trade]

    def test_update_to_new_trade_into_bitcoin_usd_trading_pair(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD',
        }))

        updated_btc_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert updated_btc_trading_pair.type == TradingPairType.BTC_USD

    def test_update_to_new_trade_into_ethereum_usd_trading_pair(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'ETH-USD',
        }))

        updated_eth_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert updated_eth_trading_pair.type == TradingPairType.ETH_USD

    def test_update_to_new_trade_into_ethereum_bitcoin_trading_pair(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'ETH-BTC',
        }))

        updated_eth_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert updated_eth_trading_pair.type == TradingPairType.ETH_BTC

    def test_update_to_new_trade_into_almost_full_trading_pair(self, mocker):
        mock = mocker.MagicMock(return_value=[])
        mock.__len__.return_value = 199
        mock.__add__.side_effect = lambda value: value

        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = mock

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD',
        }))

        updated_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert new_trade in updated_trading_pair.trades

    def test_update_to_new_trade_into_full_trading_pair(self, mocker):
        mock = mocker.MagicMock(return_value=[])
        mock.__len__.return_value = 200

        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = mock

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-USD',
        }))

        updated_trading_pair = trading_pair_service.update_new_trade(new_trade)

        assert new_trade not in updated_trading_pair.trades

    def test_update_to_new_trade_without_product(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'DOGE-USD',
        }))

        assert trading_pair_service.update_new_trade(new_trade) is None

    def test_update_to_new_trade_not_in_trading_pair_types(self):
        trading_pair_service = TradingPairService()

        new_trade = Trade(TradeMessageModel({
            'trade_id': 'a1b2c3',
            'price': 100.3,
            'size': 0.35,
            'product_id': 'BTC-ETH',
        }))

        assert trading_pair_service.update_new_trade(new_trade) is None


class TestWhenTradingPairIsCalculatingVolumeWeightAveragePrice:
    def test_vwap_calculation_to_single_trade_for_btc_usd_trading_pair(self):
        trading_pair_service = TradingPairService()

        btc_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 100.3,
                'size': 0.35,
                'product_id': 'BTC-USD'
            })),
        ]

        calculated_trading_pairs = trading_pair_service.calculate_all_volume_weight_average_price()
        calculated_btc_trading_pair = calculated_trading_pairs[TradingPairType.BTC_USD]

        assert calculated_btc_trading_pair.volume_weight_average_price == 100.3

    def test_vwap_calculation_to_single_trade_for_all_trading_pairs(self):
        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 100.3,
                'size': 0.35,
                'product_id': 'BTC-USD'
            })),
        ]

        eth_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.ETH_USD]
        eth_usd_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 200.3,
                'size': 0.7,
                'product_id': 'ETH-USD'
            })),
        ]

        eth_btc_trading_pair = trading_pair_service.trading_pairs[TradingPairType.ETH_BTC]
        eth_btc_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 123.3,
                'size': 0.7,
                'product_id': 'ETH-USD'
            })),
        ]

        calculated_trading_pairs = trading_pair_service.calculate_all_volume_weight_average_price()

        calculated_btc_usd_vwap = calculated_trading_pairs[TradingPairType.BTC_USD].volume_weight_average_price
        calculated_eth_usd_vwap = calculated_trading_pairs[TradingPairType.ETH_USD].volume_weight_average_price
        calculated_eth_btc_vwap = calculated_trading_pairs[TradingPairType.ETH_BTC].volume_weight_average_price

        assert (calculated_btc_usd_vwap, calculated_eth_usd_vwap, calculated_eth_btc_vwap) == (100.3, 200.3, 123.3)

    def test_vwap_calculation_to_couple_trades_for_btc_usd_trading_pair(self):
        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 100.3,
                'size': 0.35,
                'product_id': 'BTC-USD'
            })),
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 200.6,
                'size': 0.70,
                'product_id': 'BTC-USD'
            })),
        ]

        calculated_trading_pairs = trading_pair_service.calculate_all_volume_weight_average_price()
        calculated_btc_usd_trading_pair = calculated_trading_pairs[TradingPairType.BTC_USD]

        assert calculated_btc_usd_trading_pair.volume_weight_average_price == 167.167

    def test_vwap_calculation_to_couple_trades_for_all_trading_pairs(self):
        trading_pair_service = TradingPairService()

        btc_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 150,
                'size': 0.5,
                'product_id': 'BTC-USD'
            })),
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 300,
                'size': 1,
                'product_id': 'BTC-USD'
            })),
        ]

        eth_usd_trading_pair = trading_pair_service.trading_pairs[TradingPairType.ETH_USD]
        eth_usd_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 300,
                'size': 0.5,
                'product_id': 'ETH-USD'
            })),
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 600,
                'size': 1,
                'product_id': 'ETH-USD'
            })),
        ]

        eth_btc_trading_pair = trading_pair_service.trading_pairs[TradingPairType.ETH_BTC]
        eth_btc_trading_pair.trades = [
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 550,
                'size': 0.5,
                'product_id': 'ETH-BTC'
            })),
            Trade(TradeMessageModel({
                'trade_id': 'a1b2c3',
                'price': 600,
                'size': 1,
                'product_id': 'ETH-BTC'
            })),
        ]

        calculated_trading_pairs = trading_pair_service.calculate_all_volume_weight_average_price()

        calculated_btc_usd_vwap = calculated_trading_pairs[TradingPairType.BTC_USD].volume_weight_average_price
        calculated_eth_usd_vwap = calculated_trading_pairs[TradingPairType.ETH_USD].volume_weight_average_price
        calculated_eth_btc_usd_vwap = calculated_trading_pairs[TradingPairType.ETH_BTC].volume_weight_average_price

        assert (calculated_btc_usd_vwap, calculated_eth_usd_vwap, calculated_eth_btc_usd_vwap) == (250, 500, 583.333)
