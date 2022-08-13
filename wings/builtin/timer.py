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


class TimeLog(System):
    async def call(self, world: "World") -> None:
        time = world.get_entity(world.findall_by_compnent(Time).pop())
        if time:
            state: Time = time[Time]
            print(
                f"timestamp: {state.timestamp}, after_last_process: {state.time_between_last_call}"
            )
