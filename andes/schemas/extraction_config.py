from typing import List, Dict, Any
from pydantic import BaseModel


# create a pydantnic model for the extraction config
class ExtractionConfigSchema(BaseModel):
    extraction_type: str
    entities: List[Dict[str, Any]]

    # validate the extraction config
    @classmethod
    def validate(cls, config):
        # entities must have with at least one entity
        if len(config['entities']) == 0:
            return False
        
        # entities must have a name and label
        for entity in config['entities']:
            if 'name' not in entity or 'label' not in entity:
                return False
