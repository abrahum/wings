from typing import Dict, Type
from typing import Any as Component

ComponentType = Type[Component]
EntityId = int
Entity = Dict[ComponentType, Component]


class System:
    priority = 0

    async def call(self, world: "World") -> None:
        raise NotImplementedError


SystemType = Type[System]

from .world import World

from sys import maxsize as _maxsize


def new_world_with_time(priority: int = -_maxsize - 1) -> World:
    from .builtin import enable_time

    world = World()
    enable_time(world, priority=priority)
    return world


def new_world_with_event(priority: int = _maxsize) -> World:
    from .builtin import enable_event

    world = World()
    enable_event(world, priority=priority)
    return world


def default_world() -> World:
    from .builtin import enable_event, enable_time

    world = World()
    enable_event(world)
    enable_time(world)
    return world
