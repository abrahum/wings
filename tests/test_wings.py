from wings import default_world, System, World
from wings.builtin import Time, Event


class TimeLog(System):
    async def call(self, world: World) -> None:
        time = world.get_entity(world.findall_by_compnent(Time).pop())
        if time:
            state: Time = time[Time]
            print(
                f"timestamp: {state.timestamp}, after_last_process: {state.time_between_last_call}"
            )


class EventLog(System):
    async def call(self, world: "World") -> None:
        for id in world.findall_by_compnent(Event):
            print(world.get_entity(id)[TestEvent])


class TestEvent:
    def __str__(self) -> str:
        return "Just Test Event"


def test_base():
    import asyncio

    async def run():
        world = default_world()
        world.add_system(TimeLog(), priority=0)
        world.add_system(EventLog())
        await world.process()
        await asyncio.sleep(1)
        world.create_entity(Event(), TestEvent())
        await world.process()
        await asyncio.sleep(1)
        await world.process()

    asyncio.run(run())
