from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException


class TextPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'text'

  @property
  def required(self):
    if self.property.options is None:
      return False

    return self.property.options.get('required', False)

  @property
  def maxlength(self):
    if self.property.options is None:
      return False

    return self.property.options.get('maxlength', 0)

  @property
  def allowed_keys(self):
    if self.property.options is None:
      return 'all'

    return self.property.options.get('allowedKeys', 'all')

  @property
  def minlength(self):
    return self.property.options.get('minlength', 0)

  def read(self, data):
    val = super().read(data)

    if self.required and (val is None or val == ''):
      raise ValidationException(f'Field is required', api_field=self.property.name)

    if self.maxlength > 0 and val is not None and len(val) > self.maxlength:
      raise ValidationException(f'Field cannot be more than {self.maxlength} characters long.', api_field=self.property.name)

    if self.allowed_keys != 'all':
      if self.allowed_keys == 'alpha' and not val.isalpha():
        raise ValidationException(f'Field may contain only letters.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric' and not val.isalnum():
        raise ValidationException(f'Field may contain only letters and numbers.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric-space' and not self.isAlphaNumericSpace(val):
        raise ValidationException(f'Field may contain only letters, numbers, and spaces.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric-extra' and not self.isAlphaNumericExtra(val):
        raise ValidationException(f'Field may contain only letters, numbers, space, dash, and underscore.', api_field=self.property.name)

    return val

  def isAlphaNumericSpace(self, val):
    return all(x.isalnum() or x.isspace() for x in val)

  def isAlphaNumericExtra(self, val):
    return all(x.isalnum() or x.isspace() or x=='-' or x=='_' for x in val)



