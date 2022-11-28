from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class DropdownOptionsPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'dropdown-options'

  def read(self, data):
    val = data.get(self.property.name)
    dropdown_value = val.get('value', {})
    dropdown_options = self.property.options.get('values', {})
    check_hash = { str(x): x for x in dropdown_options.keys() }
    check_hash['None'] = None

    if dropdown_value is None:
      dropdown_value = self.property.default

    if str(dropdown_value) not in check_hash:
      raise ValidationException('Invalid Value: ' + str(dropdown_value) + ' - must be in set ' + ','.join(list(dropdown_options.keys())))

    return {
      'value': dropdown_value,
      'options': dropdown_options
    }
