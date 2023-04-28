from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class DateTimePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'datetime'

  def read(self, data):
    val = super().read(data)

    if val == "":
      val = self.property.default
      
    return val