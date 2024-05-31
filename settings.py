from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator


class MySettings(BaseModel):
    metadata_key:str = "your metadata key"
    metadata_value:str = "your metadata value"
    delete_document_of_selected_metadata: bool =False

@plugin
def settings_schema():
    return MySettings.schema()
    
