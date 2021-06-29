from .trade_product_message_model import TradeProductMessageModel


class TradeMessageModel:
    products = {
        product.value: product for product in TradeProductMessageModel
    }

    def __init__(self, trade_message):
        self.id = trade_message['trade_id']
        self.price = float(trade_message['price'])
        self.size = float(trade_message['size'])
        self.product = self.products[trade_message['product_id']] if trade_message['product_id'] in self.products else None
