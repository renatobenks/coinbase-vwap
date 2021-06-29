from src.Infra.Models.trade_product_message_model import TradeProductMessageModel
from src.Infra.Models.trade_message_model import TradeMessageModel


class TestWhenTradeMessageModelHasBeenCreated:
    def test_trade_message_creation(self):
        trade_message_model = TradeMessageModel({
            'trade_id': '123',
            'price': '100',
            'size': '1',
            'product_id': 'BTC-USD',
        })

        assert trade_message_model.id == '123'
        assert trade_message_model.price == 100
        assert trade_message_model.size == 1
        assert trade_message_model.product == TradeProductMessageModel.BTC_USD

    def test_trade_message_with_unknown_product(self):
        trade_message_model = TradeMessageModel({
            'trade_id': '123',
            'price': '100',
            'size': '1',
            'product_id': 'DOGE-ETH',
        })

        assert trade_message_model.product is None

    def test_trade_message_available_products(self):
        assert TradeMessageModel.products == {
            TradeProductMessageModel.BTC_USD.value: TradeProductMessageModel.BTC_USD,
            TradeProductMessageModel.ETH_BTC.value: TradeProductMessageModel.ETH_BTC,
            TradeProductMessageModel.ETH_USD.value: TradeProductMessageModel.ETH_USD,
            TradeProductMessageModel.BTC_ETH.value: TradeProductMessageModel.BTC_ETH,
        }
