from src.Infra.Models import trade_message_model

from src.Domain.DomainModels import trade_domain
from src.Domain.DomainModels import trading_pair_domain

from src.Application.ApplicationServices import calculate_tradings


class TestWhenTradingsAreCalculatingVWAP:
    def test_vwap_calculation_to_all_trading_pairs_without_trades(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 0,
        }

    def test_vwap_calculation_to_bitcoin_for_usd_trading_pair_with_single_trade(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        btc_usd_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.BTC_USD
        ]

        btc_usd_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'BTC-USD',
                    'price': '123.45',
                    'size': '0.541',
                }),
            ),
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 123.45,
            trading_pair_domain.TradingPairType.ETH_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 0,
        }

    def test_vwap_calculation_to_bitcoin_for_usd_trading_pair_with_couple_trades(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        btc_usd_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.BTC_USD
        ]

        btc_usd_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'BTC-USD',
                    'price': '123.45',
                    'size': '0.541',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'BTC-USD',
                    'price': '123.40',
                    'size': '0.540',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'BTC-USD',
                    'price': '123.35',
                    'size': '0.539',
                }),
            ),
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 123.40,
            trading_pair_domain.TradingPairType.ETH_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 0,
        }

    def test_vwap_calculation_to_ethereum_for_usd_trading_pair_with_single_trade(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        eth_usd_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.ETH_USD
        ]

        eth_usd_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-USD',
                    'price': '214.45',
                    'size': '0.541',
                }),
            ),
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_USD.value: 214.45,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 0,
        }

    def test_vwap_calculation_to_ethereum_for_usd_trading_pair_with_couple_trades(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        eth_usd_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.ETH_USD
        ]

        eth_usd_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-USD',
                    'price': '214.45',
                    'size': '0.541',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-USD',
                    'price': '214.40',
                    'size': '0.239',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-USD',
                    'price': '214.35',
                    'size': '0.620',
                }),
            ),
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_USD.value: 214.397,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 0,
        }

    def test_vwap_calculation_to_ethereum_for_bitcoin_trading_pair_with_single_trade(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        eth_btc_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.ETH_BTC
        ]

        eth_btc_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-BTC',
                    'price': '23.45',
                    'size': '0.541',
                })
            )
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 23.45,
        }

    def test_vwap_calculation_to_ethereum_for_bitcoin_trading_pair_with_couple_trades(self):
        calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()

        eth_btc_trading_pair = calculate_tradings_use_case.trading_pair_service.trading_pairs[
            trading_pair_domain.TradingPairType.ETH_BTC
        ]

        eth_btc_trading_pair.trades = [
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-BTC',
                    'price': '23.45',
                    'size': '0.541',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-BTC',
                    'price': '23.40',
                    'size': '0.345',
                }),
            ),
            trade_domain.Trade(
                trade_message_model.TradeMessageModel({
                    'trade_id': 'a1b2c3',
                    'product_id': 'ETH-BTC',
                    'price': '23.35',
                    'size': '0.240',
                }),
            ),
        ]

        assert calculate_tradings_use_case.calculate_vwap() == {
            trading_pair_domain.TradingPairType.BTC_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_USD.value: 0,
            trading_pair_domain.TradingPairType.ETH_BTC.value: 23.413,
        }
