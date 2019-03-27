from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class NumericPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'numeric'

  @property
  def min(self):
    return None if not self.property.options else self.property.options.get('min')

  @property
  def max(self):
    return None if not self.property.options else self.property.options.get('max')

  def too_low(self, val):
    return self.min is not None and val < self.min

  def too_high(self, val):
    return self.max is not None and val > self.max

  def read(self, data):
    val = super().read(data)

    if not val:
      if not self.property.default:
        self.property.default = 0 if not self.min else self.min

      val = self.property.default

    try:
     val = int(val)

    except Exception as e:
      raise ValidationException('Invalid Number: ' + str(val))

    if (self.too_low(val)) or (self.too_high(val)):
      raise ValidationException('Invalid Number: ' + str(val) + \
          ' - must be in range ' + str(self.min) + ' to ' + str(self.max))

    return val
