from src.Domain.DomainServices import trading_pair_domain_service


class CalculateTradingsUseCase:
    def __init__(self):
        self.trading_pair_service = trading_pair_domain_service.TradingPairService()

    def calculate_vwap(self):
        return dict(map(lambda trading_pair: (
            trading_pair.type.value,
            trading_pair.volume_weight_average_price,
        ), self.trading_pair_service.calculate_all_volume_weight_average_price().values()))
