from coinbase_pro_websocket_adapter import (
    CoinbaseProWebsocketAdapter,
    COINBASE_PRO_WEBSOCKET_URL,
    ChannelType,
)


class TestWhenAdapterToCoinbaseProWebsocketHasBeenCreated:
    def test_coinbase_pro_client_creation(self, mocker):
        mock = mocker.patch('cbpro.WebsocketClient')
        coinbase_products = ['BTC-USD']

        CoinbaseProWebsocketAdapter(products=coinbase_products)

        mock.assert_called_once_with(
            url=COINBASE_PRO_WEBSOCKET_URL,
            channels=['matches'],
            products=coinbase_products,
            should_print=False,
        )


class TestWhenAdapterToCoinbaseProWebsocketIsOpening:
    def test_websocket_opening(self, mocker):
        websocket_adapter = CoinbaseProWebsocketAdapter()

        mocker.patch.object(websocket_adapter.client, 'start')

        websocket_adapter.open()

        websocket_adapter.client.start.assert_called_once()


class TestWhenAdapterToCoinbaseProWebsocketIsClosing:
    def test_websocket_closure(self, mocker):
        websocket_adapter = CoinbaseProWebsocketAdapter()

        mocker.patch.object(websocket_adapter.client, 'close')

        websocket_adapter.close()

        websocket_adapter.client.close.assert_called_once()


class TestWhenAdapterToCoinbaseProWebsocketIsSubscribingToMatchChannel:
    message = {'type': 'match'}

    def test_websocket_match_channel_subscription(self, mocker):
        websocket_adapter = CoinbaseProWebsocketAdapter()
        client_on_message = mocker.patch.object(websocket_adapter.client, 'on_message')

        def on_message(message): pass
        subscription = websocket_adapter.subscribe(channel=ChannelType.MATCH, callback=on_message)
        subscription.match_message(self.message)

        client_on_message.assert_called_once_with(self.message)

    def test_websocket_match_channel_not_matching_subscriber(self, mocker):
        websocket_adapter = CoinbaseProWebsocketAdapter()

        on_message_stub = mocker.stub(name='on_message_stub')
        websocket_adapter.subscribe(channel=ChannelType.MATCH, callback=on_message_stub)
        websocket_adapter.client.on_message({'type': 'nomatch'})

        on_message_stub.assert_not_called()

    def test_websocket_match_channel_matching_subscriber(self, mocker):
        websocket_adapter = CoinbaseProWebsocketAdapter()

        on_message_stub = mocker.stub(name='on_message_stub')
        websocket_adapter.subscribe(channel=ChannelType.MATCH, callback=on_message_stub)
        websocket_adapter.client.on_message(self.message)

        on_message_stub.assert_called_once_with(self.message)


