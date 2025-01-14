from utils.time import epoch_time

rps_history: dict[int, list[str, int]] = {
    # example
    # 1709604430 (epoch time): 23 (amount of requests)
}


class RateLimits:
    def __init__(self, max_rps: int) -> None:
        global rps_history
        self.max_rps = max_rps
        self.rps_history = rps_history

    @property
    def is_limited(self) -> bool:
        time = epoch_time()
        rps_amount = self.rps_history.get(time)
        return rps_amount > self.max_rps if rps_amount is not None else False

    @property
    def new(self) -> None:
        time = epoch_time()
        rps_amount = self.rps_history.get(time)
        if rps_amount is None:
            self.rps_history[time] = 1
        self.rps_history[time] += 1

    @property
    def amount(self) -> int:
        time = epoch_time()
        rps_amount = self.rps_history.get(time)
        if rps_amount is None:
            return 0
        return rps_amount

    @property
    def history(self) -> dict[int, int]:
        return self.rps_history
