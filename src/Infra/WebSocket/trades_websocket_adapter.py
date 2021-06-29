from src.Infra.Models import trade_product_message_model
from src.Infra.Models import trade_message_model
from src.Infra.WebSocket import coinbase_pro_websocket_adapter


class TradesWebsocketAdapter(coinbase_pro_websocket_adapter.CoinbaseProWebsocketAdapter):
    def __init__(self, trade_callback):
        super().__init__(
            channels=['matches'],
            products=[
                trade_product_message_model.TradeProductMessageModel.BTC_USD.value,
                trade_product_message_model.TradeProductMessageModel.ETH_USD.value,
                trade_product_message_model.TradeProductMessageModel.ETH_BTC.value,
            ],
        )

        self.subscription_callback = trade_callback

    def open(self):
        if callable(self.subscription_callback):
            super().open()
            super().subscribe(
                channel=coinbase_pro_websocket_adapter.ChannelType.MATCH,
                callback=lambda trade_message: (
                    self.subscription_callback(trade_message_model.TradeMessageModel(trade_message))
                ),
            )


