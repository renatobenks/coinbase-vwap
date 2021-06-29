from src.Infra.Models.trade_message_model import TradeMessageModel

from src.Application.ApplicationServices import update_tradings

from src.Domain.DomainServices import trading_pair_domain_service
from src.Domain.DomainModels import trade_domain
from src.Domain.DomainModels import trading_pair_domain


class TestWhenTradingsStartListening:
    def test_listening_to_upcoming_trades(self, mocker):
        update_trading_trades_use_case = update_tradings.UpdateTradingsUseCase(
            trading_pair_domain_service.TradingPairService()
        )

        mocker.patch.object(update_trading_trades_use_case.trades_websocket_adapter, 'open')

        update_trading_trades_use_case.start_listening_upcoming_trades()

        update_trading_trades_use_case.trades_websocket_adapter.open.assert_called_once()


class TestWhenTradingsAreUpdating:
    def test_update_to_new_trade(self, mocker):
        trading_pair_service = trading_pair_domain_service.TradingPairService()

        trade_message = TradeMessageModel({
            'trade_id': '123',
            'product_id': 'BTC-USD',
            'price': '123.45',
            'size': '0.541',
        })

        new_trade = trade_domain.Trade(trade_message)

        mocker.patch('src.Domain.DomainModels.trade_domain.Trade')
        trade_domain.Trade.return_value = new_trade

        update_trading_trades_use_case = update_tradings.UpdateTradingsUseCase(trading_pair_service)

        mocker.patch.object(trading_pair_service, 'update_new_trade')

        update_trading_trades_use_case.update_new_trade(trade_message)

        trading_pair_service.update_new_trade.assert_called_once_with(trade=new_trade)

    def test_update_to_new_upcoming_trade_in_bitcoin_for_usd_tradings(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        existent_btc_usd_trades = [
            trade_domain.Trade(TradeMessageModel({
                'trade_id': '123',
                'product_id': 'BTC-USD',
                'price': '45.45',
                'size': '0.132',
            }))
        ]

        new_message = {
            'type': 'match',
            'trade_id': '123',
            'product_id': 'BTC-USD',
            'price': '123.45',
            'size': '0.541',
        }

        new_btc_usd_trade = trade_domain.Trade(TradeMessageModel(new_message))

        trading_pair_service = trading_pair_domain_service.TradingPairService()
        btc_usd_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.BTC_USD]
        btc_usd_trading_pair.trades = existent_btc_usd_trades

        mocker.patch('src.Domain.DomainModels.trade_domain.Trade')
        trade_domain.Trade.return_value = new_btc_usd_trade

        update_trading_trades_use_case = update_tradings.UpdateTradingsUseCase(trading_pair_service)

        update_trading_trades_use_case.start_listening_upcoming_trades()
        update_trading_trades_use_case.trades_websocket_adapter.client.on_message(new_message)

        updated_btc_usd_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.BTC_USD]

        assert updated_btc_usd_trading_pair.trades == existent_btc_usd_trades + [new_btc_usd_trade]

    def test_update_to_new_upcoming_trade_in_ethereum_for_usd_tradings(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        existent_eth_usd_trades = [
            trade_domain.Trade(TradeMessageModel({
                'trade_id': '123',
                'product_id': 'ETH-USD',
                'price': '45.45',
                'size': '0.132',
            }))
        ]

        new_message = {
            'type': 'match',
            'trade_id': '123',
            'product_id': 'ETH-USD',
            'price': '123.45',
            'size': '0.541',
        }

        new_eth_usd_trade = trade_domain.Trade(TradeMessageModel(new_message))

        trading_pair_service = trading_pair_domain_service.TradingPairService()
        eth_usd_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.ETH_USD]
        eth_usd_trading_pair.trades = existent_eth_usd_trades

        mocker.patch('src.Domain.DomainModels.trade_domain.Trade')
        trade_domain.Trade.return_value = new_eth_usd_trade

        update_trading_trades_use_case = update_tradings.UpdateTradingsUseCase(trading_pair_service)

        update_trading_trades_use_case.start_listening_upcoming_trades()
        update_trading_trades_use_case.trades_websocket_adapter.client.on_message(new_message)

        updated_eth_usd_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.ETH_USD]

        assert updated_eth_usd_trading_pair.trades == existent_eth_usd_trades + [new_eth_usd_trade]

    def test_update_to_new_upcoming_trade_in_ethereum_for_bitcoin_tradings(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        existent_eth_btc_trades = [
            trade_domain.Trade(TradeMessageModel({
                'trade_id': '123',
                'product_id': 'ETH-BTC',
                'price': '45.45',
                'size': '0.132',
            }))
        ]

        new_message = {
            'type': 'match',
            'trade_id': '123',
            'product_id': 'ETH-BTC',
            'price': '123.45',
            'size': '0.541',
        }

        new_eth_btc_trade = trade_domain.Trade(TradeMessageModel(new_message))

        trading_pair_service = trading_pair_domain_service.TradingPairService()
        eth_btc_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.ETH_BTC]
        eth_btc_trading_pair.trades = existent_eth_btc_trades

        mocker.patch('src.Domain.DomainModels.trade_domain.Trade')
        trade_domain.Trade.return_value = new_eth_btc_trade

        update_trading_trades_use_case = update_tradings.UpdateTradingsUseCase(trading_pair_service)

        update_trading_trades_use_case.start_listening_upcoming_trades()
        update_trading_trades_use_case.trades_websocket_adapter.client.on_message(new_message)

        updated_eth_btc_trading_pair = trading_pair_service.trading_pairs[trading_pair_domain.TradingPairType.ETH_BTC]

        assert updated_eth_btc_trading_pair.trades == existent_eth_btc_trades + [new_eth_btc_trade]
