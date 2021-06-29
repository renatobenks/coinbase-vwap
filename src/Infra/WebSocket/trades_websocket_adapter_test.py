import cbpro

from src.Infra.Models import trade_message_model
from src.Infra.WebSocket import trades_websocket_adapter


class TestWhenWebsocketForTradesHasBeenCreated:
    def test_trades_websocket_creation(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        trades_websocket_adapter.TradesWebsocketAdapter(trade_callback=None)

        cbpro.WebsocketClient.assert_called_once_with(
            url='wss://ws-feed.pro.coinbase.com/',
            channels=['matches'],
            products=['BTC-USD', 'ETH-USD', 'ETH-BTC'],
            should_print=False,
        )


class TestWhenTradesWebsocketIsOpening:
    def test_connection_not_opened_to_missing_callback(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        trades_websocket = trades_websocket_adapter.TradesWebsocketAdapter(trade_callback=None)
        mocker.patch.object(trades_websocket.client, 'start')

        trades_websocket.open()

        trades_websocket.client.start.assert_not_called()

    def test_subscription_not_opened_to_missing_callback(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        trades_websocket = trades_websocket_adapter.TradesWebsocketAdapter(trade_callback=None)
        mocker.patch.object(trades_websocket, 'subscribe')

        trades_websocket.open()

        trades_websocket.subscribe.assert_not_called()

    def test_opening_connection_to_coinbase_pro_websocket(self, mocker):
        mocker.patch('cbpro.WebsocketClient')

        trades_websocket = trades_websocket_adapter.TradesWebsocketAdapter(trade_callback=lambda trade: trade)
        mocker.patch.object(trades_websocket.client, 'start')

        trades_websocket.open()

        trades_websocket.client.start.assert_called_once()

    def test_subscription_to_match_channel_for_new_trade(self, mocker):
        new_trade_message = {
            'type': 'match',
            'trade_id': '123',
            'price': '100.3',
            'size': '0.541',
            'product_id': 'BTC-USD',
        }

        new_trade = trade_message_model.TradeMessageModel(new_trade_message)

        mocker.patch('cbpro.WebsocketClient')
        mocker.patch('src.Infra.Models.trade_message_model.TradeMessageModel')
        trade_message_model.TradeMessageModel.return_value = new_trade

        trade_callback_stub = mocker.stub()

        trades_websocket = trades_websocket_adapter.TradesWebsocketAdapter(trade_callback=trade_callback_stub)
        trades_websocket.open()
        trades_websocket.client.on_message(new_trade_message)

        trade_callback_stub.assert_called_once_with(new_trade)
