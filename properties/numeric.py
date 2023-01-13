from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class NumericPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'numeric'

  @property
  def min(self):
    return self.property.options.get('min')

  @property
  def max(self):
    return self.property.options.get('max')

  @property
  def decimal_places(self):
    return self.property.options.get('decimalPlaces',0)

  def too_low(self, val):
    return self.min is not None and val < self.min

  def too_high(self, val):
    return self.max is not None and val > self.max

  def read(self, data):
    val = super().read(data)

    if val == "":
      val = self.property.default

    try:
      if self.decimal_places == 0:
        val = int(val)
      else:
        val = float(format(val, f'.{self.decimal_places}f'))

    except Exception as e:
      raise ValidationException('Invalid Number: ' + str(val))

    if (self.too_low(val)) or (self.too_high(val)):
      raise ValidationException('Invalid Number: ' + str(val) + \
          ' - must be in range ' + str(self.min) + ' to ' + str(self.max))

    return val
