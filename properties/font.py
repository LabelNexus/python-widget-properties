
from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class FontPropertyType(BasePropertyType):

  @staticmethod
  def default(option):
    return 'Roboto'

  @property
  def type_name(self):
    return 'font'

  def read(self, data):
    val = data.get(self.property.name)
    if val is None:
      val = self.property.default

    return val
