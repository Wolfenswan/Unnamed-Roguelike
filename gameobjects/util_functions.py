def entities_at_pos(entities, x, y):
    return [ent for ent in entities if ent.pos == (x, y)]


def entity_at_pos(entities, x, y):
    return next((ent for ent in entities if ent.pos == (x, y)), None)

#
# def interactable_entity_at_pos(entities, x, y):
#     entity = next((entity for entity in entities if entity.pos == (x, y)
#                    and entity.architecture and entity.architecture.on_interaction), None)
#     return entity