import enum
import cbpro

COINBASE_PRO_WEBSOCKET_URL = 'wss://ws-feed.pro.coinbase.com/'


class ChannelType(enum.Enum):
    MATCH = 'match'


class CoinbaseProWebsocketAdapter:
    def __init__(self, products=None, channels=None):
        self.client = cbpro.WebsocketClient(
            url=COINBASE_PRO_WEBSOCKET_URL,
            channels=channels or ['matches'],
            products=products,
            should_print=False,
        )

    def open(self):
        self.client.start()

    def subscribe(self, channel, callback):
        subscription = Subscription(channel.value, callback, self.client.on_message)
        self.client.on_message = subscription.match_message
        return subscription

    def close(self):
        self.client.close()


class Subscription:
    def __init__(self, channel, callback, on_message):
        self.channel = channel
        self.callback = callback
        self.on_message = on_message

    def match_message(self, message):
        self.on_message(message)
        self.callback(message) if self.channel == message['type'] else 0
