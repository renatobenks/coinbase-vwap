from src.Infra.WebSocket import trades_websocket_adapter

from src.Domain.DomainModels import trade_domain


class UpdateTradingsUseCase:
    def __init__(self, trading_pair_service):
        self.trading_pair_service = trading_pair_service
        self.trades_websocket_adapter = trades_websocket_adapter.TradesWebsocketAdapter(
            trade_callback=self.update_new_trade
        )

    def start_listening_upcoming_trades(self):
        self.trades_websocket_adapter.open()

    def update_new_trade(self, trade_message):
        self.trading_pair_service.update_new_trade(trade=trade_domain.Trade(trade_message))
