from typing import Dict, List, Set, Iterable

from wings import Entity, EntityId, ComponentType, System, Component, SystemType


class World:
    def __init__(self) -> None:
        self._entities: Dict[EntityId, Entity] = {}
        self._components: Dict[ComponentType, Set[EntityId]] = {}
        self._systems: List[System] = []
        self._entity_id: EntityId = 0

    def create_entity(self, *components: Component) -> EntityId:
        """
        创建新的实体
        """
        self._entity_id += 1
        for component in components:
            self.add_component(self._entity_id, component)
        return self._entity_id

    def add_component(self, entity_id: EntityId, component: Component) -> None:
        """
        向现有实体中添加组件
        """
        c_type: ComponentType = type(component)
        if c_type not in self._components:
            self._components[c_type] = set()
        self._components[c_type].add(entity_id)
        if entity_id not in self._entities:
            self._entities[entity_id] = {}
        self._entities[entity_id][c_type] = component

    def add_system(self, system: System, priority: int = 0) -> None:
        """
        添加系统, 添加后将会按照优先级重新排序
        """
        system.priority = priority
        self._systems.append(system)
        self._systems.sort(key=lambda s: s.priority)

    def del_entity(self, entity_id: EntityId) -> None:
        """
        删除实体
        """
        for component_name in self._entities[entity_id]:
            self._components[component_name].discard(entity_id)
            if not self._components[component_name]:
                del self._components[component_name]
        del self._entities[entity_id]

    def del_component(self, entity_id: EntityId, component_type: ComponentType) -> None:
        """
        从实体中删除组件
        """
        self._components[component_type].discard(entity_id)
        if not self._components[component_type]:
            del self._components[component_type]
        del self._entities[entity_id][component_type]
        if not self._entities[entity_id]:
            del self._entities[entity_id]

    def del_system(self, system_type: SystemType) -> None:
        """
        删除系统
        """
        for s in self._systems:
            if type(s) == system_type:
                self._systems.remove(s)

    def entity_exists(self, entity_id: EntityId) -> bool:
        """
        判断实体是否存在
        """
        return entity_id in self._entities

    def get_entity(self, entity_id: EntityId) -> Entity:
        """
        返回实体
        Warnning: 请勿从返回的字典中移除组件, 请使用 del_component 移除组件
        """
        return self._entities[entity_id]

    def findall_by_compnent(self, compnent_type: ComponentType) -> List[EntityId]:
        """
        返回所有持有该组件的实体
        """
        if compnent_type in self._components:
            return [i for i in self._components[compnent_type]]
        return []

    def iter_entity(self, ids: List[EntityId]) -> Iterable[Entity]:
        for id in ids:
            yield self.get_entity(id)

    async def process(self) -> None:
        """
        单步运行所有 system
        """
        for system in self._systems:
            await system.call(world=self)
