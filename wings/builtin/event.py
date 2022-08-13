from wings import System, World
from sys import maxsize


class Event:
    pass


class EventClear(System):
    async def call(self, world: World) -> None:
        for id in world.findall_by_compnent(Event):
            world.del_entity(id)


def enable_event(world: World, priority: int = maxsize):
    world.add_system(EventClear(), priority=priority)
