from time import sleep
from pprint import pprint

from src.Application.ApplicationServices import calculate_tradings
from src.Application.ApplicationServices import update_tradings

__version__ = '0.1'


def run():
    calculate_tradings_use_case = calculate_tradings.CalculateTradingsUseCase()
    update_tradings_use_case = update_tradings.UpdateTradingsUseCase(
        trading_pair_service=calculate_tradings_use_case.trading_pair_service
    )

    update_tradings_use_case.start_listening_upcoming_trades()

    while True:
        pprint(calculate_tradings_use_case.calculate_vwap())
        sleep(1)
