def entities_at_pos(entities, x, y):
    return [ent for ent in entities if ent.pos == (x, y)]


def blocking_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.blocks.get('walk', False)), None)
    # for entity in entities:
    #     if entity.blocks.get('walk', False) and entity.x == x and entity.y == y:
    #         return entity
    return entity


def fighter_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.blocks.get('walk', False) and entity.fighter), None)
    return entity


def interactable_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.architecture and entity.architecture.on_interaction), None)
    # for entity in entities:
    #     if entity.x == x and entity.y == y and entity.architecture and entity.architecture.on_interaction:
    #         return entity
    return entity