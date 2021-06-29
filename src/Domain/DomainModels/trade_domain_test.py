from src.Domain.DomainModels import trade_domain


class TradeMessageMock:
    def __init__(self):
        self.id = 'a1b2c3'
        self.price = 100.12
        self.size = 1
        self.product = 'BTC'


class TestWhenTradeHasBeenCreated:
    def test_trade_creation(self):
        trade = trade_domain.Trade(trade=TradeMessageMock())

        assert trade.id == 'a1b2c3'
        assert trade.price == 100.12
        assert trade.volume == 1
        assert trade.product == 'BTC'
