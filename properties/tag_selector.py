
from .base_property_type import BasePropertyType

class TagSelectorPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'tag-selector'