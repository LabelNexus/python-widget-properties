from .base_property_type import BasePropertyType

class TextPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'text'
