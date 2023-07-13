
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class TimeRangePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'time-range'

  def read(self, data):
    val = super().read(data)

    if val == "":
      val = self.property.default
      
    return val