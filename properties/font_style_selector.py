from .base_property_type import BasePropertyType
from lumavate_exceptions import ValidationException

class FontStyleSelectorPropertyType(BasePropertyType):
  @property
  def type_name(self):
    return 'font-style-selector'

  @property
  def mode(self):
    if self.property.default is None:
      return 'text'

    return self.property.default.get('mode', 'text')

  @property
  def bold(self):
    if self.property.default is None:
      return {'hidden': False, 'default': False}

    return self.property.default.get('bold', {'hidden': False, 'default': False})

  @property
  def italics(self):
    if self.property.default is None:
      return {'hidden': False, 'default': False}

    return self.property.default.get('italics', {'hidden': False, 'default': False})

  @property
  def alignment(self):
    if self.property.default is None:
      return {'hidden': False, 'default': 'left'}

    return self.property.default.get('alignment', {'hidden': False, 'default': 'left'})

  @property
  def custom_options(self):
    if self.property.default is None:
      return {'hideColor': False, 'hideSize': False}

    return self.property.default.get('customOptions', {'hideColor': False, 'hideSize': False})

  @property
  def custom(self):
    if self.property.options is None:
      return True

    return self.property.options.get('custom', True)

