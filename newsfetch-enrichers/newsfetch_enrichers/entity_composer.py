from common.datatypes import Entity


def create_new_entity(named_entity):
    return Entity(entity=named_entity.entity,
                  label=named_entity.label,
                  start_offset=named_entity.start_offset,
                  end_offset=named_entity.end_offset,
                  confidence=named_entity.confidence)

class EntityComposer_HuggingFace_BI_Strategy():
    def compose(self, named_entities):
        current_entity = None
        composed_entities = []

        for named_entity in named_entities:
            if named_entity.model_label.startswith('B-'):
                if current_entity:
                    offset_diff = named_entity.start_offset - current_entity.end_offset
                    if offset_diff == 0:
                        current_entity.entity = current_entity.entity + named_entity.entity
                        current_entity.end_offset = named_entity.end_offset
                        continue

                current_entity = create_new_entity(named_entity)
                composed_entities.append(current_entity)

            elif named_entity.model_label.startswith('I-'):
                if current_entity:
                    offset_diff = named_entity.start_offset - current_entity.end_offset
                    if offset_diff == 0:
                        current_entity.entity = current_entity.entity + named_entity.entity
                        current_entity.end_offset = named_entity.end_offset
                    elif offset_diff == 1:
                        current_entity.entity = current_entity.entity + ' ' + named_entity.entity
                        current_entity.end_offset = named_entity.end_offset
                    else:
                        current_entity = create_new_entity(named_entity)
                        composed_entities.append(current_entity)
                else:
                    current_entity = create_new_entity(named_entity)
                    composed_entities.append(current_entity)

        for composed_entity in composed_entities:
            composed_entity.entity = composed_entity.entity.replace('##', '').replace(' .', '.')
            composed_entity.entity = composed_entity.entity.replace('_', '').replace('▁', '')

        return composed_entities


class EntityComposer_AllenAI_BILOU_Strategy():
    def compose(self, named_entities):
        current_entity = None
        composed_entities = []

        for named_entity in named_entities:
            if named_entity.model_label.startswith('B-') or named_entity.model_label.startswith('U-'):
                current_entity = create_new_entity(named_entity)
                composed_entities.append(current_entity)
            else:
                if current_entity:
                    current_entity.entity = current_entity.entity + ' ' + named_entity.entity
                    current_entity.end_offset = named_entity.end_offset

        return composed_entities
