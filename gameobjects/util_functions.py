def get_blocking_entity_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None


def get_interactable_entity_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.x == destination_x and entity.y == destination_y and entity.architecture and entity.architecture.on_interaction:
            return entity
    return None