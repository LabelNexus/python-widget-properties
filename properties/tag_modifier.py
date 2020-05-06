from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class TagModifierPropertyType(BasePropertyType):
  @property
  def tag_type(self):
    return self.property.options.get('tagType')

  @property
  def type_name(self):
    return 'tag-modifier'

