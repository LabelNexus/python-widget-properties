from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class TimezonePropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'timezone'
