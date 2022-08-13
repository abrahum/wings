from wings import System, World
from time import time as _time


class Time:
    def __init__(self) -> None:
        self.started: bool = False
        self.timestamp: float = 0.0
        self.time_between_last_call: float = 0.0


class Timer(System):
    async def call(self, world: World) -> None:
        time = world.findall_by_compnent(Time).pop()
        time = world.get_entity(time)
        if time:
            state: Time = time[Time]
            now = _time()
            if state.started:
                state.time_between_last_call = now - state.timestamp
                state.timestamp = now
            else:
                state.time_between_last_call = 0.0
                state.timestamp = now
                state.started = True


from sys import maxsize as _maxsize


def enable_time(world: World, priority: int = -_maxsize - 1):
    world.create_entity(Time())
    world.add_system(Timer(), priority=priority)
