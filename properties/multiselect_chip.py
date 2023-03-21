
from .base_property_type import BasePropertyType

class MultiselectChipPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'multiselect-chip'