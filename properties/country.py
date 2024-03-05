from .base_property_type import BasePropertyType

class CountryPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'country'
