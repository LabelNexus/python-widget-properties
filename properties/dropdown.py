from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class DropdownPropertyType(BasePropertyType):
  @staticmethod
  def options(options):
    if options is None:
      return {}

    return { x['value']: x['displayName'] for x in options }

  @staticmethod
  def default(option):
    return option['value']

  @property
  def type_name(self):
    return 'dropdown'

  def read(self, data):
    val = data.get(self.property.name)

    check_hash = { str(x): x for x in self.property.options }
    check_hash['None'] = None

    if val is None:
      val = self.property.default

    if str(val) not in check_hash:
      raise ValidationException('Invalid Value: ' + str(val) + ' - must be in set ' + ','.join(list(self.property.options.keys())))

    return val
