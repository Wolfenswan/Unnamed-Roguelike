from gameobjects.block_levels import BlockLevel


def entities_at_pos(entities, x, y):
    return [ent for ent in entities if ent.pos == (x, y)]


def entity_at_pos(entities, x, y):
    return next((ent for ent in entities if ent.pos == (x, y)), None)


def blocking_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.blocks.get(BlockLevel.WALK, False)), None)
    return entity


def fighter_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.fighter and entity.blocks.get(BlockLevel.WALK, False)), None)
    return entity


def interactable_entity_at_pos(entities, x, y):
    entity = next((entity for entity in entities if entity.pos == (x, y)
                   and entity.architecture and entity.architecture.on_interaction), None)
    # for entity in entities:
    #     if entity.x == x and entity.y == y and entity.architecture and entity.architecture.on_interaction:
    #         return entity
    return entity