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
      if self.allowed_keys == 'alpha' and not self.is_alpha(val):
        raise ValidationException(f'Field may contain only letters.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric' and not val.is_alpha_numeric():
        raise ValidationException(f'Field may contain only letters and numbers.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric-space' and not self.is_alpha_numeric_space(val):
        raise ValidationException(f'Field may contain only letters, numbers, and spaces.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric-extra' and not self.is_alpha_numeric_extra(val):
        raise ValidationException(f'Field may contain only letters, numbers, space, dash, and underscore.', api_field=self.property.name)
      if self.allowed_keys == 'alpha-numeric-extra-nospace' and not self.is_alpha_numeric_extra_nospace(val):
        raise ValidationException(f'Field may contain only letters, numbers, dash, and underscore.', api_field=self.property.name)

    return val

  def is_alpha(self, val):
    return self.is_ascii(val) and val.isalpha()

  def is_alpha_numeric(self, val):
    return self.is_ascii(val) and val.isalnum()

  def is_alpha_numeric_space(self, val):
    return self.is_ascii(val) and all(x.isalnum() or x.isspace() for x in val)

  def is_alpha_numeric_extra(self, val):
    return self.is_ascii(val) and all(x.isalnum() or x.isspace() or x=='-' or x=='_' for x in val)

  def is_alpha_numeric_extra_nospace(self, val):
    return self.is_ascii(val) and all(x.isalnum() or x=='-' or x=='_' for x in val)

  def is_ascii(self, val):
    try:
      val.encode('ascii', 'strict')
    except Exception as e:
      return False

    return True


