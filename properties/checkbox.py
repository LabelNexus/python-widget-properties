from .base_property_type import BasePropertyType

class CheckboxPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'checkbox'

  def read(self, data):
    return str(super().read(data)).lower() == 'true'
